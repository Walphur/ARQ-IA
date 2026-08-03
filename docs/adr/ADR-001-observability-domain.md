# ADR-001 — Observability Domain

| Campo | Valor |
|-------|-------|
| Estado | Accepted |
| Fecha | 2026-08-03 |
| Épica | E01-F01 |
| Relacionados | ADR-002 Ports & Adapters, ADR-003 OBS_MODE |

## Contexto

ARQ-IA necesita correlación, logs estructurados, traces y métricas RED sin convertir la observabilidad en lógica de negocio ni acoplarla al Domain Handbook / MDO.

## Decisión

Existe un **dominio de infraestructura de Observability** con:

- Taxonomía de contexto: `request_id`, `trace_id`, `tenant_id`, `project_id`, `job_id`, `user_id`, `workspace_id`, `organization_id`, `feature`, `module`, `component`, `version`, `environment`.
- Servicio explícito `ObservabilityService` como API de aplicación.
- `trace_id` es responsabilidad exclusiva del backend; el frontend solo propaga `X-Request-Id`.
- La observabilidad no altera reglas de cómputo, presupuestos ni entidades MDO.

## Consecuencias

- Los handlers de negocio pueden registrar logs vía el servicio sin conocer vendors.
- Campos de taxonomía nullable cuando no aplican.
- Cambios futuros de APM no requieren tocar el dominio de obra.
