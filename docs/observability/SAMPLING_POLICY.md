# Sampling policy — E01-F01

## Modos

| OBS_MODE | Traces | Logs | Metrics |
|----------|--------|------|---------|
| off | none | WARNING+ | none |
| basic | 100% in-process (no export) | INFO+ JSON | 100% RED counters |
| full | 100% until volume justifies ratio; export OTLP if endpoint set | INFO+ JSON | 100% RED |

## Cardinality

Solo labels allowlist (`service`, `env`, `route_template`, `status_class`, `version`, `component`, `module`, `feature`, `plan`).  
Paths con IDs se normalizan a `{id}`.

## Futuro

Tail-based sampling y ratios por tenant quedan fuera de F01 (requiere E04/workers y evaluación de costo).
