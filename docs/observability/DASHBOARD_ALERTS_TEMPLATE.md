# Dashboard & alerts template — E01-F01

## Panels (golden)

1. Request rate — `arqia_http_requests_total`
2. Error rate 5xx — ratio `status_class="5xx"`
3. Latency — `arqia_http_request_duration_seconds_sum / count`
4. Queue depth — **stub 0** hasta E04

## Alertas P0 (plantilla)

| Alerta | Condición sugerida |
|--------|--------------------|
| 5xx spike | error rate > 1% / 5m |
| Metrics scrape fail | `/metrics` 401/5xx sostenido |
| DLQ > 0 | N/A hasta E04 (documentar placeholder) |
| Worker memory | N/A hasta workers |

Scrape: `GET /metrics` con `X-Metrics-Token` / Bearer.
