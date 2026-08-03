# ADR-003 — OBS_MODE

| Campo | Valor |
|-------|-------|
| Estado | Accepted |
| Fecha | 2026-08-03 |
| Épica | E01-F01 |
| Relacionados | ADR-001, ADR-002 |

## Contexto

El roadmap mencionaba `obs.enhanced` vía FeatureFlag (E01-F03). F01 no puede implementar el store de flags. Se necesita un control de costo/verbosidad que escale.

## Decisión

Usar variable de entorno:

```
OBS_MODE=off|basic|full
```

| Modo | Correlation | Logs JSON | Spans/`trace_id` | RED `/metrics` | OTLP export |
|------|-------------|-----------|------------------|----------------|-------------|
| off | Sí | mínimo | No | No (404) | No |
| basic | Sí | Sí | In-process | Sí | No |
| full | Sí | Sí | Sí | Sí | Si hay endpoint |

`full` sin `OTEL_EXPORTER_OTLP_ENDPOINT` degrada a tracing in-process + warning (no tumba el boot).

Migración futura a FeatureFlag `obs.mode` queda para E01-F03 sin cambiar el contrato semántico de modos.

## Consecuencias

- Operación simple en Render vía env.
- No depende de OLTP/flags.
- Documenta el desvío controlado respecto al nombre `obs.enhanced` del roadmap.
