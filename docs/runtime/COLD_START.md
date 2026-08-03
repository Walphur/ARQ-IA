# Cold start — Runtime E01-F02

## Orden de bootstrap

1. `configure_observability()`
2. Crear SQLAlchemy `engine`
3. `configure_runtime(engine)` — **no** hace ping DB
4. App sirve tráfico

## Probes

| Probe | Path | Espera DB |
|-------|------|-----------|
| Render liveness | `/health` | No |
| Ops readiness | `/ready` | Sí (timeout `READY_DB_TIMEOUT_MS`, default 500ms) |

Cold start típico: `/health` debe responder antes de que la DB esté caliente. `/ready` puede devolver 503 hasta que el ping funcione.
