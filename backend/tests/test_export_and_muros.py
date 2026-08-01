"""Regresion: aberturas y altura de muro."""

import cv2
import numpy as np
import pytest

import motor_ia


@pytest.fixture(autouse=True)
def mock_tesseract(monkeypatch):
    monkeypatch.setattr(motor_ia.pytesseract, "image_to_string", lambda *a, **k: "5")


def _png_muros_con_abertura():
    img = np.ones((420, 520, 3), dtype=np.uint8) * 255
    cv2.line(img, (40, 360), (220, 360), (0, 255, 0), 8)
    cv2.putText(img, "5", (235, 368), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    cv2.line(img, (80, 80), (80, 300), (0, 0, 255), 5)
    # Abertura cian
    cv2.rectangle(img, (200, 120), (260, 200), (255, 255, 0), -1)
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_aberturas_tienen_precio():
    png = _png_muros_con_abertura()
    r = motor_ia.procesar_plano_ia(png, 1.0, tipo_plano="muros")
    nombres = [i["nom"] for i in r["items"]]
    assert "Mano Obra: Aberturas" in nombres
    assert "Materiales: Aberturas" in nombres
    assert r.get("altura_muro") == 2.6


def test_altura_muro_cambia_superficie():
    png = _png_muros_con_abertura()
    bajo = motor_ia.procesar_plano_ia(png, 1.0, tipo_plano="muros", altura_muro=2.0)
    alto = motor_ia.procesar_plano_ia(png, 1.0, tipo_plano="muros", altura_muro=3.0)
    assert alto["total"] > bajo["total"]
    assert alto["altura_muro"] == 3.0
