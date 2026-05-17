"""Tests de regresion del motor (sin red: precios offline/cache)."""

import cv2
import numpy as np
import pytest

import motor_ia


@pytest.fixture(autouse=True)
def mock_tesseract(monkeypatch):
    """Evita depender del binario tesseract en CI / Windows sin PATH."""
    monkeypatch.setattr(motor_ia.pytesseract, "image_to_string", lambda *a, **k: "5")


def _png_muros_minimo():
    """Plano sintetico: fondo blanco, linea verde escala + numero, trazo rojo."""
    img = np.ones((420, 520, 3), dtype=np.uint8) * 255
    cv2.line(img, (40, 360), (220, 360), (0, 255, 0), 8)
    cv2.putText(img, "5", (235, 368), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    cv2.line(img, (80, 80), (80, 300), (0, 0, 255), 5)
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_procesar_muros_devuelve_estructura():
    png = _png_muros_minimo()
    r = motor_ia.procesar_plano_ia(png, referencia_metros_manual=1.0, sistema_muro="ladrillo_hueco_12", tipo_plano="muros")
    assert "items" in r
    assert isinstance(r["items"], list)
    assert "total" in r
    assert "imagen" in r and len(r["imagen"]) > 100
    assert "escala_modo" in r
    assert "avisos" in r


def test_procesar_terreno_sin_error_numerico():
    png = _png_muros_minimo()
    r = motor_ia.procesar_plano_ia(png, 1.0, tipo_plano="terreno")
    assert r["total"] == 0
    assert isinstance(r["items"], list)
