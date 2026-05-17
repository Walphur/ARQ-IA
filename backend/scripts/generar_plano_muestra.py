"""Genera un PNG sintetico solo para pruebas locales (no pisa los planos de referencia en public/)."""

from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
# No usar plano-muestra*.png: en el repo van los planos reales de referencia del estudio.
OUT = ROOT / "frontend" / "public" / "plano-sintetico-lab.png"


def main():
    w, h = 560, 440
    img = np.ones((h, w, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (60, 80), (500, 320), (210, 210, 210), -1)
    cv2.rectangle(img, (60, 80), (500, 320), (0, 0, 255), 6)
    cv2.line(img, (70, 360), (260, 360), (0, 255, 0), 10)
    cv2.putText(img, "7.30", (275, 372), cv2.FONT_HERSHEY_SIMPLEX, 1.35, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(img, "LAB sintetico (no produccion)", (70, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (120, 120, 120), 2, cv2.LINE_AA)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT), img)
    print(f"Escrito {OUT}")


if __name__ == "__main__":
    main()
