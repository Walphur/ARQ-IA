# Chaos light — Runtime E01-F02

## Escenarios

1. **DB down:** `/health` → 200; `/ready` → 503 `db_unreachable`; `/v1/platform/status` proyecta `ready=false` solo **después** de un `/ready` fallido (status no abre conexiones propias).
2. **DB lenta:** timeout → `/ready` 503 `db_timeout`; `/health` sigue 200.
3. **Storage/broker absent:** checks `skipped`/`not_configured`; no bloquean ready si DB ok.
4. **PLATFORM_MODE=degraded|maintenance|readonly:** banner visible vía status; **sin** bloqueo de APIs de negocio en F02.

## Nota

`/v1/platform/status` no ejecuta checks: solo proyecta Runtime (`PLATFORM_MODE` + última muestra de readiness).
