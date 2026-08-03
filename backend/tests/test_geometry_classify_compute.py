"""Unit tests Geometry classify + compute (sin I/O)."""

from __future__ import annotations

from geometry.classify import classify_geom_type
from geometry.compute import compute_element_geometry
from geometry.enums import GeomType, MeasureSource


def test_classify_wall_vertical():
    assert classify_geom_type("wall.masonry.brick", "architecture") == GeomType.VERTICAL_SURFACE


def test_classify_floor_horizontal():
    assert classify_geom_type("floor.carpetas", "architecture") == GeomType.HORIZONTAL_REGION


def test_classify_plumbing_linear():
    assert classify_geom_type("generic.element", "plumbing") == GeomType.LINEAR_RUN


def test_classify_opening():
    assert classify_geom_type("opening.door", "architecture") == GeomType.OPENING


def test_classify_unknown():
    assert classify_geom_type("furniture.chair", "architecture") == GeomType.UNKNOWN


def test_compute_wall_derives_length():
    out = compute_element_geometry(
        element_id="e1",
        element_type="wall.retak",
        discipline_code="architecture",
        params={"wall_face_area_m2": 30.0, "wall_height_m": 2.5},
    )
    g = out["geometry"]
    assert g["geom_type"] == GeomType.VERTICAL_SURFACE.value
    assert g["area_m2"] == 30.0
    assert g["height_m"] == 2.5
    assert g["length_m"] == 12.0
    assert g["thickness_m"] is None
    assert g["volume_m3"] is None
    assert g["bbox"] is None
    meta = g["measure_meta"]["length_m"]
    assert meta["source"] == MeasureSource.COMPUTED.value
    assert meta["derived"] is True
    codes = {i.code for i in out["issues"]}
    assert "VOLUME_UNAVAILABLE" in codes
    assert "SHAPE_UNAVAILABLE" in codes


def test_compute_wall_no_thickness_heuristic():
    out = compute_element_geometry(
        element_id="e1",
        element_type="wall.masonry.brick",
        discipline_code="architecture",
        params={"wall_face_area_m2": 10.0, "wall_height_m": 2.0, "thickness_hint": 0.15},
    )
    assert out["geometry"]["thickness_m"] is None
    assert out["geometry"]["measure_meta"]["thickness_m"]["source"] == MeasureSource.UNAVAILABLE.value


def test_compute_floor_area_from_params():
    out = compute_element_geometry(
        element_id="e2",
        element_type="floor.carpetas",
        discipline_code="architecture",
        params={"floor_area_m2": 42.5},
    )
    g = out["geometry"]
    assert g["geom_type"] == GeomType.HORIZONTAL_REGION.value
    assert g["area_m2"] == 42.5
    assert g["measure_meta"]["area_m2"]["source"] == MeasureSource.MDO_PARAMS.value


def test_compute_floor_area_from_space_column():
    out = compute_element_geometry(
        element_id="e2",
        element_type="floor.carpetas",
        discipline_code="architecture",
        params={},
        space_area_m2=55.0,
    )
    g = out["geometry"]
    assert g["area_m2"] == 55.0
    assert g["measure_meta"]["area_m2"]["source"] == MeasureSource.MDO_COLUMN.value


def test_compute_linear_sum():
    out = compute_element_geometry(
        element_id="e3",
        element_type="generic.element",
        discipline_code="plumbing",
        params={"cold_water_ml": 10.0, "hot_water_ml": 5.0, "sewage_ml": 8.0},
    )
    g = out["geometry"]
    assert g["geom_type"] == GeomType.LINEAR_RUN.value
    assert g["length_m"] == 23.0
    assert g["measure_meta"]["length_m"]["derived"] is True


def test_compute_opening_shape_unavailable():
    out = compute_element_geometry(
        element_id="e4",
        element_type="opening.door",
        discipline_code="architecture",
        params={"openings_count": 3},
    )
    g = out["geometry"]
    assert g["geom_type"] == GeomType.OPENING.value
    assert g["area_m2"] is None
    assert g["measure_meta"]["extras"]["openings_count"] == 3
    assert any(i.code == "SHAPE_UNAVAILABLE" for i in out["issues"])


def test_compute_missing_height_warning():
    out = compute_element_geometry(
        element_id="e5",
        element_type="wall.drywall",
        discipline_code="architecture",
        params={"wall_face_area_m2": 20.0},
    )
    codes = {i.code for i in out["issues"]}
    assert "MISSING_HEIGHT" in codes
    assert out["geometry"]["length_m"] is None
