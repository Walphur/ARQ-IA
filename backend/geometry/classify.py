"""Clasificación determinística Element MDO → geom_type."""

from __future__ import annotations

from geometry.enums import GeomType


def classify_geom_type(element_type: str, discipline_code: str) -> GeomType:
    et = (element_type or "").strip().lower()
    disc = (discipline_code or "").strip().lower()

    if et.startswith("wall."):
        return GeomType.VERTICAL_SURFACE
    if et.startswith("floor.") or et.startswith("slab.") or et.startswith("roof."):
        return GeomType.HORIZONTAL_REGION
    if et.startswith("opening."):
        return GeomType.OPENING
    if et == "generic.element" and disc in {"plumbing", "electrical", "hvac", "fire", "gas"}:
        return GeomType.LINEAR_RUN
    if et.startswith("lot.") or disc == "site":
        return GeomType.LOT_REGION
    return GeomType.UNKNOWN
