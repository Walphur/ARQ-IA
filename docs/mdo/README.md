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

## Process

`Process` sigue siendo SoT legacy del wedge. MDO no lo lee ni escribe en F01.
