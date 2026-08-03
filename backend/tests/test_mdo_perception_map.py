"""Fase 1 E03-F01 — detections del motor + mapper Perception→MDO (sin persistencia)."""

import cv2
import numpy as np
import pytest

import motor_ia
from mdo.perception_map import map_detections_to_mdo_proposal, wall_element_type
from mdo.typing_rules import normalize_parameter_set_data


@pytest.fixture(autouse=True)
def mock_tesseract(monkeypatch):
    monkeypatch.setattr(motor_ia.pytesseract, "image_to_string", lambda *a, **k: "5")


def _png_muros_minimo():
    img = np.ones((420, 520, 3), dtype=np.uint8) * 255
    cv2.line(img, (40, 360), (220, 360), (0, 255, 0), 8)
    cv2.putText(img, "5", (235, 368), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    cv2.line(img, (80, 80), (80, 300), (0, 0, 255), 5)
    # piso gris + abertura cian
    cv2.rectangle(img, (120, 100), (280, 220), (200, 200, 200), -1)
    cv2.rectangle(img, (150, 130), (190, 180), (255, 255, 0), -1)  # cian BGR
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_procesar_emite_detections_sin_precios():
    r = motor_ia.procesar_plano_ia(
        _png_muros_minimo(),
        referencia_metros_manual=1.0,
        sistema_muro="ladrillo_hueco_12",
        tipo_plano="muros",
    )
    assert "detections" in r
    d = r["detections"]
    assert d["tipo_plano"] == "muros"
    assert "facts" in d
    assert "wall_face_area_m2" in d["facts"]
    # No filtrar precios en detections
    blob = str(d)
    assert "mo_muro" not in blob
    assert "mat_" not in blob
    assert "precio" not in blob.lower()
    # Process legacy intacto
    assert isinstance(r["items"], list)
    assert "total" in r


def test_map_muros_proposal_has_building_level_space_element():
    detections = {
        "tipo_plano": "muros",
        "sistema_muro": "ladrillo_hueco_12",
        "altura_muro_m": 2.6,
        "facts": {
            "wall_face_area_m2": 12.5,
            "floor_area_m2": 40.0,
            "openings_count": 2,
            "wall_height_m": 2.6,
        },
    }
    p = map_detections_to_mdo_proposal(detections, process_id=99, project_name="Casa")
    assert p["building"]["external_id"] == "process:99:building"
    assert p["level"]["code"] == "PB"
    assert len(p["spaces"]) >= 1
    types = {e["element_type"] for e in p["elements"]}
    assert "wall.masonry.brick" in types
    assert "opening.door" in types
    # ParameterSet solo params/metadata
    for ps in p["parameter_sets"]:
        normalize_parameter_set_data(ps["data"])


def test_wall_element_type_mapping():
    assert wall_element_type("retak") == "wall.retak"
    assert wall_element_type("ladrillo_hueco_12") == "wall.masonry.brick"


def test_terreno_proposal_site_only():
    p = map_detections_to_mdo_proposal(
        {
            "tipo_plano": "terreno",
            "facts": {"lots": [{"lot_number": 1, "area_m2": 200.0, "perimeter_m": 60.0}]},
        },
        process_id=7,
    )
    assert p["site"] is not None
    assert p["building"] is None
    assert p["elements"] == []
