"""Genera frontend/public/plano-muestra.png: mini-plano legible (no abstracto)."""

from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "frontend" / "public" / "plano-muestra.png"

# Version en query string en el front para invalidar cache de CDN/navegador
VERSION_FILE = ROOT / "frontend" / "public" / "plano-muestra.version.txt"


def main():
    w, h = 560, 440
    img = np.ones((h, w, 3), dtype=np.uint8) * 255

    # Ambiente gris (piso) — mismo rango HSV que el motor usa para pisos
    cv2.rectangle(img, (60, 80), (500, 320), (210, 210, 210), -1)
    # Muros rojos (BGR)
    cv2.rectangle(img, (60, 80), (500, 320), (0, 0, 255), 6)

    # Linea de escala verde (segmento de referencia)
    cv2.line(img, (70, 360), (260, 360), (0, 255, 0), 10)
    # Cota en negro sobre blanco (OCR estable)
    cv2.putText(img, "7.30", (275, 372), cv2.FONT_HERSHEY_SIMPLEX, 1.35, (0, 0, 0), 3, cv2.LINE_AA)

    # Texto guia (no lo lee el motor como escala)
    cv2.putText(img, "EJEMPLO ARC-IA (mini plano)", (70, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 80, 80), 2, cv2.LINE_AA)
    cv2.putText(img, "Verde = escala  |  Rojo = muros  |  Gris = piso", (70, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (90, 90, 90), 1, cv2.LINE_AA)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT), img)
    VERSION_FILE.write_text("5\n", encoding="utf-8")
    print(f"Escrito {OUT} y {VERSION_FILE}")


if __name__ == "__main__":
    main()
