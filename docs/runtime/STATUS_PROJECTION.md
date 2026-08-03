# /v1/platform/status — proyección (no checks)

El endpoint **no** es un health-check.

- No abre conexiones a DB, object storage ni broker.
- Publica `PLATFORM_MODE`, capabilities anunciadas, `generated_at`, `api_version`, `version`, `request_id`.
- Campo `ready`: copia de la última evaluación de `RuntimeStatusService.readiness()` (vía `GET /ready`). Si nunca se muestreó, `ready=true` + reason `readiness_unsampled`.
- `DegradationBanner` debe usar solo este endpoint.
