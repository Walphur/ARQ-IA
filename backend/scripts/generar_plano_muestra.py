"""Genera frontend/public/plano-muestra.png alineado con lo que el motor espera (verde + cota legible)."""

from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "frontend" / "public" / "plano-muestra.png"


def main():
    img = np.zeros((420, 520, 3), dtype=np.uint8)
    # Linea de escala (verde BGR)
    cv2.line(img, (40, 360), (260, 360), (0, 255, 0), 8)
    # Cota legible: blanco sobre negro (maximo contraste para OCR)
    cv2.putText(img, "7.30", (275, 372), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2)
    # Muro de referencia
    cv2.line(img, (80, 80), (80, 300), (0, 0, 255), 5)
    # Piso gris claro (parche)
    cv2.rectangle(img, (100, 320), (480, 400), (200, 200, 200), -1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT), img)
    print(f"Escrito {OUT}")


if __name__ == "__main__":
    main()
