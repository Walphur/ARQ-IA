# ADR-002 — Ports & Adapters (Observability)

| Campo | Valor |
|-------|-------|
| Estado | Accepted |
| Fecha | 2026-08-03 |
| Épica | E01-F01 |
| Relacionados | ADR-001, ADR-003 |

## Contexto

El RFC E01 exige abstracción OpenTelemetry / métricas para evitar vendor lock. El dominio no debe importar SDKs externos.

## Decisión

- Ports obligatorios: `LoggerPort`, `TracerPort`, `MetricsPort`, `ClockPort`, `IdGeneratorPort`.
- Adapters concretos viven solo en `backend/infrastructure/observability/adapters/`.
- OpenTelemetry se importa únicamente en `adapters/otel.py`.
- La exposition de métricas (texto estilo Prometheus) es detalle del adapter `InMemoryMetrics`; el dominio solo ve `MetricsPort`.
- El paquete se llama `infrastructure` (no `platform`) para evitar un módulo genérico catch-all.

## Consecuencias

- Tests pueden inyectar null/in-memory adapters.
- Cambiar exporter OTLP o formato de métricas no toca `main` ni motores de visión.
- Regla enforceable: tests AST impiden imports vendor fuera de adapters.
