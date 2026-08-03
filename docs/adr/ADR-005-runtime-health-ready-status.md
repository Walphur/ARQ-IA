# ADR-005 — Runtime: /health · /ready · /v1/platform/status

| Campo | Valor |
|-------|-------|
| Estado | Accepted |
| Fecha | 2026-08-03 |
| Épica | E01-F02 |
| Paquete | `infrastructure/runtime` |

## Decisión

| Endpoint | Responsabilidad |
|----------|-----------------|
| `/health` | Liveness — proceso vivo; **sin** deps externas |
| `/ready` | Readiness — ejecuta checks (DB + stubs) |
| `/v1/platform/status` | Proyección UX/ops de `PLATFORM_MODE` + último readiness; **no ejecuta checks propios** |

`DegradationBanner` consume **exclusivamente** `/v1/platform/status`.

Render `healthCheckPath` permanece en `/health`.

## Consecuencias

- Failover FE intacto.
- Status incluye `generated_at`, `api_version`, `ready` proyectado.
- Paquete `runtime` (no `health`) para crecer sin renombrar.
