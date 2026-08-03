# ADR-008 — Geometry as regenerable projection (E03-F02)

| Campo | Valor |
|-------|-------|
| Estado | Accepted |
| Fecha | 2026-04-05 |
| Feature | E03-F02 Geometry Engine (Roadmap E06 thin slice) |
| Paquetes | `backend/geometry/*` · composition root `main` |

## Contexto

El MDO (E02-F01) es el System of Record de elementos y params. Se necesitan medidas derivadas (length, area, …) y issues de calidad sin acoplar percepción (`motor_ia`) ni precios.

Hasta ChangeSets (E07-F03), la geometría no debe pretender ser historial autoritativo.

## Decisión

1. **Dominio independiente** `backend/geometry/` — no vive dentro de `mdo/`.
2. **MDO permanece SoT** — Geometry lee tablas `mdo_*` (via `mdo_reader` Core), calcula y persiste `ElementGeometry` / `GeometryIssue`.
3. **Proyección regenerable** — cada `POST /v1/geometry/versions/{id}/compute` soft-borra geometrías/issues activos de la versión y escribe un nuevo `compute_run_id`. No hay merge incremental en F02.
4. **Sin heurística de espesor** — `thickness_m` y `volume_m3` quedan `null` / `source=unavailable` si no hay evidencia.
5. **Contrato shape null** — `bbox`, `polygon`, `centroid`, `orientation_deg` existen en el schema pero son `null` en F02; se emite `SHAPE_UNAVAILABLE`.
6. **Provenance por medida** — `measure_meta` marca `source` (`mdo_params` / `mdo_column` / `computed` / `unavailable`) y `derived` cuando aplica (p.ej. `length_m = area_m2 / height_m`).
7. **Issues con severity + source** — `info|warning|error` y `validator|compute|ingest`.
8. **Independencia de imports** — Geometry ↛ `motor_ia`, ↛ `mdo.perception_*`, ↛ `mdo.service` / `mdo.http`. Solo `main` orquesta.

## Consecuencias

- Process legacy y `/calcular` no se modifican en esta feature.
- ChangeSets futuros pueden versionar/editar geometría; hasta entonces recompute es la fuente de verdad geométrica.
- UI/costeo pueden consumir `/v1/geometry/*` sin tocar percepción.
