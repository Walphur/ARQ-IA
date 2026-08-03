# ADR-007 — Perception → MDO strangler (E03-F01)

| Campo | Valor |
|-------|-------|
| Estado | Accepted |
| Fecha | 2026-08-03 |
| Feature | E03-F01 Perception → MDO |
| Paquetes | `motor_ia` (detections) · `mdo/perception_map` · `mdo/perception_ingest` · `main` (composition root) |

## Contexto

El wedge histórico escribe solo `Process.items` (cantidades + costos). El MDO (E02-F01) es el SoT futuro. Hay que conectar percepción sin romper el flujo actual.

## Decisión

1. **`procesar_plano_ia` emite `detections`** — hechos geométricos/tipológicos **sin precios**.
2. **`perception_map`** (puro) traduce detections → propuesta Building/Level/Space/Element (+ Discipline).
3. **`perception_ingest`** persiste vía `MdoService` (upsert por `external_id` `process:{id}:…`).
4. **`/projects/{id}/calcular` y recalcular** hacen dual-write: Process legacy **siempre**; MDO best-effort. Fallo MDO → warning + `meta.mdo.ok=false`, Process se guarda igual.
5. **Independencia de imports**: `motor_ia` ↛ `mdo`; `mdo` ↛ `motor_ia`; solo `main` orquesta.
6. **No materiales/costos en MDO** en esta feature — solo entidades + ParameterSet `params` geométricos.

## Consecuencias

- Strangler: UI/cupo siguen sobre Process.
- `Process.result_meta.mdo` enlaza version/element ids.
- Demo `/calcular` (sin project) **no** escribe MDO.
- Evolución: ChangeSet/Evidence (E07+) podrá reemplazar upsert in-place.
