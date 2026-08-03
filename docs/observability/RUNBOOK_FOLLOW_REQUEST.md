# Runbook — Seguir un request (upload → costo)

## Objetivo

Dado un síntoma de usuario, localizar logs/spans del mismo flujo.

## Pasos

1. Pedir al usuario fecha/hora aproximada y obra (project).
2. Obtener `X-Request-Id` del response (Network tab) o del log de acceso.
3. Buscar en logs JSON: `request_id="<id>"`.
4. Campos útiles: `trace_id` (solo backend), `route_template`, `status_class`, `duration_ms`, `organization_id`/`tenant_id` si auth.
5. Cadena conceptual wedge: `/auth/login` → `/projects` → upload/calcular → items/total.
6. Hasta E04, `job_id` puede ser null; no esperar cola.

## Si no hay request_id

Regenerar el fallo con DevTools abierto; el frontend propaga `X-Request-Id` vía interceptor axios.
