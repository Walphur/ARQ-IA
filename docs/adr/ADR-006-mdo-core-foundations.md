# ADR-006 — MDO Core foundations (E02-F01 / Roadmap E07-F01)

| Campo | Valor |
|-------|-------|
| Estado | Accepted (implementación por fases) |
| Fecha | 2026-08-03 |
| Feature | E02-F01 Core MDO |
| Paquete | `backend/mdo/` |

## Decisiones (aprobadas pre-PASO 3)

1. **ParameterSet.data** solo `{params, metadata}` — nunca hechos estructurales.
2. **Element** tipado en dos ejes: `discipline_code` + `element_type` (no enum monolítico).
3. **System → Discipline** en F01 (grafo System+Connection del RFC §2.4 diferido).
4. **external_id** en entidades principales (IFC/Revit/APIs).
5. **display_name** desacoplado de identidad técnica (`code`/id).
6. **Migraciones Alembic** para `mdo_*` desde el día 1 (`mdo_alembic_version`). Legacy puede seguir con `create_all` hasta migración global.
7. **Independencia**: MDO no importa percepción/materiales/costos/IA/frontend; sin ciclos.
8. **Tests** de integridad, tenant y auditoría por entidad.
9. **Stop-the-line** si una decisión contradice RFC o Domain Handbook.

## Fases de implementación

| Fase | Alcance |
|------|---------|
| 1 | Models + typing_rules + Alembic + independencia |
| 2 | ProjectVersion ensure/seal + wiring HTTP mínimo |
| 3 | Jerarquía espacial Site→Building→Level→Space |
| 4 | Discipline + Element |
| 5 | ParameterSet + events + docs de límites |

## Consecuencias

- Dual-track schema: legacy `create_all` + MDO Alembic.
- Process permanece SoT legacy (strangler).
- Sin feature flag `MDO_V1` (PASO 1).
