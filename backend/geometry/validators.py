"""Validadores geométricos → GeometryIssue drafts."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional

from geometry.enums import DEFAULT_AREA_TOLERANCE_RATIO, GeomType


@dataclass
class IssueDraft:
    code: str
    message: str
    severity: str  # info|warning|error
    source: str  # validator|compute|ingest
    details: dict[str, Any] = field(default_factory=dict)


def _tol() -> float:
    try:
        return float(os.getenv("GEOMETRY_AREA_TOLERANCE_RATIO", str(DEFAULT_AREA_TOLERANCE_RATIO)))
    except ValueError:
        return DEFAULT_AREA_TOLERANCE_RATIO


def validate_geometry_result(result: dict[str, Any], *, geom_type: GeomType) -> list[IssueDraft]:
    issues: list[IssueDraft] = []
    length_m = result.get("length_m")
    height_m = result.get("height_m")
    area_m2 = result.get("area_m2")
    thickness_m = result.get("thickness_m")
    volume_m3 = result.get("volume_m3")
    meta = result.get("measure_meta") or {}

    for name, val in (
        ("length_m", length_m),
        ("height_m", height_m),
        ("area_m2", area_m2),
        ("thickness_m", thickness_m),
        ("volume_m3", volume_m3),
    ):
        if val is not None and val < 0:
            issues.append(
                IssueDraft(
                    code="NEGATIVE_MEASURE",
                    message=f"Medida negativa: {name}={val}",
                    severity="error",
                    source="validator",
                    details={name: val},
                )
            )

    if geom_type == GeomType.VERTICAL_SURFACE:
        if height_m is None:
            issues.append(
                IssueDraft(
                    code="MISSING_HEIGHT",
                    message="Muro sin height_m en params MDO.",
                    severity="warning",
                    source="validator",
                )
            )
        elif height_m <= 0:
            issues.append(
                IssueDraft(
                    code="ZERO_HEIGHT",
                    message="height_m <= 0; no se puede inferir length_m.",
                    severity="error",
                    source="validator",
                    details={"height_m": height_m},
                )
            )
        if area_m2 is None:
            issues.append(
                IssueDraft(
                    code="MISSING_AREA",
                    message="Muro sin area_m2 en params MDO.",
                    severity="warning",
                    source="validator",
                )
            )

    if geom_type == GeomType.HORIZONTAL_REGION and area_m2 is None:
        issues.append(
            IssueDraft(
                code="MISSING_AREA",
                message="Región horizontal sin area_m2.",
                severity="warning",
                source="validator",
            )
        )

    # Consistency when length was derived
    length_meta = meta.get("length_m") or {}
    if (
        length_meta.get("derived")
        and length_m is not None
        and height_m is not None
        and height_m > 0
        and area_m2 is not None
    ):
        expected = length_m * height_m
        if expected != 0:
            ratio = abs(area_m2 - expected) / abs(expected)
            if ratio > _tol():
                issues.append(
                    IssueDraft(
                        code="AREA_LENGTH_INCONSISTENT",
                        message="area_m2 no coincide con length_m * height_m dentro de tolerancia.",
                        severity="warning",
                        source="validator",
                        details={
                            "area_m2": area_m2,
                            "length_m": length_m,
                            "height_m": height_m,
                            "expected_area": expected,
                            "ratio": ratio,
                        },
                    )
                )

    return issues
