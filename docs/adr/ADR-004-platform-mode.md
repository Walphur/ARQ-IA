# ADR-004 — PLATFORM_MODE

| Campo | Valor |
|-------|-------|
| Estado | Accepted |
| Fecha | 2026-08-03 |
| Épica | E01-F02 |

## Decisión

Usar `PLATFORM_MODE=normal|degraded|maintenance|readonly` (env) para anunciar el estado operativo.

E01-F02 **no** implementa enforcement de writes/calcular. Solo publica capabilities vía `/v1/platform/status`. El bloqueo queda para Runtime Policies / Feature Flags (futuro / F03+).

## Consecuencias

- Sin FeatureFlag OLTP en F02.
- Banner y ops ven el mismo modo.
- Migración futura: flag `platform.mode` con los mismos valores.
