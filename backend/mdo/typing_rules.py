"""Reglas de tipado MDO: disciplina vs tipo concreto + límites de ParameterSet.

Decisiones PASO 2 (ajustes pre-PASO 3):
1. ParameterSet.data solo params variables y metadata — nunca hechos estructurales.
2. Element NO usa un enum monolítico; disciplina y tipo concreto se separan.
3. System se reemplaza por Discipline (ver models).
"""

from __future__ import annotations

from typing import Any

# Disciplinas seed (abiertas: se permiten códigos custom con prefijo libre).
KNOWN_DISCIPLINE_CODES = frozenset(
    {
        "architecture",
        "structure",
        "plumbing",
        "electrical",
        "hvac",
        "fire",
        "gas",
        "envelope",
        "finishes",
        "site",
        "other",
    }
)

# Tipologías concretas seed LATAM (registry abierto — no enum cerrado).
KNOWN_ELEMENT_TYPES = frozenset(
    {
        "wall.masonry.brick",
        "wall.masonry.block",
        "wall.drywall",
        "wall.steel_frame",
        "wall.retak",
        "opening.door",
        "opening.window",
        "slab.concrete",
        "floor.carpetas",
        "floor.ceramic",
        "roof.metal",
        "roof.tile",
        "column.concrete",
        "beam.concrete",
        "stair.concrete",
        "generic.element",
    }
)

# Top-level keys permitidos en ParameterSet.data
PARAMETER_SET_ALLOWED_ROOT_KEYS = frozenset({"params", "metadata"})

# Claves prohibidas en cualquier nivel de params/metadata (hechos estructurales del grafo).
PARAMETER_SET_FORBIDDEN_KEYS = frozenset(
    {
        "site_id",
        "building_id",
        "level_id",
        "space_id",
        "discipline_id",
        "element_id",
        "version_id",
        "project_id",
        "studio_id",
        "parent_id",
        "children",
        "element_type",
        "discipline",
        "discipline_code",
        "geometry",
        "polygon",
        "polygon_ref",
        "bbox",
        "host_wall_id",
        "system_id",  # legacy name — no reintroducir vía params
        "connections",
        "members",
    }
)


class MdoValidationError(ValueError):
    """Error de validación de dominio MDO (mapeable a HTTP 400)."""


def normalize_discipline_code(code: str) -> str:
    value = (code or "").strip().lower()
    if not value:
        raise MdoValidationError("discipline_code es obligatorio.")
    if len(value) > 64:
        raise MdoValidationError("discipline_code excede 64 caracteres.")
    if not all(c.isalnum() or c in "._-" for c in value):
        raise MdoValidationError("discipline_code contiene caracteres inválidos.")
    return value


def normalize_element_type(element_type: str) -> str:
    value = (element_type or "").strip().lower()
    if not value:
        raise MdoValidationError("element_type es obligatorio.")
    if len(value) > 120:
        raise MdoValidationError("element_type excede 120 caracteres.")
    if "." not in value:
        raise MdoValidationError(
            "element_type debe ser concreto con forma '<familia>.<variante>' "
            "(ej. wall.masonry.brick), no un enum monolítico."
        )
    if not all(c.isalnum() or c in "._-" for c in value):
        raise MdoValidationError("element_type contiene caracteres inválidos.")
    return value


def validate_element_classification(discipline_code: str, element_type: str) -> tuple[str, str]:
    """Separa y valida disciplina vs tipo concreto. Ambos son strings abiertos."""
    d = normalize_discipline_code(discipline_code)
    t = normalize_element_type(element_type)
    return d, t


def _assert_no_forbidden_keys(obj: Any, path: str = "") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_s = str(key)
            full = f"{path}.{key_s}" if path else key_s
            if key_s in PARAMETER_SET_FORBIDDEN_KEYS:
                raise MdoValidationError(
                    f"ParameterSet.data no puede almacenar hechos estructurales: clave prohibida '{full}'. "
                    "Usá columnas/entidades del grafo MDO."
                )
            _assert_no_forbidden_keys(value, full)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _assert_no_forbidden_keys(item, f"{path}[{i}]")


def normalize_parameter_set_data(data: Any) -> dict[str, Any]:
    """Solo params variables y metadata. Prohíbe información estructural del dominio."""
    if data is None:
        return {"params": {}, "metadata": {}}
    if not isinstance(data, dict):
        raise MdoValidationError("ParameterSet.data debe ser un objeto JSON.")
    extra = set(data.keys()) - PARAMETER_SET_ALLOWED_ROOT_KEYS
    if extra:
        raise MdoValidationError(
            "ParameterSet.data solo admite raíces 'params' y 'metadata'. "
            f"Claves rechazadas: {sorted(extra)}. "
            "No uses data para hechos estructurales (jerarquía, tipología, geometría)."
        )
    params = data.get("params", {})
    metadata = data.get("metadata", {})
    if not isinstance(params, dict):
        raise MdoValidationError("ParameterSet.data.params debe ser un objeto.")
    if not isinstance(metadata, dict):
        raise MdoValidationError("ParameterSet.data.metadata debe ser un objeto.")
    _assert_no_forbidden_keys(params, "params")
    _assert_no_forbidden_keys(metadata, "metadata")
    return {"params": params, "metadata": metadata}
