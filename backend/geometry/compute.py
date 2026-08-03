"""Motor geométrico puro: Element snapshot → medidas + measure_meta (sin I/O)."""

from __future__ import annotations

from typing import Any, Optional

from geometry.classify import classify_geom_type
from geometry.enums import GeomType, MeasureSource
from geometry.validators import IssueDraft, validate_geometry_result


def _meta(source: MeasureSource, *, derived: bool = False, formula: Optional[str] = None) -> dict:
    out: dict[str, Any] = {"source": source.value, "derived": derived}
    if formula:
        out["formula"] = formula
    return out


def _unavailable() -> dict:
    return _meta(MeasureSource.UNAVAILABLE, derived=False)


def _f(params: dict, *keys: str) -> Optional[float]:
    for k in keys:
        if k in params and params[k] is not None:
            try:
                return float(params[k])
            except (TypeError, ValueError):
                continue
    return None


def compute_element_geometry(
    *,
    element_id: str,
    element_type: str,
    discipline_code: str,
    params: dict[str, Any],
    space_area_m2: Optional[float] = None,
) -> dict[str, Any]:
    """Retorna dict listo para persistir + lista de IssueDraft previos a validación cruzada."""
    params = params if isinstance(params, dict) else {}
    geom_type = classify_geom_type(element_type, discipline_code)

    length_m = height_m = thickness_m = area_m2 = volume_m3 = None
    measure_meta: dict[str, Any] = {
        "length_m": _unavailable(),
        "height_m": _unavailable(),
        "thickness_m": _unavailable(),  # decisión: nunca heurística
        "area_m2": _unavailable(),
        "volume_m3": _unavailable(),
        "bbox": _unavailable(),
        "polygon": _unavailable(),
        "centroid": _unavailable(),
        "orientation_deg": _unavailable(),
    }
    extras: dict[str, Any] = {}
    pre_issues: list[IssueDraft] = []

    if geom_type == GeomType.VERTICAL_SURFACE:
        height_m = _f(params, "wall_height_m", "height_m")
        area_m2 = _f(params, "wall_face_area_m2", "area_m2")
        if height_m is not None:
            measure_meta["height_m"] = _meta(MeasureSource.MDO_PARAMS)
        if area_m2 is not None:
            measure_meta["area_m2"] = _meta(MeasureSource.MDO_PARAMS)
        if height_m is not None and height_m > 0 and area_m2 is not None:
            length_m = area_m2 / height_m
            measure_meta["length_m"] = _meta(
                MeasureSource.COMPUTED,
                derived=True,
                formula="area_m2 / height_m",
            )
        # thickness/volume remain unavailable
        measure_meta["volume_m3"] = _meta(MeasureSource.UNAVAILABLE)
        pre_issues.append(
            IssueDraft(
                code="VOLUME_UNAVAILABLE",
                message="Volumen no disponible: thickness_m sin evidencia.",
                severity="info",
                source="compute",
                details={"thickness_m": None},
            )
        )

    elif geom_type == GeomType.HORIZONTAL_REGION:
        area_m2 = _f(params, "floor_area_m2", "roof_area_m2", "area_m2")
        if area_m2 is None and space_area_m2 is not None:
            area_m2 = float(space_area_m2)
            measure_meta["area_m2"] = _meta(MeasureSource.MDO_COLUMN)
        elif area_m2 is not None:
            measure_meta["area_m2"] = _meta(MeasureSource.MDO_PARAMS)

    elif geom_type == GeomType.LINEAR_RUN:
        parts = []
        for key in (
            "cold_water_ml",
            "hot_water_ml",
            "sewage_ml",
            "electrical_conduit_ml",
            "length_m",
        ):
            v = _f(params, key)
            if v is not None:
                parts.append((key, v))
        if len(parts) == 1:
            length_m = parts[0][1]
            measure_meta["length_m"] = _meta(MeasureSource.MDO_PARAMS)
        elif len(parts) > 1:
            length_m = sum(v for _, v in parts)
            measure_meta["length_m"] = _meta(
                MeasureSource.COMPUTED,
                derived=True,
                formula="+".join(k for k, _ in parts),
            )
            extras["length_parts"] = {k: v for k, v in parts}

    elif geom_type == GeomType.OPENING:
        count = params.get("openings_count")
        if count is not None:
            extras["openings_count"] = count
        pre_issues.append(
            IssueDraft(
                code="SHAPE_UNAVAILABLE",
                message="Geometría de abertura (bbox/área individual) no disponible en F02.",
                severity="info",
                source="compute",
                details={"openings_count": count},
            )
        )

    elif geom_type == GeomType.LOT_REGION:
        area_m2 = _f(params, "area_m2")
        length_m = _f(params, "perimeter_m")  # perimeter as length measure
        if area_m2 is not None:
            measure_meta["area_m2"] = _meta(MeasureSource.MDO_PARAMS)
        if length_m is not None:
            measure_meta["length_m"] = _meta(MeasureSource.MDO_PARAMS)

    else:  # UNKNOWN
        pre_issues.append(
            IssueDraft(
                code="UNSUPPORTED_ELEMENT_TYPE",
                message=f"Tipo de elemento no soportado para geometría: {element_type}",
                severity="warning",
                source="compute",
                details={"element_type": element_type, "discipline_code": discipline_code},
            )
        )

    # Shape fields always null in F02 contract
    pre_issues.append(
        IssueDraft(
            code="SHAPE_UNAVAILABLE",
            message="bbox/polygon/centroid/orientation no disponibles (contrato null en F02).",
            severity="info",
            source="compute",
            details={},
        )
    )

    result = {
        "element_id": element_id,
        "geom_type": geom_type.value,
        "units": "m",
        "length_m": length_m,
        "height_m": height_m,
        "thickness_m": None,
        "area_m2": area_m2,
        "volume_m3": volume_m3,
        "bbox": None,
        "polygon": None,
        "centroid": None,
        "orientation_deg": None,
        "measure_meta": {**measure_meta, "extras": extras} if extras else measure_meta,
        "quality_flags": [],
    }

    issues = validate_geometry_result(result, geom_type=geom_type)
    # dedupe SHAPE_UNAVAILABLE if validator also adds — keep pre + validator
    issues = _merge_issues(pre_issues, issues)
    return {"geometry": result, "issues": issues}


def _merge_issues(a: list[IssueDraft], b: list[IssueDraft]) -> list[IssueDraft]:
    seen = set()
    out: list[IssueDraft] = []
    for issue in a + b:
        key = (issue.code, issue.severity, str(issue.details))
        if key in seen:
            continue
        seen.add(key)
        out.append(issue)
    return out
