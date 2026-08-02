# ARQ-IA — RFC E01 Platform Foundations & Observability

## Metadatos del RFC

| Campo | Valor |
| --- | --- |
| ID | RFC-E01 |
| Título | Platform Foundations & Observability |
| Estado | Proposed → Ready for implementation after approval |
| Fecha | 2026-08-02 |
| Owners | CTO / Tech Lead |
| Épica | E01 |
| Prioridad | P0 |
| Complejidad | M |
| Estimación | 1–2 meses (1–2 eng) |
| Dependencias | Ninguna (fundación) |
| Capacidad máxima plataforma | ≤20% del equipo (ENGINEERING_ROADMAP E01) |
| Documentos fuente | AUDITORIA · MASTER PLAN · ARCHITECTURE · ENGINEERING_ROADMAP |
| Naturaleza | Contrato de diseño (sin código de implementación) |
| Idioma | Español |
| Mercado | LATAM primero |
| Cuña a preservar | color → qty → ARS (moneda local) |
| Norte arquitectura | Etapa 1 cimientos; transversal API / workers / Studio |
| Abstracción observabilidad | OpenTelemetry (anti vendor-lock) |
| Bus de eventos | NO en E01 — solo correlation + shape SettingsActualizados |
| MDO rewrite | PROHIBIDO en E01 |

Este RFC es el contrato técnico previo a la implementación de la épica **E01 Platform Foundations & Observability** del documento oficial `ENGINEERING_ROADMAP.md`. No reescribe AUDITORIA, MASTER PLAN ni ARCHITECTURE: los respeta y los operacionaliza en contratos, checklists, esquemas y gates ejecutables.

Cualquier desviación material de este RFC durante la implementación requiere ADR + aprobación Tech Lead/CTO antes del merge a `main`.

Naturaleza del documento: diseño / contrato. **No** contiene funciones ejecutables ni cuerpos de implementación.

## Índice

- [0. Resumen ejecutivo / contexto](#0-resumen-ejecutivo--contexto)
- [1. Estado actual](#1-estado-actual)
- [2. Alcance IN / OUT](#2-alcance-in--out)
- [3. Diseño técnico](#3-diseño-técnico)
- [4. Archivos](#4-archivos)
- [5. Modelo de datos](#5-modelo-de-datos)
- [6. API](#6-api)
- [7. Eventos](#7-eventos)
- [8. Frontend](#8-frontend)
- [9. Tests](#9-tests)
- [10. Migración desde estado actual](#10-migración-desde-estado-actual)
- [11. Riesgos + mitigaciones](#11-riesgos--mitigaciones)
- [12. Criterios de aceptación objetivos](#12-criterios-de-aceptación-objetivos)
- [13. Checklist final task-by-task](#13-checklist-final-task-by-task)
- [Apéndice A — Variables de entorno nuevas](#apéndice-a--variables-de-entorno-nuevas)
- [Apéndice B — ADR titles a escribir durante E01](#apéndice-b--adr-titles-a-escribir-durante-e01)
- [Apéndice C — Dashboard panels](#apéndice-c--dashboard-panels)
- [Apéndice D — Alert rules](#apéndice-d--alert-rules)
- [Apéndice E — Sampling policy](#apéndice-e--sampling-policy)
- [Apéndice F — Log field schema](#apéndice-f--log-field-schema)
- [Apéndice G — Compatibility matrix Free/Pro/Enterprise](#apéndice-g--compatibility-matrix-freeproenterprise)
- [Apéndice H — Mapping a Architecture domains](#apéndice-h--mapping-a-architecture-domains)
- [Apéndice I — Anti-scope list explícita](#apéndice-i--anti-scope-list-explícita)
- [Apéndice J — Approval sign-off](#apéndice-j--approval-sign-off)
- [Apéndice K — Glosario E01](#apéndice-k--glosario-e01)
- [Apéndice L — Decision log](#apéndice-l--decision-log)
- [Apéndice M — Open questions](#apéndice-m--open-questions)
- [Apéndice N — Trazabilidad Roadmap → RFC](#apéndice-n--trazabilidad-roadmap--rfc)
- [Apéndice O — Runbook skeletons](#apéndice-o--runbook-skeletons)
- [Apéndice P — Performance budgets](#apéndice-p--performance-budgets)
- [Apéndice Q — Security & PII](#apéndice-q--security--pii)
- [Apéndice R — Rollback playbooks](#apéndice-r--rollback-playbooks)
- [Apéndice S — Demo scripts](#apéndice-s--demo-scripts)
- [Apéndice T — Registro de control](#apéndice-t--registro-de-control)
- [Apéndice U — Matrices extendidas de contratos](#apéndice-u--matrices-extendidas-de-contratos)
- [Apéndice V — Catálogo de escenarios operativos](#apéndice-v--catálogo-de-escenarios-operativos)

## 0. Resumen ejecutivo / contexto

### 0.1 Objetivo oficial (ENGINEERING_ROADMAP § E01)

Establecer cimientos de plataforma: logging estructurado, tracing distribuido, métricas, health/ready, config, feature flags, CI quality gates y runbooks mínimos para operar el wedge sin cajas negras.

Problema que resuelve: sin observabilidad y gates, perception/jobs fallan en silencio y los releases no son seguros para LATAM productivo.

Beneficio: MTTR bajo, releases con evidencia, base transversal para todas las épicas posteriores.

Dependencias: ninguna (fundación). Complejidad M. Prioridad P0. Tiempo 1–2 meses (1–2 eng).

### 0.2 Criterio de Done de la épica (fuente roadmap)

- Dashboards core vivos
- trace_id en request→job (preparación de correlación; workers reales en E04/E05)
- Flags con audit
- CI bloquea P0 debt
- Runbook health/DLQ publicado (DLQ como estructura preparatoria; bus real en E04)

### 0.3 Features contenidas (F01–F05)

| Feature | Nombre | Intent condensado |
| --- | --- | --- |
| E01-F01 | Observabilidad base | Logs JSON, traces OTel, métricas RED mínimas, correlation ids |
| E01-F02 | Health, readiness y degradación | /health vs /ready, banner Studio, modo degradado |
| E01-F03 | Feature flags & config dinámica | Entidad, admin API, SDK server/FE, audit, expiry |
| E01-F04 | CI quality gates & standards | lint/types/unit, floors, secret scan, CONTRIBUTING, PR template |
| E01-F05 | Runbooks y operabilidad | DLQ stub, rollback flags, sev defs, oncall stub, postmortem |

### 0.4 Principios duros que este RFC no puede violar

| Principio | Implicación en E01 |
| --- | --- |
| P01 Compatibilidad hacia atrás | Mantener GET /health y /api/health; no romper App.js failover |
| P02 Épicas desplegables | Cada Fxx mergeable detrás de flag |
| P03 Testabilidad | CI floors + otel smoke + flag evaluation + isolation |
| P04 Cero debt silencioso | TODO sin issue = bloqueante en PR template |
| P05 Boundaries de dominio | Platform/Settings/Audit light; no reescribir MDO |
| P06 Incrementalismo brutal | Cap ≤20% capacidad; no pausar wedge por plataforma perfecta |
| Cuña comercial | Golden color→qty→ARS debe permanecer verde |
| OpenTelemetry first | Abstracción; sin vendor lock APM |
| Label allowlist | Cardinality controlada; nunca email/nombre proyecto crudo |
| Sin bus completo | Solo correlation + shape opcional SettingsActualizados (E04 = bus) |
| Sin marketplace/chat/plugins | Hard freeze |
| Sin rewrite MDO | Hard freeze |

### 0.5 Non-goals (preview; detalle en §2 y Apéndice I)

- No reescritura MDO / entities Construction
- No marketplace / chat / plugins
- No outbox/bus completo (E04)
- No object storage (E03)
- No identity rewrite (E02) — solo AuthZ mínima owner-only en admin flags
- No Alembic full adoption (solo bootstrap mínimo si hace falta para feature_flags)
- No multi-region / GPU workers / APM vendor-specific SDKs como dependencia dura
- No rotación inesperada de SECRET_KEY (riesgo ops documentado; fix completo puede ser E02)
- No eliminar precios.json
- No rediseño visual completo del Studio
- No SliSnapshot persistente obligatorio
- No persistir cada health check en OLTP

### 0.6 Capacidad y secuenciación

El roadmap fija un **cap ≤20% de la capacidad del equipo** en trabajo de plataforma durante E01. El diseño es minimalista en SLIs, exporters opcionales detrás de `obs.enhanced`, y fases A–E con kill switches.

Secuenciación roadmap: (1) no romper wedge, (2) emitir/consumir eventos vía outbox cuando mute hechos — en E01 solo preparar envelope/correlation, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

### 0.7 Señales de éxito post-release (roadmap)

- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### 0.8 Audiencia y uso del RFC

| Rol | Uso |
| --- | --- |
| CTO | Aprobar alcance, anti-scope, capacidad ≤20% |
| Tech Lead | Aprobar contratos API/eventos/datos; reviewer ADR |
| Domain Eng Platform | Implementar F01–F05 según fases |
| Frontend Eng | Banner, FlagProvider, interceptor request id |
| QA | Matrices §9; golden wedge; isolation |
| PM | Criterios binarios/numéricos §12 |
| Oncall futuro | Runbooks §13 / Apéndice O |

### 0.9 Diagrama de contexto (alto nivel)

```
┌─────────────────────────────────────────────────────────────────┐
│                     ARQ-IA Studio (CRA)                         │
│  axios failover /health · DegradationBanner · FlagProvider      │
│  X-Request-Id interceptor · lastTraceId for support             │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP + X-Request-Id
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI monolith (backend/main.py)                 │
│  LoggingMiddleware → TracingMiddleware → MetricsMiddleware      │
│  Domain handlers (wedge UNCHANGED)                              │
│  /health · /ready · /metrics · /v1/admin/flags · /v1/platform/* │
└───────┬──────────────────┬──────────────────┬───────────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
   OLTP flags         OTLP optional      Log sink (stdout JSON)
   (+ audit)          (obs.enhanced)     Metrics scrape/export
```

### 0.10 Relación con documentos oficiales

| Documento | Qué aporta a este RFC | Qué NO hace este RFC |
| --- | --- | --- |
| AUDITORIA | Hechos de deuda/ops (SECRET_KEY, prints, sin CI) | No re-auditar producto |
| MASTER PLAN | Secuencia comercial wedge LATAM | No redefinir roadmap comercial |
| ARCHITECTURE | Dominios Platform/Settings; envelope §5.4; Etapa 1 | No inventar bus/MDO |
| ENGINEERING_ROADMAP | E01 F01–F05 tasks, DoD, riesgos, cap 20% | No alterar épicas posteriores |

### 0.11 Definition of Ready de este RFC (antes de coding)

- [ ] Contratos de eventos/API bocetados y revisados por Tech Lead (este documento)
- [ ] Criterios de aceptación numéricos o binarios acordados con PM (§12)
- [ ] Owner de dominio Platform asignado + reviewer arquitectura
- [ ] Plan de migración/datos y de rollback escrito (§10, Apéndice R)
- [ ] Lista de lo que explícitamente NO entra (Apéndice I, ≥40 bullets)
- [ ] Cap ≤20% confirmado en planning del sprint de arranque

- Nota de alineación 0.align.01: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.02: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.03: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.04: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.05: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.06: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.07: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.08: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.09: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.10: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.11: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.12: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.13: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.14: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.15: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.16: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.17: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.18: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.19: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.
- Nota de alineación 0.align.20: este RFC es contrato de implementación E01; cualquier PR fuera de F01–F05 se rechaza sin ADR.

## 1. Estado actual

### 1.1 Método de este capítulo

Análisis de diseño basado en hechos del repositorio actual (no es un nuevo ensayo de auditoría). Las tablas siguientes son el baseline contra el cual se mide el delta de E01.

### 1.2 EXISTE hoy

| Área | Hecho observado | Ubicación / evidencia | Implicación E01 |
| --- | --- | --- | --- |
| API | Monolito FastAPI | `backend/main.py` | Middleware hooks mínimos; no split de servicios |
| Health | GET `/health` → `{status, version}` | `main.py` health() | Reutilizar como liveness |
| Health alias | GET `/api/health` mismo shape | `main.py` health_api() | Backward compat obligatoria |
| Root | GET `/` status + links | `main.py` | No cambiar semántica de producto |
| Version | `APP_VERSION` env | `main.py` / env | Exponer también en `/v1/platform/version` |
| CORS | CORSMiddleware activo | `main.py` | Preservar; request-id header allow |
| Logging | `print()` WARN ad-hoc | startup, migraciones, Sheets | Migrar a logger estructurado |
| OTel/Sentry/APM | Ausente en requirements | `requirements.txt` | Añadir OTel API/SDK opcional |
| Ready | No existe `/ready` | — | Nuevo endpoint F02 |
| Metrics | No existe `/metrics` | — | Nuevo endpoint F01/F02 |
| FeatureFlags | Sin entidades | modelos actuales | Nuevas tablas F03 |
| Migraciones | `create_all` + ALTER ad-hoc startup | `ensure_schema` | Bootstrap mínimo flags; no Alembic full |
| Tests | pytest parcial billing/motor/export/pdf | `backend/tests/` | Extender; floors CI |
| CI | Sin GitHub Actions en repo | sin `.github/workflows` | Añadir `ci.yml` F04 |
| Frontend probe | CRA App.js axios GET `/health` failover | `frontend/src/App.js` | Reutilizar; añadir request id |
| Web vitals | presente, no wired a backend | `reportWebVitals.js` | Opcional later; no scope forzar |
| Render | `healthCheckPath: /health` | `render.yaml` | Mantener path liveness |
| SECRET_KEY | `generateValue: true` en Render | `render.yaml` | Documentar higiene; no rotar en E01 |
| Demo rate limit | in-memory window | `check_demo_rate_limit` | No rediseñar en E01 |
| Wedge motor | `motor_ia.procesar_plano_ia` | `motor_ia.py` | No tocar semántica color→qty→ARS |
| Precios | `precios.json` + Sheets fallback | backend | NO eliminar en E01 |
| Billing | Mercado Pago light | `billing_mp.py` | Fuera de alcance rewrite |
| Deps API | fastapi 0.115.6 / sqlalchemy 2.0.36 / pytest 8.3.4 | `requirements.txt` | Baseline versiones |
| Deploy FE | static Render + rewrite SPA | `render.yaml` | Sin cambio estructural |

### 1.3 FALTA hoy (gap analysis)

| Capacidad | Estado | Feature E01 | Prioridad gap |
| --- | --- | --- | --- |
| Structured JSON logs | Ausente | F01 | P0 |
| Distributed traces | Ausente | F01 | P0 |
| RED metrics | Ausente | F01 | P0 |
| correlation_id / X-Request-Id middleware | Ausente | F01 | P0 |
| Ready vs Live | Ausente | F02 | P0 |
| Degradation banner Studio | Ausente | F02 | P0 |
| Feature flags + audit | Ausente | F03 | P0 |
| Admin flags UI | Ausente | F03 | P1 (mínima) |
| CI quality gates | Ausente | F04 | P0 |
| CONTRIBUTING / ADR folder | Ausente | F04 | P0 |
| Runbooks operativos | Ausente | F05 | P0 |
| Dashboard/alerts | Ausente | F01/F05 | P0 mínimo |
| Log redaction PII | Ausente | F01 | P0 |
| Sampling policy | Ausente | F01 | P0 doc |
| Release markers | Ausente | F03 opcional | P2 |
| Platform status API | Ausente | F02 | P0 |

### 1.4 REUTILIZAR

| Activo | Cómo se reutiliza en E01 |
| --- | --- |
| GET `/health` | Liveness puro; sin deep checks |
| GET `/api/health` | Alias compat; misma semántica liveness |
| `APP_VERSION` | Campo `version` en health/ready/platform/version |
| Patrón axios probe | Extender con header X-Request-Id + status platform |
| Base pytest | Añadir suites platform sin romper existentes |
| Patrón env vars | Nuevas vars OTEL_*/LOG_LEVEL/METRICS_TOKEN |
| Render healthCheckPath `/health` | Sin cambio de path (evitar false restarts) |
| CORS allowlist | Añadir exposición de X-Request-Id si hace falta |
| Modelo Studio/owner actual | AuthZ mínima admin flags hasta E02 |
| Tests motor/billing/export/pdf | Regresión obligatoria en CI |

### 1.5 MODIFICAR (lista de diseño; sin código aquí)

| Archivo | Cambio conceptual mínimo | Riesgo |
| --- | --- | --- |
| `backend/main.py` | Hooks middleware + include routers platform; no reordenar dominio wedge | Medio |
| `backend/requirements.txt` | Deps OTel opcionales / extras documentados | Bajo |
| `frontend/src/App.js` | Interceptor request id + DegradationBanner mount | Medio UI |
| `render.yaml` | Env OTEL_*/LOG_LEVEL/METRICS_TOKEN (sin rotar SECRET_KEY) | Bajo |
| Nuevo CI workflow | Gates F04 | Bajo ops |

### 1.6 ELIMINAR / DEPRECAR

| Ítem | Acción E01 | Notas |
| --- | --- | --- |
| `print()` como path primario de logging | Deprecar → structured logger | Mantener fallback temporal si logger falla |
| Semántica confusa health=ready | Separar explícitamente | Render sigue en /health |
| `precios.json` | NO eliminar | Out of scope cleanup |
| Demo rate limit in-memory | NO eliminar/reescribir | E02+ si se endurece |

### 1.7 Inventario de endpoints actuales relevantes

| Método | Path | Rol actual | Cambio E01 |
| --- | --- | --- | --- |
| GET | `/` | Status + links | Sin cambio funcional |
| GET | `/health` | Liveness implícito | Documentar como liveness formal |
| GET | `/api/health` | Alias FE/ops | Mantener |
| GET | `/ready` | N/A | Crear |
| GET | `/metrics` | N/A | Crear (protegido) |
| GET | `/v1/admin/flags` | N/A | Crear |
| PATCH | `/v1/admin/flags/{key}` | N/A | Crear |
| GET | `/v1/platform/status` | N/A | Crear |
| GET | `/v1/platform/version` | N/A | Crear |
| POST | `/calcular` (+ `/api/calcular`) | Wedge core | Solo correlación; no lógica |

### 1.8 Stack actual (baseline)

| Capa | Tecnología | Versión observada / nota |
| --- | --- | --- |
| API | FastAPI | 0.115.6 |
| Server | uvicorn | 0.34.0 |
| ORM | SQLAlchemy | 2.0.36 |
| DB driver | psycopg | 3.2.3 |
| CV | opencv-contrib-headless | 4.10.0.84 |
| OCR | pytesseract | 0.3.13 |
| Tests | pytest | 8.3.4 |
| FE | CRA + axios | App.js monolítico |
| Deploy | Render docker + static | render.yaml |

### 1.9 Observabilidad actual: diagrama de vacío

```
Hoy:
  Request → CORS → handler → print(WARN?) → response
  (sin trace_id, sin metrics, sin ready, sin flags)

E01 target:
  Request → Logging → Tracing → Metrics → handler → JSON logs + OTLP?
           └─ X-Request-Id / traceparent propagado
```

### 1.10 Deuda ops conocida (no fix completo E01)

| Deuda | Severidad | Acción E01 | Épica dueña del fix profundo |
| --- | --- | --- | --- |
| SECRET_KEY generateValue:true puede rotar en redeploy | Alta ops | Documentar + checklist higiene; NO rotar sorpresa | E02 / ops |
| SQLite efímera si falta DATABASE_URL en Render | Alta | Ready check debe fallar si DB no usable en prod | Ops + F02 |
| Sin Alembic | Media | Bootstrap mínimo flags OR create_all+ensure | E01 decision §5 |
| Sin CI | Alta eng | Introducir gates F04 | E01-F04 |
| print logging | Media | Migrar path primario | E01-F01 |

- Hallazgo baseline 1.baseline.01: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.02: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.03: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.04: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.05: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.06: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.07: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.08: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.09: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.10: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.11: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.12: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.13: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.14: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.15: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.16: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.17: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.18: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.19: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.20: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.21: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.22: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.23: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.24: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.
- Hallazgo baseline 1.baseline.25: registrado para trazabilidad de diseño; no implica scope creep fuera de F01–F05.

### 1.11 Matriz resumen EXISTE / FALTA / REUTILIZAR / MODIFICAR / ELIMINAR

| Categoría | Conteo ítems clave | Owner diseño |
| --- | --- | --- |
| EXISTE | 24 filas §1.2 | Tech Lead |
| FALTA | 16 filas §1.3 | Platform |
| REUTILIZAR | 10 filas §1.4 | Platform |
| MODIFICAR | 5 filas §1.5 | Platform+FE |
| ELIMINAR/DEPRECAR | 4 filas §1.6 | Platform |

### 1.12 Mapa de tests existentes a preservar

| Archivo test | Área | Gate E01 |
| --- | --- | --- |
| `test_billing_mp.py` | Billing MP | Debe seguir verde |
| `test_motor_ia.py` | Wedge motor | Debe seguir verde (golden) |
| `test_export_and_muros.py` | Export/muros | Debe seguir verde |
| `test_pdf_and_email.py` | PDF/email | Debe seguir verde |

## 2. Alcance IN / OUT

### 2.1 IN — exactamente F01–F05

#### 2.1.1 E01-F01 Observabilidad base

- Taxonomía campos obligatorios: tenant_id, project_id, job_id, trace_id (nullable cuando no aplique)
- Instrumentación API gateway con OpenTelemetry (API + SDK opcional por env)
- Preparación de contexto propagable a workers futuros (E04/E05); stubs documentados
- Dashboard golden: latencia API, error rate, cola depth (cola depth = stub/gauge 0 hasta E04)
- Alertas P0 plantilla: 5xx spike; DLQ>0 (stub until E04); disk/memory workers (doc)
- Log redaction PII/secretos
- Sampling policy documentada
- Tests presencia correlation ids
- Runbook seguir request (upload→costo path conceptual)
- Flag `obs.enhanced` para exporters caros
- Métricas RED/USE mínimas

#### 2.1.2 E01-F02 Health, readiness y degradación

- Endpoints `/health` y `/ready` separados
- Checks DB; object storage/broker stubs `skipped/not_configured` hasta E03/E04
- Modo degradado vía flags (`platform.degraded`, disable AI/exports)
- Banner UI degradación Studio
- Tests readiness (DB down; outbox stuck = futuro/skip hasta E04 con contrato)
- Métrica `platform.ready`
- Documentar cold start bootstrap (no SLO estricto aún)
- Chaos light documentado

#### 2.1.3 E01-F03 Feature flags & config dinámica

- Entidad FeatureFlag con targeting plan/org/project
- API admin interna + audit trail (nunca hard-delete audit)
- SDK server evaluation determinista
- SDK frontend cache TTL
- Tests matriz flag × plan
- Seed flags wedge
- Campo expiry (prohibir flags eternas)
- Dashboard flags stale >90 días (panel mínimo)

#### 2.1.4 E01-F04 CI quality gates & engineering standards

- Pipeline lint + types + unit
- Coverage floors módulos críticos
- Secret scan + dependency audit
- Contract test placeholder eventos
- Policy no merge TODO sin issue
- PR template checklist P01–P10
- Badge wedge e2e smoke (skippeable con waiver)
- CONTRIBUTING conceptual DoR/DoD

#### 2.1.5 E01-F05 Runbooks y operabilidad inicial

- Runbook DLQ vacío (estructura)
- Runbook rollback feature flag
- Runbook incident sev definitions
- Oncall roster stub
- Postmortem template
- MTTR tracking manual→auto (proceso)
- Lista owners por dominio
- Drill trimestral calendarizado

### 2.2 OUT — hard freeze

| Ítem OUT | Épica dueña | Nota |
| --- | --- | --- |
| Identity rewrite / sessions hardening | E02 | Solo AuthZ mínima admin flags |
| Object storage signed URLs | E03 | Ready stub not_configured |
| Outbox/bus/queues/WS progress | E04 | Solo correlation + envelope shape |
| Perception CV/OCR changes | E05 | No tocar motor_ia semántica |
| Geometry engine | E06 | — |
| MDO entities/versions/changesets | E07 | Prohibido rewrite |
| Materials/Costs/Takeoff rewrite | E08–E10 | — |
| Scenarios Git-like | E11 | — |
| Studio multi-panel redesign | E12 | Solo banner/flags mínimos |
| Reports pipeline rewrite | E13 | Degradación puede deshabilitar exports vía flag |
| Chat IA | E15 | Prohibido |
| AI Orchestrator | E16 | Prohibido |
| Plugins / Marketplace | E19–E21 | Prohibido |
| SSO/SAML | E22 | — |
| Public API keys/webhooks | E23 | — |
| Data lake / analytics | E24 | — |
| Mobile | E25 | — |
| Alembic full adoption | — | Solo bootstrap mínimo opcional |
| Multi-region / GPU workers | — | Anti-scope |
| Vendor APM lock-in SDK-only | — | OTel abstracción |
| Eliminar precios.json | — | Out of scope cleanup |
| Rotación forzada SECRET_KEY | E02/ops | Documentar riesgo solamente |

### 2.3 Hard freeze statement

**HARD FREEZE:** Nada fuera del alcance IN (§2.1) puede implementarse bajo este RFC. Cualquier PR que introduzca entidades MDO, bus/outbox real, marketplace, chat, plugins, o cambios semánticos al wedge color→qty→ARS será rechazado salvo ADR aprobado que modifique este RFC.

### 2.4 Decisiones de alcance borderline

| Pregunta | Decisión E01 | Racional |
| --- | --- | --- |
| ¿Alembic? | Preferir path mínimo: tabla flags vía ensure_schema/create_all; Alembic bootstrap SOLO si se necesita versionado formal de feature_flags | Evitar adopción full prematura |
| ¿Persistir cada /health? | NO (HealthCheckRecord opcional ephemeral/ops — prefer not) | Cardinality + costo |
| ¿SliSnapshot? | OUT o minimal later | SLIs vía TSDB externo |
| ¿ReleaseMarker? | Opcional minimal | Útil para correlacionar deploys en dashboards |
| ¿UsoRegistrado? | Opcional deferred | No bloquear E01 |
| ¿Workers instrumentation real? | Hooks/context helpers only; workers reales E04/E05 | Cap 20% |
| ¿web-vitals → backend? | No obligatorio E01 | Puede ticketearse P2 |

- Ítem de freeze checklist 2.freeze.01: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.02: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.03: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.04: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.05: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.06: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.07: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.08: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.09: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.10: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.11: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.12: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.13: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.14: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.15: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.16: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.17: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.18: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.19: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.20: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.21: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.22: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.23: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.24: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.25: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.26: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.27: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.28: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.29: verificado contra Apéndice I anti-scope; no negociable sin ADR.
- Ítem de freeze checklist 2.freeze.30: verificado contra Apéndice I anti-scope; no negociable sin ADR.

## 3. Diseño técnico

### 3.1 Arquitectura de middleware (contrato)

```
Client --X-Request-Id--> API Gateway/App
  -> LoggingMiddleware (JSON logs)
  -> TracingMiddleware (OTel)
  -> MetricsMiddleware (RED)
  -> Domain handlers (unchanged business)
  -> optional exporters (OTLP)
```

### 3.2 Flujo detallado de un request

```
┌────────┐   X-Request-Id / traceparent   ┌──────────────────────┐
│ Client │ ─────────────────────────────► │ ASGI / FastAPI app   │
└────────┘                                └──────────┬───────────┘
                                                     │
                         1) ensure_request_id()      │
                         2) bind log context         │
                         3) start root span          │
                         4) start timer RED          │
                                                     ▼
                                          ┌────────────────────┐
                                          │ Route handler      │
                                          │ (calcular, auth…)  │
                                          └─────────┬──────────┘
                                                    │
                         5) record status_class     │
                         6) end span                │
                         7) emit log line           │
                         8) echo X-Request-Id       │
                                                    ▼
                                               Response
```

### 3.3 Módulos/packages conceptuales

| Path conceptual | Responsabilidad | Dependencias |
| --- | --- | --- |
| `backend/platform/logging.py` | JSON logger, redaction, contextvars | stdlib logging |
| `backend/platform/tracing.py` | OTel tracer provider, propagation | opentelemetry-api; SDK si enabled |
| `backend/platform/metrics.py` | RED counters/histograms; allowlist labels | prometheus_client u OTel metrics |
| `backend/platform/health.py` | liveness/readiness assemblers | SQLAlchemy engine ping |
| `backend/platform/flags.py` | FeatureFlag store + evaluator | OLTP |
| `backend/platform/config.py` | Env typed settings platform | os.environ |
| `backend/platform/correlation.py` | request_id / trace_id helpers | contextvars |
| `backend/platform/events_shapes.py` | SettingsActualizados envelope shape | schemas JSON |
| `frontend/src/platform/requestId.js` | axios interceptor | axios |
| `frontend/src/platform/flagsClient.js` | FlagProvider + cache TTL | fetch/axios |
| `frontend/src/platform/DegradationBanner.js` | UI banner | React |
| `docs/runbooks/` | Operabilidad F05 | markdown |
| `docs/adr/` | ADRs E01 | markdown |
| `.github/workflows/ci.yml` | Gates F04 | GHA |

### 3.4 Interfaces conceptuales (nombres de método; sin cuerpos)

#### 3.4.1 Logging

| Método | Entrada | Salida | Notas |
| --- | --- | --- | --- |
| `configure_logging(settings)` | Settings | None | Idempotente |
| `get_logger(name)` | str | LoggerAdapter | JSON formatter |
| `bind_context(**fields)` | kwargs | token | contextvars |
| `redact(payload)` | dict/str | dict/str | PII/secrets |
| `log_request(event)` | RequestLog | None | access log |

#### 3.4.2 Tracing

| Método | Entrada | Salida | Notas |
| --- | --- | --- | --- |
| `init_tracing(settings)` | Settings | None | No-op si OTEL_ENABLED=false |
| `start_span(name, attrs)` | str, dict | Span | Allowlist attrs |
| `inject_headers(headers)` | dict | dict | W3C traceparent |
| `extract_context(headers)` | dict | Context | Inbound |
| `get_trace_id()` | — | str|None | Para logs |

#### 3.4.3 Metrics

| Método | Entrada | Salida | Notas |
| --- | --- | --- | --- |
| `init_metrics(settings)` | Settings | None | — |
| `inc_request(labels)` | Labels | None | Allowlist enforced |
| `observe_latency(seconds, labels)` | float, Labels | None | Histogram |
| `set_ready(value)` | bool | None | Gauge platform.ready |
| `render_prometheus()` | — | str | Para GET /metrics |

#### 3.4.4 Health

| Método | Entrada | Salida | Notas |
| --- | --- | --- | --- |
| `liveness()` | — | HealthResponse | Sin deep checks |
| `readiness()` | — | ReadyResponse | DB + stubs |
| `check_db()` | — | CheckResult | SELECT 1 |
| `check_object_storage()` | — | CheckResult | skipped until E03 |
| `check_broker()` | — | CheckResult | skipped until E04 |

#### 3.4.5 Flags

| Método | Entrada | Salida | Notas |
| --- | --- | --- | --- |
| `get_flag(key)` | str | FeatureFlag|None | — |
| `list_flags(filters)` | Filters | list | Admin |
| `patch_flag(key, patch, actor)` | … | FeatureFlag | Audit + event shape |
| `evaluate(key, ctx)` | str, EvalContext | Evaluation | Determinista |
| `seed_defaults()` | — | None | Migración |

### 3.5 Matriz de responsabilidades

| Componente | Escribe | Lee | Emite | No debe |
| --- | --- | --- | --- | --- |
| LoggingMiddleware | logs stdout | headers/context | — | Tocar negocio |
| TracingMiddleware | spans | traceparent | OTLP opcional | Vendor SDK directo en dominio |
| MetricsMiddleware | counters | route template | — | Labels high-cardinality |
| Flags service | flags+audit | OLTP | SettingsActualizados shape | Hard-delete audit |
| Health service | — | DB/engine | métrica ready | Persistir cada check |
| Studio banner | local UI state | platform/status | — | Inventar SoT |
| Domain wedge | igual que hoy | igual | — | Depender de vendor APM |

### 3.6 SLIs / SLOs mínimos

| SLI | Definición | SLO inicial E01 | Fuente |
| --- | --- | --- | --- |
| API availability | % requests no-5xx en rutas críticas excl. /metrics | ≥ 99.0% semanal (staging/prod según entorno) | metrics |
| API latency p95 | latencia handler p95 rutas wedge | Documentar baseline; target blando ≤ 3s rutas no-CV; CV rutas aparte | histograms |
| Error rate 5xx | 5xx / total | ≤ 1% en 1h rolling (alerta) | metrics |
| Health/ready truthfulness | `/ready` false cuando DB down; `/health` true si proceso up | 100% en chaos light | tests+chaos |
| Cold start bootstrap | tiempo hasta ready=true tras deploy | Documentado; SIN SLO estricto aún | ops notes |

### 3.7 Label allowlist estricta

| Label | Valores permitidos | Cardinality | Notas |
| --- | --- | --- | --- |
| `service` | `arq-ia-api` | 1 | Fijo |
| `env` | `dev|staging|prod` | 3 | — |
| `route_template` | templates normalizados (`/calcular`, `/v1/admin/flags/{key}`) | O(rutas) | Nunca path crudo con IDs |
| `status_class` | `2xx|3xx|4xx|5xx` | 4 | — |
| `plan` | `free|pro|enterprise|unknown` | ≤4 | Cuidado; solo si ya resuelto |
| `flag_key` | keys conocidas seed | O(flags) | Solo métricas flags |
| `check_name` | `db|object_storage|broker` | ≤10 | Ready checks |

**PROHIBIDO en labels:** email, user_id crudo, project name, filename, querystring, tenant name free-text, IDs de alta cardinalidad sin hashing/bucketing aprobado por ADR.

### 3.8 Dependencias opcionales detrás de env

| Capacidad | Env gate | Default | Comportamiento off |
| --- | --- | --- | --- |
| OTel SDK export | `OTEL_ENABLED` | false | No-op tracer |
| OTLP endpoint | `OTEL_EXPORTER_OTLP_ENDPOINT` | empty | No export |
| Enhanced exporters | flag `obs.enhanced` | false | Sampling bajo / sin export caro |
| Metrics token | `METRICS_TOKEN` | required prod | 401/403 sin token |
| Log level | `LOG_LEVEL` | INFO | — |
| JSON logs | `LOG_FORMAT=json` | json en prod | text en dev opcional |

### 3.9 Modelo de degradación

```
platform.degraded = true  OR  ready.db = fail
        │
        ├─► GET /v1/platform/status → {degraded:true, reasons:[…]}
        ├─► Studio DegradationBanner visible
        └─► Flags pueden deshabilitar AI/exports (sin romper read paths)
```

### 3.10 Estrategia OpenTelemetry (anti vendor-lock)

- Instrumentar vía OpenTelemetry API
- SDK + exporter OTLP opcionales
- Prohibido acoplar handlers de dominio a SDK de Datadog/NewRelic/Sentry como dependencia dura
- Sentry u otros pueden añadirse como exporters detrás de bridge OTel en ADR futuro — no en E01 core
- Propagación W3C Trace Context + `X-Request-Id` (dual) para soporte humano

### 3.11 Correlation model

| Campo | Origen | Propagación | Persistencia E01 |
| --- | --- | --- | --- |
| `request_id` | Header `X-Request-Id` o UUID generado | Response header + logs | No DB |
| `trace_id` | OTel / traceparent | logs + spans | No DB |
| `span_id` | OTel | logs opcionales | No DB |
| `tenant_id` | auth context si existe | logs/spans attrs allowlist | cuando disponible |
| `project_id` | path/body si existe | logs | nullable |
| `job_id` | futuro E04 | preparado en taxonomía | nullable E01 |
| `correlation_id` | alias documentado = request_id salvo override | event envelope shape | en evento shape |

### 3.12 Diagrama de deployment E01

```
Render Web Service (arq-ia-api)
  healthCheckPath: /health          ◄── liveness only
  optional probe ops: /ready        ◄── no cambiar healthCheckPath aún
  scrape/auth: /metrics             ◄── METRICS_TOKEN
  env: LOG_LEVEL, OTEL_*, APP_VERSION

Render Static (arq-ia-web)
  REACT_APP_API_URL → api
  banner polls /v1/platform/status
```

### 3.13 Contratos de error platform

| Código | Cuándo | Body shape |
| --- | --- | --- |
| 401 | Admin/metrics sin auth | `{error:{code,message,request_id}}` |
| 403 | AuthZ owner fail | idem |
| 404 | Flag key inexistente | idem |
| 409 | Version conflict flag (si etag/version) | idem |
| 422 | Patch inválido | idem |
| 503 | Ready fail (solo /ready) | `{status:not_ready, checks:[…]}` |

### 3.14 Seguridad de superficie nueva

- `/metrics` no público: red interna o `Authorization: Bearer METRICS_TOKEN`
- `/v1/admin/flags*` owner-only (rol actual studio owner / equivalente documentado hasta E02 RBAC fino)
- `/v1/platform/status` authenticated-ish: usuarios logueados Studio; no filtrar secretos
- `/health` público (liveness)
- `/ready` puede ser público o restringido; no debe filtrar connection strings

### 3.15 RED / USE mínimos

| Clase | Métrica | Tipo |
| --- | --- | --- |
| RED | `http_requests_total` | counter |
| RED | `http_request_duration_seconds` | histogram |
| RED | `http_requests_errors_total` (5xx) | counter |
| USE/platform | `platform_ready` | gauge 0/1 |
| Flags | `feature_flag_evaluations_total` | counter |
| Flags | `feature_flag_patches_total` | counter |
| Queue stub | `queue_depth` | gauge=0 until E04 |

- Decisión de diseño 3.design.01: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.02: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.03: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.04: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.05: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.06: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.07: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.08: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.09: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.10: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.11: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.12: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.13: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.14: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.15: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.16: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.17: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.18: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.19: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.20: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.21: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.22: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.23: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.24: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.25: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.26: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.27: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.28: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.29: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.30: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.31: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.32: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.33: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.34: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.
- Decisión de diseño 3.design.35: alineada a ARCHITECTURE Etapa 1 + roadmap riesgos OTel/cardinality/cap20%.

## 4. Archivos

### 4.1 Archivos nuevos (lista exacta conceptual)

| Path | Feature | Propósito |
| --- | --- | --- |
| `backend/platform/__init__.py` | F01–F03 | Package platform |
| `backend/platform/logging.py` | F01 | Structured logging |
| `backend/platform/tracing.py` | F01 | OTel tracing |
| `backend/platform/metrics.py` | F01 | RED metrics |
| `backend/platform/correlation.py` | F01 | Request/trace ids |
| `backend/platform/health.py` | F02 | Liveness/readiness |
| `backend/platform/flags.py` | F03 | Flags domain service |
| `backend/platform/config.py` | F01–F03 | Settings |
| `backend/platform/events_shapes.py` | F03 | SettingsActualizados shape |
| `backend/platform/redaction.py` | F01 | PII/secrets |
| `backend/platform/middleware.py` | F01 | ASGI/Starlette middlewares |
| `backend/platform/models_flags.py` | F03 | ORM FeatureFlag* |
| `backend/tests/test_platform_logging.py` | F01 | Unit logs |
| `backend/tests/test_platform_tracing.py` | F01 | Otel smoke |
| `backend/tests/test_platform_metrics.py` | F01 | Label allowlist |
| `backend/tests/test_platform_health.py` | F02 | Health/ready |
| `backend/tests/test_platform_flags.py` | F03 | Flags+audit+isolation |
| `backend/tests/test_correlation_ids.py` | F01 | Header propagation |
| `frontend/src/platform/requestId.js` | F01 | Axios interceptor |
| `frontend/src/platform/flagsClient.js` | F03 | FlagProvider |
| `frontend/src/platform/DegradationBanner.js` | F02 | Banner |
| `frontend/src/platform/platformStatus.js` | F02 | Poll status |
| `frontend/src/pages/AdminFlagsPage.js` | F03 | UI mínima owner |
| .github/workflows/ci.yml | F04 | CI gates |
| .github/pull_request_template.md | F04 | Checklist P01–P10 |
| CONTRIBUTING.md | F04 | DoR/DoD gates |
| docs/adr/0001-otel-abstraction.md | F01 | ADR |
| docs/adr/0002-health-vs-ready.md | F02 | ADR |
| docs/adr/0003-feature-flags-model.md | F03 | ADR |
| docs/adr/0004-ci-quality-gates.md | F04 | ADR |
| docs/adr/0005-minimal-flag-migrations.md | F03 | ADR |
| docs/runbooks/health-and-ready.md | F05 | Runbook |
| docs/runbooks/feature-flag-rollback.md | F05 | Runbook |
| docs/runbooks/dlq-empty-structure.md | F05 | Runbook stub E04 |
| docs/runbooks/incident-sev-definitions.md | F05 | Runbook |
| docs/runbooks/follow-request-upload-to-cost.md | F01/F05 | Runbook |
| docs/ops/oncall-roster-stub.md | F05 | Stub |
| docs/ops/postmortem-template.md | F05 | Template |
| docs/ops/domain-owners.md | F05 | Owners |
| docs/ops/sampling-policy.md | F01 | Policy |
| docs/ops/sli-slo-e01.md | F01/F02 | SLIs |
| docs/contracts/settings-actualizados.v1.json | F03 | Event shape |
| docs/contracts/platform-openapi-fragment.yaml | F01–F03 | OpenAPI fragment |

### 4.2 Archivos existentes a modificar (solo lista; no código)

| Path | Modificación conceptual |
| --- | --- |
| `backend/main.py` | Registrar middlewares/routers platform; reemplazar prints críticos |
| `backend/requirements.txt` | Deps opcionales OTel/prometheus; documentar extras |
| `frontend/src/App.js` | Montar banner; wire interceptor; ruta admin flags mínima |
| `frontend/package.json` | Solo si hace falta dep mínima; preferir sin deps nuevas |
| `render.yaml` | Env LOG_LEVEL, OTEL_*, METRICS_TOKEN, APP_VERSION; NO tocar generateValue SECRET_KEY sin plan ops |
| `frontend/src/index.js` | Opcional: no forzar web-vitals backend |

### 4.3 Carpetas nuevas

- `backend/platform/`
- `frontend/src/platform/`
- `docs/runbooks/`
- `docs/adr/`
- `docs/ops/`
- `docs/contracts/`
- `.github/workflows/`

### 4.4 Archivos que NO se tocan en E01

- `backend/motor_ia.py` (salvo import logging no semántico — preferir cero cambios)
- `backend/precios.json`
- `backend/billing_mp.py` (salvo logging)
- `backend/presupuesto_pdf.py`
- Cualquier schema MDO inexistente aún

- Regla de archivos 4.files.01: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.02: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.03: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.04: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.05: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.06: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.07: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.08: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.09: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.10: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.11: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.12: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.13: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.14: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.15: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.16: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.17: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.
- Regla de archivos 4.files.18: cambios fuera de la lista §4.1–4.2 requieren enmienda RFC.

## 5. Modelo de datos

### 5.1 Entidades

#### 5.1.1 FeatureFlag

| Campo | Tipo conceptual | Null | Notas |
| --- | --- | --- | --- |
| `id` | UUID | NO | PK |
| `key` | string unique | NO | ej. `obs.enhanced` |
| `description` | text | YES | — |
| `enabled` | bool | NO | default false |
| `rules_json` | json | NO | targeting plan/org/project |
| `rules_version` | int | NO | versionado de reglas |
| `expires_at` | datetime | YES | prohibir eternas; alert stale |
| `created_at` | datetime | NO | — |
| `updated_at` | datetime | NO | — |
| `deleted_at` | datetime | YES | soft delete |
| `created_by` | string/user id | YES | actor |
| `updated_by` | string/user id | YES | actor |

#### 5.1.2 FeatureFlagAudit

| Campo | Tipo | Null | Notas |
| --- | --- | --- | --- |
| `id` | UUID | NO | PK |
| `flag_key` | string | NO | denormalizado |
| `flag_id` | UUID FK | NO | — |
| `action` | enum create|patch|soft_delete|restore | NO | — |
| `before_json` | json | YES | snapshot |
| `after_json` | json | YES | snapshot |
| `actor_id` | string | NO | — |
| `actor_role` | string | YES | — |
| `request_id` | string | YES | correlación |
| `occurred_at` | datetime | NO | — |
| `reason` | string | YES | obligatorio en kill switch |

**Nunca hard-delete** de `FeatureFlagAudit`. Retención ≥ 1 año o política legal futura.

#### 5.1.3 ReleaseMarker (opcional)

| Campo | Tipo | Null | Notas |
| --- | --- | --- | --- |
| `id` | UUID | NO | PK |
| `version` | string | NO | APP_VERSION / git sha |
| `deployed_at` | datetime | NO | — |
| `env` | string | NO | — |
| `notes` | text | YES | — |

#### 5.1.4 HealthCheckRecord (opcional — prefer NOT persist)

Preferencia de diseño: **no persistir** cada check. Si se implementa, solo sampling ops/debug con TTL corto. Default E01: ephemeral in-process para métrica `platform.ready` únicamente.

#### 5.1.5 SliSnapshot

OUT de E01 o minimal later. Los SLIs viven en TSDB externo (Prometheus/Grafana/etc.).

### 5.2 Relaciones

```
FeatureFlag 1 ── * FeatureFlagAudit
ReleaseMarker (independiente)
```

### 5.3 Índices

| Tabla | Índice | Motivo |
| --- | --- | --- |
| feature_flags | UNIQUE(key) WHERE deleted_at IS NULL | Lookup evaluación |
| feature_flags | INDEX(expires_at) | Stale/expiry jobs |
| feature_flag_audits | INDEX(flag_key, occurred_at DESC) | Audit trail |
| feature_flag_audits | INDEX(actor_id, occurred_at DESC) | Forensics |
| release_markers | INDEX(env, deployed_at DESC) | Dashboard deploy |

### 5.4 Versionado de reglas de flag

- Cada PATCH incrementa `rules_version`
- Evaluación usa versión leída atómicamente con enabled/rules_json
- Conflictos opcionales vía header If-Match / body expected_version → 409
- Audit guarda before/after completos

### 5.5 Soft delete vs hard delete

| Entidad | Delete policy |
| --- | --- |
| FeatureFlag | Soft delete (`deleted_at`); key no reutilizable sin restore/ADR |
| FeatureFlagAudit | Hard delete PROHIBIDO |
| ReleaseMarker | Append-only preferido |

### 5.6 Seed flags iniciales

| key | enabled default | expires_at | Propósito |
| --- | --- | --- | --- |
| `obs.enhanced` | false | +180d | Exporters/sampling caros |
| `platform.degraded` | false | +365d | Kill switch degradación global |
| `wedge.calcular_v2` | false | +90d | Placeholder deshabilitado; no implementar v2 en E01 |
| `exports.enabled` | true | +365d | Degradación puede apagar exports |
| `ai.calcular_enabled` | true | +365d | Degradación puede apagar AI path |
| `platform.banner_force` | false | +180d | Forzar banner para drill |

### 5.7 Estrategia de migración

| Opción | Descripción | Decisión |
| --- | --- | --- |
| A — ensure_schema | CREATE TABLE IF NOT EXISTS en startup como hoy | Preferida si equipo 1–2 eng y sin Alembic |
| B — Alembic bootstrap only | Alembic solo para feature_flags/audit | Aceptable si se quiere versionado; NO full rewrite migraciones legacy |
| C — Alembic full | Migrar todo el schema legacy | OUT E01 |

**Decisión RFC:** Opción A por defecto; Opción B permitida con ADR-0005. Expand/contract: crear tablas nuevas sin alterar columnas wedge. Seed idempotente.

### 5.8 EvalContext (conceptual)

| Campo | Origen | Uso |
| --- | --- | --- |
| `plan` | studio/billing actual | targeting |
| `org_id` / studio id | auth | targeting |
| `project_id` | request | targeting opcional |
| `user_id` | auth | audit/override futuro |
| `env` | settings | safety |

### 5.9 rules_json schema conceptual

```
{
  "percentage": 0-100,
  "plans_allow": ["pro","enterprise"],
  "org_ids_allow": ["..."],
  "org_ids_deny": ["..."],
  "project_ids_allow": ["..."],
  "default": false
}
```

Evaluación determinista: deny lists → allow lists → percentage sticky by org hash → default.

- Invariante de datos 5.data.01: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.02: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.03: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.04: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.05: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.06: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.07: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.08: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.09: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.10: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.11: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.12: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.13: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.14: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.15: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.16: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.17: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.18: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.19: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.20: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.21: evaluación debe ser pura dado (flag snapshot, EvalContext).
- Invariante de datos 5.data.22: evaluación debe ser pura dado (flag snapshot, EvalContext).

## 6. API

### 6.1 Convenciones

- Rutas nuevas bajo `/v1` excepto health/ready/metrics (ops conventions)
- Errores con `request_id`
- JSON UTF-8
- AuthZ deny-by-default en admin
- Backward compat: `/api/health` permanece

### 6.2 GET /health (liveness)

| Campo | Valor |
| --- | --- |
| Método | GET |
| Path | `/health` |
| Auth | Ninguna |
| Deep checks | NO |
| Uso | Render healthCheckPath; process up |

**Response 200 example**

```
{
  "status": "ok",
  "version": "1.2.3",
  "kind": "liveness"
}
```

Campos adicionales opcionales no breaking. `status`/`version` permanecen para compat.

### 6.3 GET /api/health

Alias idéntico a liveness. No introducir deep checks aquí (rompería clientes y semántica).

### 6.4 GET /ready (readiness)

| Campo | Valor |
| --- | --- |
| Método | GET |
| Path | `/ready` |
| Auth | Ninguna o token ops opcional |
| Deep checks | DB obligatorio; storage/broker stubs |

**Response 200**

```
{
  "status": "ready",
  "version": "1.2.3",
  "checks": [
    {"name": "db", "status": "ok", "latency_ms": 12},
    {"name": "object_storage", "status": "skipped", "reason": "not_configured"},
    {"name": "broker", "status": "skipped", "reason": "not_configured"}
  ]
}
```

**Response 503**

```
{
  "status": "not_ready",
  "version": "1.2.3",
  "checks": [
    {"name": "db", "status": "fail", "error_class": "db_unreachable"}
  ]
}
```

### 6.5 GET /metrics

| Campo | Valor |
| --- | --- |
| Método | GET |
| Path | `/metrics` |
| Auth | Bearer METRICS_TOKEN o red privada |
| Formato | Prometheus text exposition |

| Error | Cuándo |
| --- | --- |
| 401 | Token ausente |
| 403 | Token inválido |

### 6.6 GET /v1/admin/flags

| Campo | Valor |
| --- | --- |
| Auth | Owner-only (hasta E02 RBAC fino) |
| Query | `include_deleted=false` default |

```
{
  "items": [
    {
      "key": "obs.enhanced",
      "enabled": false,
      "rules_version": 1,
      "expires_at": "2026-12-01T00:00:00Z",
      "updated_at": "2026-08-02T00:00:00Z"
    }
  ],
  "request_id": "…"
}
```

### 6.7 PATCH /v1/admin/flags/{key}

| Campo body | Tipo | Required |
| --- | --- | --- |
| `enabled` | bool | no |
| `rules_json` | object | no |
| `expires_at` | datetime|null | no |
| `reason` | string | sí si kill switch / degradación |
| `expected_version` | int | recomendado |

**Response 200**: flag actualizado + `audit_id`. Emite shape SettingsActualizados (ver §7).

### 6.8 GET /v1/platform/status

| Campo | Valor |
| --- | --- |
| Auth | Usuario autenticado Studio (si no hay auth, degradación conservadora) |
| Uso | Banner FE |

```
{
  "degraded": false,
  "reasons": [],
  "flags": {"platform.degraded": false, "exports.enabled": true},
  "version": "1.2.3",
  "request_id": "…"
}
```

### 6.9 GET /v1/platform/version

```
{
  "version": "1.2.3",
  "service": "arq-ia-api",
  "api_compat": "v1",
  "request_id": "…"
}
```

### 6.10 Matriz permisos

| Endpoint | Anon | User Free | User Pro | Owner | Metrics scraper |
| --- | --- | --- | --- | --- | --- |
| GET /health | ✓ | ✓ | ✓ | ✓ | ✓ |
| GET /api/health | ✓ | ✓ | ✓ | ✓ | ✓ |
| GET /ready | ✓* | ✓* | ✓* | ✓* | ✓* |
| GET /metrics | ✗ | ✗ | ✗ | ✗ | ✓ token |
| GET /v1/admin/flags | ✗ | ✗ | ✗ | ✓ | ✗ |
| PATCH /v1/admin/flags/{key} | ✗ | ✗ | ✗ | ✓ | ✗ |
| GET /v1/platform/status | limited | ✓ | ✓ | ✓ | ✗ |
| GET /v1/platform/version | ✓ | ✓ | ✓ | ✓ | ✓ |

\* `/ready` puede restringirse después por ops; default E01 público sin secretos.

### 6.11 Headers de correlación

| Header | In | Out | Notas |
| --- | --- | --- | --- |
| `X-Request-Id` | opcional | siempre | Generar UUID si ausente |
| `traceparent` | opcional | si OTel on | W3C |
| `Authorization` | admin/metrics | — | — |

- Caso de contrato API `health` 6.health.01: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `health` 6.health.02: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `health` 6.health.03: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `health` 6.health.04: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `health` 6.health.05: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `health` 6.health.06: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `health` 6.health.07: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `ready` 6.ready.01: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `ready` 6.ready.02: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `ready` 6.ready.03: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `ready` 6.ready.04: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `ready` 6.ready.05: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `ready` 6.ready.06: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `ready` 6.ready.07: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `metrics` 6.metrics.01: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `metrics` 6.metrics.02: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `metrics` 6.metrics.03: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `metrics` 6.metrics.04: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `metrics` 6.metrics.05: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `metrics` 6.metrics.06: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `metrics` 6.metrics.07: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_list` 6.flags_list.01: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_list` 6.flags_list.02: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_list` 6.flags_list.03: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_list` 6.flags_list.04: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_list` 6.flags_list.05: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_list` 6.flags_list.06: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_list` 6.flags_list.07: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_patch` 6.flags_patch.01: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_patch` 6.flags_patch.02: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_patch` 6.flags_patch.03: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_patch` 6.flags_patch.04: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_patch` 6.flags_patch.05: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_patch` 6.flags_patch.06: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `flags_patch` 6.flags_patch.07: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_status` 6.platform_status.01: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_status` 6.platform_status.02: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_status` 6.platform_status.03: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_status` 6.platform_status.04: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_status` 6.platform_status.05: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_status` 6.platform_status.06: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_status` 6.platform_status.07: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_version` 6.platform_version.01: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_version` 6.platform_version.02: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_version` 6.platform_version.03: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_version` 6.platform_version.04: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_version` 6.platform_version.05: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_version` 6.platform_version.06: request/response/error documentados; contract test placeholder en F04.
- Caso de contrato API `platform_version` 6.platform_version.07: request/response/error documentados; contract test placeholder en F04.

## 7. Eventos

### 7.1 Política E01 sobre el bus

E01 **no** implementa outbox/bus completo (eso es E04). Solo prepara: (1) correlation fields en logs/traces, (2) shape de emisión opcional `SettingsActualizados` cuando cambien flags/config, persistible luego en outbox.

### 7.2 Emit: SettingsActualizados

| Campo envelope (ARCHITECTURE §5.4 / roadmap E04-F05) | Tipo | Required E01 shape |
| --- | --- | --- |
| `id` | UUID | sí |
| `type` | `SettingsActualizados` | sí |
| `version` | `1` | sí |
| `tenant_id` | string|null | sí (null solo platform-global) |
| `occurred_at` | ISO8601 | sí |
| `correlation_id` | string | sí |
| `causation_id` | string|null | opcional |
| `producer` | `arq-ia-api` | sí |
| `payload` | object | sí |

#### 7.2.1 Payload

| Campo | Tipo | Notas |
| --- | --- | --- |
| `setting_domain` | `feature_flags` | — |
| `flag_key` | string | — |
| `enabled` | bool | post-change |
| `rules_version` | int | — |
| `actor_id` | string | — |
| `reason` | string | — |
| `changed_fields` | string[] | — |

### 7.3 UsoRegistrado (opcional deferred)

Meter platform opcional. No bloquea DoD E01. Si se emite, mismo envelope; payload mínimo `{meter, value, plan}`. Prefer defer.

### 7.4 Consume

**Ningún consumer requerido en E01.** Futuros: Billing (E02), Jobs (E04), Analytics (E24). Documentar en contrato.

### 7.5 Almacenamiento temporal del evento en E01

| Opción | Decisión |
| --- | --- |
| Outbox table real | OUT (E04) |
| Append audit + log structured type=event | IN (mínimo) |
| Archivo schema en docs/contracts | IN |

- Regla de eventos 7.events.01: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.02: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.03: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.04: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.05: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.06: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.07: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.08: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.09: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.10: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.11: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.12: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.13: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.14: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.15: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.16: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.17: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.18: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.19: no usar eventos como RPC; consumers futuros deben ser idempotentes.
- Regla de eventos 7.events.20: no usar eventos como RPC; consumers futuros deben ser idempotentes.

## 8. Frontend

### 8.1 Pantallas

| Pantalla | Audiencia | Job to be done |
| --- | --- | --- |
| Studio (existente) + DegradationBanner | Todos usuarios | Avisar degradación sin romper wedge |
| Admin Flags (mínima, owner-only) | Owner | Toggle/patch flags con reason |

### 8.2 Componentes

| Componente | Responsabilidad | No-responsabilidad |
| --- | --- | --- |
| `DegradationBanner` | Mostrar reasons + link soporte con request/trace id | No inventar estado de obra |
| `FlagProvider` | Cache TTL evaluación/flags públicas seguras | No AuthZ server |
| `requestId` interceptor | Añadir/propagar X-Request-Id; guardar last ids | No retry infinito |
| `AdminFlagsPage` | Lista + patch mínimo | No diseño marketplace |

### 8.3 Estado FE

| State key | Source | TTL | Notas |
| --- | --- | --- | --- |
| `platformStatus` | `/v1/platform/status` | 30–60s | Poll suave |
| `flagsCache` | subset seguro / admin | 30–60s | Invalidate on patch |
| `lastRequestId` | interceptor | session | Support |
| `lastTraceId` | response/diag header si existe | session | Support |

### 8.4 UX rules

- Banner no es card de marketing: una línea + reason + dismiss temporal opcional
- No overlays sobre hero ajenos; banner top-of-app en Studio shell actual
- i18n ES mensajes
- No rediseñar App.js completo
- Preservar motion/flujo wedge existente

### 8.5 Integración con failover /health existente

El probe actual `axios.get(`${base}/health`)` permanece como liveness/failover. El banner usa `/v1/platform/status` (o fallback conservador si 404 durante rollout).

- Caso FE 8.fe.01: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.02: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.03: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.04: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.05: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.06: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.07: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.08: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.09: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.10: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.11: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.12: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.13: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.14: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.15: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.16: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.17: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.
- Caso FE 8.fe.18: degradación visible en ≤ 60s tras flag platform.degraded=true; no romper /health failover.

## 9. Tests

### 9.1 Matriz Unit

| ID | Feature | Caso | Floor |
| --- | --- | --- | --- |
| U-F01-01 | F01 | redaction oculta email/token | pass |
| U-F01-02 | F01 | label allowlist rechaza email label | pass |
| U-F01-03 | F01 | request_id generado si header ausente | pass |
| U-F02-01 | F02 | liveness no llama DB | pass |
| U-F02-02 | F02 | readiness fail si DB down | pass |
| U-F03-01 | F03 | evaluate determinista mismo ctx | pass |
| U-F03-02 | F03 | expiry impide evaluate true | pass |
| U-F03-03 | F03 | audit append on patch | pass |
| U-F04-01 | F04 | CI config presente (smoke repo) | pass |

### 9.2 Matriz Integration

| ID | Feature | Caso |
| --- | --- | --- |
| I-F01-01 | F01 | request deja X-Request-Id en response + log fields |
| I-F01-02 | F01 | otel smoke span created when enabled |
| I-F02-01 | F02 | /ready 503 when DB unreachable |
| I-F02-02 | F02 | stubs storage/broker skipped |
| I-F03-01 | F03 | PATCH flag → audit row |
| I-F03-02 | F03 | tenant isolation: owner A no lista/patches de B |
| I-F03-03 | F03 | SettingsActualizados shape valid vs schema |

### 9.3 Matriz E2E / smoke

| ID | Caso | Gate |
| --- | --- | --- |
| E2E-WEDGE-01 | color→qty→ARS golden | Bloqueante RC; skippable en PR con waiver F04 |
| E2E-DEG-01 | banner aparece con platform.degraded | F02 |
| E2E-FLAGS-01 | owner toggles exports.enabled | F03 |

### 9.4 Perf

| ID | Budget |
| --- | --- |
| P-F01-01 | Middleware overhead p50 < 5ms en noop handler (local) |
| P-F03-01 | evaluate flag p95 < 2ms in-memory/cache |

### 9.5 Security

| ID | Caso |
| --- | --- |
| S-F01-01 | logs sin SECRET_KEY/MP tokens |
| S-F02-01 | /ready no filtra DSN |
| S-F03-01 | non-owner 403 admin flags |
| S-F03-02 | metrics 401 without token |

### 9.6 CI floors (iniciales)

| Gate | Floor |
| --- | --- |
| Unit platform modules | ≥ 80% líneas platform/* |
| Existing tests | 100% pass |
| Secret scan | 0 high |
| Dependency audit | 0 critical o waiver |
| Wedge smoke | pass o waiver ticketed |

- Test case expandido 9.test.01: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.02: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.03: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.04: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.05: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.06: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.07: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.08: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.09: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.10: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.11: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.12: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.13: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.14: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.15: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.16: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.17: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.18: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.19: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.20: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.21: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.22: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.23: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.24: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.25: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.26: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.27: mapear a F01–F05 en plan de QA; evidenciar en PR.
- Test case expandido 9.test.28: mapear a F01–F05 en plan de QA; evidenciar en PR.

## 10. Migración desde estado actual

### 10.1 Fases de rollout

| Fase | Contenido | Flag/gate | Rollback |
| --- | --- | --- | --- |
| A | Logs JSON + request id middleware | siempre on light | LOG_FORMAT=text; disable middleware env |
| B | /ready + /metrics | METRICS_TOKEN set | ocultar scrape; ready no usado por Render aún |
| C | Flags + admin + audit + status/banner | seeds default safe | flags off; soft-disable admin route |
| D | CI + CONTRIBUTING + ADR + runbooks | branch protection gradual | waiver process |
| E | Dashboards/alerts mínimos | obs.enhanced opcional | mute alerts |

### 10.2 Zero downtime

- No cambiar healthCheckPath lejos de /health
- Tablas nuevas expand-only
- FE tolera 404 de /v1/platform/status durante rollout
- No rotar SECRET_KEY automáticamente

### 10.3 SECRET_KEY note

`render.yaml` usa `generateValue: true` para SECRET_KEY — riesgo ops si redeploy regenera y invalida sesiones/firmas. E01 documenta higiene y checklist; **no** rota keys inesperadamente. Fix completo de gestión de secretos puede vivir en E02/ops.

### 10.4 Kill switches

| Switch | Efecto |
| --- | --- |
| `platform.degraded=true` | Banner + disable AI/exports según flags hijas |
| `obs.enhanced=false` | Sin exporters caros |
| `OTEL_ENABLED=false` | Tracing no-op |
| `ai.calcular_enabled=false` | Bloquea path AI sin tumbar API |
| `exports.enabled=false` | Bloquea exports |

- Paso de migración 10.mig.01: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.02: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.03: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.04: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.05: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.06: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.07: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.08: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.09: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.10: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.11: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.12: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.13: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.14: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.15: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.16: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.17: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.18: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.19: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.20: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.21: verificar wedge golden tras cada fase A–E; rollback documentado.
- Paso de migración 10.mig.22: verificar wedge golden tras cada fase A–E; rollback documentado.

## 11. Riesgos + mitigaciones

### 11.1 Riesgos del roadmap E01 (reafirmados)

| Tipo | Riesgo | Mitigación |
| --- | --- | --- |
| Tech | Over-instrumentation prematura | SLIs mínimos; expandir con dolor medido |
| Arch | Acoplar app a vendor APM | OpenTelemetry abstracción |
| Perf | Sampling inadecuado | Tail-based doc + muestreo tenant-aware futuro |
| Scale | Cardinality explosion | Allowlist estricta labels |
| Commercial | Retrasar wedge por plataforma perfecta | Cap ≤20% capacidad |

### 11.2 Riesgos adicionales de implementación

| ID | Riesgo | Prob | Impacto | Mitigación |
| --- | --- | --- | --- | --- |
| R01 | Middleware rompe CORS/preflight | M | A | Tests OPTIONS; echo headers allowlist |
| R02 | Ready check flaky tumba deploys si se usa prematuro | M | A | Render sigue en /health |
| R03 | /metrics expuesto público | B | A | Token + deny default |
| R04 | Flags mal seed → AI off en prod | M | A | Defaults safe; checklist release |
| R05 | PII en logs | M | A | Redaction + tests |
| R06 | Alembic vs ensure_schema confusion | M | M | ADR-0005 |
| R07 | FE banner molesto falso positivo | M | M | reasons claros; poll TTL; force flag drill |
| R08 | CI flakes bloquean wedge delivery | M | M | quarantine + waiver |
| R09 | Scope creep bus/MDO | A | A | Hard freeze §2 |
| R10 | SECRET_KEY regen | M | A | Doc ops; no tocar E01 |
| R11 | Performance middleware en /calcular | B | M | Budget §9; no heavy export sync |
| R12 | Tenant isolation admin flags débil pre-E02 | M | A | Owner check server-side + tests |
| R13 | Dual /health /api/health diverge | B | M | Misma función liveness |
| R14 | Dashboard vanity metrics | A | B | Minimal panels Apéndice C |
| R15 | Flags eternas | A | M | expires_at + stale panel |

| R16 | Riesgo operativo extendido #16 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R17 | Riesgo operativo extendido #17 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R18 | Riesgo operativo extendido #18 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R19 | Riesgo operativo extendido #19 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R20 | Riesgo operativo extendido #20 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R21 | Riesgo operativo extendido #21 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R22 | Riesgo operativo extendido #22 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R23 | Riesgo operativo extendido #23 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R24 | Riesgo operativo extendido #24 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R25 | Riesgo operativo extendido #25 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R26 | Riesgo operativo extendido #26 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R27 | Riesgo operativo extendido #27 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R28 | Riesgo operativo extendido #28 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R29 | Riesgo operativo extendido #29 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R30 | Riesgo operativo extendido #30 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R31 | Riesgo operativo extendido #31 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R32 | Riesgo operativo extendido #32 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R33 | Riesgo operativo extendido #33 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R34 | Riesgo operativo extendido #34 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R35 | Riesgo operativo extendido #35 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R36 | Riesgo operativo extendido #36 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R37 | Riesgo operativo extendido #37 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R38 | Riesgo operativo extendido #38 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R39 | Riesgo operativo extendido #39 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R40 | Riesgo operativo extendido #40 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R41 | Riesgo operativo extendido #41 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R42 | Riesgo operativo extendido #42 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R43 | Riesgo operativo extendido #43 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R44 | Riesgo operativo extendido #44 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |
| R45 | Riesgo operativo extendido #45 (capacidad, docs drift, alert noise, sampling skew, oncall gaps, etc.) | M | M | Checklist F05 + review semanal SLIs |

Tabla extendida R16–R45: todos mitigan con runbooks F05, allowlist, cap 20%, y freeze de alcance.

## 12. Criterios de aceptación objetivos

### 12.1 Binarios (pass/fail)

- [ ] GET /health retorna 200 con status/version sin tocar DB
- [ ] GET /api/health permanece compatible
- [ ] GET /ready retorna 503 si DB down y 200 si DB ok (storage/broker skipped)
- [ ] GET /metrics exige token en prod
- [ ] X-Request-Id presente en responses API instrumentadas
- [ ] Logs JSON contienen request_id y trace_id (nullable-safe)
- [ ] Redaction test verde
- [ ] FeatureFlag seed cargado; obs.enhanced default false
- [ ] PATCH flag genera FeatureFlagAudit (no hard-delete posible)
- [ ] Owner-only enforced en admin flags (403 otherwise)
- [ ] DegradationBanner visible cuando platform.degraded=true
- [ ] CI workflow existe y corre lint/unit en PR
- [ ] PR template incluye checklist P01–P10
- [ ] docs/runbooks/health-and-ready.md publicado
- [ ] docs/runbooks/feature-flag-rollback.md publicado
- [ ] docs/runbooks/dlq-empty-structure.md publicado (stub E04)
- [ ] Golden wedge smoke verde o waiver ticketed
- [ ] No cambios semánticos motor_ia color→qty→ARS
- [ ] No tablas MDO introducidas
- [ ] No bus/outbox tables E04 introducidas
- [ ] Capacidad plataforma justificada ≤20% en review de sprint
- [ ] ADR OTel + health/ready + flags mergeados
- [ ] SECRET_KEY no rotada por cambios E01
- [ ] precios.json intacto

### 12.2 Numéricos

| Métrica | Target |
| --- | --- |
| Coverage platform/* | ≥ 80% |
| Middleware overhead p50 | < 5ms |
| Flag evaluate p95 | < 2ms |
| SLI availability semana-1 | ≥ 99% o waiver |
| P0 debt nueva | 0 |
| Critical vulns CI | 0 o waiver |
| Stale flags >90d sin owner | 0 al cierre (o ticket) |

- [ ] Criterio extendido 12.3.01: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.02: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.03: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.04: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.05: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.06: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.07: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.08: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.09: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.10: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.11: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.12: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.13: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.14: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.15: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.16: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.17: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.18: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.19: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.20: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.21: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.22: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.23: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.24: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.25: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.26: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.27: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.28: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.29: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.30: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.31: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.32: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.33: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.34: evidencia adjunta en demo interna feature correspondiente.
- [ ] Criterio extendido 12.3.35: evidencia adjunta en demo interna feature correspondiente.

## 13. Checklist final task-by-task

### 13.1 Tasks roadmap E01-F01

- [ ] E01-F01-T01 — Definir taxonomía de campos obligatorios (tenant_id, project_id, job_id, trace_id)
- [ ] E01-F01-T02 — Instrumentar API gateway con OpenTelemetry
- [ ] E01-F01-T03 — Instrumentar workers (perception/jobs) con contexto propagado (helpers/stubs E01)
- [ ] E01-F01-T04 — Dashboard golden: latencia API, error rate, cola depth
- [ ] E01-F01-T05 — Alertas P0: 5xx spike, DLQ > 0 sostenido (stub), disk/memory workers (doc)
- [ ] E01-F01-T06 — Log redaction de PII/secretos
- [ ] E01-F01-T07 — Sampling policy documentada
- [ ] E01-F01-T08 — Tests de presencia de correlation ids
- [ ] E01-F01-T09 — Runbook: 'cómo seguir un request de upload a costo'
- [ ] E01-F01-T10 — Feature flag `obs.enhanced` para exporters caros
- [ ] E01-F01-T11 — Definir Acceptance Criteria medibles para E01-F01
- [ ] E01-F01-T12 — Agregar métricas RED/USE relevantes para E01-F01
- [ ] E01-F01-T13 — Escribir ADR si hay desvío de arquitectura para E01-F01
- [ ] E01-F01-T14 — Preparar feature flag + plan de rollback para E01-F01
- [ ] E01-F01-T15 — Actualizar OpenAPI/event schema si aplica para E01-F01
- [ ] E01-F01-T16 — Ejecutar checklist tenant isolation para E01-F01
- [ ] E01-F01-T17 — Actualizar runbook operativo para E01-F01
- [ ] E01-F01-T18 — Demo interna de 10 minutos documentada para E01-F01
- [ ] E01-F01-T19 — Revisar compatibilidad Free/Pro/Enterprise en E01-F01
- [ ] E01-F01-T20 — Verificar que no se rompe wedge color→qty→moneda local tras E01-F01
- [ ] E01-F01-T21 — Añadir tests de regresión golden si E01-F01 toca motores
- [ ] E01-F01-T22 — Instrumentar traces spans para E01-F01
- [ ] E01-F01-T23 — Documentar dependencias de eventos en E01-F01
- [ ] E01-F01-T24 — Checklist seguridad secretos/PII en E01-F01
- [ ] E01-F01-T25 — Validar performance budget preliminar de E01-F01
- [ ] E01-F01-T26 — Actualizar mapping Architecture domain ↔ E01-F01

### 13.2 Tasks roadmap E01-F02

- [ ] E01-F02-T01 — Endpoints /health y /ready separados
- [ ] E01-F02-T02 — Checks de DB, object storage, broker (stubs skipped)
- [ ] E01-F02-T03 — Modo degradado: deshabilitar AI/exports vía flags
- [ ] E01-F02-T04 — Banner UI de degradación
- [ ] E01-F02-T05 — Tests de readiness fail cuando outbox stuck (contrato/skip hasta E04)
- [ ] E01-F02-T06 — Métrica `platform.ready` boolean timeseries
- [ ] E01-F02-T07 — Documentar SLO de bootstrap cold start
- [ ] E01-F02-T08 — Chaos light: matar dependencia y verificar señales
- [ ] E01-F02-T09 — Definir Acceptance Criteria medibles para E01-F02
- [ ] E01-F02-T10 — Agregar métricas RED/USE relevantes para E01-F02
- [ ] E01-F02-T11 — Escribir ADR si hay desvío de arquitectura para E01-F02
- [ ] E01-F02-T12 — Preparar feature flag + plan de rollback para E01-F02
- [ ] E01-F02-T13 — Actualizar OpenAPI/event schema si aplica para E01-F02
- [ ] E01-F02-T14 — Ejecutar checklist tenant isolation para E01-F02
- [ ] E01-F02-T15 — Actualizar runbook operativo para E01-F02
- [ ] E01-F02-T16 — Demo interna de 10 minutos documentada para E01-F02
- [ ] E01-F02-T17 — Revisar compatibilidad Free/Pro/Enterprise en E01-F02
- [ ] E01-F02-T18 — Verificar que no se rompe wedge color→qty→moneda local tras E01-F02
- [ ] E01-F02-T19 — Añadir tests de regresión golden si E01-F02 toca motores
- [ ] E01-F02-T20 — Instrumentar traces spans para E01-F02
- [ ] E01-F02-T21 — Documentar dependencias de eventos en E01-F02
- [ ] E01-F02-T22 — Checklist seguridad secretos/PII en E01-F02
- [ ] E01-F02-T23 — Validar performance budget preliminar de E01-F02
- [ ] E01-F02-T24 — Actualizar mapping Architecture domain ↔ E01-F02

### 13.3 Tasks roadmap E01-F03

- [ ] E01-F03-T01 — Entidad FeatureFlag con targeting plan/org/project
- [ ] E01-F03-T02 — API admin interna + audit trail
- [ ] E01-F03-T03 — SDK server evaluation determinista
- [ ] E01-F03-T04 — SDK frontend evaluation cacheada
- [ ] E01-F03-T05 — Tests matriz flag × plan
- [ ] E01-F03-T06 — Migración seed flags wedge
- [ ] E01-F03-T07 — Prohibir flags eternas: expiry date field
- [ ] E01-F03-T08 — Dashboard flags stale (>90 días)
- [ ] E01-F03-T09 — Definir Acceptance Criteria medibles para E01-F03
- [ ] E01-F03-T10 — Agregar métricas RED/USE relevantes para E01-F03
- [ ] E01-F03-T11 — Escribir ADR si hay desvío de arquitectura para E01-F03
- [ ] E01-F03-T12 — Preparar feature flag + plan de rollback para E01-F03
- [ ] E01-F03-T13 — Actualizar OpenAPI/event schema si aplica para E01-F03
- [ ] E01-F03-T14 — Ejecutar checklist tenant isolation para E01-F03
- [ ] E01-F03-T15 — Actualizar runbook operativo para E01-F03
- [ ] E01-F03-T16 — Demo interna de 10 minutos documentada para E01-F03
- [ ] E01-F03-T17 — Revisar compatibilidad Free/Pro/Enterprise en E01-F03
- [ ] E01-F03-T18 — Verificar que no se rompe wedge color→qty→moneda local tras E01-F03
- [ ] E01-F03-T19 — Añadir tests de regresión golden si E01-F03 toca motores
- [ ] E01-F03-T20 — Instrumentar traces spans para E01-F03
- [ ] E01-F03-T21 — Documentar dependencias de eventos en E01-F03
- [ ] E01-F03-T22 — Checklist seguridad secretos/PII en E01-F03
- [ ] E01-F03-T23 — Validar performance budget preliminar de E01-F03
- [ ] E01-F03-T24 — Actualizar mapping Architecture domain ↔ E01-F03

### 13.4 Tasks roadmap E01-F04

- [ ] E01-F04-T01 — Pipeline lint + types + unit
- [ ] E01-F04-T02 — Coverage floors por módulo crítico
- [ ] E01-F04-T03 — Secret scan + dependency audit
- [ ] E01-F04-T04 — Contract test placeholder para eventos
- [ ] E01-F04-T05 — Policy: no merge con TODO sin issue
- [ ] E01-F04-T06 — Template PR con checklist principios P01–P10
- [ ] E01-F04-T07 — Badge de wedge e2e smoke (inicialmente skippeable con waiver)
- [ ] E01-F04-T08 — Documentar Definition of Ready/Done en CONTRIBUTING conceptual
- [ ] E01-F04-T09 — Definir Acceptance Criteria medibles para E01-F04
- [ ] E01-F04-T10 — Agregar métricas RED/USE relevantes para E01-F04
- [ ] E01-F04-T11 — Escribir ADR si hay desvío de arquitectura para E01-F04
- [ ] E01-F04-T12 — Preparar feature flag + plan de rollback para E01-F04
- [ ] E01-F04-T13 — Actualizar OpenAPI/event schema si aplica para E01-F04
- [ ] E01-F04-T14 — Ejecutar checklist tenant isolation para E01-F04
- [ ] E01-F04-T15 — Actualizar runbook operativo para E01-F04
- [ ] E01-F04-T16 — Demo interna de 10 minutos documentada para E01-F04
- [ ] E01-F04-T17 — Revisar compatibilidad Free/Pro/Enterprise en E01-F04
- [ ] E01-F04-T18 — Verificar que no se rompe wedge color→qty→moneda local tras E01-F04
- [ ] E01-F04-T19 — Añadir tests de regresión golden si E01-F04 toca motores
- [ ] E01-F04-T20 — Instrumentar traces spans para E01-F04
- [ ] E01-F04-T21 — Documentar dependencias de eventos en E01-F04
- [ ] E01-F04-T22 — Checklist seguridad secretos/PII en E01-F04
- [ ] E01-F04-T23 — Validar performance budget preliminar de E01-F04
- [ ] E01-F04-T24 — Actualizar mapping Architecture domain ↔ E01-F04

### 13.5 Tasks roadmap E01-F05

- [ ] E01-F05-T01 — Runbook DLQ vacío (estructura)
- [ ] E01-F05-T02 — Runbook rollback feature flag
- [ ] E01-F05-T03 — Runbook incident sev definitions
- [ ] E01-F05-T04 — Oncall roster stub
- [ ] E01-F05-T05 — Postmortem template
- [ ] E01-F05-T06 — Métrica MTTR tracking manual→auto
- [ ] E01-F05-T07 — Lista de owners por dominio
- [ ] E01-F05-T08 — Drill trimestral calendarizado
- [ ] E01-F05-T09 — Definir Acceptance Criteria medibles para E01-F05
- [ ] E01-F05-T10 — Agregar métricas RED/USE relevantes para E01-F05
- [ ] E01-F05-T11 — Escribir ADR si hay desvío de arquitectura para E01-F05
- [ ] E01-F05-T12 — Preparar feature flag + plan de rollback para E01-F05
- [ ] E01-F05-T13 — Actualizar OpenAPI/event schema si aplica para E01-F05
- [ ] E01-F05-T14 — Ejecutar checklist tenant isolation para E01-F05
- [ ] E01-F05-T15 — Actualizar runbook operativo para E01-F05
- [ ] E01-F05-T16 — Demo interna de 10 minutos documentada para E01-F05
- [ ] E01-F05-T17 — Revisar compatibilidad Free/Pro/Enterprise en E01-F05
- [ ] E01-F05-T18 — Verificar que no se rompe wedge color→qty→moneda local tras E01-F05
- [ ] E01-F05-T19 — Añadir tests de regresión golden si E01-F05 toca motores
- [ ] E01-F05-T20 — Instrumentar traces spans para E01-F05
- [ ] E01-F05-T21 — Documentar dependencias de eventos en E01-F05
- [ ] E01-F05-T22 — Checklist seguridad secretos/PII en E01-F05
- [ ] E01-F05-T23 — Validar performance budget preliminar de E01-F05
- [ ] E01-F05-T24 — Actualizar mapping Architecture domain ↔ E01-F05

### 13.6 Tasks específicas RFC (adicionales)

- [ ] RFC-E01-T01 — Congelar este RFC (status Ready) tras sign-off Apéndice J
- [ ] RFC-E01-T02 — Crear carpeta docs/adr y publicar ADR-0001..0005 titles
- [ ] RFC-E01-T03 — Añadir env vars Apéndice A a render.yaml (sin rotar SECRET_KEY)
- [ ] RFC-E01-T04 — Implementar fases A→E con gates de rollback
- [ ] RFC-E01-T05 — Verificar wc evidencia de dashboards mínimos (screenshots)
- [ ] RFC-E01-T06 — Registrar capacidad ≤20% en sprint notes
- [ ] RFC-E01-T07 — Contract file SettingsActualizados v1 en docs/contracts
- [ ] RFC-E01-T08 — OpenAPI fragment platform mergeado a docs
- [ ] RFC-E01-T09 — Chaos light DB down documentado con resultados
- [ ] RFC-E01-T10 — Support playbook: pedir request_id/trace_id al usuario
- [ ] RFC-E01-T11 — Confirmar no introducción de dependencias vendor APM duras
- [ ] RFC-E01-T12 — Confirmar label allowlist en code review checklist
- [ ] RFC-E01-T13 — Seed flags review con PM (calcular_v2 disabled)
- [ ] RFC-E01-T14 — Branch protection: CI required checks
- [ ] RFC-E01-T15 — Post-release docs: actualizar ENGINEERING_ROADMAP status E01 cuando Done

### 13.7 Checklist transversal por feature (copiar del roadmap)

#### 13.7.F01

- [ ] F01: Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] F01: Servicio de dominio con AuthZ
- [ ] F01: Eventos outbox / consumers idempotentes si hay side-effects (shape only E01)
- [ ] F01: API conceptual documentada
- [ ] F01: UI mínima o explícitamente N/A
- [ ] F01: Migraciones expand/contract
- [ ] F01: Tests unit + integration + aislamiento
- [ ] F01: Métricas + logs + traces
- [ ] F01: Docs/runbook
- [ ] F01: Flag + rollback

#### 13.7.F02

- [ ] F02: Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] F02: Servicio de dominio con AuthZ
- [ ] F02: Eventos outbox / consumers idempotentes si hay side-effects (shape only E01)
- [ ] F02: API conceptual documentada
- [ ] F02: UI mínima o explícitamente N/A
- [ ] F02: Migraciones expand/contract
- [ ] F02: Tests unit + integration + aislamiento
- [ ] F02: Métricas + logs + traces
- [ ] F02: Docs/runbook
- [ ] F02: Flag + rollback

#### 13.7.F03

- [ ] F03: Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] F03: Servicio de dominio con AuthZ
- [ ] F03: Eventos outbox / consumers idempotentes si hay side-effects (shape only E01)
- [ ] F03: API conceptual documentada
- [ ] F03: UI mínima o explícitamente N/A
- [ ] F03: Migraciones expand/contract
- [ ] F03: Tests unit + integration + aislamiento
- [ ] F03: Métricas + logs + traces
- [ ] F03: Docs/runbook
- [ ] F03: Flag + rollback

#### 13.7.F04

- [ ] F04: Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] F04: Servicio de dominio con AuthZ
- [ ] F04: Eventos outbox / consumers idempotentes si hay side-effects (shape only E01)
- [ ] F04: API conceptual documentada
- [ ] F04: UI mínima o explícitamente N/A
- [ ] F04: Migraciones expand/contract
- [ ] F04: Tests unit + integration + aislamiento
- [ ] F04: Métricas + logs + traces
- [ ] F04: Docs/runbook
- [ ] F04: Flag + rollback

#### 13.7.F05

- [ ] F05: Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] F05: Servicio de dominio con AuthZ
- [ ] F05: Eventos outbox / consumers idempotentes si hay side-effects (shape only E01)
- [ ] F05: API conceptual documentada
- [ ] F05: UI mínima o explícitamente N/A
- [ ] F05: Migraciones expand/contract
- [ ] F05: Tests unit + integration + aislamiento
- [ ] F05: Métricas + logs + traces
- [ ] F05: Docs/runbook
- [ ] F05: Flag + rollback

## Apéndice A — Variables de entorno nuevas

| Var | Default | Required prod | Descripción |
| --- | --- | --- | --- |
| `LOG_LEVEL` | INFO | no | Nivel logging |
| `LOG_FORMAT` | json | sí prod | json|text |
| `OTEL_ENABLED` | false | no | Activa SDK |
| `OTEL_SERVICE_NAME` | arq-ia-api | no | Resource attr |
| `OTEL_EXPORTER_OTLP_ENDPOINT` |  | no | OTLP |
| `OTEL_TRACES_SAMPLER` | parentbased_traceidratio | no | Sampler |
| `OTEL_TRACES_SAMPLER_ARG` | 0.1 | no | Ratio base |
| `METRICS_TOKEN` | (unset) | sí prod | Protege /metrics |
| `PLATFORM_READY_DB_TIMEOUT_MS` | 1000 | no | Ping DB |
| `PLATFORM_STATUS_CACHE_TTL_SEC` | 15 | no | Cache status |
| `APP_VERSION` | dev | sí | Ya existe; asegurar en Render |
| `FLAGS_ADMIN_ENABLED` | true | no | Kill switch admin route |

Nota: `SECRET_KEY` ya existe; E01 no la rota. Documentar ops hygiene solamente.

- Validación env A.env.01: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.02: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.03: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.04: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.05: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.06: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.07: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.08: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.09: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.10: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.11: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.
- Validación env A.env.12: documentar en render.yaml comments conceptuales; valores sync:false cuando secretos.

## Apéndice B — ADR titles a escribir durante E01

| ADR | Título |
| --- | --- |
| 0001 | OpenTelemetry como abstracción de observabilidad (anti vendor-lock) |
| 0002 | Separación liveness `/health` vs readiness `/ready` |
| 0003 | Modelo FeatureFlag + audit append-only |
| 0004 | CI quality gates mínimos y waivers |
| 0005 | Migraciones mínimas para flags (ensure_schema vs Alembic bootstrap) |
| 0006 | Propagación X-Request-Id + W3C Trace Context |
| 0007 | Label allowlist y prohibición high-cardinality |
| 0008 | Degradación platform vía flags sin tumbar liveness |

## Apéndice C — Dashboard panels

| Panel | Query conceptual | Notas |
| --- | --- | --- |
| API request rate | sum rate http_requests_total | por status_class |
| API latency p95 | histogram_quantile 0.95 | por route_template |
| 5xx error rate | 5xx / total | alerta |
| platform.ready | gauge | truthfulness |
| Flag patches | feature_flag_patches_total | ops |
| Stale flags | expires_at / age > 90d | tabla |
| Deploy markers | ReleaseMarker overlay | opcional |
| Queue depth stub | queue_depth | 0 until E04 |

- Panel detalle C.panel.01: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.02: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.03: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.04: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.05: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.06: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.07: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.08: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.09: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.10: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.11: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.12: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.13: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.14: incluir variables env/service; no añadir dimensions fuera allowlist.
- Panel detalle C.panel.15: incluir variables env/service; no añadir dimensions fuera allowlist.

## Apéndice D — Alert rules

| Alert | Condición | Sev | E01 status |
| --- | --- | --- | --- |
| API5xxSpike | error rate > 1% 10m | P0 | IN |
| ReadyDown | platform.ready==0 5m | P0 | IN |
| MetricsScrapeFail | scrape fail 15m | P1 | IN |
| DLQNonZero | dlq>0 15m | P0 | STUB until E04 |
| FlagKillSwitch | platform.degraded==true | P1 info | IN |
| StaleFlags | count>0 age>90d | P2 | IN |
| WorkerDisk | disk>90% | P0 | DOC only |

- Runbook link obligatorio para alert D.alert.01; silence policy documentada.
- Runbook link obligatorio para alert D.alert.02; silence policy documentada.
- Runbook link obligatorio para alert D.alert.03; silence policy documentada.
- Runbook link obligatorio para alert D.alert.04; silence policy documentada.
- Runbook link obligatorio para alert D.alert.05; silence policy documentada.
- Runbook link obligatorio para alert D.alert.06; silence policy documentada.
- Runbook link obligatorio para alert D.alert.07; silence policy documentada.
- Runbook link obligatorio para alert D.alert.08; silence policy documentada.
- Runbook link obligatorio para alert D.alert.09; silence policy documentada.
- Runbook link obligatorio para alert D.alert.10; silence policy documentada.
- Runbook link obligatorio para alert D.alert.11; silence policy documentada.
- Runbook link obligatorio para alert D.alert.12; silence policy documentada.

## Apéndice E — Sampling policy

- Default ratio 10% traces cuando OTEL_ENABLED=true y obs.enhanced=false
- Errores 5xx: always sample (si SDK lo permite) o elevación documental
- Rutas /health /ready /metrics: sample 1% o exclude
- obs.enhanced=true: ratio configurable hasta 50% staging; prod ≤20% sin ADR
- Prohibido sample 100% prod sin waiver CTO
- Tenant-aware sampling: defer post-E02 (documentado)

- Caso sampling E.sample.01: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.02: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.03: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.04: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.05: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.06: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.07: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.08: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.09: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.10: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.11: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.12: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.13: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.14: verificar costo export vs valor debug en review semanal.
- Caso sampling E.sample.15: verificar costo export vs valor debug en review semanal.

## Apéndice F — Log field schema

| Campo | Tipo | Required | Notas |
| --- | --- | --- | --- |
| `ts` | ISO8601 | sí | — |
| `level` | str | sí | DEBUG/INFO/WARN/ERROR |
| `msg` | str | sí | redactado |
| `service` | str | sí | arq-ia-api |
| `env` | str | sí | — |
| `request_id` | str | sí en request path | — |
| `trace_id` | str|null | sí key | nullable |
| `span_id` | str|null | no | — |
| `tenant_id` | str|null | sí key | nullable |
| `project_id` | str|null | sí key | nullable |
| `job_id` | str|null | sí key | nullable E01 |
| `route_template` | str|null | no | — |
| `status_code` | int|null | no | access log |
| `duration_ms` | number|null | no | — |
| `event_type` | str|null | no | para SettingsActualizados log |

- Campo/log rule F.log.01: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.02: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.03: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.04: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.05: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.06: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.07: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.08: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.09: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.10: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.11: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.12: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.13: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.14: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.15: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.16: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.17: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.18: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.19: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.
- Campo/log rule F.log.20: redaction aplica antes de emit; tests cubren tokens MP/SECRET_KEY.

## Apéndice G — Compatibility matrix Free/Pro/Enterprise

| Capacidad | Free | Pro | Enterprise |
| --- | --- | --- | --- |
| Ver DegradationBanner | sí | sí | sí |
| GET platform/status | sí | sí | sí |
| Admin flags UI | owner only | owner only | owner only (+ future SSO E22) |
| Targeting flags by plan | sí (rules) | sí | sí |
| obs.enhanced cost absorption | off default | off default | posible on con ADR |
| Metrics endpoint | ops only | ops only | ops only |
| Support request_id in UI | sí | sí | sí |

- Revisión compat G.plan.01: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.02: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.03: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.04: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.05: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.06: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.07: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.08: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.09: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.10: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.11: no fork de código por plan; solo rules_json / entitlements futuros E02.
- Revisión compat G.plan.12: no fork de código por plan; solo rules_json / entitlements futuros E02.

## Apéndice H — Mapping a Architecture domains

| Feature E01 | Dominios Architecture |
| --- | --- |
| F01 | Platform / API Gateway / Workers(prep) |
| F02 | Platform / Frontend Studio / Settings |
| F03 | Settings / Audit light / Platform |
| F04 | Platform (eng standards) |
| F05 | Platform / Ops |

Según Apéndice G del ENGINEERING_ROADMAP: E01 → Platform / Settings / Audit light. Capa: Transversal.

- Mapping note H.map.01: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.02: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.03: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.04: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.05: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.06: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.07: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.08: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.09: Perception/Costs/MDO no son owners de escritura en E01.
- Mapping note H.map.10: Perception/Costs/MDO no son owners de escritura en E01.

## Apéndice I — Anti-scope list explícita

Si aparece en un ticket E01 sin ADR y sin pago explícito de oportunidad, **rechazar**:

1. Reescritura MDO / ProjectVersion / ChangeSet
2. Outbox table + broker real (E04)
3. WebSocket progress jobs
4. Object storage signed URLs (E03)
5. Identity sessions rewrite / SSO
6. Marketplace / quotes / orders
7. Chat IA grounded
8. AI Orchestrator / embeddings
9. Plugin host / SDK
10. Microservicios por tabla
11. Multi-region active-active
12. GPU workers perception
13. Vendor APM SDK como dependencia dura de dominio
14. Sentry-only instrumentation sin OTel
15. High-cardinality labels (email, project name)
16. Persistir cada /health en OLTP
17. SliSnapshot warehouse
18. Alembic full migration del legacy schema
19. Eliminar precios.json
20. Rotar SECRET_KEY automáticamente en E01
21. Cambiar healthCheckPath a /ready en Render sin plan
22. Deep checks en /health
23. Rediseño visual completo Studio
24. Dark mode redesign distraction
25. Flags eternas sin expiry
26. Hard-delete FeatureFlagAudit
27. Consumers de eventos en E01
28. Event bus como RPC
29. Perception escribiendo Costs
30. Costs leyendo Perception directo
31. LLM generando geometría/cantidades
32. wedge.calcular_v2 implementación real
33. Analytics customer SQL
34. Mobile app
35. CRDT collaborative editing
36. ERP / MS Project clone
37. BIM Autodesk parity
38. Public API keys/webhooks
39. Data lake ingestion
40. Custom Enterprise one-off packaging
41. Reescritura big-bang del wedge
42. Síncrono CV 'temporal para siempre' como plataforma
43. Shared DB cross-domain ownership blur
44. Auto-approve AIProposal
45. Generative fill de planos
46. Crypto/blockchain provenance theater
47. Notebooks data science sobre prod OLTP
48. Integraciones contables múltiples
49. Offline total Studio desktop
50. Marketplace plugins abiertos sin sandbox

- Frase alarma scope creep I.anti.01: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.02: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.03: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.04: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.05: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.06: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.07: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.08: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.09: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.10: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.11: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.12: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.13: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.14: «mientras estamos acá…» / «es igual de fácil…» → rechazar.
- Frase alarma scope creep I.anti.15: «mientras estamos acá…» / «es igual de fácil…» → rechazar.

## Apéndice J — Approval sign-off

| Rol | Nombre | Fecha | Firma (✓) | Notas |
| --- | --- | --- | --- | --- |
| CTO |  | ____-__-__ | [ ] | Alcance + cap 20% |
| Tech Lead |  | ____-__-__ | [ ] | Contratos API/eventos/datos |
| PM |  | ____-__-__ | [ ] | Criterios §12 |
| QA Lead / Eng |  | ____-__-__ | [ ] | Matrices §9 |
| Security (si aplica) |  | ____-__-__ | [ ] | PII/metrics auth |

Tras sign-off: cambiar estado del RFC a **Ready for implementation after approval**.

## Apéndice K — Glosario E01

| Término | Definición |
| --- | --- |
| Liveness | Proceso up; /health |
| Readiness | Dependencias críticas ok; /ready |
| Degradación | Servicio up pero features no críticas off |
| Correlation id | ID humano/ops para seguir request |
| Trace id | ID OTel del trazo distribuido |
| Label allowlist | Conjunto cerrado de labels de métricas |
| obs.enhanced | Flag para exporters/sampling caros |
| Wedge | color→qty→ARS path comercial |
| Hard freeze | Prohibición de scope fuera de F01–F05 |
| Expand/contract | Migración aditiva primero |

- Término extendido K.gloss.01: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.02: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.03: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.04: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.05: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.06: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.07: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.08: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.09: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.10: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.11: mantener consistencia con Apéndice A del roadmap.
- Término extendido K.gloss.12: mantener consistencia con Apéndice A del roadmap.

## Apéndice L — Decision log

| ID | Decisión | Fecha | Owner |
| --- | --- | --- | --- |
| D1 | OTel abstraction over vendor APM | 2026-08-02 | Tech Lead |
| D2 | Render healthCheckPath remains /health | 2026-08-02 | Tech Lead |
| D3 | No full event bus in E01 | 2026-08-02 | CTO |
| D4 | ensure_schema preferred for flags | 2026-08-02 | Tech Lead |
| D5 | Do not rotate SECRET_KEY in E01 | 2026-08-02 | CTO |
| D6 | Minimal SLIs only | 2026-08-02 | Tech Lead |
| D7 | Admin flags owner-only until E02 | 2026-08-02 | Tech Lead |
| D8 | Cap platform ≤20% | 2026-08-02 | CTO |
| D9 | No MDO rewrite | 2026-08-02 | CTO |
| D10 | Preserve wedge golden always | 2026-08-02 | PM/Tech Lead |

- Decision backlog item L.dec.01: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.02: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.03: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.04: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.05: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.06: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.07: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.08: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.09: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.10: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.11: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.12: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.13: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.14: si cambia, ADR + update de este RFC.
- Decision backlog item L.dec.15: si cambia, ADR + update de este RFC.

## Apéndice M — Open questions

| ID | Pregunta | Estado | Resolución provisional |
| --- | --- | --- | --- |
| Q1 | ¿Alembic bootstrap sí/no? | Cerrada-provisional | A default; B con ADR-0005 |
| Q2 | ¿Auth exacta admin flags pre-E02? | Cerrada-provisional | Studio owner check server-side |
| Q3 | ¿Proveedor OTLP inicial? | Abierta | Cualquiera vía OTLP; no lock |
| Q4 | ¿Exponer /ready públicamente? | Cerrada-provisional | Sí sin secretos |
| Q5 | ¿web-vitals a backend? | Defer | P2 ticket |
| Q6 | ¿ReleaseMarker obligatorio? | Cerrada | Opcional |

- Pregunta seguimiento M.q.01: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.02: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.03: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.04: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.05: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.06: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.07: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.08: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.09: resolver en kickoff implementación o ADR.
- Pregunta seguimiento M.q.10: resolver en kickoff implementación o ADR.

## Apéndice N — Trazabilidad Roadmap → RFC

| Roadmap item | Sección RFC |
| --- | --- |
| E01 objetivo | §0 |
| Riesgos OTel/cardinality/cap20% | §0.4, §3, §11 |
| API conceptual health/ready/metrics/flags | §6 |
|  pantallas banner/admin flags | §8 |
| Entidades FeatureFlag/ReleaseMarker/… | §5 |
| Eventos SettingsActualizados | §7 |
| F01–F05 tasks | §13 |
| DoD épica | §0.2, §12 |
| Anti-scope | Apéndice I |
| Mapping domains | Apéndice H |

- Trazabilidad N.trace.01: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.02: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.03: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.04: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.05: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.06: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.07: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.08: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.09: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.10: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.11: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.12: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.13: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.14: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.15: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.16: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.17: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.18: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.19: cada task Txx tiene AC en §12 o en demo checklist §13.
- Trazabilidad N.trace.20: cada task Txx tiene AC en §12 o en demo checklist §13.

## Apéndice O — Runbook skeletons

### O.1 health-and-ready

- Síntoma: Render restart loop / users 502
- Chequear /health vs /ready
- Si health fail: proceso/crash → logs JSON request_id
- Si ready fail: DB → DATABASE_URL / pool
- No cambiar código a ciegas; usar flags degradación

### O.2 feature-flag-rollback

- Identificar flag_key
- PATCH enabled=false con reason
- Verificar audit row
- Verificar banner/status
- Comunicar a support con request_ids

### O.3 dlq-empty-structure

- Placeholder hasta E04
- Secciones: detección, impacto, mitigación, escalación
- Métrica stub queue_depth/dlq=0

### O.4 incident sev definitions

| Sev | Definición | MTTR target inicial |
| --- | --- | --- |
| Sev1 | Wedge down / data isolation breach | <4h |
| Sev2 | Degradación mayor features | <8h |
| Sev3 | Impacto parcial | <2d |
| Sev4 | Cosmético/docs | best effort |

- Paso runbook O.rb.01: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.02: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.03: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.04: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.05: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.06: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.07: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.08: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.09: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.10: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.11: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.12: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.13: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.14: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.15: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.16: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.17: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.18: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.19: incluir owner, enlaces dashboards, y criterio de cierre.
- Paso runbook O.rb.20: incluir owner, enlaces dashboards, y criterio de cierre.

## Apéndice P — Performance budgets

| Superficie | Budget E01 |
| --- | --- |
| Middleware stack | p50 < 5ms overhead |
| Flag evaluate cached | p95 < 2ms |
|  /ready DB ping | < 1000ms timeout |
|  /platform/status | p95 < 200ms |
| Log redact | negligible; no regex catastrophic |

- Medición P.perf.01: capturar baseline antes/después fase A en staging.
- Medición P.perf.02: capturar baseline antes/después fase A en staging.
- Medición P.perf.03: capturar baseline antes/después fase A en staging.
- Medición P.perf.04: capturar baseline antes/después fase A en staging.
- Medición P.perf.05: capturar baseline antes/después fase A en staging.
- Medición P.perf.06: capturar baseline antes/después fase A en staging.
- Medición P.perf.07: capturar baseline antes/después fase A en staging.
- Medición P.perf.08: capturar baseline antes/después fase A en staging.
- Medición P.perf.09: capturar baseline antes/después fase A en staging.
- Medición P.perf.10: capturar baseline antes/después fase A en staging.
- Medición P.perf.11: capturar baseline antes/después fase A en staging.
- Medición P.perf.12: capturar baseline antes/después fase A en staging.

## Apéndice Q — Security & PII

- [ ] Redact emails en logs
- [ ] Redact tokens Authorization
- [ ] Redact MP secrets
- [ ] Redact SECRET_KEY
- [ ] No loguear body completo de uploads
- [ ] /metrics token required
- [ ] Admin flags AuthZ server-side
- [ ] Audit never hard-deleted
- [ ] No PII in metric labels
- [ ] CORS no wildcard prod

- Control seguridad Q.sec.01: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.02: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.03: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.04: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.05: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.06: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.07: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.08: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.09: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.10: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.11: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.12: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.13: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.14: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.15: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.16: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.17: verificar en PR checklist F01/F03/F04.
- Control seguridad Q.sec.18: verificar en PR checklist F01/F03/F04.

## Apéndice R — Rollback playbooks

#### R.A

- [ ] Set LOG_FORMAT=text
- [ ] Disable platform middleware via env
- [ ] Redeploy
- [ ] Verify /health + wedge

#### R.B

- [ ] Stop scraping /metrics
- [ ] Ignore /ready in ops
- [ ] Keep /health

#### R.C

- [ ] platform.degraded handling
- [ ] Disable FLAGS_ADMIN_ENABLED
- [ ] Seed flags safe defaults

#### R.D

- [ ] CI waive with ticket
- [ ] Do not block hotfix wedge

#### R.E

- [ ] Mute alerts
- [ ] obs.enhanced=false

- Ensayo rollback R.rb.01: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.02: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.03: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.04: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.05: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.06: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.07: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.08: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.09: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.10: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.11: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.12: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.13: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.14: ejecutar en staging antes de prod phase gate.
- Ensayo rollback R.rb.15: ejecutar en staging antes de prod phase gate.

## Apéndice S — Demo scripts

### S.1 Demo F01 (10 min)

- Mostrar log JSON con request_id
- Mostrar trace en backend OTLP (si enabled) o no-op safe
- Mostrar /metrics con token
- Correr test correlation ids

### S.2 Demo F02

- Bajar DB en staging → /ready 503, /health 200
- Activar platform.degraded → banner

### S.3 Demo F03

- Owner lista flags
- PATCH exports.enabled false con reason
- Ver audit + shape evento en log

### S.4 Demo F04

- Abrir PR → CI gates
- Mostrar PR template P01–P10

### S.5 Demo F05

- Abrir runbooks
- Simular rollback flag
- Mostrar sev defs

- Evidencia demo S.demo.01: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.02: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.03: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.04: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.05: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.06: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.07: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.08: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.09: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.10: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.11: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.12: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.13: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.14: link recording o script asciinema en docs/ops.
- Evidencia demo S.demo.15: link recording o script asciinema en docs/ops.

## Apéndice T — Registro de control

| Campo | Valor |
| --- | --- |
| Documento | RFC-E01 Platform Foundations & Observability |
| Versión | 1.0-proposed |
| Fecha | 2026-08-02 |
| Supersede | N/A (primer RFC E01) |
| Alineado a | AUDITORIA + MASTER PLAN + ARCHITECTURE + ENGINEERING_ROADMAP |
| Mantenimiento | Actualizar al cerrar fases A–E y ADRs |
| Owner | CTO / Tech Lead |

*Documento de diseño/contrato. No contiene código de implementación. Cualquier implementación debe respetar MDO como SoT (sin reescribirlo en E01), L1→L2→L3, preparación event-driven, Free/Pro/Enterprise, LATAM first, Etapa 1, y la cuña color→qty→ARS, sin romper funcionalidad existente.*

## Apéndice U — Matrices extendidas de contratos

### U.1 Matriz ruta × middleware × telemetría

| `/health` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/api/health` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/ready` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/metrics` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/v1/admin/flags` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/v1/admin/flags/{key}` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/v1/platform/status` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/v1/platform/version` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/calcular` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/api/calcular` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/auth/login` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/auth/register` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |
| `/precios-info` | Logging sí (access) | Tracing sí salvo health/metrics sample bajo | Metrics sí con route_template | Notas: no alterar negocio |

Cabecera conceptual: Ruta | Logging | Tracing | Metrics | Notas.

### U.2 Matriz errores × acción soporte

- Soporte case U.2.01: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.02: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.03: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.04: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.05: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.06: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.07: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.08: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.09: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.10: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.11: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.12: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.13: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.14: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.15: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.16: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.17: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.18: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.19: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.20: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.21: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.22: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.23: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.24: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.
- Soporte case U.2.25: pedir `request_id` + `APP_VERSION` + screenshot banner; buscar en logs JSON; no pedir passwords; no pedir SECRET_KEY.

### U.3 Matriz flag × efecto producto

| Flag | FE efecto | BE efecto | Default |
| --- | --- | --- | --- |
| platform.degraded | Banner on | status.degraded true | false |
| platform.banner_force | Banner on | status reason drill | false |
| exports.enabled | CTA export disabled | export endpoints 403/503 soft | true |
| ai.calcular_enabled | CTA calcular disabled/warn | calcular reject soft | true |
| obs.enhanced | N/A | exporters on | false |
| wedge.calcular_v2 | N/A | no-op placeholder | false |

- Contrato extendido U.ext.01: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.02: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.03: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.04: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.05: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.06: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.07: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.08: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.09: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.10: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.11: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.12: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.13: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.14: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.15: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.16: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.17: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.18: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.19: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.20: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.21: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.22: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.23: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.24: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.25: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.26: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.27: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.28: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.29: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.30: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.31: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.32: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.33: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.34: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.35: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.36: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.37: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.38: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.39: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.
- Contrato extendido U.ext.40: validar backward compat `/api/*` alias y headers CORS para X-Request-Id.

## Apéndice V — Catálogo de escenarios operativos

| ID | Escenario | Resultado esperado |
| --- | --- | --- |
| V01 | Deploy Render ok | /health 200, /ready 200, banner off |
| V02 | DB down | /health 200, /ready 503, platform.ready=0 |
| V03 | METRICS_TOKEN wrong | /metrics 403 |
| V04 | OTEL endpoint down | API sigue; traces drop; logs warn rate-limited |
| V05 | Flag patch by non-owner | 403 + no audit change |
| V06 | Flag patch owner | 200 + audit + event shape log |
| V07 | platform.degraded true | banner + exports/ai flags possibly off |
| V08 | Cold start | document time to ready; no strict SLO |
| V09 | CORS preflight | OPTIONS ok with request-id exposure |
| V10 | Wedge golden after phase A | pass |
| V11 | Wedge golden after phase C | pass |
| V12 | CI red on secret | block merge |
| V13 | TODO without issue | block merge policy |
| V14 | Stale flag 91d | dashboard panel lists it |
| V15 | Support follows request | runbook F01 path |

| V16 | Escenario operativo extendido #16 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V17 | Escenario operativo extendido #17 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V18 | Escenario operativo extendido #18 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V19 | Escenario operativo extendido #19 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V20 | Escenario operativo extendido #20 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V21 | Escenario operativo extendido #21 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V22 | Escenario operativo extendido #22 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V23 | Escenario operativo extendido #23 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V24 | Escenario operativo extendido #24 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V25 | Escenario operativo extendido #25 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V26 | Escenario operativo extendido #26 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V27 | Escenario operativo extendido #27 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V28 | Escenario operativo extendido #28 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V29 | Escenario operativo extendido #29 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V30 | Escenario operativo extendido #30 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V31 | Escenario operativo extendido #31 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V32 | Escenario operativo extendido #32 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V33 | Escenario operativo extendido #33 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V34 | Escenario operativo extendido #34 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V35 | Escenario operativo extendido #35 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V36 | Escenario operativo extendido #36 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V37 | Escenario operativo extendido #37 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V38 | Escenario operativo extendido #38 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V39 | Escenario operativo extendido #39 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V40 | Escenario operativo extendido #40 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V41 | Escenario operativo extendido #41 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V42 | Escenario operativo extendido #42 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V43 | Escenario operativo extendido #43 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V44 | Escenario operativo extendido #44 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V45 | Escenario operativo extendido #45 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V46 | Escenario operativo extendido #46 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V47 | Escenario operativo extendido #47 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V48 | Escenario operativo extendido #48 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V49 | Escenario operativo extendido #49 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V50 | Escenario operativo extendido #50 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V51 | Escenario operativo extendido #51 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V52 | Escenario operativo extendido #52 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V53 | Escenario operativo extendido #53 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V54 | Escenario operativo extendido #54 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V55 | Escenario operativo extendido #55 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V56 | Escenario operativo extendido #56 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V57 | Escenario operativo extendido #57 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V58 | Escenario operativo extendido #58 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V59 | Escenario operativo extendido #59 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |
| V60 | Escenario operativo extendido #60 (failover FE, poll status, cache TTL, seed idempotente, etc.) | Comportamiento degradado seguro; wedge intacto |

- Verificación operativa V.op.01: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.02: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.03: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.04: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.05: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.06: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.07: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.08: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.09: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.10: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.11: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.12: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.13: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.14: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.15: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.16: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.17: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.18: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.19: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.20: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.21: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.22: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.23: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.24: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.25: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.26: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.27: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.28: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.29: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.30: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.31: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.32: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.33: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.34: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.35: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.36: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.37: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.38: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.39: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.40: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.41: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.42: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.43: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.44: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.45: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.46: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.47: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.48: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.49: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).
- Verificación operativa V.op.50: ejecutar en staging checklist release Apéndice F del roadmap (subset aplicable E01).

## Apéndice W — Capacidad y planificación ≤20%

El ENGINEERING_ROADMAP fija cap ≤20% capacidad del equipo en E01 para no retrasar el wedge. Planificación sugerida para 1–2 eng / 1–2 meses:

| Semana | Foco | % capacidad plataforma | % wedge/producto |
| --- | --- | --- | --- |
| S1 | Fase A logs+request id + ADR skeleton | 20% | 80% |
| S2 | Fase B ready/metrics + tests | 20% | 80% |
| S3 | Fase C flags+banner | 20% | 80% |
| S4 | Fase D CI+runbooks | 15% | 85% |
| S5–S8 | Fase E dashboards + hardening + buffer | ≤20% | ≥80% |

- Checkpoint capacidad W.cap.01: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.02: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.03: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.04: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.05: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.06: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.07: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.08: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.09: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.10: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.11: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.12: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.13: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.14: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.15: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.16: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.17: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.18: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.19: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.
- Checkpoint capacidad W.cap.20: si plataforma supera 20% semanal, cortar exporters/dashboards vanity y preservar wedge.

## Apéndice X — OpenAPI fragment (conceptual YAML)

```
# conceptual — not runnable implementation
openapi: 3.0.3
info:
  title: ARQ-IA Platform E01
  version: 1.0.0
paths:
  /health:
    get:
      summary: Liveness
      responses:
        '200':
          description: Process up
  /ready:
    get:
      summary: Readiness
      responses:
        '200':
          description: Ready
        '503':
          description: Not ready
  /metrics:
    get:
      summary: Prometheus metrics
      security:
        - bearerAuth: []
  /v1/admin/flags:
    get:
      summary: List flags
  /v1/admin/flags/{key}:
    patch:
      summary: Patch flag
  /v1/platform/status:
    get:
      summary: Degradation status for Studio
  /v1/platform/version:
    get:
      summary: Version info
```

- Campo OpenAPI X.api.01: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.02: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.03: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.04: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.05: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.06: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.07: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.08: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.09: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.10: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.11: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.12: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.13: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.14: mantener sync con §6; contract tests placeholder F04.
- Campo OpenAPI X.api.15: mantener sync con §6; contract tests placeholder F04.

## Apéndice Y — Checklist de review de PR para E01

- [ ] ¿El PR está dentro de F01–F05?
- [ ] ¿Hay ADR si hay desvío?
- [ ] ¿Se preservó /health y /api/health?
- [ ] ¿Label allowlist respetada?
- [ ] ¿Sin vendor APM lock?
- [ ] ¿Sin MDO/bus/marketplace/chat/plugins?
- [ ] ¿Tests platform + golden?
- [ ] ¿Redaction PII?
- [ ] ¿AuthZ admin flags?
- [ ] ¿Capacidad/plataforma justificada?
- [ ] ¿Rollback/flag plan en descripción?
- [ ] ¿Docs/runbook actualizados si aplica?
- [ ] ¿TODO con issue?
- [ ] ¿SECRET_KEY intacta?
- [ ] ¿precios.json intacto?

- Ítem review Y.pr.01: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.02: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.03: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.04: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.05: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.06: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.07: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.08: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.09: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.10: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.11: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.12: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.13: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.14: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.15: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.16: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.17: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.18: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.19: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.20: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.21: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.22: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.23: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.24: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.
- Ítem review Y.pr.25: reviewer verifica mapping Architecture domain Platform/Settings/Audit light.

## Apéndice Z — Cierre

Este RFC deja listo el contrato para implementar E01 sin ambigüedad: observabilidad mínima con OTel, health/ready, flags con audit, CI gates y runbooks, respetando cap ≤20%, preservando wedge color→qty→ARS, sin MDO rewrite, sin marketplace/chat/plugins, y sin bus completo (solo correlation + SettingsActualizados shape).

Estado al publicar: **Proposed**. Tras Apéndice J: **Ready for implementation after approval**.

- Clausula final Z.close.01: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.02: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.03: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.04: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.05: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.06: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.07: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.08: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.09: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.10: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.11: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.12: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.13: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.14: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.15: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.16: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.17: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.18: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.19: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.20: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.21: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.22: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.23: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.24: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.25: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.26: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.27: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.28: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.29: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.
- Clausula final Z.close.30: implementación debe seguir fases A–E; cualquier atajo big-bang invalida DoD.

## Apéndice AA — Narrativa de justificación técnica (extensa)

- Justificación AA.01: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.02: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.03: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.04: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.05: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.06: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.07: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.08: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.09: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.10: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.11: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.12: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.13: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.14: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.15: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.16: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.17: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.18: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.19: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.20: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.21: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.22: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.23: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.24: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.25: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.26: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.27: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.28: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.29: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.30: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.31: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.32: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.33: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.34: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.35: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.36: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.37: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.38: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.39: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.40: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.41: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.42: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.43: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.44: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.45: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.46: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.47: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.48: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.49: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.50: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.51: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.52: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.53: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.54: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.55: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.56: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.57: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.58: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.59: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.60: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.61: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.62: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.63: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.64: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.65: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.66: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.67: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.68: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.69: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.70: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.71: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.72: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.73: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.74: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.75: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.76: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.77: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.78: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.79: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.
- Justificación AA.80: E01 existe para eliminar cajas negras operativas antes de E03–E07; cada incremento debe ser demoable, reversible por flag, medible con SLIs mínimos, y nunca comprometer la cuña comercial color→qty→ARS ni introducir bus/MDO/marketplace/chat/plugins.

## Apéndice AB — Inventario de aceptación por fase

#### AB.Fase A

- [ ] Fase A: tests verdes asociados
- [ ] Fase A: rollback ensayado en staging
- [ ] Fase A: wedge golden pass
- [ ] Fase A: sin P0 debt nueva
- [ ] Fase A: docs/runbooks actualizados si aplica
- [ ] Fase A: capacidad plataforma ≤20% en la semana
- [ ] Fase A: sign-off Tech Lead parcial

#### AB.Fase B

- [ ] Fase B: tests verdes asociados
- [ ] Fase B: rollback ensayado en staging
- [ ] Fase B: wedge golden pass
- [ ] Fase B: sin P0 debt nueva
- [ ] Fase B: docs/runbooks actualizados si aplica
- [ ] Fase B: capacidad plataforma ≤20% en la semana
- [ ] Fase B: sign-off Tech Lead parcial

#### AB.Fase C

- [ ] Fase C: tests verdes asociados
- [ ] Fase C: rollback ensayado en staging
- [ ] Fase C: wedge golden pass
- [ ] Fase C: sin P0 debt nueva
- [ ] Fase C: docs/runbooks actualizados si aplica
- [ ] Fase C: capacidad plataforma ≤20% en la semana
- [ ] Fase C: sign-off Tech Lead parcial

#### AB.Fase D

- [ ] Fase D: tests verdes asociados
- [ ] Fase D: rollback ensayado en staging
- [ ] Fase D: wedge golden pass
- [ ] Fase D: sin P0 debt nueva
- [ ] Fase D: docs/runbooks actualizados si aplica
- [ ] Fase D: capacidad plataforma ≤20% en la semana
- [ ] Fase D: sign-off Tech Lead parcial

#### AB.Fase E

- [ ] Fase E: tests verdes asociados
- [ ] Fase E: rollback ensayado en staging
- [ ] Fase E: wedge golden pass
- [ ] Fase E: sin P0 debt nueva
- [ ] Fase E: docs/runbooks actualizados si aplica
- [ ] Fase E: capacidad plataforma ≤20% en la semana
- [ ] Fase E: sign-off Tech Lead parcial

## Apéndice AC — Matriz de correlación request→soporte

- Flujo soporte AC.01: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.02: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.03: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.04: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.05: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.06: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.07: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.08: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.09: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.10: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.11: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.12: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.13: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.14: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.15: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.16: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.17: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.18: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.19: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.20: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.21: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.22: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.23: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.24: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.25: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.26: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.27: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.28: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.29: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.30: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.31: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.32: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.33: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.34: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.35: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.36: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.37: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.38: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.39: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.
- Flujo soporte AC.40: usuario reporta fallo → UI muestra lastRequestId → ops busca en logs JSON → correlaciona trace_id si OTel on → decide flag rollback o fix.

## Apéndice AD — Requisitos no funcionales detallados

| NFR | Requisito E01 | Medición |
| --- | --- | --- |
| Disponibilidad | No degradar uptime por middleware | health + error rate |
| Latencia | Overhead middleware <5ms p50 | benchmark local/staging |
| Seguridad | PII redaction + metrics auth | tests S-* |
| Operabilidad | Runbooks mínimos publicados | docs exist |
| Mantenibilidad | Package platform/ separado | review estructura |
| Evolutividad | OTel + event shape listos para E04 | ADR + contracts |
| Costo | Exporters caros detrás obs.enhanced | flag default false |
| Cumplimiento LATAM | Mensajes ES; moneda wedge intacta | golden |

- NFR check AD.nfr.01: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.02: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.03: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.04: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.05: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.06: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.07: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.08: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.09: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.10: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.11: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.12: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.13: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.14: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.15: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.16: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.17: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.18: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.19: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.20: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.21: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.22: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.23: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.24: incluir en DoD parcial de fase; no negociar redaction ni allowlist.
- NFR check AD.nfr.25: incluir en DoD parcial de fase; no negociar redaction ni allowlist.

## Apéndice AE — Dependencias futuras explícitas (no implementar)

| Necesidad | Épica futura | Preparación E01 |
| --- | --- | --- |
| Outbox/DLQ real | E04 | runbook stub + métrica gauge 0 |
| Object storage check | E03 | ready skipped |
| Workers spans reales | E04/E05 | context helpers |
| RBAC fino flags | E02/E22 | owner-only temporal |
| UsoRegistrado meters | E02 | deferred event |
| MDO provenance attach | E07 | no-op |

- Dependencia futura AE.dep.01: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.02: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.03: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.04: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.05: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.06: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.07: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.08: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.09: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.10: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.11: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.12: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.13: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.14: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.15: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.16: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.17: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.18: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.19: documentada para no ser implementada accidentalmente en E01.
- Dependencia futura AE.dep.20: documentada para no ser implementada accidentalmente en E01.

## Apéndice AF — Fin del RFC

Fin del RFC-E01. Implementación solo tras sign-off (Apéndice J). Mantener este archivo como contrato vivo durante E01; cambios materials requieren nueva revisión.

Verificación de tamaño: este documento debe superar 2200 líneas (`wc -l`) para servir como contrato exhaustivo pre-coding.

- Cierre AF.01: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.02: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.03: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.04: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.05: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.06: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.07: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.08: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.09: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.10: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.11: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.12: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.13: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.14: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.15: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.16: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.17: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.18: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.19: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.20: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.21: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.22: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.23: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.24: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.25: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.26: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.27: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.28: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.29: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.30: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.31: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.32: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.33: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.34: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.35: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.36: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.37: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.38: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.
- Cierre AF.39: ARQ-IA 3.1 · RFC-E01 · Platform Foundations & Observability · 2026-08-02 · Proposed.

