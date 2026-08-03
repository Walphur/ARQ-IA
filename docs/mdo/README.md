# MDO — Modelo Digital de la Obra

Paquete: `backend/mdo/`  
Feature: **E02-F01** (RFC) / Roadmap **E07-F01**  
ADR: [ADR-006](../adr/ADR-006-mdo-core-foundations.md) · [LIMITS](./LIMITS.md) · [MIGRATION_PLAN](./MIGRATION_PLAN.md)

## Implementación por fases

| Fase | Commit scope | Tests |
|------|----------------|-------|
| 1 | Models, typing_rules, Alembic, independencia | `test_mdo_phase1_*`, `test_mdo_typing_rules` |
| 2 | ProjectVersion ensure/seal + HTTP wiring | `test_mdo_phase2_*` |
| 3 | Site→Building→Level→Space | `test_mdo_phase3_*` |
| 4 | Discipline + Element tipado | `test_mdo_phase4_*` |
| 5 | ParameterSet + cierre docs | `test_mdo_phase5_*` |

## API (auth Bearer)

| Método | Path |
|--------|------|
| POST | `/v1/mdo/projects/{id}/ensure` |
| GET | `/v1/mdo/projects/{id}/versions` |
| GET/POST seal | `/v1/mdo/versions/{id}` · `/seal` |
| GET | `/v1/mdo/versions/{id}/tree` |
| CRUD | sites, buildings, levels, spaces, disciplines, elements |
| PUT/DELETE | parameter-sets |
| GET | `/v1/mdo/projects/{id}/events` |

## Independencia

Composition root: `main.py` importa MDO. MDO **no** importa `main`, `motor_ia`, materials, costs ni frontend.

## Relación con Process

`Process` sigue siendo el SoT file-centric del wedge actual.

Desde **E03-F01**, `/projects/{id}/calcular` hace dual-write:

1. Process.items + total (legacy, inalterado para UI/cupo)
2. MDO Building/Level/Space/Element vía `perception_ingest` (best-effort)

Ver [ADR-007](../adr/ADR-007-perception-mdo-strangler.md).

## Perception → MDO

| Pieza | Rol |
|-------|-----|
| `motor_ia.detections` | Hechos geométricos sin precios |
| `mdo/perception_map.py` | Mapper puro |
| `mdo/perception_ingest.py` | Persistencia MdoService |
| `main._try_ingest_perception_mdo` | Composition root + aislamiento de fallos |
