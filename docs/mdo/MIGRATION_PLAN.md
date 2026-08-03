# Plan de migración schema — MDO vs legacy

## Estado actual (E02-F01)

| Dominio | Mecanismo |
|---------|-----------|
| Legacy (Studio/User/Project/Process/…) | `Base.metadata.create_all` + ALTER ensures ad-hoc en `main.startup` |
| MDO (`mdo_*`) | **Alembic** dedicado, version table `mdo_alembic_version` |

MDO **no** usa `create_all()`.

## Por qué Alembic solo en MDO ahora

- Compatibilidad: no forzar migración global del monolito en esta feature.
- El grafo MDO evolucionará rápido; necesita historial de revisiones real.
- Aislamiento: fallos de migrate MDO no deben mezclarse con DDL legacy opaco.

## Plan hacia Alembic global

1. Mantener branch Alembic `mdo` / version table dedicada durante E02-F01–F0x.
2. Cuando Roadmap endurezca Identity (E02) o Platform DB, introducir Alembic root en `backend/`.
3. Importar revisiones MDO como branch label o squash baseline `mdo@head` → revisión única en el root.
4. Migrar tablas legacy a revisiones Alembic; retirar `create_all` del startup.
5. Unificar version table o documentar multi-head explícito.

## Operación

```bash
cd backend
DATABASE_URL=... python3 -c "from mdo.setup import run_mdo_migrations; run_mdo_migrations('$DATABASE_URL')"
```

Startup de la app invocará `run_mdo_migrations` a partir de Fase 2 (wiring).
