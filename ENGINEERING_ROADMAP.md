# ARQ-IA 3.1 — ENGINEERING ROADMAP

| Campo | Valor |
|-------|-------|
| Documento | ARQ-IA 3.1 — Engineering Roadmap |
| Fecha | 2026-08-02 |
| Estado | Plan de ingeniería oficial |
| Audiencia | CTO / Tech Lead / PM / Staff Eng |
| Naturaleza | Planificación (sin código) |
| Alcance | Conversión de arquitectura aprobada en plan multi-año ejecutable |
| Fuente de verdad | MDO (Modelo Digital de la Obra) |
| Capas | L1 Percepción → L2 Twin → L3 Inteligencia |
| Principio IA | La IA nunca inventa geometría ni cantidades |
| Crecimiento | Event-driven + plugins |
| Monetización | Free / Pro / Enterprise |
| Mercado | LATAM primero |
| Norte técnico | Etapas de arquitectura 1–5 |
| Cuña comercial | Plano coloreado → cantidades → presupuesto moneda local |
| Evolución | Incremental, testeable, desplegable; nunca romper funcionalidad existente |

---

## Índice

1. [Principios](#1-principios)
2. [Catálogo de Épicas](#2-catálogo-de-épicas)
   - [E01 Platform Foundations & Observability](#e01-platform-foundations--observability)
   - [E02 Identity, Tenancy & Billing hardening](#e02-identity-tenancy--billing-hardening)
   - [E03 Media & Object Storage](#e03-media--object-storage)
   - [E04 Async Jobs & Event Bus (Outbox)](#e04-async-jobs--event-bus-outbox)
   - [E05 Perception Engine (CV/OCR) modernization](#e05-perception-engine-cvocr-modernization)
   - [E06 Geometry Engine](#e06-geometry-engine)
   - [E07 MDO Core (entities, versions, changesets)](#e07-mdo-core-entities-versions-changesets)
   - [E08 Materials Engine](#e08-materials-engine)
   - [E09 Costs & PriceBooks](#e09-costs--pricebooks)
   - [E10 Takeoff Projections & Signed Budgets](#e10-takeoff-projections--signed-budgets)
   - [E11 Scenarios (Git-like)](#e11-scenarios-git-like)
   - [E12 Frontend Workspace & Model Explorer](#e12-frontend-workspace--model-explorer)
   - [E13 Reports (PDF/Excel) & Exports](#e13-reports-pdfexcel--exports)
   - [E14 Notifications & Email](#e14-notifications--email)
   - [E15 Chat IA grounded](#e15-chat-ia-grounded)
   - [E16 AI Orchestrator / Guards / Eval](#e16-ai-orchestrator--guards--eval)
   - [E17 Timeline / Progress / Certifications](#e17-timeline--progress--certifications)
   - [E18 Procurement light / Purchase Orders](#e18-procurement-light--purchase-orders)
   - [E19 Plugin Host & Module SDK](#e19-plugin-host--module-sdk)
   - [E20 Domain Plugins (Steel/HA/Gas/Fire/etc packs)](#e20-domain-plugins-steelhagasfireetc-packs)
   - [E21 Marketplace](#e21-marketplace)
   - [E22 Enterprise (SSO, RBAC fine, multi-company, audit export, DR)](#e22-enterprise-sso-rbac-fine-multi-company-audit-export-dr)
   - [E23 Public API & Integrations](#e23-public-api--integrations)
   - [E24 Data Platform / Analytics (later)](#e24-data-platform--analytics-later)
   - [E25 Mobile Site Ops (later)](#e25-mobile-site-ops-later)
3. [Features y Tasks por Épica (detalle exhaustivo)](#3-features-y-tasks-por-épica-detalle-exhaustivo)
4. [Matriz Feature × Capability](#4-matriz-feature--capability)
5. [Detalle de Tasks transversales y checklists](#5-detalle-de-tasks-transversales-y-checklists)
6. [Dependencias](#6-dependencias)
7. [Riesgos](#7-riesgos)
8. [Criterio de calidad (Definition of Done global)](#8-criterio-de-calidad-definition-of-done-global)
9. [Roadmap visual](#9-roadmap-visual)
10. [Backlog MoSCoW](#10-backlog-moscow)
11. [MVP comercial](#11-mvp-comercial)
12. [Versión 1.0](#12-versión-10)
13. [Versión 2.0](#13-versión-20)
14. [Versión 3.0](#14-versión-30)
15. [Conclusión — un solo desarrollador](#15-conclusión--un-solo-desarrollador)
- [Apéndice A — Glosario](#apéndice-a--glosario)
- [Apéndice B — Plantilla de Epic brief](#apéndice-b--plantilla-de-epic-brief)
- [Apéndice C — Plantilla de Feature brief](#apéndice-c--plantilla-de-feature-brief)
- [Apéndice D — RACI sugerido](#apéndice-d--raci-sugerido)
- [Apéndice E — Métricas de engineering health](#apéndice-e--métricas-de-engineering-health)
- [Apéndice F — Checklist release](#apéndice-f--checklist-release)
- [Apéndice G — Mapping Epic → Architecture domains](#apéndice-g--mapping-epic--architecture-domains)
- [Apéndice H — Anti-scope creep list](#apéndice-h--anti-scope-creep-list)

---

## Nota de uso

Este documento **no** re-audita producto ni resume el Master Plan / Arquitectura como ensayo. Convierte decisiones ya aprobadas (AUDITORIA, MASTER PLAN, ARCHITECTURE) en un plan de ingeniería multi-año: épicas, features, tasks, dependencias, riesgos, criterios de calidad y secuenciación.

Reglas operativas del plan:
1. El MDO es la única fuente de verdad de la obra digital.
2. L1 produce evidencias; L2 materializa el twin; L3 asiste con citas.
3. La IA nunca inventa geometría ni cantidades autoritativas.
4. Todo crecimiento significativo es event-driven y/o vía plugins.
5. Free / Pro / Enterprise son ejes de cuota y capacidad, no forks de código.
6. LATAM first: moneda local, unidades, flujos estudio/constructor.
7. Las etapas de arquitectura 1–5 son el norte de secuenciación técnica.
8. Se preserva la cuña comercial: plano coloreado → cantidades → presupuesto moneda local.
9. Nunca se rompe funcionalidad existente; cada épica es incremental, testeable y desplegable.
10. Debemos preferir deuda visible + ticketed sobre tech debt silencioso.

---

## 1. Principios

Principios de ingeniería que gobiernan priorización, diseño de épicas, aceptación de PRs y definición de done. Cada principio incluye racional, tabla de implicaciones y anti-patrones.

### P01 — Compatibilidad hacia atrás en cada release

**Racional:** Los usuarios LATAM no pueden perder el wedge operativo entre deploys.

| Dimensión | Implicación operativa |
|-------|-------|
| Compatibilidad API | Versionado `/v1` + deprecación anunciada ≥ 1 ciclo |
| Datos | Migraciones expand/contract; dual-read cuando haga falta |
| UX | Feature flags; fallback al flujo legacy si el nuevo falla |
| Eventos | Campos nuevos opcionales; consumers tolerantes |
| Contratos | Contract tests en CI contra esquemas publicados |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P02 — Épicas desplegables de forma independiente

**Racional:** Una épica que no puede ir a producción sola no es una épica: es un programa.

| Dimensión | Implicación operativa |
|-------|-------|
| Slice vertical | Backend + eventos + UI mínima + tests + métricas |
| Feature flag | Default off hasta validación |
| Rollback | Plan documentado en el brief de la épica |
| No big-bang | Prohibido esperar a que 'todo el twin' esté listo |
| Demo | Cada épica tiene demo path de ≤ 15 minutos |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P03 — Testabilidad como requisito de diseño

**Racional:** Si no se puede probar de forma automatizable, el diseño está incompleto.

| Dimensión | Implicación operativa |
|-------|-------|
| Unit | Motores deterministas (geometría, fórmulas, costos) |
| Contract | Eventos y APIs con esquemas versionados |
| Integration | Outbox → bus → consumer → proyección |
| E2E wedge | Color→qty→moneda local en cada release candidate |
| Isolation | Suite multi-tenant obligatoria |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P04 — Cero tech debt silencioso

**Racional:** La deuda no documentada es más cara que la deuda explícita.

| Dimensión | Implicación operativa |
|-------|-------|
| Ticket | TODO/FIXME referencia issue con owner y fecha |
| ADR | Desvíos arquitectónicos requieren ADR |
| Budget | Cada sprint reserva capacidad de pago de deuda P0/P1 |
| Gate | No merge con debt P0 nuevo sin waiver CTO |
| Visibilidad | Board de deuda revisado quincenalmente |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P05 — Clean architecture / boundaries de dominio

**Racional:** Los bounded contexts de arquitectura son contratos, no sugerencias.

| Dimensión | Implicación operativa |
|-------|-------|
| Ownership | Un dominio escribe sus entidades; otros leen vía API/eventos |
| Anti-corruption | IA y plugins nunca escriben stores ajenos directo |
| Dependencias | Perception↛Costs; AI↛Geometry write |
| Módulos | Packages lógicos aunque el deploy sea modular monolito |
| Tests de arquitectura | Import lints / archunit-like |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P06 — Incrementalismo brutal

**Racional:** El wedge existente debe mejorar en cada fase, no pausarse para la plataforma perfecta.

| Dimensión | Implicación operativa |
|-------|-------|
| Thin slice | Primero vertical mínimo sobre MDO |
| Strangler | Reemplazar file-centric por twin sin apagar producto |
| Medición | Cada incremento mejora métrica de wedge o fiabilidad |
| Stop rule | Si no es demoable en ≤ 4 semanas, partirlo |
| Preserve | Nunca romper color→qty→presupuesto |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P07 — Observabilidad first-class

**Racional:** Sin traces/métricas/logs estructurados, perception y costos son cajas negras.

| Dimensión | Implicación operativa |
|-------|-------|
| Correlación | trace_id / request_id / job_id / tenant_id |
| SLIs | Latencia API, cola depth, tasa DLQ, confidence promedio |
| Alertas | Error budget por clase de operación |
| Auditoría | Hechos comerciales separados de logs de app |
| Dashboards | Core vivos antes de Etapa 2 |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P08 — Seguridad y aislamiento multi-tenant desde día 0

**Racional:** Una fuga cross-tenant destruye confianza SMB y Enterprise por igual.

| Dimensión | Implicación operativa |
|-------|-------|
| AuthZ | Checks en capa de dominio, no solo gateway |
| Storage keys | Prefijo org/project obligatorio |
| Tests | Suite de aislamiento tenant en CI |
| Least privilege | Service accounts por worker capability |
| Review | Threat model ligero por épica P0 |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P09 — Confidence scores y provenance en hechos cuantitativos

**Racional:** Cantidad sin provenance no es dato de ingeniería; es rumor.

| Dimensión | Implicación operativa |
|-------|-------|
| Campos | confidence, source, formula_id, evidence_ids |
| UI | Indicadores de calidad visibles en takeoff |
| Gates | Presupuesto firmado exige umbrales o override auditado |
| IA | Citas deben apuntar a hechos con provenance |
| Métricas | % líneas bajo umbral en dashboard |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P10 — HITL para decisiones de dinero

**Racional:** Ningún presupuesto firmado, certificación o compra nace solo de L3.

| Dimensión | Implicación operativa |
|-------|-------|
| Firmas | Rol humano explícito + hash de snapshot |
| AIProposal | draft → accepted/rejected por humano |
| Overrides | Razón obligatoria + audit append-only |
| Chat | Uso en docs genera evento auditable |
| Compras | PO requiere aprobación según plan/rol |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P11 — Determinismo de motores L1/L2

**Racional:** Misma entrada + misma versión de pipeline → misma salida (salvo seeds documentados).

| Dimensión | Implicación operativa |
|-------|-------|
| Versionado | pipeline_version / formula_version en cada job |
| Replay | Re-ejecutar sobre mismos assets |
| Golden tests | Fixtures de planos LATAM canónicos |
| No LLM en L2 write | Prohibido path generativo a geometría/cantidades |
| Seeds | Si hay aleatoriedad, documentada y fijable |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P12 — Event-driven para extensión, sync para UX inmediata

**Racional:** No todo es async; no todo es sync. Elegir por clase de operación.

| Dimensión | Implicación operativa |
|-------|-------|
| Sync | Lecturas, ediciones pequeñas, auth |
| Async | Perception, reports, embeddings, exports grandes |
| Outbox | Mutación + evento atómicos lógicamente |
| Idempotencia | Consumers safe ante redelivery |
| WS | Progreso y presencia, no SoT |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P13 — Feature flags y entitlements por plan

**Racional:** Free/Pro/Enterprise se expresan como flags y meters, no branches de código.

| Dimensión | Implicación operativa |
|-------|-------|
| Entitlements | Fuente de verdad de capacidad |
| UI | Degradación graceful, no crash |
| Meters | Uso via eventos UsoRegistrado/UsoConsumido |
| Tests | Matriz plan × feature en CI smoke |
| Pricing | Cambios de plan sin redeploy de lógica de dominio |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P14 — LATAM-first en datos y UX

**Racional:** Moneda local, formatos ES, latencia tolerante, workflows de estudio/constructor.

| Dimensión | Implicación operativa |
|-------|-------|
| Currency | Project.currency + CurrencyRate |
| i18n | ES-AR / ES-LATAM prioritario |
| Offline-ish | Jobs resumibles; UI de progreso robusta |
| Pricebooks | Regionales por default |
| Soporte | Flujos de estudio pequeño primero |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P15 — Performance budgets explícitos

**Racional:** Sin presupuesto, percepción y twin se vuelven lentos sin alarma.

| Dimensión | Implicación operativa |
|-------|-------|
| API p95 | Por clase lectura vs mutación |
| Jobs | SLO por cola perception/geometry/materials/costs/reports |
| Frontend | TTI workspace y bundle budget |
| Regresión | Benchmarks CI motores críticos |
| Fairness | Noisy neighbor controls |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P16 — Soft-delete + retención sobre hard-delete

**Racional:** Hechos comerciales y lineage no se borran; se retienen.

| Dimensión | Implicación operativa |
|-------|-------|
| Inmutables | SignedBudget, Certification, AuditEvent, usage |
| Soft delete | Scenarios, media según política |
| Legal hold | Enterprise puede congelar retención |
| GC | Jobs de retención explícitos |
| UX | Archivado visible vs borrado falso |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P17 — Citation-first en IA comercial

**Racional:** Respuesta sin cita a MDO/proyección no se usa en documentos de dinero.

| Dimensión | Implicación operativa |
|-------|-------|
| Guards | Policy engine refuse-without-citation |
| Eval | Suite de alucinación en CI/nightly |
| UX | Citas clickeables a entity/version |
| Evento | ChatRespuestaUsadaEnDoc |
| Quotas | Degradación Free sin saltarse guards |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P18 — Plugins por capability contracts, no forks

**Racional:** Steel/HA/Gas/Fire extienden tipologías y fórmulas sin tocar core.

| Dimensión | Implicación operativa |
|-------|-------|
| Manifest | Versionado + capabilities declaradas |
| Sandbox | Límites CPU/mem/IO |
| Compat matrix | Core semver ↔ plugin semver |
| Marketplace gate | Firma y review antes de publicar |
| SDK | Documentado + ejemplos |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P19 — Seguridad de supply chain y secretos

**Racional:** Workers, LLM keys y storage credentials son superficie de ataque.

| Dimensión | Implicación operativa |
|-------|-------|
| Secrets | Inyección + rotación |
| Deps | Lockfiles + audit CI |
| Plugins | Allowlist de APIs host |
| Least privilege | IAM por servicio |
| Scanning | Secrets scan en CI |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P20 — Operabilidad y runbooks

**Racional:** Si no hay runbook de DLQ/job stuck, no está listo para Pro.

| Dimensión | Implicación operativa |
|-------|-------|
| Runbooks | DLQ, replay, scale-out, rollback flag |
| Oncall | Severities y owners por dominio |
| Chaos light | Kill worker y verificar recuperación |
| Postmortems | Blameless + action items ticketed |
| Drill | Ejercicio trimestral de restore |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P21 — Diseño para 1 desarrollador y para un equipo

**Racional:** Ejecutable por 1 eng (camino crítico) o 1–3 eng (tracks paralelos).

| Dimensión | Implicación operativa |
|-------|-------|
| Critical path | Documentado en §6 y §15 |
| Parallelism | Tracks UI / platform / engines |
| Docs | Briefs cortos en tickets |
| Definition of Ready | Contratos claros antes de code |
| WIP limits | Evitar N épicas a medias |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P22 — No microservicios prematuros

**Racional:** Boundaries lógicos primero; split físico solo con dolor medido (Etapa 5).

| Dimensión | Implicación operativa |
|-------|-------|
| Modular monolith | Default Etapas 1–3 |
| Workers | Procesos separados por carga |
| Split criteria | Deploy coupling, scaling asymmetry, ownership |
| Anti-pattern | 1 servicio = 1 tabla |
| ADR | Obligatorio para cada split |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### P23 — Medir confianza del twin, no solo uptime

**Racional:** Uptime alto con takeoff incorrecto es fracaso de producto.

| Dimensión | Implicación operativa |
|-------|-------|
| Quality flags | En ElementGeometry y TakeoffLine |
| Dashboards | % líneas con confidence < umbral |
| Feedback | Overrides humanos → mejora fórmulas/UX |
| Release gate | No degradar golden set wedge |
| Customer signal | Tasa de overrides por tipología |

**Anti-patrones asociados:**
- Ignorar el principio 'solo por este sprint'.
- Tratarlo como slogan sin gate en PR/release.
- Documentar excepción sin ADR ni fecha de remediación.
- Optimizar velocidad local sacrificando SoT o aislamiento tenant.

### 1.24 Tabla resumen de principios × gate de release

| Principio | Gate CI | Gate Release | Owner típico |
|-------|-------|-------|-------|
| P01 Compat | Contract tests | Changelog + deprecations | Staff Eng |
| P02 Deployable epic | Flag tests | Rollback plan | Tech Lead |
| P03 Tests | Coverage + e2e smoke | Golden wedge pass | QA/Eng |
| P04 No silent debt | Issue-linked TODOs | P0 debt = 0 | Tech Lead |
| P05 Boundaries | Import/arch lints | ADR check | Architect |
| P06 Incremental | Demo checklist | Metric delta | PM/TL |
| P07 Observability | Otel smoke | Dashboards live | Platform |
| P08 Tenant isolation | Isolation suite | Security review | Security |
| P09 Provenance | Schema asserts | UI quality visible | Domain Eng |
| P10 HITL money | AuthZ firmas | Audit sample | Domain Eng |
| P11 Determinism | Golden fixtures | Replay verified | Engines |
| P12 Sync/Async | Job contracts | SLO queues green | Platform |
| P13 Plans/flags | Plan matrix smoke | Entitlements OK | Billing Eng |
| P14 LATAM | i18n/currency tests | Pricebook regional | Product Eng |
| P15 Perf budgets | Bench CI | p95 within budget | Platform |
| P16 Soft-delete | Delete policy tests | Retention dry-run | Platform |
| P17 Citations | Eval refuse suite | No uncited money claims | AI Eng |
| P18 Plugins | Manifest schema | Sandbox limits | Platform |
| P19 Supply chain | Dep audit | Secrets scan | Platform |
| P20 Runbooks | Link presence | Oncall ack | SRE/TL |
| P21 1-dev capable | Scope review | Critical path updated | CTO/TL |
| P22 No premature MS | Topology review | Split justification | Architect |
| P23 Twin trust | Quality metrics | Confidence dashboard | Domain Eng |

---
---

## 2. Catálogo de Épicas

Catálogo oficial de épicas de ingeniería. Cada épica es un incremento potencialmente desplegable alineado a las etapas de arquitectura 1–5 y a la preservación de la cuña comercial.

### 2.0 Mapa rápido

| ID | Épica | Prioridad | Complejidad | Tiempo (1–3 eng) | Etapa arch |
|-------|-------|-------|-------|-------|-------|
| E01 | Platform Foundations & Observability | P0 | M | 1–2 meses | 1 |
| E02 | Identity, Tenancy & Billing hardening | P0 | L | 1.5–3 meses | 1 |
| E03 | Media & Object Storage | P0 | M | 1–2 meses | 1 |
| E04 | Async Jobs & Event Bus (Outbox) | P0 | L | 1.5–3 meses | 1 |
| E05 | Perception Engine (CV/OCR) | P0 | XL | 2–4 meses | 1 |
| E06 | Geometry Engine | P0 | XL | 2–4 meses | 2 |
| E07 | MDO Core | P0 | XL | 2–5 meses | 1 |
| E08 | Materials Engine | P0 | L | 1.5–3 meses | 2 |
| E09 | Costs & PriceBooks | P0 | L | 1.5–3 meses | 2 |
| E10 | Takeoff Projections & Signed Budgets | P0 | M | 1–2 meses | 2 |
| E11 | Scenarios (Git-like) | P1 | L | 2–3 meses | 2 |
| E12 | Frontend Workspace & Model Explorer | P0 | L | 2–4 meses | 1–2 |
| E13 | Reports & Exports | P1 | M | 1.5–2.5 meses | 3 |
| E14 | Notifications & Email | P1 | S | 0.5–1.5 meses | 1–3 |
| E15 | Chat IA grounded | P1 | L | 2–3.5 meses | 3 |
| E16 | AI Orchestrator / Guards / Eval | P0 | L | 2–3.5 meses | 3 |
| E17 | Timeline / Progress / Certifications | P2 | M | 1.5–3 meses | 3 |
| E18 | Procurement light / POs | P2 | M | 1.5–2.5 meses | 4 prep |
| E19 | Plugin Host & Module SDK | P2 | XL | 3–5 meses | 4 |
| E20 | Domain Plugins packs | P2 | L | 3–6 meses | 4 |
| E21 | Marketplace | P3 | XL | 4–7 meses | 4 |
| E22 | Enterprise | P2 | XL | 6–12 meses | 5 |
| E23 | Public API & Integrations | P2 | L | 2–4 meses | 5 |
| E24 | Data Platform / Analytics | P3 | L | 3–5 meses | 5+ |
| E25 | Mobile Site Ops | P3 | L | 4–7 meses | 5+ |

### E01 Platform Foundations & Observability

**Objetivo.** Establecer cimientos de plataforma: logging estructurado, tracing distribuido, métricas, health/ready, config, feature flags, CI quality gates y runbooks mínimos para operar el wedge sin cajas negras.

**Problema que resuelve.** Sin observabilidad y gates, perception/jobs fallan en silencio y los releases no son seguros para LATAM productivo.

**Beneficio.** MTTR bajo, releases con evidencia, base transversal para todas las épicas posteriores.

**Dependencias (epic IDs).** — (fundación)

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Over-instrumentation prematura | SLIs mínimos por clase; expandir con dolor medido |
| Arch | Acoplar app a vendor APM | OpenTelemetry como abstracción |
| Perf | Sampling inadecuado | Tail-based + muestreo tenant-aware |
| Scale | Cardinality explosion en labels | Allowlist estricta de labels |
| Commercial | Retrasar wedge por plataforma perfecta | Cap ≤20% capacidad del equipo en E01 |

**Complejidad:** M  |  **Prioridad:** P0  |  **Tiempo estimado:** 1–2 meses (1–2 eng)

**Arquitectura involucrada.** Etapa 1 cimientos; transversal a API, workers y Studio

**Módulos/dominios afectados.**
- Platform
- API Gateway
- Workers
- Frontend Studio
- Settings

**Eventos nuevos / relevantes.**
- SettingsActualizados
- UsoRegistrado (meter platform opcional)

**Entidades nuevas / relevantes.**
- FeatureFlag
- ReleaseMarker
- HealthCheckRecord
- SliSnapshot

**API (conceptual).**
- GET /health
- GET /ready
- GET /metrics (internal)
- GET/PATCH /v1/admin/flags

**Pantallas.**
- Admin flags (internal)
- Banner de degradación en Studio

**Base de datos (logical stores).**
- OLTP config/flags
- Metrics TSDB externo
- Log sink

**Tests necesarios.**
- CI lint/type/unit floors
- Otel smoke
- Flag evaluation
- Tenant label injection

**Migraciones.**
- feature_flags
- índices audit mínimos

**Criterio de Done.** Dashboards core vivos; trace_id en request→job; flags con audit; CI bloquea P0 debt; runbook health/DLQ publicado.

**Features contenidas (detalle en §3):** E01-F01 Observabilidad base (logs/traces/metrics), E01-F02 Health, readiness y degradación, E01-F03 Feature flags & config dinámica, E01-F04 CI quality gates & engineering standards, E01-F05 Runbooks y operabilidad inicial

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E01.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E01.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E02 Identity, Tenancy & Billing hardening

**Objetivo.** Endurecer Identity/Membership/Org, aislamiento tenant, sesiones, roles base y meters/entitlements Free/Pro/Enterprise sin fork de código.

**Problema que resuelve.** AuthZ inconsistente y billing frágil impiden vender Pro y exponen riesgo cross-tenant.

**Beneficio.** Base segura multi-tenant + monetización medible alineada a arquitectura.

**Dependencias (epic IDs).** E01

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Roles ad-hoc en frontend | AuthZ server-side obligatoria en dominio |
| Arch | Billing acoplado a UI | Billing domain + eventos de uso |
| Perf | Checks AuthZ caros | Cache membership con invalidación por evento |
| Scale | Orgs grandes | Paginación memberships + búsqueda |
| Commercial | Upgrade path confuso | Entitlements claros + UX plan |

**Complejidad:** L  |  **Prioridad:** P0  |  **Tiempo estimado:** 1.5–3 meses (1–2 eng)

**Arquitectura involucrada.** Dominios Identity + Billing; tenancy §1.13 arquitectura

**Módulos/dominios afectados.**
- Identity
- Billing
- Projects
- Settings
- Audit

**Eventos nuevos / relevantes.**
- UsuarioRegistrado
- UsuarioInvitado
- MiembroRolCambiado
- SuscripcionCambiada
- UsoRegistrado
- UsoConsumido
- QuotaUmbralAlcanzado
- PagoFallido

**Entidades nuevas / relevantes.**
- Organization
- User
- Membership
- Session
- PlanEntitlement
- UsageMeter
- InvoiceRef

**API (conceptual).**
- POST /v1/auth/*
- CRUD /v1/orgs
- CRUD /v1/memberships
- GET /v1/billing/entitlements
- GET /v1/billing/usage

**Pantallas.**
- Login/Registro
- Invitaciones
- Org settings
- Plan & usage
- Upgrade Pro

**Base de datos (logical stores).**
- OLTP identity/billing
- Append-only usage_events

**Tests necesarios.**
- AuthN/AuthZ matrix
- Tenant isolation suite
- Meter idempotency
- Plan matrix smoke

**Migraciones.**
- org.plan
- usage_events
- entitlements seed Free/Pro/Enterprise

**Criterio de Done.** Aislamiento CI verde; meters registran upload/AI/export; upgrade Free→Pro sin downtime; roles base en API.

**Features contenidas (detalle en §3):** E02-F01 AuthN sesiones y recuperación, E02-F02 Organizations & memberships, E02-F03 Entitlements Free/Pro/Enterprise, E02-F04 Usage meters & quotas, E02-F05 Billing provider integration light, E02-F06 Audit identity actions

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E02.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E02.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E03 Media & Object Storage

**Objetivo.** Pipeline robusto de upload, object storage por tenant, derivados, checksums, retención y eventos de medios.

**Problema que resuelve.** Planos/PDFs son el input del wedge; storage frágil rompe perception y confianza.

**Beneficio.** Ingestión confiable e aislada; base para L1.

**Dependencias (epic IDs).** E01, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Uploads grandes fallan | Multipart + resume |
| Arch | URLs firmadas mal scoped | Prefijo org/project + TTL corto |
| Perf | Derivados bloquean request | Job async DerivadoGenerado |
| Scale | Costos de storage | Lifecycle + retención |
| Commercial | Límites Free poco claros | Quotas en entitlements |

**Complejidad:** M  |  **Prioridad:** P0  |  **Tiempo estimado:** 1–2 meses (1 eng)

**Arquitectura involucrada.** Dominio Media; almacenamiento §9

**Módulos/dominios afectados.**
- Media
- Projects
- Billing
- Notifications

**Eventos nuevos / relevantes.**
- PlanoSubido
- MediaAssetListo
- DerivadoGenerado
- MediaRetencionAplicada

**Entidades nuevas / relevantes.**
- MediaAsset
- MediaDerivative
- UploadSession
- RetentionPolicy

**API (conceptual).**
- POST .../media/upload-url
- POST .../media/complete
- GET /v1/media/{id}
- DELETE soft

**Pantallas.**
- Uploader con progreso
- Galería de planos
- Errores de cuota

**Base de datos (logical stores).**
- OLTP media metadata
- Object store
- Derivatives

**Tests necesarios.**
- Checksum
- Tenant key isolation
- Quota enforcement
- MIME sniff

**Migraciones.**
- media_assets
- derivatives
- upload_sessions

**Criterio de Done.** Upload→evento→listo observable; soft-delete; quotas Free; signed URLs scoped; retention dry-run.

**Features contenidas (detalle en §3):** E03-F01 Upload sessions & signed URLs, E03-F02 Derivatives pipeline, E03-F03 MediaAsset lifecycle & retention, E03-F04 Security & malware light

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E03.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E03.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E04 Async Jobs & Event Bus (Outbox)

**Objetivo.** Jobs API, colas por clase, outbox, idempotencia, DLQ, progreso WS y semántica de entrega para desacoplar L1/L2.

**Problema que resuelve.** CV/OCR/reportes síncronos en HTTP no escalan ni son confiables.

**Beneficio.** Extensibilidad event-driven real; hito Etapa 1.

**Dependencias (epic IDs).** E01, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Dual-write sin outbox | Outbox obligatorio |
| Arch | Bus como RPC | Eventos de hecho + envelope estándar |
| Perf | Poison messages | DLQ + circuit break |
| Scale | Noisy neighbor | Fairness multi-tenant |
| Commercial | Jobs stuck sin UX | WS progress + timeouts |

**Complejidad:** L  |  **Prioridad:** P0  |  **Tiempo estimado:** 1.5–3 meses (1–2 eng)

**Arquitectura involucrada.** Eventing §5; Colas §8; Etapa 1

**Módulos/dominios afectados.**
- Platform Jobs
- Outbox
- WS gateway
- Producers/Consumers

**Eventos nuevos / relevantes.**
- job.progress
- job.completed
- job.failed
- eventos dominio vía envelope

**Entidades nuevas / relevantes.**
- Job
- JobAttempt
- OutboxMessage
- DeadLetter
- ConsumerCheckpoint

**API (conceptual).**
- POST /v1/jobs
- GET /v1/jobs/{id}
- POST /v1/jobs/{id}/cancel
- WS project channel

**Pantallas.**
- Job tray / toasts
- Admin DLQ internal

**Base de datos (logical stores).**
- OLTP jobs+outbox
- Queue broker

**Tests necesarios.**
- Outbox atomicity
- Idempotent consumer
- Retry/DLQ
- Cancel
- Ordering

**Migraciones.**
- jobs
- outbox
- dlq
- checkpoints

**Criterio de Done.** Flujo async observable; DLQ runbook; idempotencia demostrada; WS progress en Studio.

**Features contenidas (detalle en §3):** E04-F01 Jobs API & state machine, E04-F02 Outbox pattern, E04-F03 Queues, retries, DLQ, fairness, E04-F04 WebSocket progress & presence light, E04-F05 Event envelope & schema registry light

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E04.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E04.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E05 Perception Engine (CV/OCR) modernization

**Objetivo.** Modernizar L1: pipeline versionado ingest→normalize→OCR→color segmentation→symbol assist→evidence pack; nunca calcular costos.

**Problema que resuelve.** Percepción no versionada o acoplada impide replay, provenance y evolución segura del wedge.

**Beneficio.** Evidencias tipadas confiables para color→tipología→cantidades.

**Dependencias (epic IDs).** E03, E04

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Nondeterminism / model drift | pipeline_version + golden fixtures LATAM |
| Arch | Perception escribe costos | Prohibido; solo Evidence/ColorRegion |
| Perf | Costo CPU/GPU | Cola dedicada + quotas plan |
| Scale | Picos de upload | Fairness + backpressure |
| Commercial | Scans LATAM de baja calidad | Confidence UI + mapping humano |

**Complejidad:** XL  |  **Prioridad:** P0  |  **Tiempo estimado:** 2–4 meses (1–3 eng)

**Arquitectura involucrada.** L1 Perception; Etapa 1

**Módulos/dominios afectados.**
- Vision/Perception
- Media
- Billing
- MDO evidence attach

**Eventos nuevos / relevantes.**
- PercepcionIniciada
- PlanoProcesado
- PercepcionFallida
- EvidenciaCreada
- ColorMapActualizado

**Entidades nuevas / relevantes.**
- PerceptionJob
- Evidence
- ColorRegion
- OcrBlock
- PipelineVersion

**API (conceptual).**
- POST /v1/perception/jobs
- GET evidences
- PATCH color-map
- GET pipeline-versions

**Pantallas.**
- Overlay evidencias
- Color→tipología mapper
- Confidence heatmap

**Base de datos (logical stores).**
- OLTP perception
- Blob masks/features
- Object store

**Tests necesarios.**
- Golden planos LATAM
- Determinism replay
- No cost side-effects
- Failure taxonomy

**Migraciones.**
- evidences
- color_regions
- perception_jobs

**Criterio de Done.** Evidence pack + confidence; color map UX; replay por pipeline_version; eventos listos para Geometry.

**Features contenidas (detalle en §3):** E05-F01 Pipeline versioning & job orchestration, E05-F02 Normalize + OCR, E05-F03 Color segmentation (wedge crítico), E05-F04 Symbol assist & evidence pack, E05-F05 Replay, golden sets & quality gates

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E05.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E05.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E06 Geometry Engine

**Objetivo.** Motor determinista de medición/topología: calibración de escala, L/A/V/conteos, validadores; escribe solo vía ChangeSets.

**Problema que resuelve.** Sin geometría autoritativa las cantidades no son ingeniería auditable.

**Beneficio.** Medidas confiables; base dura del twin L2 (Etapa 2).

**Dependencias (epic IDs).** E05, E07

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Escala mal calibrada | UX calibración + blockers de compute |
| Arch | Mutación silenciosa MDO | Solo ChangeSet/ChangeOp |
| Perf | Polígonos pesados | Jobs + spatial index |
| Scale | Multi-sheet | Incremental por sheet |
| Commercial | UX difícil | Calibración guiada < 2 minutos |

**Complejidad:** XL  |  **Prioridad:** P0  |  **Tiempo estimado:** 2–4 meses (1–2 eng)

**Arquitectura involucrada.** Geometry domain; Etapa 2

**Módulos/dominios afectados.**
- Geometry
- Construction/MDO
- Perception
- Frontend canvas

**Eventos nuevos / relevantes.**
- CalibracionActualizada
- GeometriaCalculada
- GeometriaInvalidaDetectada
- ModeloActualizado

**Entidades nuevas / relevantes.**
- ElementGeometry
- Calibration
- GeometryIssue
- MeasureSet

**API (conceptual).**
- POST calibrate
- POST compute-geometry
- GET issues
- GET measures

**Pantallas.**
- Calibration tool
- Geometry issues panel
- Measure inspector

**Base de datos (logical stores).**
- OLTP geometry refs
- Blob geom payloads
- Issues

**Tests necesarios.**
- Unit measures
- Polygon close
- Scale absence
- Golden sheets

**Migraciones.**
- element_geometries
- calibrations
- geometry_issues

**Criterio de Done.** Compute→ChangeOps; issues visibles; golden verde; cero path LLM→geometry.

**Features contenidas (detalle en §3):** E06-F01 Calibration de escala, E06-F02 Compute measures determinista, E06-F03 Validators & GeometryIssue, E06-F04 Spatial relations light, E06-F05 Integration contract con MDO

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E06.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E06.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E07 MDO Core (entities, versions, changesets)

**Objetivo.** Implementar MDO como SoT: grafo espacial/sistemas/elementos, ProjectVersion, ChangeSet/ChangeOp, proyecciones y lineage.

**Problema que resuelve.** Sin twin versionado el producto permanece file-centric y bloquea escenarios e IA grounded.

**Beneficio.** Source of truth estable; habilita Etapas 1–3.

**Dependencias (epic IDs).** E01, E02, E04

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Schema incompleto eterno | Cerrar MDO schema v1 + evolve |
| Arch | God aggregate | Entidades + ChangeOps acotados |
| Perf | Proyecciones stale | Invalidación event-driven |
| Scale | Explosión de versions | Snapshots lógicos + diffs |
| Commercial | Migración mental usuario | Wedge sobre MDO sin romper UX |

**Complejidad:** XL  |  **Prioridad:** P0  |  **Tiempo estimado:** 2–5 meses (1–3 eng)

**Arquitectura involucrada.** MDO §2; Construction; Etapa 1

**Módulos/dominios afectados.**
- Construction/MDO
- Projects
- Scenarios mínimo
- Projections

**Eventos nuevos / relevantes.**
- ModeloActualizado
- ElementoCreado
- ElementoTipificado
- EspacioActualizado
- ProyeccionInvalidada
- ChangeSetCreado
- ChangeSetConfirmado

**Entidades nuevas / relevantes.**
- Site
- Building
- Level
- Space
- System
- Element
- ProjectVersion
- ChangeSet
- ChangeOp
- Connection
- ParameterSet

**API (conceptual).**
- CRUD entidades scoped
- POST changesets
- GET version tree
- GET projections

**Pantallas.**
- Model Explorer
- Inspector
- Version badge

**Base de datos (logical stores).**
- OLTP graph
- Doc payloads
- Projection cache

**Tests necesarios.**
- ChangeSet apply
- Version immutability
- Tenant isolation
- Projection rebuild

**Migraciones.**
- mdo core
- versions
- changesets
- projections

**Criterio de Done.** Wedge sobre ProjectVersion; versions inmutables al cerrar; lineage evidence→element; AuthZ API.

**Features contenidas (detalle en §3):** E07-F01 MDO schema v1 entities, E07-F02 ProjectVersion lifecycle, E07-F03 ChangeSet / ChangeOp engine, E07-F04 Projections materializadas, E07-F05 Strangler: wedge escribe a MDO, E07-F06 Quality flags & provenance on entities

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E07.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E07.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E08 Materials Engine

**Objetivo.** Fórmulas versionadas tipología→takeoff determinista con waste, overrides auditados y provenance completa.

**Problema que resuelve.** Cantidades ad-hoc no escalan ni son auditables; bloquean plugins tipológicos.

**Beneficio.** Takeoff reproducible; contrato estable para Costs y plugins.

**Dependencias (epic IDs).** E06, E07

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | DSL demasiado poderoso | Sandbox de expresiones limitado |
| Arch | Materials lee Perception | Solo geometría tipada MDO |
| Perf | Recalc full lento | Incremental por ChangeSet |
| Scale | Catálogo grande | Índices + lazy |
| Commercial | Edge LATAM | Overrides + feedback |

**Complejidad:** L  |  **Prioridad:** P0  |  **Tiempo estimado:** 1.5–3 meses (1–2 eng)

**Arquitectura involucrada.** Materials; Etapa 2

**Módulos/dominios afectados.**
- Materials
- MDO
- Plugins contracts
- Costs

**Eventos nuevos / relevantes.**
- MaterialCalculado
- TakeoffOverrideAplicado
- FormulaVersionPublicada
- TipologiaMapeada

**Entidades nuevas / relevantes.**
- Typology
- Formula
- TakeoffLine
- MaterialCatalogItem
- WasteFactor
- TakeoffOverride

**API (conceptual).**
- POST materials/compute
- GET takeoff
- POST override
- CRUD formulas admin

**Pantallas.**
- Takeoff table
- Override modal
- Typology mapper

**Base de datos (logical stores).**
- OLTP takeoff
- Formulas
- Catalog

**Tests necesarios.**
- Formula golden
- Override audit
- Incremental
- Units

**Migraciones.**
- typologies seed
- formulas
- takeoff_lines

**Criterio de Done.** Color→typology→formula→TakeoffLine con provenance; overrides HITL; MaterialCalculado emitido.

**Features contenidas (detalle en §3):** E08-F01 Typology & catalog core LATAM, E08-F02 Formula engine versionado, E08-F03 Takeoff compute & lines, E08-F04 Overrides HITL, E08-F05 Plugin-ready formula contracts

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E08.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E08.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E09 Costs & PriceBooks

**Objetivo.** Valorizar takeoff con PriceBooks, moneda local, ajustes y totales por version/scenario.

**Problema que resuelve.** Sin costos locales confiables el wedge comercial no cierra venta.

**Beneficio.** Presupuesto en moneda del proyecto; base SignedBudget y Pro.

**Dependencias (epic IDs).** E08, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | FX/multimoneda | CurrencyRate as_of + freeze on sign |
| Arch | Costs←Perception | Solo TakeoffLine |
| Perf | Recalc | Incremental + cache totals |
| Scale | Pricebooks grandes | Import async |
| Commercial | Precios viejos | source metadata + import |

**Complejidad:** L  |  **Prioridad:** P0  |  **Tiempo estimado:** 1.5–3 meses (1–2 eng)

**Arquitectura involucrada.** Costs; LATAM-first; Etapa 2

**Módulos/dominios afectados.**
- Costs
- Materials
- Billing
- Reports

**Eventos nuevos / relevantes.**
- CostoActualizado
- PresupuestoCreado
- PricebookActualizado
- CurrencyRatesActualizadas

**Entidades nuevas / relevantes.**
- Pricebook
- PriceItem
- Budget
- BudgetLine
- CurrencyRate

**API (conceptual).**
- CRUD pricebooks
- POST budgets/compute
- GET budgets/{id}
- POST currency-rates

**Pantallas.**
- Pricebook editor
- Budget summary
- Currency settings

**Base de datos (logical stores).**
- OLTP costs
- Pricebooks

**Tests necesarios.**
- Decimal money
- FX freeze
- Recompute
- Plan limits

**Migraciones.**
- pricebooks
- budgets
- currency_rates

**Criterio de Done.** Budget total en Project.currency; CostoActualizado; precision tests; pricebook org/project.

**Features contenidas (detalle en §3):** E09-F01 Pricebook management, E09-F02 Currency & FX, E09-F03 Budget compute, E09-F04 Plan gates on costs features

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E09.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E09.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E10 Takeoff Projections & Signed Budgets

**Objetivo.** Proyecciones de takeoff/costo estables y SignedBudget inmutable con hash, HITL y lineage comercial.

**Problema que resuelve.** Sin cierre firmado no hay hecho comercial auditable ni confianza de cobro/entrega.

**Beneficio.** Cierre del wedge comercial; base certificaciones y compliance.

**Dependencias (epic IDs).** E09, E07

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Snapshot incompleto | Freeze takeoff+prices+FX+versions |
| Arch | Mutar budget firmado | Inmutabilidad enforce + tests |
| Perf | Snapshots pesados | Object store + hash |
| Scale | Muchos signs | Retención política |
| Commercial | Firma UX fricción | Flujo corto + roles claros |

**Complejidad:** M  |  **Prioridad:** P0  |  **Tiempo estimado:** 1–2 meses (1 eng)

**Arquitectura involucrada.** Costs + Audit; hechos comerciales inmutables

**Módulos/dominios afectados.**
- Costs
- Reports
- Audit
- Notifications

**Eventos nuevos / relevantes.**
- PresupuestoFirmado
- ProyeccionInvalidada

**Entidades nuevas / relevantes.**
- SignedBudget
- TakeoffProjection
- CostProjection
- SignatureMeta

**API (conceptual).**
- POST budgets/{id}/sign
- GET signed/{id}
- GET projections/takeoff|cost

**Pantallas.**
- Sign budget wizard
- Signed vault read-only
- Projection views

**Base de datos (logical stores).**
- OLTP signed refs
- Immutable snapshot blobs
- Projections

**Tests necesarios.**
- Immutability
- Hash verify
- AuthZ sign roles
- Projection consistency

**Migraciones.**
- signed_budgets
- projection tables harden

**Criterio de Done.** Sign crea snapshot+hash; no mutate; evento PresupuestoFirmado; proyección takeoff estable post-sign.

**Features contenidas (detalle en §3):** E10-F01 Takeoff/Cost projections API, E10-F02 SignedBudget HITL, E10-F03 Commercial audit trail

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E10.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E10.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E11 Scenarios (Git-like)

**Objetivo.** Branching Git-like del MDO: Scenario, compare, merge rules básicas, promote baseline; sin romper baseline de producción.

**Problema que resuelve.** Sin escenarios no hay alternativas de cómputo/costo controladas (Etapa 2).

**Beneficio.** Explorar opciones con lineage; upsell Pro.

**Dependencias (epic IDs).** E07, E08, E09

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Merge conflicts complejos | MVP compare+promote; merge limitado |
| Arch | Scenario como copia full pesada | Versions + diffs |
| Perf | Compare lento | Projections diff |
| Scale | Branches zombie | Soft-delete + límites plan |
| Commercial | Confusión UX | Metáfora Git suave para constructores |

**Complejidad:** L  |  **Prioridad:** P1  |  **Tiempo estimado:** 2–3 meses (1–2 eng)

**Arquitectura involucrada.** Scenarios §12; Etapa 2

**Módulos/dominios afectados.**
- Scenarios
- MDO
- Materials
- Costs
- Frontend

**Eventos nuevos / relevantes.**
- EscenarioCreado
- EscenarioMerged
- EscenarioPromovido
- EscenarioEliminado
- ConflictoDetectado

**Entidades nuevas / relevantes.**
- Scenario
- ScenarioCompare
- MergeConflict

**API (conceptual).**
- POST scenarios
- POST compare
- POST merge
- POST promote
- DELETE soft

**Pantallas.**
- Scenario switcher
- Compare view
- Conflict resolver MVP

**Base de datos (logical stores).**
- OLTP scenarios
- Compare cache

**Tests necesarios.**
- Branch isolation
- Promote rules
- Plan limits
- No baseline corrupt

**Migraciones.**
- scenarios
- compare_jobs

**Criterio de Done.** Crear branch, compute takeoff/cost aislado, compare, promote con AuthZ; Free limit branches.

**Features contenidas (detalle en §3):** E11-F01 Scenario CRUD & head versions, E11-F02 Compare takeoff/cost, E11-F03 Merge MVP & conflicts, E11-F04 Promote to baseline

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E11.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E11.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E12 Frontend Workspace & Model Explorer

**Objetivo.** Studio multi-panel: canvas plano, árbol MDO, inspector, costos, jobs; i18n ES; flags por plan; sin cards innecesarias — preservar motion del wedge.

**Problema que resuelve.** Backend MDO sin workspace cohesivo no convierte ni retiene.

**Beneficio.** UX unificada sobre twin; base chat/reports panels.

**Dependencias (epic IDs).** E05, E07, E08, E09, E04

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Estado UI duplica MDO | Server SoT; UI cache descartable |
| Arch | BFF god | BFF solo agrega proyecciones |
| Perf | Bundle/TTI | Code-split panels |
| Scale | Proyectos grandes tree | Virtualización |
| Commercial | UX regresa a file-centric | Version badge siempre visible |

**Complejidad:** L  |  **Prioridad:** P0  |  **Tiempo estimado:** 2–4 meses (1–2 eng)

**Arquitectura involucrada.** Frontend Studio; BFF opcional

**Módulos/dominios afectados.**
- Frontend
- BFF
- All read models

**Eventos nuevos / relevantes.**
- (consume) job.*, ModeloActualizado, CostoActualizado

**Entidades nuevas / relevantes.**
- UiPreference
- WorkspaceLayout

**API (conceptual).**
- Read projections
- WS
- PATCH settings UI

**Pantallas.**
- Workspace shell
- Canvas
- Explorer
- Inspector
- Budget panel
- Jobs

**Base de datos (logical stores).**
- OLTP ui prefs
- client cache

**Tests necesarios.**
- E2E wedge
- a11y critical
- Plan flag UI
- Visual smoke

**Migraciones.**
- ui_preferences

**Criterio de Done.** Flujo wedge completo en Studio sobre MDO; progress jobs; explorer navega entidades; no inventa datos.

**Features contenidas (detalle en §3):** E12-F01 Workspace shell & layout, E12-F02 Canvas plano + overlays, E12-F03 Model Explorer & Inspector, E12-F04 Takeoff & Budget panels, E12-F05 Jobs tray & notifications UI

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E12.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E12.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E13 Reports (PDF/Excel) & Exports

**Objetivo.** Generación async de reportes PDF/Excel desde proyecciones MDO/costos con lineage; meters por plan.

**Problema que resuelve.** Sin exports confiables el cierre comercial y entrega a cliente final se frena.

**Beneficio.** Artefactos compartibles; upsell Pro; base certificación docs.

**Dependencias (epic IDs).** E10, E04, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Templates frágiles | Fixtures + visual/pdf hash tests |
| Arch | Report lee DB alien | Solo projections/APIs |
| Perf | PDF grandes | Cola reports + timeouts |
| Scale | Abuse Free | Quotas |
| Commercial | Brand weak en PDF | Template LATAM marca ARQ-IA |

**Complejidad:** M  |  **Prioridad:** P1  |  **Tiempo estimado:** 1.5–2.5 meses (1 eng)

**Arquitectura involucrada.** Reports domain; Etapa 3

**Módulos/dominios afectados.**
- Reports
- Costs
- Materials
- Media
- Billing

**Eventos nuevos / relevantes.**
- ReporteSolicitado
- ReporteGenerado
- ReporteFallido

**Entidades nuevas / relevantes.**
- ReportJob
- ReportArtifact
- ReportTemplate

**API (conceptual).**
- POST reports
- GET report jobs
- GET artifact url

**Pantallas.**
- Report picker
- History artifacts

**Base de datos (logical stores).**
- OLTP report jobs
- Object store artifacts

**Tests necesarios.**
- Golden PDF/XLSX subset
- Quota
- Tenant isolation artifacts
- Citation of version ids

**Migraciones.**
- report_jobs
- templates seed

**Criterio de Done.** Export takeoff+budget async; artifact signed URL; meters; version_id impreso; Free limits.

**Features contenidas (detalle en §3):** E13-F01 Report job pipeline, E13-F02 PDF budget/takeoff, E13-F03 Excel exports, E13-F04 Entitlements & abuse controls

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E13.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E13.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E14 Notifications & Email

**Objetivo.** Notificaciones in-app + email para jobs, invitaciones, firmas, cuotas; preferencias usuario; sin spam.

**Problema que resuelve.** Usuarios no se enteran de fallos/completions → soporte y churn.

**Beneficio.** Cierre de loops operativos; mejor activación.

**Dependencias (epic IDs).** E02, E04

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Duplicados | Idempotency keys notif |
| Arch | Emails con datos sensibles | Minimize payload + AuthZ links |
| Perf | Burst | Queue notify + batch |
| Scale | Provider limits | Backoff |
| Commercial | Spam | Preferences + digests |

**Complejidad:** S  |  **Prioridad:** P1  |  **Tiempo estimado:** 0.5–1.5 meses (1 eng)

**Arquitectura involucrada.** Notifications domain

**Módulos/dominios afectados.**
- Notifications
- Identity
- Billing
- Jobs

**Eventos nuevos / relevantes.**
- NotificacionEnviada
- NotificacionFallida

**Entidades nuevas / relevantes.**
- Notification
- NotificationPreference
- EmailDelivery

**API (conceptual).**
- GET notifications
- POST mark-read
- PATCH preferences

**Pantallas.**
- Bell tray
- Preferences

**Base de datos (logical stores).**
- OLTP notifications
- Email provider

**Tests necesarios.**
- Idempotency
- Preference respect
- Tenant links
- Template i18n

**Migraciones.**
- notifications
- preferences

**Criterio de Done.** In-app+email para job fail/complete, invite, quota, signed budget; prefs; métricas delivery.

**Features contenidas (detalle en §3):** E14-F01 In-app notifications, E14-F02 Email templates ES, E14-F03 Preferences & digests

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E14.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E14.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E15 Chat IA grounded

**Objetivo.** Chat de proyecto con retrieval + tools read-only sobre MDO/proyecciones, citas obligatorias, memoria acotada, streaming UX.

**Problema que resuelve.** Chat sin grounding alucina cantidades y destruye confianza comercial.

**Beneficio.** Asistencia útil Etapa 3; diferenciación Pro sin romper SoT.

**Dependencias (epic IDs).** E16, E07, E10, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Alucinaciones | Guards E16 + refuse |
| Arch | Chat escribe geometría | Tools read-only + AIProposal HITL |
| Perf | Latencia/tokens | Cache retrieval + quotas |
| Scale | Costo Free abuse | Hard meters |
| Commercial | Overpromise IA | Copy UX honesto |

**Complejidad:** L  |  **Prioridad:** P1  |  **Tiempo estimado:** 2–3.5 meses (1–2 eng)

**Arquitectura involucrada.** Chat §11; L3; Etapa 3

**Módulos/dominios afectados.**
- Chat
- AI
- MDO projections
- Billing
- Frontend

**Eventos nuevos / relevantes.**
- ChatIniciado
- MensajeChatRegistrado
- ChatRespuestaUsadaEnDoc

**Entidades nuevas / relevantes.**
- ChatThread
- ChatMessage
- ChatCitation
- ChatMemorySlice

**API (conceptual).**
- POST threads/messages
- GET history
- WS/SSE stream

**Pantallas.**
- Chat panel
- Citation preview
- Insert-to-doc confirm

**Base de datos (logical stores).**
- OLTP chat
- Vector index embeddings
- Object optional

**Tests necesarios.**
- Refuse without citation
- Tool allowlist
- Tenant isolation threads
- Quota

**Migraciones.**
- chat_threads
- messages
- embeddings refs

**Criterio de Done.** Chat responde con citas a version/entities; no write autoritativo; meters; evento uso en doc.

**Features contenidas (detalle en §3):** E15-F01 Threads & messages, E15-F02 Context assembly & retrieval UX, E15-F03 Insert to doc / commercial use, E15-F04 Memory & multi-user light

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E15.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E15.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E16 AI Orchestrator / Guards / Eval

**Objetivo.** Orquestador L3, tools read-only, policy guards (citation, no-geometry-write), AIProposal HITL, eval de alucinaciones, quotas.

**Problema que resuelve.** Sin guards la IA puede contaminar el twin o afirmar costos inventados.

**Beneficio.** IA segura y medible; habilita Chat y propuestas.

**Dependencias (epic IDs).** E07, E10, E02, E04

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Guard bypass | Defense in depth + tests red team |
| Arch | LLM escribe stores | Allowlist tools + repo writes solo proposal |
| Perf | Eval flaky | Golden prompts estables |
| Scale | Costo tokens | Cache + plan limits |
| Commercial | Ship chat before guards | E16 antes o junto a E15 hard gate |

**Complejidad:** L  |  **Prioridad:** P0  |  **Tiempo estimado:** 2–3.5 meses (1–2 eng)

**Arquitectura involucrada.** AI §10; Etapa 3; anti-alucinación

**Módulos/dominios afectados.**
- AI Orchestrator
- Policy
- Eval
- Embeddings
- Billing

**Eventos nuevos / relevantes.**
- AIProposalCreada
- AIProposalResuelta
- EmbeddingsActualizados
- AIQuotaExcedida

**Entidades nuevas / relevantes.**
- AIProposal
- ToolCallLog
- EvalCase
- EmbeddingChunk
- PolicyDecision

**API (conceptual).**
- POST ai/propose
- POST ai/complete (internal)
- GET proposals
- POST proposals/{id}/resolve

**Pantallas.**
- Proposal review
- Admin eval dashboard internal

**Base de datos (logical stores).**
- OLTP proposals
- Vector index
- Eval fixtures store

**Tests necesarios.**
- Refuse-without-citation
- Tool allowlist
- No geometry tool
- Eval CI subset

**Migraciones.**
- ai_proposals
- embeddings
- eval_cases

**Criterio de Done.** Guards en path; proposals HITL; eval nightly; quotas; cero write autoritativo desde LLM.

**Features contenidas (detalle en §3):** E16-F01 Orchestrator & tool allowlist, E16-F02 Policy guards, E16-F03 AIProposal HITL, E16-F04 Embeddings index, E16-F05 Eval service & quotas

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E16.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E16.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E17 Timeline / Progress / Certifications

**Objetivo.** Hitos, secuencia constructiva ligera y certificaciones inmutables ligadas a snapshots del twin.

**Problema que resuelve.** Sin timeline/certificaciones el producto no acompaña ejecución ni cierres de periodo.

**Beneficio.** Puente estudio→obra; hecho comercial adicional; Enterprise readiness.

**Dependencias (epic IDs).** E07, E10, E13

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Certificación sin freeze correcto | Reusar snapshot pattern SignedBudget |
| Arch | Timeline como Gantt completo prematuro | MVP hitos + links elementos |
| Perf | Snapshots frecuentes | On-demand + retención |
| Scale | Obra grande | Paginación hitos |
| Commercial | Scope creep scheduling | Anti-scope: no MS Project clone |

**Complejidad:** M  |  **Prioridad:** P2  |  **Tiempo estimado:** 1.5–3 meses (1 eng)

**Arquitectura involucrada.** Timeline domain; Etapa 3 parcial

**Módulos/dominios afectados.**
- Timeline
- MDO
- Reports
- Audit

**Eventos nuevos / relevantes.**
- HitoCreado
- SecuenciaActualizada
- CertificacionEmitida

**Entidades nuevas / relevantes.**
- Milestone
- WorkSequence
- Certification
- ProgressNote

**API (conceptual).**
- CRUD milestones
- PATCH sequence
- POST certifications/issue
- GET certifications

**Pantallas.**
- Timeline board
- Certification wizard
- Progress notes

**Base de datos (logical stores).**
- OLTP timeline
- Immutable cert snapshots

**Tests necesarios.**
- Cert immutability
- Link integrity
- AuthZ issue cert
- Plan gates

**Migraciones.**
- milestones
- sequences
- certifications

**Criterio de Done.** Hitos linkeados; emitir certificación con hash; UI read-only post-emisión; evento CertificacionEmitida.

**Features contenidas (detalle en §3):** E17-F01 Milestones & sequence MVP, E17-F02 Progress notes light, E17-F03 Certifications immutable

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E17.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E17.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E18 Procurement light / Purchase Orders

**Objetivo.** Órdenes de compra ligeras desde takeoff/budget lines, con aprobación HITL y estados básicos (no ERP completo).

**Problema que resuelve.** Constructores necesitan pasar de cantidades a pedido sin Excel paralelo eterno.

**Beneficio.** Extiende wedge hacia ejecución; puente a Marketplace E21.

**Dependencias (epic IDs).** E10, E09, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Estados PO complejos | MVP draft/submitted/approved/ordered/cancelled |
| Arch | ERP scope creep | Anti-scope lista dura |
| Perf | OK | N/A early |
| Scale | Integraciones proveedor | Manual first |
| Commercial | Marketplace confusion | PO local antes de marketplace |

**Complejidad:** M  |  **Prioridad:** P2  |  **Tiempo estimado:** 1.5–2.5 meses (1 eng)

**Arquitectura involucrada.** Procurement light; pre-Marketplace

**Módulos/dominios afectados.**
- Procurement
- Costs
- Notifications
- Audit

**Eventos nuevos / relevantes.**
- OrdenCompraCreada
- OrdenCompraAprobada
- OrdenCompraCancelada

**Entidades nuevas / relevantes.**
- PurchaseOrder
- PurchaseOrderLine
- Approval

**API (conceptual).**
- CRUD POs
- POST submit/approve/cancel
- GET from-budget

**Pantallas.**
- PO list/editor
- Approval queue

**Base de datos (logical stores).**
- OLTP procurement

**Tests necesarios.**
- HITL approve
- Line linkage takeoff
- Immutability after ordered
- AuthZ

**Migraciones.**
- purchase_orders
- po_lines

**Criterio de Done.** Crear PO desde budget lines; aprobar; cancelar; audit; sin inventar cantidades.

**Features contenidas (detalle en §3):** E18-F01 PO from budget lines, E18-F02 Approvals HITL, E18-F03 Cancel & export

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E18.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E18.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E19 Plugin Host & Module SDK

**Objetivo.** Host de plugins con manifest, capability contracts, sandbox, versionado e instalación org/project.

**Problema que resuelve.** Sin host, tipologías especializadas fuerzan forks del core.

**Beneficio.** Extensibilidad Etapa 4; base E20/E21.

**Dependencias (epic IDs).** E07, E08, E01, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Sandbox escape | Allowlist APIs + resource limits |
| Arch | Plugins write arbitrary MDO | Capability contracts only |
| Perf | Plugin lento | Timeouts + isolation |
| Scale | Compat matrix | Semver + CI compat tests |
| Commercial | SDK antes de demanda | 1–2 plugins first-party primero |

**Complejidad:** XL  |  **Prioridad:** P2  |  **Tiempo estimado:** 3–5 meses (1–2 eng)

**Arquitectura involucrada.** Plugins §13; Etapa 4

**Módulos/dominios afectados.**
- Plugins/Registry
- Materials contracts
- Billing entitlements
- Audit

**Eventos nuevos / relevantes.**
- PluginInstalado
- PluginActualizado
- PluginDeshabilitado
- PluginValidacionFallida

**Entidades nuevas / relevantes.**
- PluginManifest
- PluginInstallation
- PluginVersion
- CapabilityGrant

**API (conceptual).**
- POST plugins/install
- GET registry
- PATCH enable/disable
- GET manifests

**Pantallas.**
- Plugin manager
- Install wizard
- Permissions review

**Base de datos (logical stores).**
- OLTP registry
- Artifact store signed

**Tests necesarios.**
- Manifest schema
- Sandbox limits
- Tenant install isolation
- Disable kills execution

**Migraciones.**
- plugins
- installations
- grants

**Criterio de Done.** Instalar plugin first-party; ejecutar fórmula tipológica vía contract; disable seguro; eventos; entitlements.

**Features contenidas (detalle en §3):** E19-F01 Manifest & registry, E19-F02 Host runtime sandbox, E19-F03 Install lifecycle, E19-F04 SDK & sample plugin

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E19.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E19.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E20 Domain Plugins (Steel/HA/Gas/Fire/etc packs)

**Objetivo.** Empaquetar tipologías/fórmulas de disciplinas como plugins first-party: Steel Frame, Hormigón Armado, Gas, Fire, etc.

**Problema que resuelve.** Dominios especializados no deben inflar el core ni retrasar wedge.

**Beneficio.** Cobertura vertical sin fork; monetización packs Pro/Enterprise.

**Dependencias (epic IDs).** E19, E08, E09

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Fórmulas incorrectas dominio | Expert review + golden cases |
| Arch | Plugin depende de APIs inestables | Contracts versionados |
| Perf | Packs pesados | Lazy load |
| Scale | Muchos packs | Release trains |
| Commercial | Pack incompleto daña marca | Beta labeled + HITL |

**Complejidad:** L  |  **Prioridad:** P2  |  **Tiempo estimado:** 3–6 meses (1–2 eng, escalonado)

**Arquitectura involucrada.** Plugins tipológicos; Etapa 4

**Módulos/dominios afectados.**
- Domain packs
- Materials
- Costs mappings
- Docs

**Eventos nuevos / relevantes.**
- FormulaVersionPublicada (por pack)
- PluginInstalado

**Entidades nuevas / relevantes.**
- PackTypology set
- PackFormula set
- PackFixture

**API (conceptual).**
- (via plugin host)
- Admin pack publish internal

**Pantallas.**
- Pack marketplace cards later
- Pack config params

**Base de datos (logical stores).**
- Plugin artifacts
- Seed fixtures

**Tests necesarios.**
- Golden per pack
- Compat matrix
- No core hardcode

**Migraciones.**
- seed pack registry entries

**Criterio de Done.** ≥2 packs first-party instalables produciendo takeoff correcto en fixtures; docs; flags.

**Features contenidas (detalle en §3):** E20-F01 Steel Frame pack, E20-F02 Hormigón Armado pack, E20-F03 Gas pack, E20-F04 Fire / otras packs pipeline

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E20.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E20.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E21 Marketplace

**Objetivo.** Marketplace light: catálogo proveedores, cotizaciones, órdenes básicas, sync precios; solo después de MDO/PO estables.

**Problema que resuelve.** Demanda de compra integrada aparece tras wedge; hacerlo antes es prematuro (anti-pattern arquitectura).

**Beneficio.** Ecosistema y monetización Etapa 4; cierra loop cantidades→compra.

**Dependencias (epic IDs).** E18, E19, E09, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Integraciones frágiles | Provider adapter interface |
| Arch | Marketplace antes de MDO | Gate dependencia dura |
| Perf | Sync catálogos | Jobs + incremental |
| Scale | Ops proveedores | Onboarding limitado piloto |
| Commercial | Cold start suppliers | First-party curated LATAM |

**Complejidad:** XL  |  **Prioridad:** P3  |  **Tiempo estimado:** 4–7 meses (1–3 eng)

**Arquitectura involucrada.** Marketplace domain; Etapa 4

**Módulos/dominios afectados.**
- Marketplace
- Procurement
- Costs
- Billing
- Notifications

**Eventos nuevos / relevantes.**
- ProveedorSeleccionado
- CotizacionCreada
- CompraRealizada
- OrdenCancelada
- CatalogoProveedorSincronizado

**Entidades nuevas / relevantes.**
- Provider
- CatalogItem
- Quote
- MarketplaceOrder

**API (conceptual).**
- GET providers/catalog
- POST quotes
- POST orders
- POST sync

**Pantallas.**
- Catalog browse
- Quote compare
- Order status

**Base de datos (logical stores).**
- OLTP marketplace
- Synced catalog store

**Tests necesarios.**
- Order HITL
- Price sync integrity
- Tenant isolation
- Refund/cancel paths

**Migraciones.**
- providers
- catalogs
- quotes
- orders

**Criterio de Done.** Piloto con N proveedores; quote→order; evento CompraRealizada; entitlements; no alucinar stock/precios.

**Features contenidas (detalle en §3):** E21-F01 Provider & catalog sync, E21-F02 Quotes, E21-F03 Orders & payments light, E21-F04 Trust & compliance light

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E21.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E21.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E22 Enterprise (SSO, RBAC fine, multi-company, audit export, DR)

**Objetivo.** Capacidades Enterprise: SSO/SAML/OIDC, RBAC/ABAC fino, multi-company, audit export, retención/DR, residency options.

**Problema que resuelve.** Cuentas grandes LATAM no compran sin SSO, audit y controles finos.

**Beneficio.** Contratos Enterprise; Etapa 5.

**Dependencias (epic IDs).** E02, E01, E07, E10

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | SSO edge cases | Pilot IdP matrix |
| Arch | Over-compliance theater | Priorizar controles pedidos por pilots |
| Perf | AuthZ fino costoso | Caching + policy engine |
| Scale | Multi-region cost | DR warm standby opcional no multi-active early |
| Commercial | Custom forever | Packaging estándar + extras pagos |

**Complejidad:** XL  |  **Prioridad:** P2  |  **Tiempo estimado:** 6–12 meses incremental (1–3 eng)

**Arquitectura involucrada.** Enterprise §14; Etapa 5

**Módulos/dominios afectados.**
- Identity
- Audit
- Settings
- Platform
- Billing

**Eventos nuevos / relevantes.**
- MiembroRolCambiado (fine)
- PoliticaRetencionCambiada
- SuscripcionCambiada

**Entidades nuevas / relevantes.**
- OrgUnit
- Team
- RoleBinding
- SsoConnection
- LegalHold
- AuditExportJob

**API (conceptual).**
- SSO config
- RBAC admin
- POST audit/export
- DR status internal

**Pantallas.**
- Enterprise admin
- SSO setup
- Roles matrix
- Audit export

**Base de datos (logical stores).**
- OLTP enterprise
- Cold audit store
- Backup infra

**Tests necesarios.**
- SSO login
- ABAC denials
- Audit completeness sample
- Restore drill

**Migraciones.**
- org_units
- role_bindings
- sso_connections
- legal_holds

**Criterio de Done.** SSO piloto; roles finos en recursos críticos; audit export; restore drill documentado; multi-company básico.

**Features contenidas (detalle en §3):** E22-F01 SSO/SAML/OIDC, E22-F02 RBAC/ABAC fino, E22-F03 Audit export & legal hold, E22-F04 Multi-company & DR light

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E22.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E22.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E23 Public API & Integrations

**Objetivo.** API pública estable Pro/Enterprise, keys, webhooks, quotas, OpenAPI, integraciones contables light.

**Problema que resuelve.** Partners y Enterprise necesitan automatizar sin UI; sin esto hay churn a tools internas.

**Beneficio.** Plataforma integrable; Etapa 5 automation.

**Dependencias (epic IDs).** E07, E10, E02, E04

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Breaking changes | Versioning estricto + contract tests |
| Arch | API expone internals | Resources de dominio estables |
| Perf | Abuse | Quotas + rate limits |
| Scale | Webhook storms | Backoff + DLQ |
| Commercial | API Free abuse | Pro+ only |

**Complejidad:** L  |  **Prioridad:** P2  |  **Tiempo estimado:** 2–4 meses (1–2 eng)

**Arquitectura involucrada.** Public API §7.12; Etapa 5

**Módulos/dominios afectados.**
- API Gateway
- Identity keys
- Webhooks
- Docs

**Eventos nuevos / relevantes.**
- WebhookDelivery*
- UsoRegistrado (api)

**Entidades nuevas / relevantes.**
- ApiKey
- WebhookEndpoint
- WebhookDelivery

**API (conceptual).**
- /public/v1/* resources
- webhooks management

**Pantallas.**
- Developer portal light
- Keys & webhooks admin

**Base de datos (logical stores).**
- OLTP keys/webhooks
- Delivery logs

**Tests necesarios.**
- Contract OpenAPI
- Key authz
- Webhook signature
- Rate limits

**Migraciones.**
- api_keys
- webhook_endpoints
- deliveries

**Criterio de Done.** OpenAPI publicada; keys; webhooks eventos comerciales; quotas; portal mínimo.

**Features contenidas (detalle en §3):** E23-F01 API keys & public resources, E23-F02 Webhooks, E23-F03 Integrations accounting light

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E23.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E23.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E24 Data Platform / Analytics (later)

**Objetivo.** Warehouse analítico desacoplado de OLTP para product analytics y métricas de negocio; no confundir con audit legal.

**Problema que resuelve.** Analítica pesada sobre OLTP degrada twin y mezcla compliance con product metrics.

**Beneficio.** Decisiones de producto/negocio sin poner en riesgo OLTP (post Etapa 5 inicio).

**Dependencias (epic IDs).** E01, E04, E07, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | ETL fragile | Managed pipelines + contracts |
| Arch | Analytics como SoT | Prohibido; solo lecturas derivadas |
| Perf | CDC load | Incremental |
| Scale | Cost warehouse | Start narrow marts |
| Commercial | Vanity metrics | North-star wedge funnels |

**Complejidad:** L  |  **Prioridad:** P3  |  **Tiempo estimado:** 3–5 meses (1 eng) later

**Arquitectura involucrada.** Analytics fase; §6.10

**Módulos/dominios afectados.**
- Data platform
- Billing metrics
- Product analytics

**Eventos nuevos / relevantes.**
- (consume domain events to lake)

**Entidades nuevas / relevantes.**
- AnalyticsEvent
- MartWedgeFunnel
- MartQuality

**API (conceptual).**
- Internal BI only initially

**Pantallas.**
- Internal dashboards

**Base de datos (logical stores).**
- Lake/warehouse
- OLTP untouched

**Tests necesarios.**
- PII minimization
- Tenant aggregation rules
- Freshness

**Migraciones.**
- pipelines as code

**Criterio de Done.** Marts wedge funnel + quality + billing; acceso interno; lag documentado; no uso como SoT.

**Features contenidas (detalle en §3):** E24-F01 Event ingestion to lake, E24-F02 Marts wedge & quality, E24-F03 Self-serve later

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E24.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E24.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

### E25 Mobile Site Ops (later)

**Objetivo.** App móvil light para obra: progreso, fotos, hitos, consulta takeoff/presupuesto; offline-ish; no reemplaza Studio desktop.

**Problema que resuelve.** Campo no usa desktop; sin móvil la ejecución queda fuera del twin.

**Beneficio.** Adopción obra; datos de progreso al MDO; diferenciación late.

**Dependencias (epic IDs).** E12, E17, E03, E02

**Riesgos y mitigación.**

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Offline sync conflicts | Append notes first; limited edits |
| Arch | Mobile escribe geometría | Prohibido; solo progress/media |
| Perf | Media mobile | Compression pipeline |
| Scale | Device fragmentation | RN/Flutter choice ADR |
| Commercial | App store tax early | PWA first option evaluate |

**Complejidad:** L  |  **Prioridad:** P3  |  **Tiempo estimado:** 4–7 meses (1–2 eng) later

**Arquitectura involucrada.** Mobile client; post core platform

**Módulos/dominios afectados.**
- Mobile
- Timeline
- Media
- Notifications
- Identity

**Eventos nuevos / relevantes.**
- HitoCreado (mobile)
- MediaAssetListo
- Progress notes events

**Entidades nuevas / relevantes.**
- MobileSession
- OfflineQueue

**API (conceptual).**
- Subset API mobile
- upload media
- milestones

**Pantallas.**
- Home obra
- Camera upload
- Milestone check
- Read takeoff

**Base de datos (logical stores).**
- Local device store
- Same backend stores

**Tests necesarios.**
- Auth
- Offline queue
- Tenant
- Upload resume

**Migraciones.**
- mobile_sessions optional

**Criterio de Done.** MVP campo: login, ver presupuesto/takeoff, subir foto, marcar hito; sin edición geométrica.

**Features contenidas (detalle en §3):** E25-F01 Mobile auth & project picker, E25-F02 Read models field, E25-F03 Capture media & progress, E25-F04 Distribution & ops

**Notas de secuenciación.** Esta épica debe respetar: (1) no romper wedge existente, (2) emitir/consumir eventos vía outbox cuando mute hechos, (3) AuthZ tenant en toda API nueva, (4) flags para rollout, (5) métricas mínimas antes de declarar done.

**Definition of Ready (DoR) específica E25.**
- Contratos de eventos/API bocetados y revisados por Tech Lead
- Dependencias de épicas en estado usable (no necesariamente perfectas)
- Criterios de aceptación numéricos o binarios acordados con PM
- Owner de dominio asignado + reviewer de arquitectura si XL
- Plan de migración/datos y de rollback escrito
- Lista de lo que explícitamente NO entra (anti-scope)

**Señales de éxito post-release E25.**
- SLIs acordados en verde durante 7 días o waiver documentado
- Cero incidentes P0 de aislamiento tenant atribuibles a la épica
- Wedge e2e no degradado en golden set
- Deuda P0 nueva = 0; P1 ticketed con fecha
- Demo grabada o scriptable disponible para onboarding

---

## 3. Features y Tasks por Épica (detalle exhaustivo)

Bajo cada épica se listan Features (`Fxx`) lo más independientes posible, y bajo cada Feature tasks concretas (`Txx`) cubriendo entidad, servicio, eventos, API, frontend, docs, tests, migraciones y métricas. Las épicas E01–E16 están detalle exhaustivo; E17–E25 mantienen solidez operativa.

### 3.01 E01 — Platform Foundations & Observability

Prioridad P0 · Complejidad M · Depende de: — (fundación)

#### E01-F01 — Observabilidad base (logs/traces/metrics)

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E01` que avance el objetivo (Establecer cimientos de plataforma: logging estructurado, tracing distribuido, métricas, health/ready, config, feature f...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E01-F01-T01` — Definir taxonomía de campos obligatorios (tenant_id, project_id, job_id, trace_id)
- `E01-F01-T02` — Instrumentar API gateway con OpenTelemetry
- `E01-F01-T03` — Instrumentar workers (perception/jobs) con contexto propagado
- `E01-F01-T04` — Dashboard golden: latencia API, error rate, cola depth
- `E01-F01-T05` — Alertas P0: 5xx spike, DLQ > 0 sostenido, disk/memory workers
- `E01-F01-T06` — Log redaction de PII/secretos
- `E01-F01-T07` — Sampling policy documentada
- `E01-F01-T08` — Tests de presencia de correlation ids
- `E01-F01-T09` — Runbook: 'cómo seguir un request de upload a costo'
- `E01-F01-T10` — Feature flag `obs.enhanced` para exporters caros
- `E01-F01-T11` — Definir Acceptance Criteria medibles para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T12` — Agregar métricas RED/USE relevantes para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T13` — Escribir ADR si hay desvío de arquitectura para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T14` — Preparar feature flag + plan de rollback para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T15` — Actualizar OpenAPI/event schema si aplica para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T16` — Ejecutar checklist tenant isolation para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T17` — Actualizar runbook operativo para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T18` — Demo interna de 10 minutos documentada para E01-F01 (Observabilidad base (logs/traces/metrics))
- `E01-F01-T19` — Revisar compatibilidad Free/Pro/Enterprise en E01-F01
- `E01-F01-T20` — Verificar que no se rompe wedge color→qty→moneda local tras E01-F01
- `E01-F01-T21` — Añadir tests de regresión golden si E01-F01 toca motores
- `E01-F01-T22` — Instrumentar traces spans para E01-F01
- `E01-F01-T23` — Documentar dependencias de eventos en E01-F01
- `E01-F01-T24` — Checklist seguridad secretos/PII en E01-F01
- `E01-F01-T25` — Validar performance budget preliminar de E01-F01
- `E01-F01-T26` — Actualizar mapping Architecture domain ↔ E01-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E01-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E01-F02 — Health, readiness y degradación

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E01` que avance el objetivo (Establecer cimientos de plataforma: logging estructurado, tracing distribuido, métricas, health/ready, config, feature f...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E01-F02-T01` — Endpoints /health y /ready separados
- `E01-F02-T02` — Checks de DB, object storage, broker
- `E01-F02-T03` — Modo degradado: deshabilitar AI/exports vía flags
- `E01-F02-T04` — Banner UI de degradación
- `E01-F02-T05` — Tests de readiness fail cuando outbox stuck
- `E01-F02-T06` — Métrica `platform.ready` boolean timeseries
- `E01-F02-T07` — Documentar SLO de bootstrap cold start
- `E01-F02-T08` — Chaos light: matar dependencia y verificar señales
- `E01-F02-T09` — Definir Acceptance Criteria medibles para E01-F02 (Health, readiness y degradación)
- `E01-F02-T10` — Agregar métricas RED/USE relevantes para E01-F02 (Health, readiness y degradación)
- `E01-F02-T11` — Escribir ADR si hay desvío de arquitectura para E01-F02 (Health, readiness y degradación)
- `E01-F02-T12` — Preparar feature flag + plan de rollback para E01-F02 (Health, readiness y degradación)
- `E01-F02-T13` — Actualizar OpenAPI/event schema si aplica para E01-F02 (Health, readiness y degradación)
- `E01-F02-T14` — Ejecutar checklist tenant isolation para E01-F02 (Health, readiness y degradación)
- `E01-F02-T15` — Actualizar runbook operativo para E01-F02 (Health, readiness y degradación)
- `E01-F02-T16` — Demo interna de 10 minutos documentada para E01-F02 (Health, readiness y degradación)
- `E01-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E01-F02
- `E01-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E01-F02
- `E01-F02-T19` — Añadir tests de regresión golden si E01-F02 toca motores
- `E01-F02-T20` — Instrumentar traces spans para E01-F02
- `E01-F02-T21` — Documentar dependencias de eventos en E01-F02
- `E01-F02-T22` — Checklist seguridad secretos/PII en E01-F02
- `E01-F02-T23` — Validar performance budget preliminar de E01-F02
- `E01-F02-T24` — Actualizar mapping Architecture domain ↔ E01-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E01-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E01-F03 — Feature flags & config dinámica

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E01` que avance el objetivo (Establecer cimientos de plataforma: logging estructurado, tracing distribuido, métricas, health/ready, config, feature f...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E01-F03-T01` — Entidad FeatureFlag con targeting plan/org/project
- `E01-F03-T02` — API admin interna + audit trail
- `E01-F03-T03` — SDK server evaluation determinista
- `E01-F03-T04` — SDK frontend evaluation cacheada
- `E01-F03-T05` — Tests matriz flag × plan
- `E01-F03-T06` — Migración seed flags wedge
- `E01-F03-T07` — Prohibir flags eternas: expiry date field
- `E01-F03-T08` — Dashboard flags stale (>90 días)
- `E01-F03-T09` — Definir Acceptance Criteria medibles para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T10` — Agregar métricas RED/USE relevantes para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T11` — Escribir ADR si hay desvío de arquitectura para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T12` — Preparar feature flag + plan de rollback para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T13` — Actualizar OpenAPI/event schema si aplica para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T14` — Ejecutar checklist tenant isolation para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T15` — Actualizar runbook operativo para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T16` — Demo interna de 10 minutos documentada para E01-F03 (Feature flags & config dinámica)
- `E01-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E01-F03
- `E01-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E01-F03
- `E01-F03-T19` — Añadir tests de regresión golden si E01-F03 toca motores
- `E01-F03-T20` — Instrumentar traces spans para E01-F03
- `E01-F03-T21` — Documentar dependencias de eventos en E01-F03
- `E01-F03-T22` — Checklist seguridad secretos/PII en E01-F03
- `E01-F03-T23` — Validar performance budget preliminar de E01-F03
- `E01-F03-T24` — Actualizar mapping Architecture domain ↔ E01-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E01-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E01-F04 — CI quality gates & engineering standards

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E01` que avance el objetivo (Establecer cimientos de plataforma: logging estructurado, tracing distribuido, métricas, health/ready, config, feature f...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E01-F04-T01` — Pipeline lint + types + unit
- `E01-F04-T02` — Coverage floors por módulo crítico
- `E01-F04-T03` — Secret scan + dependency audit
- `E01-F04-T04` — Contract test placeholder para eventos
- `E01-F04-T05` — Policy: no merge con TODO sin issue
- `E01-F04-T06` — Template PR con checklist principios P01–P10
- `E01-F04-T07` — Badge de wedge e2e smoke (inicialmente skippeable con waiver)
- `E01-F04-T08` — Documentar Definition of Ready/Done en CONTRIBUTING conceptual
- `E01-F04-T09` — Definir Acceptance Criteria medibles para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T10` — Agregar métricas RED/USE relevantes para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T11` — Escribir ADR si hay desvío de arquitectura para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T12` — Preparar feature flag + plan de rollback para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T13` — Actualizar OpenAPI/event schema si aplica para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T14` — Ejecutar checklist tenant isolation para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T15` — Actualizar runbook operativo para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T16` — Demo interna de 10 minutos documentada para E01-F04 (CI quality gates & engineering standards)
- `E01-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E01-F04
- `E01-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E01-F04
- `E01-F04-T19` — Añadir tests de regresión golden si E01-F04 toca motores
- `E01-F04-T20` — Instrumentar traces spans para E01-F04
- `E01-F04-T21` — Documentar dependencias de eventos en E01-F04
- `E01-F04-T22` — Checklist seguridad secretos/PII en E01-F04
- `E01-F04-T23` — Validar performance budget preliminar de E01-F04
- `E01-F04-T24` — Actualizar mapping Architecture domain ↔ E01-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E01-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E01-F05 — Runbooks y operabilidad inicial

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E01` que avance el objetivo (Establecer cimientos de plataforma: logging estructurado, tracing distribuido, métricas, health/ready, config, feature f...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E01-F05-T01` — Runbook DLQ vacío (estructura)
- `E01-F05-T02` — Runbook rollback feature flag
- `E01-F05-T03` — Runbook incident sev definitions
- `E01-F05-T04` — Oncall roster stub
- `E01-F05-T05` — Postmortem template
- `E01-F05-T06` — Métrica MTTR tracking manual→auto
- `E01-F05-T07` — Lista de owners por dominio
- `E01-F05-T08` — Drill trimestral calendarizado
- `E01-F05-T09` — Definir Acceptance Criteria medibles para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T10` — Agregar métricas RED/USE relevantes para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T11` — Escribir ADR si hay desvío de arquitectura para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T12` — Preparar feature flag + plan de rollback para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T13` — Actualizar OpenAPI/event schema si aplica para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T14` — Ejecutar checklist tenant isolation para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T15` — Actualizar runbook operativo para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T16` — Demo interna de 10 minutos documentada para E01-F05 (Runbooks y operabilidad inicial)
- `E01-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E01-F05
- `E01-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E01-F05
- `E01-F05-T19` — Añadir tests de regresión golden si E01-F05 toca motores
- `E01-F05-T20` — Instrumentar traces spans para E01-F05
- `E01-F05-T21` — Documentar dependencias de eventos en E01-F05
- `E01-F05-T22` — Checklist seguridad secretos/PII en E01-F05
- `E01-F05-T23` — Validar performance budget preliminar de E01-F05
- `E01-F05-T24` — Actualizar mapping Architecture domain ↔ E01-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E01-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.02 E02 — Identity, Tenancy & Billing hardening

Prioridad P0 · Complejidad L · Depende de: E01

#### E02-F01 — AuthN sesiones y recuperación

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E02` que avance el objetivo (Endurecer Identity/Membership/Org, aislamiento tenant, sesiones, roles base y meters/entitlements Free/Pro/Enterprise si...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E02-F01-T01` — Modelo User/Session con rotación de tokens
- `E02-F01-T02` — Flujos registro/login/logout/reset
- `E02-F01-T03` — Rate limit auth endpoints
- `E02-F01-T04` — Tests brute-force soft lock
- `E02-F01-T05` — Evento UsuarioRegistrado
- `E02-F01-T06` — i18n ES mensajes auth
- `E02-F01-T07` — Métricas login success/fail
- `E02-F01-T08` — Audit login failures
- `E02-F01-T09` — Definir Acceptance Criteria medibles para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T10` — Agregar métricas RED/USE relevantes para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T11` — Escribir ADR si hay desvío de arquitectura para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T12` — Preparar feature flag + plan de rollback para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T13` — Actualizar OpenAPI/event schema si aplica para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T14` — Ejecutar checklist tenant isolation para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T15` — Actualizar runbook operativo para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T16` — Demo interna de 10 minutos documentada para E02-F01 (AuthN sesiones y recuperación)
- `E02-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E02-F01
- `E02-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E02-F01
- `E02-F01-T19` — Añadir tests de regresión golden si E02-F01 toca motores
- `E02-F01-T20` — Instrumentar traces spans para E02-F01
- `E02-F01-T21` — Documentar dependencias de eventos en E02-F01
- `E02-F01-T22` — Checklist seguridad secretos/PII en E02-F01
- `E02-F01-T23` — Validar performance budget preliminar de E02-F01
- `E02-F01-T24` — Actualizar mapping Architecture domain ↔ E02-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E02-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E02-F02 — Organizations & memberships

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E02` que avance el objetivo (Endurecer Identity/Membership/Org, aislamiento tenant, sesiones, roles base y meters/entitlements Free/Pro/Enterprise si...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E02-F02-T01` — Entidad Organization como tenant root
- `E02-F02-T02` — Membership roles base (owner/admin/editor/viewer)
- `E02-F02-T03` — Invitaciones por email
- `E02-F02-T04` — Eventos UsuarioInvitado / MiembroRolCambiado
- `E02-F02-T05` — AuthZ helpers de dominio
- `E02-F02-T06` — Tests isolation cross-org
- `E02-F02-T07` — UI org settings + members
- `E02-F02-T08` — Soft-disable member
- `E02-F02-T09` — Definir Acceptance Criteria medibles para E02-F02 (Organizations & memberships)
- `E02-F02-T10` — Agregar métricas RED/USE relevantes para E02-F02 (Organizations & memberships)
- `E02-F02-T11` — Escribir ADR si hay desvío de arquitectura para E02-F02 (Organizations & memberships)
- `E02-F02-T12` — Preparar feature flag + plan de rollback para E02-F02 (Organizations & memberships)
- `E02-F02-T13` — Actualizar OpenAPI/event schema si aplica para E02-F02 (Organizations & memberships)
- `E02-F02-T14` — Ejecutar checklist tenant isolation para E02-F02 (Organizations & memberships)
- `E02-F02-T15` — Actualizar runbook operativo para E02-F02 (Organizations & memberships)
- `E02-F02-T16` — Demo interna de 10 minutos documentada para E02-F02 (Organizations & memberships)
- `E02-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E02-F02
- `E02-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E02-F02
- `E02-F02-T19` — Añadir tests de regresión golden si E02-F02 toca motores
- `E02-F02-T20` — Instrumentar traces spans para E02-F02
- `E02-F02-T21` — Documentar dependencias de eventos en E02-F02
- `E02-F02-T22` — Checklist seguridad secretos/PII en E02-F02
- `E02-F02-T23` — Validar performance budget preliminar de E02-F02
- `E02-F02-T24` — Actualizar mapping Architecture domain ↔ E02-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E02-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E02-F03 — Entitlements Free/Pro/Enterprise

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E02` que avance el objetivo (Endurecer Identity/Membership/Org, aislamiento tenant, sesiones, roles base y meters/entitlements Free/Pro/Enterprise si...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E02-F03-T01` — Tabla de capacidades por plan (proyectos, storage, AI, exports, plugins)
- `E02-F03-T02` — Servicio entitlements consultable
- `E02-F03-T03` — Feature flags ligadas a plan
- `E02-F03-T04` — Tests matriz plan × capability
- `E02-F03-T05` — UX upgrade y paywall no agresivo
- `E02-F03-T06` — Evento SuscripcionCambiada
- `E02-F03-T07` — Documentar límites Free LATAM
- `E02-F03-T08` — Admin override Enterprise custom
- `E02-F03-T09` — Definir Acceptance Criteria medibles para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T10` — Agregar métricas RED/USE relevantes para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T11` — Escribir ADR si hay desvío de arquitectura para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T12` — Preparar feature flag + plan de rollback para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T13` — Actualizar OpenAPI/event schema si aplica para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T14` — Ejecutar checklist tenant isolation para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T15` — Actualizar runbook operativo para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T16` — Demo interna de 10 minutos documentada para E02-F03 (Entitlements Free/Pro/Enterprise)
- `E02-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E02-F03
- `E02-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E02-F03
- `E02-F03-T19` — Añadir tests de regresión golden si E02-F03 toca motores
- `E02-F03-T20` — Instrumentar traces spans para E02-F03
- `E02-F03-T21` — Documentar dependencias de eventos en E02-F03
- `E02-F03-T22` — Checklist seguridad secretos/PII en E02-F03
- `E02-F03-T23` — Validar performance budget preliminar de E02-F03
- `E02-F03-T24` — Actualizar mapping Architecture domain ↔ E02-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E02-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E02-F04 — Usage meters & quotas

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E02` que avance el objetivo (Endurecer Identity/Membership/Org, aislamiento tenant, sesiones, roles base y meters/entitlements Free/Pro/Enterprise si...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E02-F04-T01` — Append-only usage_events
- `E02-F04-T02` — Meters: uploads, pages, AI tokens, exports, jobs minutes
- `E02-F04-T03` — Idempotency key por consumo
- `E02-F04-T04` — Eventos UsoRegistrado/UsoConsumido/QuotaUmbralAlcanzado
- `E02-F04-T05` — UI usage bars
- `E02-F04-T06` — Bloqueo graceful al exceder Free
- `E02-F04-T07` — Tests race conditions meters
- `E02-F04-T08` — Reconciliación diaria job
- `E02-F04-T09` — Definir Acceptance Criteria medibles para E02-F04 (Usage meters & quotas)
- `E02-F04-T10` — Agregar métricas RED/USE relevantes para E02-F04 (Usage meters & quotas)
- `E02-F04-T11` — Escribir ADR si hay desvío de arquitectura para E02-F04 (Usage meters & quotas)
- `E02-F04-T12` — Preparar feature flag + plan de rollback para E02-F04 (Usage meters & quotas)
- `E02-F04-T13` — Actualizar OpenAPI/event schema si aplica para E02-F04 (Usage meters & quotas)
- `E02-F04-T14` — Ejecutar checklist tenant isolation para E02-F04 (Usage meters & quotas)
- `E02-F04-T15` — Actualizar runbook operativo para E02-F04 (Usage meters & quotas)
- `E02-F04-T16` — Demo interna de 10 minutos documentada para E02-F04 (Usage meters & quotas)
- `E02-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E02-F04
- `E02-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E02-F04
- `E02-F04-T19` — Añadir tests de regresión golden si E02-F04 toca motores
- `E02-F04-T20` — Instrumentar traces spans para E02-F04
- `E02-F04-T21` — Documentar dependencias de eventos en E02-F04
- `E02-F04-T22` — Checklist seguridad secretos/PII en E02-F04
- `E02-F04-T23` — Validar performance budget preliminar de E02-F04
- `E02-F04-T24` — Actualizar mapping Architecture domain ↔ E02-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E02-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E02-F05 — Billing provider integration light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E02` que avance el objetivo (Endurecer Identity/Membership/Org, aislamiento tenant, sesiones, roles base y meters/entitlements Free/Pro/Enterprise si...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E02-F05-T01` — Abstracción PaymentProvider
- `E02-F05-T02` — Checkout Free→Pro
- `E02-F05-T03` — Webhook PagoFallido handling
- `E02-F05-T04` — InvoiceRef storage
- `E02-F05-T05` — Tests webhook signatures
- `E02-F05-T06` — No hard-delete invoices
- `E02-F05-T07` — Runbook pago fallido
- `E02-F05-T08` — LATAM currency display
- `E02-F05-T09` — Definir Acceptance Criteria medibles para E02-F05 (Billing provider integration light)
- `E02-F05-T10` — Agregar métricas RED/USE relevantes para E02-F05 (Billing provider integration light)
- `E02-F05-T11` — Escribir ADR si hay desvío de arquitectura para E02-F05 (Billing provider integration light)
- `E02-F05-T12` — Preparar feature flag + plan de rollback para E02-F05 (Billing provider integration light)
- `E02-F05-T13` — Actualizar OpenAPI/event schema si aplica para E02-F05 (Billing provider integration light)
- `E02-F05-T14` — Ejecutar checklist tenant isolation para E02-F05 (Billing provider integration light)
- `E02-F05-T15` — Actualizar runbook operativo para E02-F05 (Billing provider integration light)
- `E02-F05-T16` — Demo interna de 10 minutos documentada para E02-F05 (Billing provider integration light)
- `E02-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E02-F05
- `E02-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E02-F05
- `E02-F05-T19` — Añadir tests de regresión golden si E02-F05 toca motores
- `E02-F05-T20` — Instrumentar traces spans para E02-F05
- `E02-F05-T21` — Documentar dependencias de eventos en E02-F05
- `E02-F05-T22` — Checklist seguridad secretos/PII en E02-F05
- `E02-F05-T23` — Validar performance budget preliminar de E02-F05
- `E02-F05-T24` — Actualizar mapping Architecture domain ↔ E02-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E02-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E02-F06 — Audit identity actions

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E02` que avance el objetivo (Endurecer Identity/Membership/Org, aislamiento tenant, sesiones, roles base y meters/entitlements Free/Pro/Enterprise si...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E02-F06-T01` — AuditEvent para cambios de rol y plan
- `E02-F06-T02` — Retención append-only
- `E02-F06-T03` — Export CSV básico (admin)
- `E02-F06-T04` — Tests non-repudiation fields
- `E02-F06-T05` — Pantalla audit mínima org admin
- `E02-F06-T06` — PII minimization policy
- `E02-F06-T07` — Definir Acceptance Criteria medibles para E02-F06 (Audit identity actions)
- `E02-F06-T08` — Agregar métricas RED/USE relevantes para E02-F06 (Audit identity actions)
- `E02-F06-T09` — Escribir ADR si hay desvío de arquitectura para E02-F06 (Audit identity actions)
- `E02-F06-T10` — Preparar feature flag + plan de rollback para E02-F06 (Audit identity actions)
- `E02-F06-T11` — Actualizar OpenAPI/event schema si aplica para E02-F06 (Audit identity actions)
- `E02-F06-T12` — Ejecutar checklist tenant isolation para E02-F06 (Audit identity actions)
- `E02-F06-T13` — Actualizar runbook operativo para E02-F06 (Audit identity actions)
- `E02-F06-T14` — Demo interna de 10 minutos documentada para E02-F06 (Audit identity actions)
- `E02-F06-T15` — Revisar compatibilidad Free/Pro/Enterprise en E02-F06
- `E02-F06-T16` — Verificar que no se rompe wedge color→qty→moneda local tras E02-F06
- `E02-F06-T17` — Añadir tests de regresión golden si E02-F06 toca motores
- `E02-F06-T18` — Instrumentar traces spans para E02-F06
- `E02-F06-T19` — Documentar dependencias de eventos en E02-F06
- `E02-F06-T20` — Checklist seguridad secretos/PII en E02-F06
- `E02-F06-T21` — Validar performance budget preliminar de E02-F06
- `E02-F06-T22` — Actualizar mapping Architecture domain ↔ E02-F06

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E02-F06-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.03 E03 — Media & Object Storage

Prioridad P0 · Complejidad M · Depende de: E01, E02

#### E03-F01 — Upload sessions & signed URLs

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E03` que avance el objetivo (Pipeline robusto de upload, object storage por tenant, derivados, checksums, retención y eventos de medios....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E03-F01-T01` — Crear UploadSession con cuota check
- `E03-F01-T02` — Presigned URL scoped org/project
- `E03-F01-T03` — Complete con checksum
- `E03-F01-T04` — Evento PlanoSubido
- `E03-F01-T05` — Tests URL no reusable cross-tenant
- `E03-F01-T06` — UI uploader multiparte
- `E03-F01-T07` — Métricas bytes uploaded
- `E03-F01-T08` — Abort session cleanup job
- `E03-F01-T09` — Definir Acceptance Criteria medibles para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T10` — Agregar métricas RED/USE relevantes para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T11` — Escribir ADR si hay desvío de arquitectura para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T12` — Preparar feature flag + plan de rollback para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T13` — Actualizar OpenAPI/event schema si aplica para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T14` — Ejecutar checklist tenant isolation para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T15` — Actualizar runbook operativo para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T16` — Demo interna de 10 minutos documentada para E03-F01 (Upload sessions & signed URLs)
- `E03-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E03-F01
- `E03-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E03-F01
- `E03-F01-T19` — Añadir tests de regresión golden si E03-F01 toca motores
- `E03-F01-T20` — Instrumentar traces spans para E03-F01
- `E03-F01-T21` — Documentar dependencias de eventos en E03-F01
- `E03-F01-T22` — Checklist seguridad secretos/PII en E03-F01
- `E03-F01-T23` — Validar performance budget preliminar de E03-F01
- `E03-F01-T24` — Actualizar mapping Architecture domain ↔ E03-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E03-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E03-F02 — Derivatives pipeline

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E03` que avance el objetivo (Pipeline robusto de upload, object storage por tenant, derivados, checksums, retención y eventos de medios....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E03-F02-T01` — Job thumbnails/page renders
- `E03-F02-T02` — Evento DerivadoGenerado
- `E03-F02-T03` — Storage keys versionadas
- `E03-F02-T04` — Tests de formatos PDF/PNG/JPG
- `E03-F02-T05` — Reintento idempotente
- `E03-F02-T06` — UI preview sheet
- `E03-F02-T07` — Budget tiempo job derivados
- `E03-F02-T08` — DLQ handling
- `E03-F02-T09` — Definir Acceptance Criteria medibles para E03-F02 (Derivatives pipeline)
- `E03-F02-T10` — Agregar métricas RED/USE relevantes para E03-F02 (Derivatives pipeline)
- `E03-F02-T11` — Escribir ADR si hay desvío de arquitectura para E03-F02 (Derivatives pipeline)
- `E03-F02-T12` — Preparar feature flag + plan de rollback para E03-F02 (Derivatives pipeline)
- `E03-F02-T13` — Actualizar OpenAPI/event schema si aplica para E03-F02 (Derivatives pipeline)
- `E03-F02-T14` — Ejecutar checklist tenant isolation para E03-F02 (Derivatives pipeline)
- `E03-F02-T15` — Actualizar runbook operativo para E03-F02 (Derivatives pipeline)
- `E03-F02-T16` — Demo interna de 10 minutos documentada para E03-F02 (Derivatives pipeline)
- `E03-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E03-F02
- `E03-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E03-F02
- `E03-F02-T19` — Añadir tests de regresión golden si E03-F02 toca motores
- `E03-F02-T20` — Instrumentar traces spans para E03-F02
- `E03-F02-T21` — Documentar dependencias de eventos en E03-F02
- `E03-F02-T22` — Checklist seguridad secretos/PII en E03-F02
- `E03-F02-T23` — Validar performance budget preliminar de E03-F02
- `E03-F02-T24` — Actualizar mapping Architecture domain ↔ E03-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E03-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E03-F03 — MediaAsset lifecycle & retention

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E03` que avance el objetivo (Pipeline robusto de upload, object storage por tenant, derivados, checksums, retención y eventos de medios....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E03-F03-T01` — Soft-delete MediaAsset
- `E03-F03-T02` — RetentionPolicy por org
- `E03-F03-T03` — Job MediaRetencionAplicada
- `E03-F03-T04` — Legal hold stub (Enterprise later)
- `E03-F03-T05` — Tests never hard-delete referenced assets in signed budgets
- `E03-F03-T06` — UI archive/restore
- `E03-F03-T07` — Cost report storage per org
- `E03-F03-T08` — Documentar políticas Free vs Pro
- `E03-F03-T09` — Definir Acceptance Criteria medibles para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T10` — Agregar métricas RED/USE relevantes para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T11` — Escribir ADR si hay desvío de arquitectura para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T12` — Preparar feature flag + plan de rollback para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T13` — Actualizar OpenAPI/event schema si aplica para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T14` — Ejecutar checklist tenant isolation para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T15` — Actualizar runbook operativo para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T16` — Demo interna de 10 minutos documentada para E03-F03 (MediaAsset lifecycle & retention)
- `E03-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E03-F03
- `E03-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E03-F03
- `E03-F03-T19` — Añadir tests de regresión golden si E03-F03 toca motores
- `E03-F03-T20` — Instrumentar traces spans para E03-F03
- `E03-F03-T21` — Documentar dependencias de eventos en E03-F03
- `E03-F03-T22` — Checklist seguridad secretos/PII en E03-F03
- `E03-F03-T23` — Validar performance budget preliminar de E03-F03
- `E03-F03-T24` — Actualizar mapping Architecture domain ↔ E03-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E03-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E03-F04 — Security & malware light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E03` que avance el objetivo (Pipeline robusto de upload, object storage por tenant, derivados, checksums, retención y eventos de medios....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E03-F04-T01` — MIME sniff server-side
- `E03-F04-T02` — Size limits por plan
- `E03-F04-T03` — Optional AV hook interface
- `E03-F04-T04` — Block executable masquerade
- `E03-F04-T05` — Tests content-type mismatch
- `E03-F04-T06` — Audit acceso a signed URL issues
- `E03-F04-T07` — Rate limit upload-url
- `E03-F04-T08` — Runbook asset comprometido
- `E03-F04-T09` — Definir Acceptance Criteria medibles para E03-F04 (Security & malware light)
- `E03-F04-T10` — Agregar métricas RED/USE relevantes para E03-F04 (Security & malware light)
- `E03-F04-T11` — Escribir ADR si hay desvío de arquitectura para E03-F04 (Security & malware light)
- `E03-F04-T12` — Preparar feature flag + plan de rollback para E03-F04 (Security & malware light)
- `E03-F04-T13` — Actualizar OpenAPI/event schema si aplica para E03-F04 (Security & malware light)
- `E03-F04-T14` — Ejecutar checklist tenant isolation para E03-F04 (Security & malware light)
- `E03-F04-T15` — Actualizar runbook operativo para E03-F04 (Security & malware light)
- `E03-F04-T16` — Demo interna de 10 minutos documentada para E03-F04 (Security & malware light)
- `E03-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E03-F04
- `E03-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E03-F04
- `E03-F04-T19` — Añadir tests de regresión golden si E03-F04 toca motores
- `E03-F04-T20` — Instrumentar traces spans para E03-F04
- `E03-F04-T21` — Documentar dependencias de eventos en E03-F04
- `E03-F04-T22` — Checklist seguridad secretos/PII en E03-F04
- `E03-F04-T23` — Validar performance budget preliminar de E03-F04
- `E03-F04-T24` — Actualizar mapping Architecture domain ↔ E03-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E03-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.04 E04 — Async Jobs & Event Bus (Outbox)

Prioridad P0 · Complejidad L · Depende de: E01, E02

#### E04-F01 — Jobs API & state machine

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E04` que avance el objetivo (Jobs API, colas por clase, outbox, idempotencia, DLQ, progreso WS y semántica de entrega para desacoplar L1/L2....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E04-F01-T01` — Entidad Job con estados queued/running/succeeded/failed/cancelled
- `E04-F01-T02` — API create/get/cancel
- `E04-F01-T03` — Attempts con backoff
- `E04-F01-T04` — Timeouts por tipo de cola
- `E04-F01-T05` — Tests state transitions
- `E04-F01-T06` — Métricas duración por tipo
- `E04-F01-T07` — AuthZ job pertenece a project/org
- `E04-F01-T08` — Documentar catálogo de job types
- `E04-F01-T09` — Definir Acceptance Criteria medibles para E04-F01 (Jobs API & state machine)
- `E04-F01-T10` — Agregar métricas RED/USE relevantes para E04-F01 (Jobs API & state machine)
- `E04-F01-T11` — Escribir ADR si hay desvío de arquitectura para E04-F01 (Jobs API & state machine)
- `E04-F01-T12` — Preparar feature flag + plan de rollback para E04-F01 (Jobs API & state machine)
- `E04-F01-T13` — Actualizar OpenAPI/event schema si aplica para E04-F01 (Jobs API & state machine)
- `E04-F01-T14` — Ejecutar checklist tenant isolation para E04-F01 (Jobs API & state machine)
- `E04-F01-T15` — Actualizar runbook operativo para E04-F01 (Jobs API & state machine)
- `E04-F01-T16` — Demo interna de 10 minutos documentada para E04-F01 (Jobs API & state machine)
- `E04-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E04-F01
- `E04-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E04-F01
- `E04-F01-T19` — Añadir tests de regresión golden si E04-F01 toca motores
- `E04-F01-T20` — Instrumentar traces spans para E04-F01
- `E04-F01-T21` — Documentar dependencias de eventos en E04-F01
- `E04-F01-T22` — Checklist seguridad secretos/PII en E04-F01
- `E04-F01-T23` — Validar performance budget preliminar de E04-F01
- `E04-F01-T24` — Actualizar mapping Architecture domain ↔ E04-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E04-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E04-F02 — Outbox pattern

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E04` que avance el objetivo (Jobs API, colas por clase, outbox, idempotencia, DLQ, progreso WS y semántica de entrega para desacoplar L1/L2....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E04-F02-T01` — Tabla outbox transaccional con agregados
- `E04-F02-T02` — Publisher relay
- `E04-F02-T03` — Dedup keys
- `E04-F02-T04` — Tests dual-write safety
- `E04-F02-T05` — Ordering per aggregate id
- `E04-F02-T06` — Monitor lag outbox
- `E04-F02-T07` — Alert lag > umbral
- `E04-F02-T08` — Runbook stuck outbox
- `E04-F02-T09` — Definir Acceptance Criteria medibles para E04-F02 (Outbox pattern)
- `E04-F02-T10` — Agregar métricas RED/USE relevantes para E04-F02 (Outbox pattern)
- `E04-F02-T11` — Escribir ADR si hay desvío de arquitectura para E04-F02 (Outbox pattern)
- `E04-F02-T12` — Preparar feature flag + plan de rollback para E04-F02 (Outbox pattern)
- `E04-F02-T13` — Actualizar OpenAPI/event schema si aplica para E04-F02 (Outbox pattern)
- `E04-F02-T14` — Ejecutar checklist tenant isolation para E04-F02 (Outbox pattern)
- `E04-F02-T15` — Actualizar runbook operativo para E04-F02 (Outbox pattern)
- `E04-F02-T16` — Demo interna de 10 minutos documentada para E04-F02 (Outbox pattern)
- `E04-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E04-F02
- `E04-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E04-F02
- `E04-F02-T19` — Añadir tests de regresión golden si E04-F02 toca motores
- `E04-F02-T20` — Instrumentar traces spans para E04-F02
- `E04-F02-T21` — Documentar dependencias de eventos en E04-F02
- `E04-F02-T22` — Checklist seguridad secretos/PII en E04-F02
- `E04-F02-T23` — Validar performance budget preliminar de E04-F02
- `E04-F02-T24` — Actualizar mapping Architecture domain ↔ E04-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E04-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E04-F03 — Queues, retries, DLQ, fairness

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E04` que avance el objetivo (Jobs API, colas por clase, outbox, idempotencia, DLQ, progreso WS y semántica de entrega para desacoplar L1/L2....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E04-F03-T01` — Colas: perception, geometry, materials, costs, reports, ai, default
- `E04-F03-T02` — Retry policy + jitter
- `E04-F03-T03` — DLQ entity + admin inspect
- `E04-F03-T04` — Fairness por tenant (token bucket / sharding keys)
- `E04-F03-T05` — Circuit breaker por dependency
- `E04-F03-T06` — Tests poison message
- `E04-F03-T07` — SLO dashboards por cola
- `E04-F03-T08` — Cancelación cooperativa
- `E04-F03-T09` — Definir Acceptance Criteria medibles para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T10` — Agregar métricas RED/USE relevantes para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T11` — Escribir ADR si hay desvío de arquitectura para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T12` — Preparar feature flag + plan de rollback para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T13` — Actualizar OpenAPI/event schema si aplica para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T14` — Ejecutar checklist tenant isolation para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T15` — Actualizar runbook operativo para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T16` — Demo interna de 10 minutos documentada para E04-F03 (Queues, retries, DLQ, fairness)
- `E04-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E04-F03
- `E04-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E04-F03
- `E04-F03-T19` — Añadir tests de regresión golden si E04-F03 toca motores
- `E04-F03-T20` — Instrumentar traces spans para E04-F03
- `E04-F03-T21` — Documentar dependencias de eventos en E04-F03
- `E04-F03-T22` — Checklist seguridad secretos/PII en E04-F03
- `E04-F03-T23` — Validar performance budget preliminar de E04-F03
- `E04-F03-T24` — Actualizar mapping Architecture domain ↔ E04-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E04-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E04-F04 — WebSocket progress & presence light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E04` que avance el objetivo (Jobs API, colas por clase, outbox, idempotencia, DLQ, progreso WS y semántica de entrega para desacoplar L1/L2....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E04-F04-T01` — Canal project:{id}
- `E04-F04-T02` — Eventos job.progress/completed/failed
- `E04-F04-T03` — AuthZ en handshake WS
- `E04-F04-T04` — Frontend job tray
- `E04-F04-T05` — Backoff reconnect
- `E04-F04-T06` — Tests load ligero WS
- `E04-F04-T07` — No usar WS como SoT
- `E04-F04-T08` — Métricas conexiones WS
- `E04-F04-T09` — Definir Acceptance Criteria medibles para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T10` — Agregar métricas RED/USE relevantes para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T11` — Escribir ADR si hay desvío de arquitectura para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T12` — Preparar feature flag + plan de rollback para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T13` — Actualizar OpenAPI/event schema si aplica para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T14` — Ejecutar checklist tenant isolation para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T15` — Actualizar runbook operativo para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T16` — Demo interna de 10 minutos documentada para E04-F04 (WebSocket progress & presence light)
- `E04-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E04-F04
- `E04-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E04-F04
- `E04-F04-T19` — Añadir tests de regresión golden si E04-F04 toca motores
- `E04-F04-T20` — Instrumentar traces spans para E04-F04
- `E04-F04-T21` — Documentar dependencias de eventos en E04-F04
- `E04-F04-T22` — Checklist seguridad secretos/PII en E04-F04
- `E04-F04-T23` — Validar performance budget preliminar de E04-F04
- `E04-F04-T24` — Actualizar mapping Architecture domain ↔ E04-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E04-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E04-F05 — Event envelope & schema registry light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E04` que avance el objetivo (Jobs API, colas por clase, outbox, idempotencia, DLQ, progreso WS y semántica de entrega para desacoplar L1/L2....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E04-F05-T01` — Envelope: id, type, version, tenant, occurred_at, correlation
- `E04-F05-T02` — Naming conventions dominio.Evento
- `E04-F05-T03` — JSON schema versionado
- `E04-F05-T04` — Consumer tolerant readers
- `E04-F05-T05` — Tests schema evolution add-optional
- `E04-F05-T06` — Docs catálogo inicial
- `E04-F05-T07` — Prohibir breaking changes sin version bump
- `E04-F05-T08` — CI contract check
- `E04-F05-T09` — Definir Acceptance Criteria medibles para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T10` — Agregar métricas RED/USE relevantes para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T11` — Escribir ADR si hay desvío de arquitectura para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T12` — Preparar feature flag + plan de rollback para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T13` — Actualizar OpenAPI/event schema si aplica para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T14` — Ejecutar checklist tenant isolation para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T15` — Actualizar runbook operativo para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T16` — Demo interna de 10 minutos documentada para E04-F05 (Event envelope & schema registry light)
- `E04-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E04-F05
- `E04-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E04-F05
- `E04-F05-T19` — Añadir tests de regresión golden si E04-F05 toca motores
- `E04-F05-T20` — Instrumentar traces spans para E04-F05
- `E04-F05-T21` — Documentar dependencias de eventos en E04-F05
- `E04-F05-T22` — Checklist seguridad secretos/PII en E04-F05
- `E04-F05-T23` — Validar performance budget preliminar de E04-F05
- `E04-F05-T24` — Actualizar mapping Architecture domain ↔ E04-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E04-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.05 E05 — Perception Engine (CV/OCR) modernization

Prioridad P0 · Complejidad XL · Depende de: E03, E04

#### E05-F01 — Pipeline versioning & job orchestration

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E05` que avance el objetivo (Modernizar L1: pipeline versionado ingest→normalize→OCR→color segmentation→symbol assist→evidence pack; nunca calcular c...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E05-F01-T01` — Definir PipelineVersion inmutable (semver + hash artefactos)
- `E05-F01-T02` — PerceptionJob state machine sobre E04 Jobs
- `E05-F01-T03` — Eventos PercepcionIniciada/PlanoProcesado/PercepcionFallida
- `E05-F01-T04` — Registro de métricas por etapa del pipeline
- `E05-F01-T05` — Cancelación cooperativa mid-pipeline
- `E05-F01-T06` — Tests de transición y timeout
- `E05-F01-T07` — Quota pages/jobs por plan
- `E05-F01-T08` — Runbook pipeline stuck
- `E05-F01-T09` — Feature flag `perception.vNext`
- `E05-F01-T10` — Documentar taxonomía error_code
- `E05-F01-T11` — Definir Acceptance Criteria medibles para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T12` — Agregar métricas RED/USE relevantes para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T13` — Escribir ADR si hay desvío de arquitectura para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T14` — Preparar feature flag + plan de rollback para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T15` — Actualizar OpenAPI/event schema si aplica para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T16` — Ejecutar checklist tenant isolation para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T17` — Actualizar runbook operativo para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T18` — Demo interna de 10 minutos documentada para E05-F01 (Pipeline versioning & job orchestration)
- `E05-F01-T19` — Revisar compatibilidad Free/Pro/Enterprise en E05-F01
- `E05-F01-T20` — Verificar que no se rompe wedge color→qty→moneda local tras E05-F01
- `E05-F01-T21` — Añadir tests de regresión golden si E05-F01 toca motores
- `E05-F01-T22` — Instrumentar traces spans para E05-F01
- `E05-F01-T23` — Documentar dependencias de eventos en E05-F01
- `E05-F01-T24` — Checklist seguridad secretos/PII en E05-F01
- `E05-F01-T25` — Validar performance budget preliminar de E05-F01
- `E05-F01-T26` — Actualizar mapping Architecture domain ↔ E05-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E05-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E05-F02 — Normalize + OCR

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E05` que avance el objetivo (Modernizar L1: pipeline versionado ingest→normalize→OCR→color segmentation→symbol assist→evidence pack; nunca calcular c...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E05-F02-T01` — Normalización DPI/orientación/colorespace
- `E05-F02-T02` — OCR blocks con bbox + confidence + text
- `E05-F02-T03` — Almacenamiento OcrBlock + raw ref
- `E05-F02-T04` — Idioma ES prioritario + nums planos
- `E05-F02-T05` — Tests fixtures texto/cotas
- `E05-F02-T06` — No inventar geometría desde OCR
- `E05-F02-T07` — Métrica ocr.char_confidence_avg
- `E05-F02-T08` — PII redaction opcional en logs OCR
- `E05-F02-T09` — Definir Acceptance Criteria medibles para E05-F02 (Normalize + OCR)
- `E05-F02-T10` — Agregar métricas RED/USE relevantes para E05-F02 (Normalize + OCR)
- `E05-F02-T11` — Escribir ADR si hay desvío de arquitectura para E05-F02 (Normalize + OCR)
- `E05-F02-T12` — Preparar feature flag + plan de rollback para E05-F02 (Normalize + OCR)
- `E05-F02-T13` — Actualizar OpenAPI/event schema si aplica para E05-F02 (Normalize + OCR)
- `E05-F02-T14` — Ejecutar checklist tenant isolation para E05-F02 (Normalize + OCR)
- `E05-F02-T15` — Actualizar runbook operativo para E05-F02 (Normalize + OCR)
- `E05-F02-T16` — Demo interna de 10 minutos documentada para E05-F02 (Normalize + OCR)
- `E05-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E05-F02
- `E05-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E05-F02
- `E05-F02-T19` — Añadir tests de regresión golden si E05-F02 toca motores
- `E05-F02-T20` — Instrumentar traces spans para E05-F02
- `E05-F02-T21` — Documentar dependencias de eventos en E05-F02
- `E05-F02-T22` — Checklist seguridad secretos/PII en E05-F02
- `E05-F02-T23` — Validar performance budget preliminar de E05-F02
- `E05-F02-T24` — Actualizar mapping Architecture domain ↔ E05-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E05-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E05-F03 — Color segmentation (wedge crítico)

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E05` que avance el objetivo (Modernizar L1: pipeline versionado ingest→normalize→OCR→color segmentation→symbol assist→evidence pack; nunca calcular c...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E05-F03-T01` — Segmentación por color_key → ColorRegion + mask_ref + area_px
- `E05-F03-T02` — Evento EvidenciaCreada / ColorMapActualizado
- `E05-F03-T03` — API PATCH mapping color→typology_candidate (baja autoridad)
- `E05-F03-T04` — UI mapper color wedges
- `E05-F03-T05` — Tests colores canónicos LATAM sample set
- `E05-F03-T06` — Confidence por región
- `E05-F03-T07` — Reproceso al cambiar mapping sin recomputar todo si es posible
- `E05-F03-T08` — Benchmark tiempo segmentación
- `E05-F03-T09` — Definir Acceptance Criteria medibles para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T10` — Agregar métricas RED/USE relevantes para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T11` — Escribir ADR si hay desvío de arquitectura para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T12` — Preparar feature flag + plan de rollback para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T13` — Actualizar OpenAPI/event schema si aplica para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T14` — Ejecutar checklist tenant isolation para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T15` — Actualizar runbook operativo para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T16` — Demo interna de 10 minutos documentada para E05-F03 (Color segmentation (wedge crítico))
- `E05-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E05-F03
- `E05-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E05-F03
- `E05-F03-T19` — Añadir tests de regresión golden si E05-F03 toca motores
- `E05-F03-T20` — Instrumentar traces spans para E05-F03
- `E05-F03-T21` — Documentar dependencias de eventos en E05-F03
- `E05-F03-T22` — Checklist seguridad secretos/PII en E05-F03
- `E05-F03-T23` — Validar performance budget preliminar de E05-F03
- `E05-F03-T24` — Actualizar mapping Architecture domain ↔ E05-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E05-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E05-F04 — Symbol assist & evidence pack

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E05` que avance el objetivo (Modernizar L1: pipeline versionado ingest→normalize→OCR→color segmentation→symbol assist→evidence pack; nunca calcular c...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E05-F04-T01` — Detector/assist de símbolos (baja autoridad)
- `E05-F04-T02` — Empaquetado Evidence tipada (kind, label, geom_ref, confidence, lineage asset)
- `E05-F04-T03` — Prohibir escritura a Costs/Materials
- `E05-F04-T04` — Tests anti-side-effect arch
- `E05-F04-T05` — Export debug pack (Pro/internal)
- `E05-F04-T06` — Overlay Studio de evidencias
- `E05-F04-T07` — Heatmap confidence
- `E05-F04-T08` — Eval set semanal calidad percepción
- `E05-F04-T09` — Definir Acceptance Criteria medibles para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T10` — Agregar métricas RED/USE relevantes para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T11` — Escribir ADR si hay desvío de arquitectura para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T12` — Preparar feature flag + plan de rollback para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T13` — Actualizar OpenAPI/event schema si aplica para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T14` — Ejecutar checklist tenant isolation para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T15` — Actualizar runbook operativo para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T16` — Demo interna de 10 minutos documentada para E05-F04 (Symbol assist & evidence pack)
- `E05-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E05-F04
- `E05-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E05-F04
- `E05-F04-T19` — Añadir tests de regresión golden si E05-F04 toca motores
- `E05-F04-T20` — Instrumentar traces spans para E05-F04
- `E05-F04-T21` — Documentar dependencias de eventos en E05-F04
- `E05-F04-T22` — Checklist seguridad secretos/PII en E05-F04
- `E05-F04-T23` — Validar performance budget preliminar de E05-F04
- `E05-F04-T24` — Actualizar mapping Architecture domain ↔ E05-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E05-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E05-F05 — Replay, golden sets & quality gates

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E05` que avance el objetivo (Modernizar L1: pipeline versionado ingest→normalize→OCR→color segmentation→symbol assist→evidence pack; nunca calcular c...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E05-F05-T01` — Replay job sobre mismo MediaAsset + pipeline_version
- `E05-F05-T02` — Golden set planos LATAM en CI (subset) y nightly (full)
- `E05-F05-T03` — Diff de evidencias con tolerancia
- `E05-F05-T04` — Gate: no regressar métricas clave sin waiver
- `E05-F05-T05` — Dashboard drift
- `E05-F05-T06` — Documentar proceso de promover pipeline_version
- `E05-F05-T07` — Canary pipeline en % tenants
- `E05-F05-T08` — Rollback a pipeline anterior
- `E05-F05-T09` — Definir Acceptance Criteria medibles para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T10` — Agregar métricas RED/USE relevantes para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T11` — Escribir ADR si hay desvío de arquitectura para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T12` — Preparar feature flag + plan de rollback para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T13` — Actualizar OpenAPI/event schema si aplica para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T14` — Ejecutar checklist tenant isolation para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T15` — Actualizar runbook operativo para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T16` — Demo interna de 10 minutos documentada para E05-F05 (Replay, golden sets & quality gates)
- `E05-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E05-F05
- `E05-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E05-F05
- `E05-F05-T19` — Añadir tests de regresión golden si E05-F05 toca motores
- `E05-F05-T20` — Instrumentar traces spans para E05-F05
- `E05-F05-T21` — Documentar dependencias de eventos en E05-F05
- `E05-F05-T22` — Checklist seguridad secretos/PII en E05-F05
- `E05-F05-T23` — Validar performance budget preliminar de E05-F05
- `E05-F05-T24` — Actualizar mapping Architecture domain ↔ E05-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E05-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.06 E06 — Geometry Engine

Prioridad P0 · Complejidad XL · Depende de: E05, E07

#### E06-F01 — Calibration de escala

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E06` que avance el objetivo (Motor determinista de medición/topología: calibración de escala, L/A/V/conteos, validadores; escribe solo vía ChangeSets...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E06-F01-T01` — Modelo Calibration por PlanSheet
- `E06-F01-T02` — API/UI dos puntos + distancia real
- `E06-F01-T03` — Evento CalibracionActualizada
- `E06-F01-T04` — Bloquear compute si calibration_status != ready
- `E06-F01-T05` — Tests unidades m/cm/mm
- `E06-F01-T06` — Persistencia en ProjectSettings defaults
- `E06-F01-T07` — Métrica time_to_calibrate
- `E06-F01-T08` — UX wizard LATAM
- `E06-F01-T09` — Definir Acceptance Criteria medibles para E06-F01 (Calibration de escala)
- `E06-F01-T10` — Agregar métricas RED/USE relevantes para E06-F01 (Calibration de escala)
- `E06-F01-T11` — Escribir ADR si hay desvío de arquitectura para E06-F01 (Calibration de escala)
- `E06-F01-T12` — Preparar feature flag + plan de rollback para E06-F01 (Calibration de escala)
- `E06-F01-T13` — Actualizar OpenAPI/event schema si aplica para E06-F01 (Calibration de escala)
- `E06-F01-T14` — Ejecutar checklist tenant isolation para E06-F01 (Calibration de escala)
- `E06-F01-T15` — Actualizar runbook operativo para E06-F01 (Calibration de escala)
- `E06-F01-T16` — Demo interna de 10 minutos documentada para E06-F01 (Calibration de escala)
- `E06-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E06-F01
- `E06-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E06-F01
- `E06-F01-T19` — Añadir tests de regresión golden si E06-F01 toca motores
- `E06-F01-T20` — Instrumentar traces spans para E06-F01
- `E06-F01-T21` — Documentar dependencias de eventos en E06-F01
- `E06-F01-T22` — Checklist seguridad secretos/PII en E06-F01
- `E06-F01-T23` — Validar performance budget preliminar de E06-F01
- `E06-F01-T24` — Actualizar mapping Architecture domain ↔ E06-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E06-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E06-F02 — Compute measures determinista

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E06` que avance el objetivo (Motor determinista de medición/topología: calibración de escala, L/A/V/conteos, validadores; escribe solo vía ChangeSets...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E06-F02-T01` — Cálculo L/A/V/count desde evidencias+calibración
- `E06-F02-T02` — Versionado de geometry engine
- `E06-F02-T03` — Evento GeometriaCalculada
- `E06-F02-T04` — Escritura ElementGeometry vía ChangeSet
- `E06-F02-T05` — Tests golden numeric tolerance
- `E06-F02-T06` — Incremental recompute por sheet
- `E06-F02-T07` — Benchmark p95 compute
- `E06-F02-T08` — Prohibir floats de dinero aquí (solo geometría)
- `E06-F02-T09` — Definir Acceptance Criteria medibles para E06-F02 (Compute measures determinista)
- `E06-F02-T10` — Agregar métricas RED/USE relevantes para E06-F02 (Compute measures determinista)
- `E06-F02-T11` — Escribir ADR si hay desvío de arquitectura para E06-F02 (Compute measures determinista)
- `E06-F02-T12` — Preparar feature flag + plan de rollback para E06-F02 (Compute measures determinista)
- `E06-F02-T13` — Actualizar OpenAPI/event schema si aplica para E06-F02 (Compute measures determinista)
- `E06-F02-T14` — Ejecutar checklist tenant isolation para E06-F02 (Compute measures determinista)
- `E06-F02-T15` — Actualizar runbook operativo para E06-F02 (Compute measures determinista)
- `E06-F02-T16` — Demo interna de 10 minutos documentada para E06-F02 (Compute measures determinista)
- `E06-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E06-F02
- `E06-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E06-F02
- `E06-F02-T19` — Añadir tests de regresión golden si E06-F02 toca motores
- `E06-F02-T20` — Instrumentar traces spans para E06-F02
- `E06-F02-T21` — Documentar dependencias de eventos en E06-F02
- `E06-F02-T22` — Checklist seguridad secretos/PII en E06-F02
- `E06-F02-T23` — Validar performance budget preliminar de E06-F02
- `E06-F02-T24` — Actualizar mapping Architecture domain ↔ E06-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E06-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E06-F03 — Validators & GeometryIssue

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E06` que avance el objetivo (Motor determinista de medición/topología: calibración de escala, L/A/V/conteos, validadores; escribe solo vía ChangeSets...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E06-F03-T01` — Validadores: cierre polígono, solapes, escala ausente, degenerados
- `E06-F03-T02` — Evento GeometriaInvalidaDetectada
- `E06-F03-T03` — Panel issues en Studio
- `E06-F03-T04` — Severidades blocker/warning
- `E06-F03-T05` — Tests cada validador
- `E06-F03-T06` — No auto-fix silencioso sin ChangeOp
- `E06-F03-T07` — Métrica issues_per_sheet
- `E06-F03-T08` — Deep link issue→canvas
- `E06-F03-T09` — Definir Acceptance Criteria medibles para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T10` — Agregar métricas RED/USE relevantes para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T11` — Escribir ADR si hay desvío de arquitectura para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T12` — Preparar feature flag + plan de rollback para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T13` — Actualizar OpenAPI/event schema si aplica para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T14` — Ejecutar checklist tenant isolation para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T15` — Actualizar runbook operativo para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T16` — Demo interna de 10 minutos documentada para E06-F03 (Validators & GeometryIssue)
- `E06-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E06-F03
- `E06-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E06-F03
- `E06-F03-T19` — Añadir tests de regresión golden si E06-F03 toca motores
- `E06-F03-T20` — Instrumentar traces spans para E06-F03
- `E06-F03-T21` — Documentar dependencias de eventos en E06-F03
- `E06-F03-T22` — Checklist seguridad secretos/PII en E06-F03
- `E06-F03-T23` — Validar performance budget preliminar de E06-F03
- `E06-F03-T24` — Actualizar mapping Architecture domain ↔ E06-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E06-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E06-F04 — Spatial relations light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E06` que avance el objetivo (Motor determinista de medición/topología: calibración de escala, L/A/V/conteos, validadores; escribe solo vía ChangeSets...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E06-F04-T01` — Connections básicas entre elementos
- `E06-F04-T02` — Containment space/element hints
- `E06-F04-T03` — Tests topología simple
- `E06-F04-T04` — Payload refs eficientes
- `E06-F04-T05` — Documentar límites (no GIS completo)
- `E06-F04-T06` — Feature flag relations
- `E06-F04-T07` — Eventos ModeloActualizado summary
- `E06-F04-T08` — Perf budget relations
- `E06-F04-T09` — Definir Acceptance Criteria medibles para E06-F04 (Spatial relations light)
- `E06-F04-T10` — Agregar métricas RED/USE relevantes para E06-F04 (Spatial relations light)
- `E06-F04-T11` — Escribir ADR si hay desvío de arquitectura para E06-F04 (Spatial relations light)
- `E06-F04-T12` — Preparar feature flag + plan de rollback para E06-F04 (Spatial relations light)
- `E06-F04-T13` — Actualizar OpenAPI/event schema si aplica para E06-F04 (Spatial relations light)
- `E06-F04-T14` — Ejecutar checklist tenant isolation para E06-F04 (Spatial relations light)
- `E06-F04-T15` — Actualizar runbook operativo para E06-F04 (Spatial relations light)
- `E06-F04-T16` — Demo interna de 10 minutos documentada para E06-F04 (Spatial relations light)
- `E06-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E06-F04
- `E06-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E06-F04
- `E06-F04-T19` — Añadir tests de regresión golden si E06-F04 toca motores
- `E06-F04-T20` — Instrumentar traces spans para E06-F04
- `E06-F04-T21` — Documentar dependencias de eventos en E06-F04
- `E06-F04-T22` — Checklist seguridad secretos/PII en E06-F04
- `E06-F04-T23` — Validar performance budget preliminar de E06-F04
- `E06-F04-T24` — Actualizar mapping Architecture domain ↔ E06-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E06-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E06-F05 — Integration contract con MDO

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E06` que avance el objetivo (Motor determinista de medición/topología: calibración de escala, L/A/V/conteos, validadores; escribe solo vía ChangeSets...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E06-F05-T01` — ChangeOp types para geometry upsert
- `E06-F05-T02` — Idempotencia apply
- `E06-F05-T03` — AuthZ editor+
- `E06-F05-T04` — Tests isolation
- `E06-F05-T05` — Projection invalidate hooks
- `E06-F05-T06` — Trace geometry→version_id
- `E06-F05-T07` — Docs contrato L1→L2
- `E06-F05-T08` — Arch test: geometry no importa costs
- `E06-F05-T09` — Definir Acceptance Criteria medibles para E06-F05 (Integration contract con MDO)
- `E06-F05-T10` — Agregar métricas RED/USE relevantes para E06-F05 (Integration contract con MDO)
- `E06-F05-T11` — Escribir ADR si hay desvío de arquitectura para E06-F05 (Integration contract con MDO)
- `E06-F05-T12` — Preparar feature flag + plan de rollback para E06-F05 (Integration contract con MDO)
- `E06-F05-T13` — Actualizar OpenAPI/event schema si aplica para E06-F05 (Integration contract con MDO)
- `E06-F05-T14` — Ejecutar checklist tenant isolation para E06-F05 (Integration contract con MDO)
- `E06-F05-T15` — Actualizar runbook operativo para E06-F05 (Integration contract con MDO)
- `E06-F05-T16` — Demo interna de 10 minutos documentada para E06-F05 (Integration contract con MDO)
- `E06-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E06-F05
- `E06-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E06-F05
- `E06-F05-T19` — Añadir tests de regresión golden si E06-F05 toca motores
- `E06-F05-T20` — Instrumentar traces spans para E06-F05
- `E06-F05-T21` — Documentar dependencias de eventos en E06-F05
- `E06-F05-T22` — Checklist seguridad secretos/PII en E06-F05
- `E06-F05-T23` — Validar performance budget preliminar de E06-F05
- `E06-F05-T24` — Actualizar mapping Architecture domain ↔ E06-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E06-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.07 E07 — MDO Core (entities, versions, changesets)

Prioridad P0 · Complejidad XL · Depende de: E01, E02, E04

#### E07-F01 — MDO schema v1 entities

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E07` que avance el objetivo (Implementar MDO como SoT: grafo espacial/sistemas/elementos, ProjectVersion, ChangeSet/ChangeOp, proyecciones y lineage....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E07-F01-T01` — Modelar Site/Building/Level/Space/Zone
- `E07-F01-T02` — Modelar System/Element/Assembly/ParameterSet
- `E07-F01-T03` — IDs estables + lineage fields
- `E07-F01-T04` — Validaciones de grafo mínimas
- `E07-F01-T05` — Migraciones expand
- `E07-F01-T06` — Seed tipologías core LATAM refs
- `E07-F01-T07` — Tests integridad referencial lógica
- `E07-F01-T08` — Documentar límites MDO (qué NO es)
- `E07-F01-T09` — Índices tenant/project/version
- `E07-F01-T10` — Soft-delete policies
- `E07-F01-T11` — Definir Acceptance Criteria medibles para E07-F01 (MDO schema v1 entities)
- `E07-F01-T12` — Agregar métricas RED/USE relevantes para E07-F01 (MDO schema v1 entities)
- `E07-F01-T13` — Escribir ADR si hay desvío de arquitectura para E07-F01 (MDO schema v1 entities)
- `E07-F01-T14` — Preparar feature flag + plan de rollback para E07-F01 (MDO schema v1 entities)
- `E07-F01-T15` — Actualizar OpenAPI/event schema si aplica para E07-F01 (MDO schema v1 entities)
- `E07-F01-T16` — Ejecutar checklist tenant isolation para E07-F01 (MDO schema v1 entities)
- `E07-F01-T17` — Actualizar runbook operativo para E07-F01 (MDO schema v1 entities)
- `E07-F01-T18` — Demo interna de 10 minutos documentada para E07-F01 (MDO schema v1 entities)
- `E07-F01-T19` — Revisar compatibilidad Free/Pro/Enterprise en E07-F01
- `E07-F01-T20` — Verificar que no se rompe wedge color→qty→moneda local tras E07-F01
- `E07-F01-T21` — Añadir tests de regresión golden si E07-F01 toca motores
- `E07-F01-T22` — Instrumentar traces spans para E07-F01
- `E07-F01-T23` — Documentar dependencias de eventos en E07-F01
- `E07-F01-T24` — Checklist seguridad secretos/PII en E07-F01
- `E07-F01-T25` — Validar performance budget preliminar de E07-F01
- `E07-F01-T26` — Actualizar mapping Architecture domain ↔ E07-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E07-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E07-F02 — ProjectVersion lifecycle

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E07` que avance el objetivo (Implementar MDO como SoT: grafo espacial/sistemas/elementos, ProjectVersion, ChangeSet/ChangeOp, proyecciones y lineage....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E07-F02-T01` — Crear versiones; cerrar inmutable
- `E07-F02-T02` — parent_version_id chain
- `E07-F02-T03` — is_baseline flag
- `E07-F02-T04` — Summary change_summary
- `E07-F02-T05` — Tests immutability enforce
- `E07-F02-T06` — API get version tree
- `E07-F02-T07` — UI version badge
- `E07-F02-T08` — Evento ModeloActualizado
- `E07-F02-T09` — Definir Acceptance Criteria medibles para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T10` — Agregar métricas RED/USE relevantes para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T11` — Escribir ADR si hay desvío de arquitectura para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T12` — Preparar feature flag + plan de rollback para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T13` — Actualizar OpenAPI/event schema si aplica para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T14` — Ejecutar checklist tenant isolation para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T15` — Actualizar runbook operativo para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T16` — Demo interna de 10 minutos documentada para E07-F02 (ProjectVersion lifecycle)
- `E07-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E07-F02
- `E07-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E07-F02
- `E07-F02-T19` — Añadir tests de regresión golden si E07-F02 toca motores
- `E07-F02-T20` — Instrumentar traces spans para E07-F02
- `E07-F02-T21` — Documentar dependencias de eventos en E07-F02
- `E07-F02-T22` — Checklist seguridad secretos/PII en E07-F02
- `E07-F02-T23` — Validar performance budget preliminar de E07-F02
- `E07-F02-T24` — Actualizar mapping Architecture domain ↔ E07-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E07-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E07-F03 — ChangeSet / ChangeOp engine

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E07` que avance el objetivo (Implementar MDO como SoT: grafo espacial/sistemas/elementos, ProjectVersion, ChangeSet/ChangeOp, proyecciones y lineage....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E07-F03-T01` — ChangeSet draft/confirmed/conflict
- `E07-F03-T02` — ChangeOp add/update/remove
- `E07-F03-T03` — Apply idempotent
- `E07-F03-T04` — Eventos ChangeSetCreado/Confirmado
- `E07-F03-T05` — Optimistic concurrency
- `E07-F03-T06` — Tests conflict detection básica
- `E07-F03-T07` — AuthZ author roles
- `E07-F03-T08` — Audit before/after refs
- `E07-F03-T09` — Prohibir apply sin tenant check
- `E07-F03-T10` — Métricas ops_per_changeset
- `E07-F03-T11` — Definir Acceptance Criteria medibles para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T12` — Agregar métricas RED/USE relevantes para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T13` — Escribir ADR si hay desvío de arquitectura para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T14` — Preparar feature flag + plan de rollback para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T15` — Actualizar OpenAPI/event schema si aplica para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T16` — Ejecutar checklist tenant isolation para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T17` — Actualizar runbook operativo para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T18` — Demo interna de 10 minutos documentada para E07-F03 (ChangeSet / ChangeOp engine)
- `E07-F03-T19` — Revisar compatibilidad Free/Pro/Enterprise en E07-F03
- `E07-F03-T20` — Verificar que no se rompe wedge color→qty→moneda local tras E07-F03
- `E07-F03-T21` — Añadir tests de regresión golden si E07-F03 toca motores
- `E07-F03-T22` — Instrumentar traces spans para E07-F03
- `E07-F03-T23` — Documentar dependencias de eventos en E07-F03
- `E07-F03-T24` — Checklist seguridad secretos/PII en E07-F03
- `E07-F03-T25` — Validar performance budget preliminar de E07-F03
- `E07-F03-T26` — Actualizar mapping Architecture domain ↔ E07-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E07-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E07-F04 — Projections materializadas

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E07` que avance el objetivo (Implementar MDO como SoT: grafo espacial/sistemas/elementos, ProjectVersion, ChangeSet/ChangeOp, proyecciones y lineage....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E07-F04-T01` — Takeoff projection skeleton
- `E07-F04-T02` — Model tree projection
- `E07-F04-T03` — Invalidación ProyeccionInvalidada
- `E07-F04-T04` — Rebuild job
- `E07-F04-T05` — Cache keys versionados
- `E07-F04-T06` — Tests eventual consistency window
- `E07-F04-T07` — Perf budget rebuild
- `E07-F04-T08` — API read projections
- `E07-F04-T09` — Definir Acceptance Criteria medibles para E07-F04 (Projections materializadas)
- `E07-F04-T10` — Agregar métricas RED/USE relevantes para E07-F04 (Projections materializadas)
- `E07-F04-T11` — Escribir ADR si hay desvío de arquitectura para E07-F04 (Projections materializadas)
- `E07-F04-T12` — Preparar feature flag + plan de rollback para E07-F04 (Projections materializadas)
- `E07-F04-T13` — Actualizar OpenAPI/event schema si aplica para E07-F04 (Projections materializadas)
- `E07-F04-T14` — Ejecutar checklist tenant isolation para E07-F04 (Projections materializadas)
- `E07-F04-T15` — Actualizar runbook operativo para E07-F04 (Projections materializadas)
- `E07-F04-T16` — Demo interna de 10 minutos documentada para E07-F04 (Projections materializadas)
- `E07-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E07-F04
- `E07-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E07-F04
- `E07-F04-T19` — Añadir tests de regresión golden si E07-F04 toca motores
- `E07-F04-T20` — Instrumentar traces spans para E07-F04
- `E07-F04-T21` — Documentar dependencias de eventos en E07-F04
- `E07-F04-T22` — Checklist seguridad secretos/PII en E07-F04
- `E07-F04-T23` — Validar performance budget preliminar de E07-F04
- `E07-F04-T24` — Actualizar mapping Architecture domain ↔ E07-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E07-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E07-F05 — Strangler: wedge escribe a MDO

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E07` que avance el objetivo (Implementar MDO como SoT: grafo espacial/sistemas/elementos, ProjectVersion, ChangeSet/ChangeOp, proyecciones y lineage....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E07-F05-T01` — Adaptar flujo color→qty para persistir Element/TakeoffLine en version
- `E07-F05-T02` — Dual-read legacy si aplica
- `E07-F05-T03` — Feature flag `mdo.wedge`
- `E07-F05-T04` — E2E wedge sobre MDO
- `E07-F05-T05` — Rollback flag
- `E07-F05-T06` — Migración datos proyectos piloto
- `E07-F05-T07` — Métrica % proyectos on MDO
- `E07-F05-T08` — Docs para soporte
- `E07-F05-T09` — Definir Acceptance Criteria medibles para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T10` — Agregar métricas RED/USE relevantes para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T11` — Escribir ADR si hay desvío de arquitectura para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T12` — Preparar feature flag + plan de rollback para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T13` — Actualizar OpenAPI/event schema si aplica para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T14` — Ejecutar checklist tenant isolation para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T15` — Actualizar runbook operativo para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T16` — Demo interna de 10 minutos documentada para E07-F05 (Strangler: wedge escribe a MDO)
- `E07-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E07-F05
- `E07-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E07-F05
- `E07-F05-T19` — Añadir tests de regresión golden si E07-F05 toca motores
- `E07-F05-T20` — Instrumentar traces spans para E07-F05
- `E07-F05-T21` — Documentar dependencias de eventos en E07-F05
- `E07-F05-T22` — Checklist seguridad secretos/PII en E07-F05
- `E07-F05-T23` — Validar performance budget preliminar de E07-F05
- `E07-F05-T24` — Actualizar mapping Architecture domain ↔ E07-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E07-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E07-F06 — Quality flags & provenance on entities

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E07` que avance el objetivo (Implementar MDO como SoT: grafo espacial/sistemas/elementos, ProjectVersion, ChangeSet/ChangeOp, proyecciones y lineage....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E07-F06-T01` — quality_flags en ElementGeometry/Element
- `E07-F06-T02` — provenance evidence_ids
- `E07-F06-T03` — API filter by quality
- `E07-F06-T04` — UI badges
- `E07-F06-T05` — Tests schema
- `E07-F06-T06` — Dashboard twin trust
- `E07-F06-T07` — Gate firmas usa quality
- `E07-F06-T08` — Docs semántica flags
- `E07-F06-T09` — Definir Acceptance Criteria medibles para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T10` — Agregar métricas RED/USE relevantes para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T11` — Escribir ADR si hay desvío de arquitectura para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T12` — Preparar feature flag + plan de rollback para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T13` — Actualizar OpenAPI/event schema si aplica para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T14` — Ejecutar checklist tenant isolation para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T15` — Actualizar runbook operativo para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T16` — Demo interna de 10 minutos documentada para E07-F06 (Quality flags & provenance on entities)
- `E07-F06-T17` — Revisar compatibilidad Free/Pro/Enterprise en E07-F06
- `E07-F06-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E07-F06
- `E07-F06-T19` — Añadir tests de regresión golden si E07-F06 toca motores
- `E07-F06-T20` — Instrumentar traces spans para E07-F06
- `E07-F06-T21` — Documentar dependencias de eventos en E07-F06
- `E07-F06-T22` — Checklist seguridad secretos/PII en E07-F06
- `E07-F06-T23` — Validar performance budget preliminar de E07-F06
- `E07-F06-T24` — Actualizar mapping Architecture domain ↔ E07-F06

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E07-F06-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.08 E08 — Materials Engine

Prioridad P0 · Complejidad L · Depende de: E06, E07

#### E08-F01 — Typology & catalog core LATAM

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E08` que avance el objetivo (Fórmulas versionadas tipología→takeoff determinista con waste, overrides auditados y provenance completa....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E08-F01-T01` — Catálogo tipologías core (muros, losas, carpetas, etc. wedge)
- `E08-F01-T02` — MaterialCatalogItem unidades
- `E08-F01-T03` — Region tags LATAM
- `E08-F01-T04` — API list/search
- `E08-F01-T05` — Seed migración
- `E08-F01-T06` — Tests unidades
- `E08-F01-T07` — UI mapper tipologías
- `E08-F01-T08` — Evento TipologiaMapeada
- `E08-F01-T09` — Definir Acceptance Criteria medibles para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T10` — Agregar métricas RED/USE relevantes para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T11` — Escribir ADR si hay desvío de arquitectura para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T12` — Preparar feature flag + plan de rollback para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T13` — Actualizar OpenAPI/event schema si aplica para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T14` — Ejecutar checklist tenant isolation para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T15` — Actualizar runbook operativo para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T16` — Demo interna de 10 minutos documentada para E08-F01 (Typology & catalog core LATAM)
- `E08-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E08-F01
- `E08-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E08-F01
- `E08-F01-T19` — Añadir tests de regresión golden si E08-F01 toca motores
- `E08-F01-T20` — Instrumentar traces spans para E08-F01
- `E08-F01-T21` — Documentar dependencias de eventos en E08-F01
- `E08-F01-T22` — Checklist seguridad secretos/PII en E08-F01
- `E08-F01-T23` — Validar performance budget preliminar de E08-F01
- `E08-F01-T24` — Actualizar mapping Architecture domain ↔ E08-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E08-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E08-F02 — Formula engine versionado

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E08` que avance el objetivo (Fórmulas versionadas tipología→takeoff determinista con waste, overrides auditados y provenance completa....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E08-F02-T01` — Formula expression_ref + inputs + unit_out
- `E08-F02-T02` — Publicación FormulaVersionPublicada
- `E08-F02-T03` — Sandbox eval determinista
- `E08-F02-T04` — Golden tests fórmulas wedge
- `E08-F02-T05` — WasteFactor aplicado explícito
- `E08-F02-T06` — Docs autoring fórmulas
- `E08-F02-T07` — Prohibir I/O en fórmulas
- `E08-F02-T08` — Benchmark eval 10k lines
- `E08-F02-T09` — Definir Acceptance Criteria medibles para E08-F02 (Formula engine versionado)
- `E08-F02-T10` — Agregar métricas RED/USE relevantes para E08-F02 (Formula engine versionado)
- `E08-F02-T11` — Escribir ADR si hay desvío de arquitectura para E08-F02 (Formula engine versionado)
- `E08-F02-T12` — Preparar feature flag + plan de rollback para E08-F02 (Formula engine versionado)
- `E08-F02-T13` — Actualizar OpenAPI/event schema si aplica para E08-F02 (Formula engine versionado)
- `E08-F02-T14` — Ejecutar checklist tenant isolation para E08-F02 (Formula engine versionado)
- `E08-F02-T15` — Actualizar runbook operativo para E08-F02 (Formula engine versionado)
- `E08-F02-T16` — Demo interna de 10 minutos documentada para E08-F02 (Formula engine versionado)
- `E08-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E08-F02
- `E08-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E08-F02
- `E08-F02-T19` — Añadir tests de regresión golden si E08-F02 toca motores
- `E08-F02-T20` — Instrumentar traces spans para E08-F02
- `E08-F02-T21` — Documentar dependencias de eventos en E08-F02
- `E08-F02-T22` — Checklist seguridad secretos/PII en E08-F02
- `E08-F02-T23` — Validar performance budget preliminar de E08-F02
- `E08-F02-T24` — Actualizar mapping Architecture domain ↔ E08-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E08-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E08-F03 — Takeoff compute & lines

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E08` que avance el objetivo (Fórmulas versionadas tipología→takeoff determinista con waste, overrides auditados y provenance completa....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E08-F03-T01` — Generar TakeoffLine por element/material
- `E08-F03-T02` — Campos provenance formula_id/evidence
- `E08-F03-T03` — Evento MaterialCalculado
- `E08-F03-T04` — Incremental recompute
- `E08-F03-T05` — API GET takeoff filtrable
- `E08-F03-T06` — UI tabla takeoff
- `E08-F03-T07` — Tests idempotencia
- `E08-F03-T08` — Métricas lines_count / low_confidence_pct
- `E08-F03-T09` — Definir Acceptance Criteria medibles para E08-F03 (Takeoff compute & lines)
- `E08-F03-T10` — Agregar métricas RED/USE relevantes para E08-F03 (Takeoff compute & lines)
- `E08-F03-T11` — Escribir ADR si hay desvío de arquitectura para E08-F03 (Takeoff compute & lines)
- `E08-F03-T12` — Preparar feature flag + plan de rollback para E08-F03 (Takeoff compute & lines)
- `E08-F03-T13` — Actualizar OpenAPI/event schema si aplica para E08-F03 (Takeoff compute & lines)
- `E08-F03-T14` — Ejecutar checklist tenant isolation para E08-F03 (Takeoff compute & lines)
- `E08-F03-T15` — Actualizar runbook operativo para E08-F03 (Takeoff compute & lines)
- `E08-F03-T16` — Demo interna de 10 minutos documentada para E08-F03 (Takeoff compute & lines)
- `E08-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E08-F03
- `E08-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E08-F03
- `E08-F03-T19` — Añadir tests de regresión golden si E08-F03 toca motores
- `E08-F03-T20` — Instrumentar traces spans para E08-F03
- `E08-F03-T21` — Documentar dependencias de eventos en E08-F03
- `E08-F03-T22` — Checklist seguridad secretos/PII en E08-F03
- `E08-F03-T23` — Validar performance budget preliminar de E08-F03
- `E08-F03-T24` — Actualizar mapping Architecture domain ↔ E08-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E08-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E08-F04 — Overrides HITL

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E08` que avance el objetivo (Fórmulas versionadas tipología→takeoff determinista con waste, overrides auditados y provenance completa....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E08-F04-T01` — TakeoffOverride con reason obligatoria
- `E08-F04-T02` — Evento TakeoffOverrideAplicado
- `E08-F04-T03` — AuthZ roles
- `E08-F04-T04` — Audit append-only
- `E08-F04-T05` — UI modal override
- `E08-F04-T06` — Tests no override anónimo
- `E08-F04-T07` — Impacto en presupuesto marcado
- `E08-F04-T08` — Report overrides count
- `E08-F04-T09` — Definir Acceptance Criteria medibles para E08-F04 (Overrides HITL)
- `E08-F04-T10` — Agregar métricas RED/USE relevantes para E08-F04 (Overrides HITL)
- `E08-F04-T11` — Escribir ADR si hay desvío de arquitectura para E08-F04 (Overrides HITL)
- `E08-F04-T12` — Preparar feature flag + plan de rollback para E08-F04 (Overrides HITL)
- `E08-F04-T13` — Actualizar OpenAPI/event schema si aplica para E08-F04 (Overrides HITL)
- `E08-F04-T14` — Ejecutar checklist tenant isolation para E08-F04 (Overrides HITL)
- `E08-F04-T15` — Actualizar runbook operativo para E08-F04 (Overrides HITL)
- `E08-F04-T16` — Demo interna de 10 minutos documentada para E08-F04 (Overrides HITL)
- `E08-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E08-F04
- `E08-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E08-F04
- `E08-F04-T19` — Añadir tests de regresión golden si E08-F04 toca motores
- `E08-F04-T20` — Instrumentar traces spans para E08-F04
- `E08-F04-T21` — Documentar dependencias de eventos en E08-F04
- `E08-F04-T22` — Checklist seguridad secretos/PII en E08-F04
- `E08-F04-T23` — Validar performance budget preliminar de E08-F04
- `E08-F04-T24` — Actualizar mapping Architecture domain ↔ E08-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E08-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E08-F05 — Plugin-ready formula contracts

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E08` que avance el objetivo (Fórmulas versionadas tipología→takeoff determinista con waste, overrides auditados y provenance completa....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E08-F05-T01` — Interface capability materials.formulas
- `E08-F05-T02` — Validación schema params tipología
- `E08-F05-T03` — Tests contrato
- `E08-F05-T04` — Docs para E19/E20
- `E08-F05-T05` — Feature flag external formulas off by default
- `E08-F05-T06` — Compat version field
- `E08-F05-T07` — Ejemplo fórmula plugin stub
- `E08-F05-T08` — Arch test core sin hardcode steel/gas
- `E08-F05-T09` — Definir Acceptance Criteria medibles para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T10` — Agregar métricas RED/USE relevantes para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T11` — Escribir ADR si hay desvío de arquitectura para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T12` — Preparar feature flag + plan de rollback para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T13` — Actualizar OpenAPI/event schema si aplica para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T14` — Ejecutar checklist tenant isolation para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T15` — Actualizar runbook operativo para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T16` — Demo interna de 10 minutos documentada para E08-F05 (Plugin-ready formula contracts)
- `E08-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E08-F05
- `E08-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E08-F05
- `E08-F05-T19` — Añadir tests de regresión golden si E08-F05 toca motores
- `E08-F05-T20` — Instrumentar traces spans para E08-F05
- `E08-F05-T21` — Documentar dependencias de eventos en E08-F05
- `E08-F05-T22` — Checklist seguridad secretos/PII en E08-F05
- `E08-F05-T23` — Validar performance budget preliminar de E08-F05
- `E08-F05-T24` — Actualizar mapping Architecture domain ↔ E08-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E08-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.09 E09 — Costs & PriceBooks

Prioridad P0 · Complejidad L · Depende de: E08, E02

#### E09-F01 — Pricebook management

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E09` que avance el objetivo (Valorizar takeoff con PriceBooks, moneda local, ajustes y totales por version/scenario....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E09-F01-T01` — Pricebook org/project scoped
- `E09-F01-T02` — PriceItem material_code/unit_price/taxes
- `E09-F01-T03` — Import CSV async job
- `E09-F01-T04` — Evento PricebookActualizado
- `E09-F01-T05` — UI editor
- `E09-F01-T06` — Tests decimal rounding LATAM
- `E09-F01-T07` — Versionado light valid_from
- `E09-F01-T08` — AuthZ admin/editor
- `E09-F01-T09` — Definir Acceptance Criteria medibles para E09-F01 (Pricebook management)
- `E09-F01-T10` — Agregar métricas RED/USE relevantes para E09-F01 (Pricebook management)
- `E09-F01-T11` — Escribir ADR si hay desvío de arquitectura para E09-F01 (Pricebook management)
- `E09-F01-T12` — Preparar feature flag + plan de rollback para E09-F01 (Pricebook management)
- `E09-F01-T13` — Actualizar OpenAPI/event schema si aplica para E09-F01 (Pricebook management)
- `E09-F01-T14` — Ejecutar checklist tenant isolation para E09-F01 (Pricebook management)
- `E09-F01-T15` — Actualizar runbook operativo para E09-F01 (Pricebook management)
- `E09-F01-T16` — Demo interna de 10 minutos documentada para E09-F01 (Pricebook management)
- `E09-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E09-F01
- `E09-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E09-F01
- `E09-F01-T19` — Añadir tests de regresión golden si E09-F01 toca motores
- `E09-F01-T20` — Instrumentar traces spans para E09-F01
- `E09-F01-T21` — Documentar dependencias de eventos en E09-F01
- `E09-F01-T22` — Checklist seguridad secretos/PII en E09-F01
- `E09-F01-T23` — Validar performance budget preliminar de E09-F01
- `E09-F01-T24` — Actualizar mapping Architecture domain ↔ E09-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E09-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E09-F02 — Currency & FX

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E09` que avance el objetivo (Valorizar takeoff con PriceBooks, moneda local, ajustes y totales por version/scenario....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E09-F02-T01` — Project.currency default ARS
- `E09-F02-T02` — CurrencyRate as_of
- `E09-F02-T03` — Evento CurrencyRatesActualizadas
- `E09-F02-T04` — Display localization
- `E09-F02-T05` — Tests conversión
- `E09-F02-T06` — Freeze rates policy doc
- `E09-F02-T07` — UI currency settings
- `E09-F02-T08` — Prohibir float binary money
- `E09-F02-T09` — Definir Acceptance Criteria medibles para E09-F02 (Currency & FX)
- `E09-F02-T10` — Agregar métricas RED/USE relevantes para E09-F02 (Currency & FX)
- `E09-F02-T11` — Escribir ADR si hay desvío de arquitectura para E09-F02 (Currency & FX)
- `E09-F02-T12` — Preparar feature flag + plan de rollback para E09-F02 (Currency & FX)
- `E09-F02-T13` — Actualizar OpenAPI/event schema si aplica para E09-F02 (Currency & FX)
- `E09-F02-T14` — Ejecutar checklist tenant isolation para E09-F02 (Currency & FX)
- `E09-F02-T15` — Actualizar runbook operativo para E09-F02 (Currency & FX)
- `E09-F02-T16` — Demo interna de 10 minutos documentada para E09-F02 (Currency & FX)
- `E09-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E09-F02
- `E09-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E09-F02
- `E09-F02-T19` — Añadir tests de regresión golden si E09-F02 toca motores
- `E09-F02-T20` — Instrumentar traces spans para E09-F02
- `E09-F02-T21` — Documentar dependencias de eventos en E09-F02
- `E09-F02-T22` — Checklist seguridad secretos/PII en E09-F02
- `E09-F02-T23` — Validar performance budget preliminar de E09-F02
- `E09-F02-T24` — Actualizar mapping Architecture domain ↔ E09-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E09-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E09-F03 — Budget compute

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E09` que avance el objetivo (Valorizar takeoff con PriceBooks, moneda local, ajustes y totales por version/scenario....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E09-F03-T01` — Budget + BudgetLine desde takeoff
- `E09-F03-T02` — Adjustments auditables
- `E09-F03-T03` — Eventos PresupuestoCreado/CostoActualizado
- `E09-F03-T04` — Incremental update
- `E09-F03-T05` — API get totals by category
- `E09-F03-T06` — UI budget summary
- `E09-F03-T07` — Tests idempotencia
- `E09-F03-T08` — Métricas compute latency
- `E09-F03-T09` — Definir Acceptance Criteria medibles para E09-F03 (Budget compute)
- `E09-F03-T10` — Agregar métricas RED/USE relevantes para E09-F03 (Budget compute)
- `E09-F03-T11` — Escribir ADR si hay desvío de arquitectura para E09-F03 (Budget compute)
- `E09-F03-T12` — Preparar feature flag + plan de rollback para E09-F03 (Budget compute)
- `E09-F03-T13` — Actualizar OpenAPI/event schema si aplica para E09-F03 (Budget compute)
- `E09-F03-T14` — Ejecutar checklist tenant isolation para E09-F03 (Budget compute)
- `E09-F03-T15` — Actualizar runbook operativo para E09-F03 (Budget compute)
- `E09-F03-T16` — Demo interna de 10 minutos documentada para E09-F03 (Budget compute)
- `E09-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E09-F03
- `E09-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E09-F03
- `E09-F03-T19` — Añadir tests de regresión golden si E09-F03 toca motores
- `E09-F03-T20` — Instrumentar traces spans para E09-F03
- `E09-F03-T21` — Documentar dependencias de eventos en E09-F03
- `E09-F03-T22` — Checklist seguridad secretos/PII en E09-F03
- `E09-F03-T23` — Validar performance budget preliminar de E09-F03
- `E09-F03-T24` — Actualizar mapping Architecture domain ↔ E09-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E09-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E09-F04 — Plan gates on costs features

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E09` que avance el objetivo (Valorizar takeoff con PriceBooks, moneda local, ajustes y totales por version/scenario....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E09-F04-T01` — Free: 1 pricebook, export limitado
- `E09-F04-T02` — Pro: multi pricebook, scenarios cost later
- `E09-F04-T03` — Entitlements checks
- `E09-F04-T04` — Tests plan matrix
- `E09-F04-T05` — UX upgrade prompts
- `E09-F04-T06` — Meter exports
- `E09-F04-T07` — Docs límites
- `E09-F04-T08` — Admin enterprise custom prices sync stub
- `E09-F04-T09` — Definir Acceptance Criteria medibles para E09-F04 (Plan gates on costs features)
- `E09-F04-T10` — Agregar métricas RED/USE relevantes para E09-F04 (Plan gates on costs features)
- `E09-F04-T11` — Escribir ADR si hay desvío de arquitectura para E09-F04 (Plan gates on costs features)
- `E09-F04-T12` — Preparar feature flag + plan de rollback para E09-F04 (Plan gates on costs features)
- `E09-F04-T13` — Actualizar OpenAPI/event schema si aplica para E09-F04 (Plan gates on costs features)
- `E09-F04-T14` — Ejecutar checklist tenant isolation para E09-F04 (Plan gates on costs features)
- `E09-F04-T15` — Actualizar runbook operativo para E09-F04 (Plan gates on costs features)
- `E09-F04-T16` — Demo interna de 10 minutos documentada para E09-F04 (Plan gates on costs features)
- `E09-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E09-F04
- `E09-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E09-F04
- `E09-F04-T19` — Añadir tests de regresión golden si E09-F04 toca motores
- `E09-F04-T20` — Instrumentar traces spans para E09-F04
- `E09-F04-T21` — Documentar dependencias de eventos en E09-F04
- `E09-F04-T22` — Checklist seguridad secretos/PII en E09-F04
- `E09-F04-T23` — Validar performance budget preliminar de E09-F04
- `E09-F04-T24` — Actualizar mapping Architecture domain ↔ E09-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E09-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.10 E10 — Takeoff Projections & Signed Budgets

Prioridad P0 · Complejidad M · Depende de: E09, E07

#### E10-F01 — Takeoff/Cost projections API

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E10` que avance el objetivo (Proyecciones de takeoff/costo estables y SignedBudget inmutable con hash, HITL y lineage comercial....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E10-F01-T01` — Materializar proyección takeoff por version
- `E10-F01-T02` — Materializar proyección cost
- `E10-F01-T03` — ETags / cache
- `E10-F01-T04` — Invalidación correcta
- `E10-F01-T05` — Tests consistency vs lines
- `E10-F01-T06` — UI views read models
- `E10-F01-T07` — Perf budget
- `E10-F01-T08` — Docs consumers (chat/reports)
- `E10-F01-T09` — Definir Acceptance Criteria medibles para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T10` — Agregar métricas RED/USE relevantes para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T11` — Escribir ADR si hay desvío de arquitectura para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T12` — Preparar feature flag + plan de rollback para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T13` — Actualizar OpenAPI/event schema si aplica para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T14` — Ejecutar checklist tenant isolation para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T15` — Actualizar runbook operativo para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T16` — Demo interna de 10 minutos documentada para E10-F01 (Takeoff/Cost projections API)
- `E10-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E10-F01
- `E10-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E10-F01
- `E10-F01-T19` — Añadir tests de regresión golden si E10-F01 toca motores
- `E10-F01-T20` — Instrumentar traces spans para E10-F01
- `E10-F01-T21` — Documentar dependencias de eventos en E10-F01
- `E10-F01-T22` — Checklist seguridad secretos/PII en E10-F01
- `E10-F01-T23` — Validar performance budget preliminar de E10-F01
- `E10-F01-T24` — Actualizar mapping Architecture domain ↔ E10-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E10-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E10-F02 — SignedBudget HITL

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E10` que avance el objetivo (Proyecciones de takeoff/costo estables y SignedBudget inmutable con hash, HITL y lineage comercial....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E10-F02-T01` — Wizard confirmación totales + warnings confidence
- `E10-F02-T02` — SignatureMeta actor/rol/timestamp
- `E10-F02-T03` — Hash snapshot
- `E10-F02-T04` — Evento PresupuestoFirmado
- `E10-F02-T05` — Tests immutability
- `E10-F02-T06` — Notificación interesados
- `E10-F02-T07` — Vault UI read-only
- `E10-F02-T08` — Prohibir AI auto-sign
- `E10-F02-T09` — Definir Acceptance Criteria medibles para E10-F02 (SignedBudget HITL)
- `E10-F02-T10` — Agregar métricas RED/USE relevantes para E10-F02 (SignedBudget HITL)
- `E10-F02-T11` — Escribir ADR si hay desvío de arquitectura para E10-F02 (SignedBudget HITL)
- `E10-F02-T12` — Preparar feature flag + plan de rollback para E10-F02 (SignedBudget HITL)
- `E10-F02-T13` — Actualizar OpenAPI/event schema si aplica para E10-F02 (SignedBudget HITL)
- `E10-F02-T14` — Ejecutar checklist tenant isolation para E10-F02 (SignedBudget HITL)
- `E10-F02-T15` — Actualizar runbook operativo para E10-F02 (SignedBudget HITL)
- `E10-F02-T16` — Demo interna de 10 minutos documentada para E10-F02 (SignedBudget HITL)
- `E10-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E10-F02
- `E10-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E10-F02
- `E10-F02-T19` — Añadir tests de regresión golden si E10-F02 toca motores
- `E10-F02-T20` — Instrumentar traces spans para E10-F02
- `E10-F02-T21` — Documentar dependencias de eventos en E10-F02
- `E10-F02-T22` — Checklist seguridad secretos/PII en E10-F02
- `E10-F02-T23` — Validar performance budget preliminar de E10-F02
- `E10-F02-T24` — Actualizar mapping Architecture domain ↔ E10-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E10-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E10-F03 — Commercial audit trail

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E10` que avance el objetivo (Proyecciones de takeoff/costo estables y SignedBudget inmutable con hash, HITL y lineage comercial....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E10-F03-T01` — AuditEvent enlazado
- `E10-F03-T02` — Retención no hard-delete
- `E10-F03-T03` — Export signed package (pdf later E13)
- `E10-F03-T04` — Tests legal fields
- `E10-F03-T05` — Runbook disputa de presupuesto
- `E10-F03-T06` — Métrica signed_count
- `E10-F03-T07` — Gate quality flags
- `E10-F03-T08` — Docs proceso comercial LATAM
- `E10-F03-T09` — Definir Acceptance Criteria medibles para E10-F03 (Commercial audit trail)
- `E10-F03-T10` — Agregar métricas RED/USE relevantes para E10-F03 (Commercial audit trail)
- `E10-F03-T11` — Escribir ADR si hay desvío de arquitectura para E10-F03 (Commercial audit trail)
- `E10-F03-T12` — Preparar feature flag + plan de rollback para E10-F03 (Commercial audit trail)
- `E10-F03-T13` — Actualizar OpenAPI/event schema si aplica para E10-F03 (Commercial audit trail)
- `E10-F03-T14` — Ejecutar checklist tenant isolation para E10-F03 (Commercial audit trail)
- `E10-F03-T15` — Actualizar runbook operativo para E10-F03 (Commercial audit trail)
- `E10-F03-T16` — Demo interna de 10 minutos documentada para E10-F03 (Commercial audit trail)
- `E10-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E10-F03
- `E10-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E10-F03
- `E10-F03-T19` — Añadir tests de regresión golden si E10-F03 toca motores
- `E10-F03-T20` — Instrumentar traces spans para E10-F03
- `E10-F03-T21` — Documentar dependencias de eventos en E10-F03
- `E10-F03-T22` — Checklist seguridad secretos/PII en E10-F03
- `E10-F03-T23` — Validar performance budget preliminar de E10-F03
- `E10-F03-T24` — Actualizar mapping Architecture domain ↔ E10-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E10-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.11 E11 — Scenarios (Git-like)

Prioridad P1 · Complejidad L · Depende de: E07, E08, E09

#### E11-F01 — Scenario CRUD & head versions

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E11` que avance el objetivo (Branching Git-like del MDO: Scenario, compare, merge rules básicas, promote baseline; sin romper baseline de producción....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E11-F01-T01` — Scenario branch_name/head_version_id
- `E11-F01-T02` — Evento EscenarioCreado
- `E11-F01-T03` — Límites por plan
- `E11-F01-T04` — UI switcher
- `E11-F01-T05` — Tests isolation data
- `E11-F01-T06` — Soft-delete EscenarioEliminado
- `E11-F01-T07` — AuthZ
- `E11-F01-T08` — Defaults baseline scenario
- `E11-F01-T09` — Definir Acceptance Criteria medibles para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T10` — Agregar métricas RED/USE relevantes para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T11` — Escribir ADR si hay desvío de arquitectura para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T12` — Preparar feature flag + plan de rollback para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T13` — Actualizar OpenAPI/event schema si aplica para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T14` — Ejecutar checklist tenant isolation para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T15` — Actualizar runbook operativo para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T16` — Demo interna de 10 minutos documentada para E11-F01 (Scenario CRUD & head versions)
- `E11-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E11-F01
- `E11-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E11-F01
- `E11-F01-T19` — Añadir tests de regresión golden si E11-F01 toca motores
- `E11-F01-T20` — Instrumentar traces spans para E11-F01
- `E11-F01-T21` — Documentar dependencias de eventos en E11-F01
- `E11-F01-T22` — Checklist seguridad secretos/PII en E11-F01
- `E11-F01-T23` — Validar performance budget preliminar de E11-F01
- `E11-F01-T24` — Actualizar mapping Architecture domain ↔ E11-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E11-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E11-F02 — Compare takeoff/cost

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E11` que avance el objetivo (Branching Git-like del MDO: Scenario, compare, merge rules básicas, promote baseline; sin romper baseline de producción....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E11-F02-T01` — ScenarioCompare job
- `E11-F02-T02` — Diff summary lines/totals
- `E11-F02-T03` — UI compare
- `E11-F02-T04` — Tests numeric diffs
- `E11-F02-T05` — Perf budget
- `E11-F02-T06` — Export compare csv later
- `E11-F02-T07` — Métricas compare usage
- `E11-F02-T08` — Docs interpretación diffs
- `E11-F02-T09` — Definir Acceptance Criteria medibles para E11-F02 (Compare takeoff/cost)
- `E11-F02-T10` — Agregar métricas RED/USE relevantes para E11-F02 (Compare takeoff/cost)
- `E11-F02-T11` — Escribir ADR si hay desvío de arquitectura para E11-F02 (Compare takeoff/cost)
- `E11-F02-T12` — Preparar feature flag + plan de rollback para E11-F02 (Compare takeoff/cost)
- `E11-F02-T13` — Actualizar OpenAPI/event schema si aplica para E11-F02 (Compare takeoff/cost)
- `E11-F02-T14` — Ejecutar checklist tenant isolation para E11-F02 (Compare takeoff/cost)
- `E11-F02-T15` — Actualizar runbook operativo para E11-F02 (Compare takeoff/cost)
- `E11-F02-T16` — Demo interna de 10 minutos documentada para E11-F02 (Compare takeoff/cost)
- `E11-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E11-F02
- `E11-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E11-F02
- `E11-F02-T19` — Añadir tests de regresión golden si E11-F02 toca motores
- `E11-F02-T20` — Instrumentar traces spans para E11-F02
- `E11-F02-T21` — Documentar dependencias de eventos en E11-F02
- `E11-F02-T22` — Checklist seguridad secretos/PII en E11-F02
- `E11-F02-T23` — Validar performance budget preliminar de E11-F02
- `E11-F02-T24` — Actualizar mapping Architecture domain ↔ E11-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E11-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E11-F03 — Merge MVP & conflicts

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E11` que avance el objetivo (Branching Git-like del MDO: Scenario, compare, merge rules básicas, promote baseline; sin romper baseline de producción....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E11-F03-T01` — Merge rules subset documentado
- `E11-F03-T02` — ConflictoDetectado tipos
- `E11-F03-T03` — UI resolver mínimo (accept ours/theirs)
- `E11-F03-T04` — Tests conflictos entity_id
- `E11-F03-T05` — No auto-merge silencioso money lines
- `E11-F03-T06` — Feature flag merge
- `E11-F03-T07` — Runbook merge stuck
- `E11-F03-T08` — Audit merge
- `E11-F03-T09` — Definir Acceptance Criteria medibles para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T10` — Agregar métricas RED/USE relevantes para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T11` — Escribir ADR si hay desvío de arquitectura para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T12` — Preparar feature flag + plan de rollback para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T13` — Actualizar OpenAPI/event schema si aplica para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T14` — Ejecutar checklist tenant isolation para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T15` — Actualizar runbook operativo para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T16` — Demo interna de 10 minutos documentada para E11-F03 (Merge MVP & conflicts)
- `E11-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E11-F03
- `E11-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E11-F03
- `E11-F03-T19` — Añadir tests de regresión golden si E11-F03 toca motores
- `E11-F03-T20` — Instrumentar traces spans para E11-F03
- `E11-F03-T21` — Documentar dependencias de eventos en E11-F03
- `E11-F03-T22` — Checklist seguridad secretos/PII en E11-F03
- `E11-F03-T23` — Validar performance budget preliminar de E11-F03
- `E11-F03-T24` — Actualizar mapping Architecture domain ↔ E11-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E11-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E11-F04 — Promote to baseline

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E11` que avance el objetivo (Branching Git-like del MDO: Scenario, compare, merge rules básicas, promote baseline; sin romper baseline de producción....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E11-F04-T01` — EscenarioPromovido
- `E11-F04-T02` — AuthZ owner/admin
- `E11-F04-T03` — HITL confirm
- `E11-F04-T04` — Tests baseline integrity
- `E11-F04-T05` — Notifications
- `E11-F04-T06` — Version label conventions
- `E11-F04-T07` — Prohibir promote con blockers geometry
- `E11-F04-T08` — Docs
- `E11-F04-T09` — Definir Acceptance Criteria medibles para E11-F04 (Promote to baseline)
- `E11-F04-T10` — Agregar métricas RED/USE relevantes para E11-F04 (Promote to baseline)
- `E11-F04-T11` — Escribir ADR si hay desvío de arquitectura para E11-F04 (Promote to baseline)
- `E11-F04-T12` — Preparar feature flag + plan de rollback para E11-F04 (Promote to baseline)
- `E11-F04-T13` — Actualizar OpenAPI/event schema si aplica para E11-F04 (Promote to baseline)
- `E11-F04-T14` — Ejecutar checklist tenant isolation para E11-F04 (Promote to baseline)
- `E11-F04-T15` — Actualizar runbook operativo para E11-F04 (Promote to baseline)
- `E11-F04-T16` — Demo interna de 10 minutos documentada para E11-F04 (Promote to baseline)
- `E11-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E11-F04
- `E11-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E11-F04
- `E11-F04-T19` — Añadir tests de regresión golden si E11-F04 toca motores
- `E11-F04-T20` — Instrumentar traces spans para E11-F04
- `E11-F04-T21` — Documentar dependencias de eventos en E11-F04
- `E11-F04-T22` — Checklist seguridad secretos/PII en E11-F04
- `E11-F04-T23` — Validar performance budget preliminar de E11-F04
- `E11-F04-T24` — Actualizar mapping Architecture domain ↔ E11-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E11-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.12 E12 — Frontend Workspace & Model Explorer

Prioridad P0 · Complejidad L · Depende de: E05, E07, E08, E09, E04

#### E12-F01 — Workspace shell & layout

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E12` que avance el objetivo (Studio multi-panel: canvas plano, árbol MDO, inspector, costos, jobs; i18n ES; flags por plan; sin cards innecesarias — ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E12-F01-T01` — Shell multi-panel responsive desktop-first + mobile usable
- `E12-F01-T02` — Persist layout prefs
- `E12-F01-T03` — Feature flags panels
- `E12-F01-T04` — i18n ES
- `E12-F01-T05` — Tests layout breakpoints
- `E12-F01-T06` — Performance bundle budgets
- `E12-F01-T07` — Empty states wedge
- `E12-F01-T08` — Error boundaries
- `E12-F01-T09` — Definir Acceptance Criteria medibles para E12-F01 (Workspace shell & layout)
- `E12-F01-T10` — Agregar métricas RED/USE relevantes para E12-F01 (Workspace shell & layout)
- `E12-F01-T11` — Escribir ADR si hay desvío de arquitectura para E12-F01 (Workspace shell & layout)
- `E12-F01-T12` — Preparar feature flag + plan de rollback para E12-F01 (Workspace shell & layout)
- `E12-F01-T13` — Actualizar OpenAPI/event schema si aplica para E12-F01 (Workspace shell & layout)
- `E12-F01-T14` — Ejecutar checklist tenant isolation para E12-F01 (Workspace shell & layout)
- `E12-F01-T15` — Actualizar runbook operativo para E12-F01 (Workspace shell & layout)
- `E12-F01-T16` — Demo interna de 10 minutos documentada para E12-F01 (Workspace shell & layout)
- `E12-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E12-F01
- `E12-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E12-F01
- `E12-F01-T19` — Añadir tests de regresión golden si E12-F01 toca motores
- `E12-F01-T20` — Instrumentar traces spans para E12-F01
- `E12-F01-T21` — Documentar dependencias de eventos en E12-F01
- `E12-F01-T22` — Checklist seguridad secretos/PII en E12-F01
- `E12-F01-T23` — Validar performance budget preliminar de E12-F01
- `E12-F01-T24` — Actualizar mapping Architecture domain ↔ E12-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E12-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E12-F02 — Canvas plano + overlays

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E12` que avance el objetivo (Studio multi-panel: canvas plano, árbol MDO, inspector, costos, jobs; i18n ES; flags por plan; sin cards innecesarias — ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E12-F02-T01` — Render sheet + color regions + evidences
- `E12-F02-T02` — Calibration interactions
- `E12-F02-T03` — Selection sync con explorer
- `E12-F02-T04` — Tests canvas interactions critical
- `E12-F02-T05` — Perf pan/zoom
- `E12-F02-T06` — Accessibility keyboard basics
- `E12-F02-T07` — No overlay sticker spam (design rules)
- `E12-F02-T08` — Motion sutil load/progress
- `E12-F02-T09` — Definir Acceptance Criteria medibles para E12-F02 (Canvas plano + overlays)
- `E12-F02-T10` — Agregar métricas RED/USE relevantes para E12-F02 (Canvas plano + overlays)
- `E12-F02-T11` — Escribir ADR si hay desvío de arquitectura para E12-F02 (Canvas plano + overlays)
- `E12-F02-T12` — Preparar feature flag + plan de rollback para E12-F02 (Canvas plano + overlays)
- `E12-F02-T13` — Actualizar OpenAPI/event schema si aplica para E12-F02 (Canvas plano + overlays)
- `E12-F02-T14` — Ejecutar checklist tenant isolation para E12-F02 (Canvas plano + overlays)
- `E12-F02-T15` — Actualizar runbook operativo para E12-F02 (Canvas plano + overlays)
- `E12-F02-T16` — Demo interna de 10 minutos documentada para E12-F02 (Canvas plano + overlays)
- `E12-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E12-F02
- `E12-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E12-F02
- `E12-F02-T19` — Añadir tests de regresión golden si E12-F02 toca motores
- `E12-F02-T20` — Instrumentar traces spans para E12-F02
- `E12-F02-T21` — Documentar dependencias de eventos en E12-F02
- `E12-F02-T22` — Checklist seguridad secretos/PII en E12-F02
- `E12-F02-T23` — Validar performance budget preliminar de E12-F02
- `E12-F02-T24` — Actualizar mapping Architecture domain ↔ E12-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E12-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E12-F03 — Model Explorer & Inspector

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E12` que avance el objetivo (Studio multi-panel: canvas plano, árbol MDO, inspector, costos, jobs; i18n ES; flags por plan; sin cards innecesarias — ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E12-F03-T01` — Árbol Site→…→Element
- `E12-F03-T02` — Inspector campos + quality flags
- `E12-F03-T03` — Deep links entity
- `E12-F03-T04` — Virtualized tree
- `E12-F03-T05` — Tests navigation
- `E12-F03-T06` — Optimistic UI solo no-autoritativo
- `E12-F03-T07` — Version badge
- `E12-F03-T08` — Search facets light
- `E12-F03-T09` — Definir Acceptance Criteria medibles para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T10` — Agregar métricas RED/USE relevantes para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T11` — Escribir ADR si hay desvío de arquitectura para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T12` — Preparar feature flag + plan de rollback para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T13` — Actualizar OpenAPI/event schema si aplica para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T14` — Ejecutar checklist tenant isolation para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T15` — Actualizar runbook operativo para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T16` — Demo interna de 10 minutos documentada para E12-F03 (Model Explorer & Inspector)
- `E12-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E12-F03
- `E12-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E12-F03
- `E12-F03-T19` — Añadir tests de regresión golden si E12-F03 toca motores
- `E12-F03-T20` — Instrumentar traces spans para E12-F03
- `E12-F03-T21` — Documentar dependencias de eventos en E12-F03
- `E12-F03-T22` — Checklist seguridad secretos/PII en E12-F03
- `E12-F03-T23` — Validar performance budget preliminar de E12-F03
- `E12-F03-T24` — Actualizar mapping Architecture domain ↔ E12-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E12-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E12-F04 — Takeoff & Budget panels

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E12` que avance el objetivo (Studio multi-panel: canvas plano, árbol MDO, inspector, costos, jobs; i18n ES; flags por plan; sin cards innecesarias — ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E12-F04-T01` — Tabla takeoff con confidence
- `E12-F04-T02` — Budget summary moneda local
- `E12-F04-T03` — Override/sign entry points
- `E12-F04-T04` — E2E wedge UI
- `E12-F04-T05` — Plan paywalls
- `E12-F04-T06` — Loading/skeleton jobs
- `E12-F04-T07` — WS live totals refresh
- `E12-F04-T08` — Docs in-app tips LATAM
- `E12-F04-T09` — Definir Acceptance Criteria medibles para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T10` — Agregar métricas RED/USE relevantes para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T11` — Escribir ADR si hay desvío de arquitectura para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T12` — Preparar feature flag + plan de rollback para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T13` — Actualizar OpenAPI/event schema si aplica para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T14` — Ejecutar checklist tenant isolation para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T15` — Actualizar runbook operativo para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T16` — Demo interna de 10 minutos documentada para E12-F04 (Takeoff & Budget panels)
- `E12-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E12-F04
- `E12-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E12-F04
- `E12-F04-T19` — Añadir tests de regresión golden si E12-F04 toca motores
- `E12-F04-T20` — Instrumentar traces spans para E12-F04
- `E12-F04-T21` — Documentar dependencias de eventos en E12-F04
- `E12-F04-T22` — Checklist seguridad secretos/PII en E12-F04
- `E12-F04-T23` — Validar performance budget preliminar de E12-F04
- `E12-F04-T24` — Actualizar mapping Architecture domain ↔ E12-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E12-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E12-F05 — Jobs tray & notifications UI

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E12` que avance el objetivo (Studio multi-panel: canvas plano, árbol MDO, inspector, costos, jobs; i18n ES; flags por plan; sin cards innecesarias — ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E12-F05-T01` — Tray progreso
- `E12-F05-T02` — Toasts fallos accionables
- `E12-F05-T03` — Retry UX donde aplique
- `E12-F05-T04` — Tests ws reconnect
- `E12-F05-T05` — Badge counts
- `E12-F05-T06` — Integración E14 later
- `E12-F05-T07` — No spam toasts
- `E12-F05-T08` — Métrica ui_job_ack_time
- `E12-F05-T09` — Definir Acceptance Criteria medibles para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T10` — Agregar métricas RED/USE relevantes para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T11` — Escribir ADR si hay desvío de arquitectura para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T12` — Preparar feature flag + plan de rollback para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T13` — Actualizar OpenAPI/event schema si aplica para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T14` — Ejecutar checklist tenant isolation para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T15` — Actualizar runbook operativo para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T16` — Demo interna de 10 minutos documentada para E12-F05 (Jobs tray & notifications UI)
- `E12-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E12-F05
- `E12-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E12-F05
- `E12-F05-T19` — Añadir tests de regresión golden si E12-F05 toca motores
- `E12-F05-T20` — Instrumentar traces spans para E12-F05
- `E12-F05-T21` — Documentar dependencias de eventos en E12-F05
- `E12-F05-T22` — Checklist seguridad secretos/PII en E12-F05
- `E12-F05-T23` — Validar performance budget preliminar de E12-F05
- `E12-F05-T24` — Actualizar mapping Architecture domain ↔ E12-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E12-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.13 E13 — Reports (PDF/Excel) & Exports

Prioridad P1 · Complejidad M · Depende de: E10, E04, E02

#### E13-F01 — Report job pipeline

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E13` que avance el objetivo (Generación async de reportes PDF/Excel desde proyecciones MDO/costos con lineage; meters por plan....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E13-F01-T01` — Catálogo templates takeoff/budget/compare
- `E13-F01-T02` — Job async cola reports
- `E13-F01-T03` — Eventos solicitudo/generado/fallido
- `E13-F01-T04` — Storage artifact
- `E13-F01-T05` — Tests isolation
- `E13-F01-T06` — UI picker + history
- `E13-F01-T07` — Timeouts/DLQ
- `E13-F01-T08` — Métricas duración
- `E13-F01-T09` — Definir Acceptance Criteria medibles para E13-F01 (Report job pipeline)
- `E13-F01-T10` — Agregar métricas RED/USE relevantes para E13-F01 (Report job pipeline)
- `E13-F01-T11` — Escribir ADR si hay desvío de arquitectura para E13-F01 (Report job pipeline)
- `E13-F01-T12` — Preparar feature flag + plan de rollback para E13-F01 (Report job pipeline)
- `E13-F01-T13` — Actualizar OpenAPI/event schema si aplica para E13-F01 (Report job pipeline)
- `E13-F01-T14` — Ejecutar checklist tenant isolation para E13-F01 (Report job pipeline)
- `E13-F01-T15` — Actualizar runbook operativo para E13-F01 (Report job pipeline)
- `E13-F01-T16` — Demo interna de 10 minutos documentada para E13-F01 (Report job pipeline)
- `E13-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E13-F01
- `E13-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E13-F01
- `E13-F01-T19` — Añadir tests de regresión golden si E13-F01 toca motores
- `E13-F01-T20` — Instrumentar traces spans para E13-F01
- `E13-F01-T21` — Documentar dependencias de eventos en E13-F01
- `E13-F01-T22` — Checklist seguridad secretos/PII en E13-F01
- `E13-F01-T23` — Validar performance budget preliminar de E13-F01
- `E13-F01-T24` — Actualizar mapping Architecture domain ↔ E13-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E13-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E13-F02 — PDF budget/takeoff

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E13` que avance el objetivo (Generación async de reportes PDF/Excel desde proyecciones MDO/costos con lineage; meters por plan....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E13-F02-T01` — Template PDF marca
- `E13-F02-T02` — Incluir version_id, currency, timestamp, confidence summary
- `E13-F02-T03` — Tests golden
- `E13-F02-T04` — i18n ES
- `E13-F02-T05` — Prohibir números no citados de MDO
- `E13-F02-T06` — Optional signed budget annex
- `E13-F02-T07` — Feature flag
- `E13-F02-T08` — Perf pages
- `E13-F02-T09` — Definir Acceptance Criteria medibles para E13-F02 (PDF budget/takeoff)
- `E13-F02-T10` — Agregar métricas RED/USE relevantes para E13-F02 (PDF budget/takeoff)
- `E13-F02-T11` — Escribir ADR si hay desvío de arquitectura para E13-F02 (PDF budget/takeoff)
- `E13-F02-T12` — Preparar feature flag + plan de rollback para E13-F02 (PDF budget/takeoff)
- `E13-F02-T13` — Actualizar OpenAPI/event schema si aplica para E13-F02 (PDF budget/takeoff)
- `E13-F02-T14` — Ejecutar checklist tenant isolation para E13-F02 (PDF budget/takeoff)
- `E13-F02-T15` — Actualizar runbook operativo para E13-F02 (PDF budget/takeoff)
- `E13-F02-T16` — Demo interna de 10 minutos documentada para E13-F02 (PDF budget/takeoff)
- `E13-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E13-F02
- `E13-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E13-F02
- `E13-F02-T19` — Añadir tests de regresión golden si E13-F02 toca motores
- `E13-F02-T20` — Instrumentar traces spans para E13-F02
- `E13-F02-T21` — Documentar dependencias de eventos en E13-F02
- `E13-F02-T22` — Checklist seguridad secretos/PII en E13-F02
- `E13-F02-T23` — Validar performance budget preliminar de E13-F02
- `E13-F02-T24` — Actualizar mapping Architecture domain ↔ E13-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E13-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E13-F03 — Excel exports

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E13` que avance el objetivo (Generación async de reportes PDF/Excel desde proyecciones MDO/costos con lineage; meters por plan....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E13-F03-T01` — XLSX takeoff lines + costs
- `E13-F03-T02` — Columnas provenance
- `E13-F03-T03` — Tests roundtrip critical columns
- `E13-F03-T04` — Quota Free rows
- `E13-F03-T05` — UI download
- `E13-F03-T06` — Meter export
- `E13-F03-T07` — Docs mapping columnas
- `E13-F03-T08` — Async for large
- `E13-F03-T09` — Definir Acceptance Criteria medibles para E13-F03 (Excel exports)
- `E13-F03-T10` — Agregar métricas RED/USE relevantes para E13-F03 (Excel exports)
- `E13-F03-T11` — Escribir ADR si hay desvío de arquitectura para E13-F03 (Excel exports)
- `E13-F03-T12` — Preparar feature flag + plan de rollback para E13-F03 (Excel exports)
- `E13-F03-T13` — Actualizar OpenAPI/event schema si aplica para E13-F03 (Excel exports)
- `E13-F03-T14` — Ejecutar checklist tenant isolation para E13-F03 (Excel exports)
- `E13-F03-T15` — Actualizar runbook operativo para E13-F03 (Excel exports)
- `E13-F03-T16` — Demo interna de 10 minutos documentada para E13-F03 (Excel exports)
- `E13-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E13-F03
- `E13-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E13-F03
- `E13-F03-T19` — Añadir tests de regresión golden si E13-F03 toca motores
- `E13-F03-T20` — Instrumentar traces spans para E13-F03
- `E13-F03-T21` — Documentar dependencias de eventos en E13-F03
- `E13-F03-T22` — Checklist seguridad secretos/PII en E13-F03
- `E13-F03-T23` — Validar performance budget preliminar de E13-F03
- `E13-F03-T24` — Actualizar mapping Architecture domain ↔ E13-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E13-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E13-F04 — Entitlements & abuse controls

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E13` que avance el objetivo (Generación async de reportes PDF/Excel desde proyecciones MDO/costos con lineage; meters por plan....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E13-F04-T01` — Limits Free/Pro
- `E13-F04-T02` — Rate limits
- `E13-F04-T03` — Watermark Free opcional
- `E13-F04-T04` — Tests plan matrix
- `E13-F04-T05` — UX upgrade
- `E13-F04-T06` — Audit exports
- `E13-F04-T07` — Runbook abuse
- `E13-F04-T08` — Dashboard export volume
- `E13-F04-T09` — Definir Acceptance Criteria medibles para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T10` — Agregar métricas RED/USE relevantes para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T11` — Escribir ADR si hay desvío de arquitectura para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T12` — Preparar feature flag + plan de rollback para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T13` — Actualizar OpenAPI/event schema si aplica para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T14` — Ejecutar checklist tenant isolation para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T15` — Actualizar runbook operativo para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T16` — Demo interna de 10 minutos documentada para E13-F04 (Entitlements & abuse controls)
- `E13-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E13-F04
- `E13-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E13-F04
- `E13-F04-T19` — Añadir tests de regresión golden si E13-F04 toca motores
- `E13-F04-T20` — Instrumentar traces spans para E13-F04
- `E13-F04-T21` — Documentar dependencias de eventos en E13-F04
- `E13-F04-T22` — Checklist seguridad secretos/PII en E13-F04
- `E13-F04-T23` — Validar performance budget preliminar de E13-F04
- `E13-F04-T24` — Actualizar mapping Architecture domain ↔ E13-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E13-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.14 E14 — Notifications & Email

Prioridad P1 · Complejidad S · Depende de: E02, E04

#### E14-F01 — In-app notifications

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E14` que avance el objetivo (Notificaciones in-app + email para jobs, invitaciones, firmas, cuotas; preferencias usuario; sin spam....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E14-F01-T01` — Entidad Notification
- `E14-F01-T02` — API list/mark
- `E14-F01-T03` — UI bell
- `E14-F01-T04` — Eventos dominio→notif mapper
- `E14-F01-T05` — Tests authz
- `E14-F01-T06` — Retention cleanup
- `E14-F01-T07` — Métricas unread
- `E14-F01-T08` — No PII excess
- `E14-F01-T09` — Definir Acceptance Criteria medibles para E14-F01 (In-app notifications)
- `E14-F01-T10` — Agregar métricas RED/USE relevantes para E14-F01 (In-app notifications)
- `E14-F01-T11` — Escribir ADR si hay desvío de arquitectura para E14-F01 (In-app notifications)
- `E14-F01-T12` — Preparar feature flag + plan de rollback para E14-F01 (In-app notifications)
- `E14-F01-T13` — Actualizar OpenAPI/event schema si aplica para E14-F01 (In-app notifications)
- `E14-F01-T14` — Ejecutar checklist tenant isolation para E14-F01 (In-app notifications)
- `E14-F01-T15` — Actualizar runbook operativo para E14-F01 (In-app notifications)
- `E14-F01-T16` — Demo interna de 10 minutos documentada para E14-F01 (In-app notifications)
- `E14-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E14-F01
- `E14-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E14-F01
- `E14-F01-T19` — Añadir tests de regresión golden si E14-F01 toca motores
- `E14-F01-T20` — Instrumentar traces spans para E14-F01
- `E14-F01-T21` — Documentar dependencias de eventos en E14-F01
- `E14-F01-T22` — Checklist seguridad secretos/PII en E14-F01
- `E14-F01-T23` — Validar performance budget preliminar de E14-F01
- `E14-F01-T24` — Actualizar mapping Architecture domain ↔ E14-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E14-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E14-F02 — Email templates ES

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E14` que avance el objetivo (Notificaciones in-app + email para jobs, invitaciones, firmas, cuotas; preferencias usuario; sin spam....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E14-F02-T01` — Templates invite/job/quota/sign
- `E14-F02-T02` — Provider abstraction
- `E14-F02-T03` — Eventos enviada/fallida
- `E14-F02-T04` — Tests render
- `E14-F02-T05` — Unsubscribe/prefs
- `E14-F02-T06` — Bounce handling light
- `E14-F02-T07` — Rate limits
- `E14-F02-T08` — Runbook provider down
- `E14-F02-T09` — Definir Acceptance Criteria medibles para E14-F02 (Email templates ES)
- `E14-F02-T10` — Agregar métricas RED/USE relevantes para E14-F02 (Email templates ES)
- `E14-F02-T11` — Escribir ADR si hay desvío de arquitectura para E14-F02 (Email templates ES)
- `E14-F02-T12` — Preparar feature flag + plan de rollback para E14-F02 (Email templates ES)
- `E14-F02-T13` — Actualizar OpenAPI/event schema si aplica para E14-F02 (Email templates ES)
- `E14-F02-T14` — Ejecutar checklist tenant isolation para E14-F02 (Email templates ES)
- `E14-F02-T15` — Actualizar runbook operativo para E14-F02 (Email templates ES)
- `E14-F02-T16` — Demo interna de 10 minutos documentada para E14-F02 (Email templates ES)
- `E14-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E14-F02
- `E14-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E14-F02
- `E14-F02-T19` — Añadir tests de regresión golden si E14-F02 toca motores
- `E14-F02-T20` — Instrumentar traces spans para E14-F02
- `E14-F02-T21` — Documentar dependencias de eventos en E14-F02
- `E14-F02-T22` — Checklist seguridad secretos/PII en E14-F02
- `E14-F02-T23` — Validar performance budget preliminar de E14-F02
- `E14-F02-T24` — Actualizar mapping Architecture domain ↔ E14-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E14-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E14-F03 — Preferences & digests

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E14` que avance el objetivo (Notificaciones in-app + email para jobs, invitaciones, firmas, cuotas; preferencias usuario; sin spam....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E14-F03-T01` — Preference model channels/events
- `E14-F03-T02` — Digest opcional
- `E14-F03-T03` — Tests respect prefs
- `E14-F03-T04` — UI preferences
- `E14-F03-T05` — Defaults sensatos
- `E14-F03-T06` — Enterprise disable email external stub
- `E14-F03-T07` — Docs
- `E14-F03-T08` — Metric opt-out rate
- `E14-F03-T09` — Definir Acceptance Criteria medibles para E14-F03 (Preferences & digests)
- `E14-F03-T10` — Agregar métricas RED/USE relevantes para E14-F03 (Preferences & digests)
- `E14-F03-T11` — Escribir ADR si hay desvío de arquitectura para E14-F03 (Preferences & digests)
- `E14-F03-T12` — Preparar feature flag + plan de rollback para E14-F03 (Preferences & digests)
- `E14-F03-T13` — Actualizar OpenAPI/event schema si aplica para E14-F03 (Preferences & digests)
- `E14-F03-T14` — Ejecutar checklist tenant isolation para E14-F03 (Preferences & digests)
- `E14-F03-T15` — Actualizar runbook operativo para E14-F03 (Preferences & digests)
- `E14-F03-T16` — Demo interna de 10 minutos documentada para E14-F03 (Preferences & digests)
- `E14-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E14-F03
- `E14-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E14-F03
- `E14-F03-T19` — Añadir tests de regresión golden si E14-F03 toca motores
- `E14-F03-T20` — Instrumentar traces spans para E14-F03
- `E14-F03-T21` — Documentar dependencias de eventos en E14-F03
- `E14-F03-T22` — Checklist seguridad secretos/PII en E14-F03
- `E14-F03-T23` — Validar performance budget preliminar de E14-F03
- `E14-F03-T24` — Actualizar mapping Architecture domain ↔ E14-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E14-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.15 E15 — Chat IA grounded

Prioridad P1 · Complejidad L · Depende de: E16, E07, E10, E02

#### E15-F01 — Threads & messages

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E15` que avance el objetivo (Chat de proyecto con retrieval + tools read-only sobre MDO/proyecciones, citas obligatorias, memoria acotada, streaming ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E15-F01-T01` — ChatThread scoped project/version
- `E15-F01-T02` — Mensajes role/content/citations
- `E15-F01-T03` — Eventos ChatIniciado/MensajeChatRegistrado
- `E15-F01-T04` — AuthZ project members
- `E15-F01-T05` — UI panel streaming
- `E15-F01-T06` — Tests isolation
- `E15-F01-T07` — Retention policy
- `E15-F01-T08` — i18n ES
- `E15-F01-T09` — Definir Acceptance Criteria medibles para E15-F01 (Threads & messages)
- `E15-F01-T10` — Agregar métricas RED/USE relevantes para E15-F01 (Threads & messages)
- `E15-F01-T11` — Escribir ADR si hay desvío de arquitectura para E15-F01 (Threads & messages)
- `E15-F01-T12` — Preparar feature flag + plan de rollback para E15-F01 (Threads & messages)
- `E15-F01-T13` — Actualizar OpenAPI/event schema si aplica para E15-F01 (Threads & messages)
- `E15-F01-T14` — Ejecutar checklist tenant isolation para E15-F01 (Threads & messages)
- `E15-F01-T15` — Actualizar runbook operativo para E15-F01 (Threads & messages)
- `E15-F01-T16` — Demo interna de 10 minutos documentada para E15-F01 (Threads & messages)
- `E15-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E15-F01
- `E15-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E15-F01
- `E15-F01-T19` — Añadir tests de regresión golden si E15-F01 toca motores
- `E15-F01-T20` — Instrumentar traces spans para E15-F01
- `E15-F01-T21` — Documentar dependencias de eventos en E15-F01
- `E15-F01-T22` — Checklist seguridad secretos/PII en E15-F01
- `E15-F01-T23` — Validar performance budget preliminar de E15-F01
- `E15-F01-T24` — Actualizar mapping Architecture domain ↔ E15-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E15-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E15-F02 — Context assembly & retrieval UX

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E15` que avance el objetivo (Chat de proyecto con retrieval + tools read-only sobre MDO/proyecciones, citas obligatorias, memoria acotada, streaming ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E15-F02-T01` — Context pack from projections
- `E15-F02-T02` — Mostrar scope version
- `E15-F02-T03` — Citation chips clickeables
- `E15-F02-T04` — Tests citation present
- `E15-F02-T05` — Empty evidence UX
- `E15-F02-T06` — Perf context size budget
- `E15-F02-T07` — Modes: ask/explain/find (no invent)
- `E15-F02-T08` — Docs límites chat
- `E15-F02-T09` — Definir Acceptance Criteria medibles para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T10` — Agregar métricas RED/USE relevantes para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T11` — Escribir ADR si hay desvío de arquitectura para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T12` — Preparar feature flag + plan de rollback para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T13` — Actualizar OpenAPI/event schema si aplica para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T14` — Ejecutar checklist tenant isolation para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T15` — Actualizar runbook operativo para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T16` — Demo interna de 10 minutos documentada para E15-F02 (Context assembly & retrieval UX)
- `E15-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E15-F02
- `E15-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E15-F02
- `E15-F02-T19` — Añadir tests de regresión golden si E15-F02 toca motores
- `E15-F02-T20` — Instrumentar traces spans para E15-F02
- `E15-F02-T21` — Documentar dependencias de eventos en E15-F02
- `E15-F02-T22` — Checklist seguridad secretos/PII en E15-F02
- `E15-F02-T23` — Validar performance budget preliminar de E15-F02
- `E15-F02-T24` — Actualizar mapping Architecture domain ↔ E15-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E15-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E15-F03 — Insert to doc / commercial use

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E15` que avance el objetivo (Chat de proyecto con retrieval + tools read-only sobre MDO/proyecciones, citas obligatorias, memoria acotada, streaming ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E15-F03-T01` — Acción insertar en reporte con confirm HITL
- `E15-F03-T02` — Evento ChatRespuestaUsadaEnDoc
- `E15-F03-T03` — Bloquear insert si sin citas
- `E15-F03-T04` — Tests
- `E15-F03-T05` — Audit
- `E15-F03-T06` — Meter
- `E15-F03-T07` — UI warning
- `E15-F03-T08` — Integration E13
- `E15-F03-T09` — Definir Acceptance Criteria medibles para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T10` — Agregar métricas RED/USE relevantes para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T11` — Escribir ADR si hay desvío de arquitectura para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T12` — Preparar feature flag + plan de rollback para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T13` — Actualizar OpenAPI/event schema si aplica para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T14` — Ejecutar checklist tenant isolation para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T15` — Actualizar runbook operativo para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T16` — Demo interna de 10 minutos documentada para E15-F03 (Insert to doc / commercial use)
- `E15-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E15-F03
- `E15-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E15-F03
- `E15-F03-T19` — Añadir tests de regresión golden si E15-F03 toca motores
- `E15-F03-T20` — Instrumentar traces spans para E15-F03
- `E15-F03-T21` — Documentar dependencias de eventos en E15-F03
- `E15-F03-T22` — Checklist seguridad secretos/PII en E15-F03
- `E15-F03-T23` — Validar performance budget preliminar de E15-F03
- `E15-F03-T24` — Actualizar mapping Architecture domain ↔ E15-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E15-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E15-F04 — Memory & multi-user light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E15` que avance el objetivo (Chat de proyecto con retrieval + tools read-only sobre MDO/proyecciones, citas obligatorias, memoria acotada, streaming ...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E15-F04-T01` — Memoria resumen acotada
- `E15-F04-T02` — No memory cross-project
- `E15-F04-T03` — Presence light optional
- `E15-F04-T04` — Tests leakage
- `E15-F04-T05` — Clear memory control
- `E15-F04-T06` — Enterprise disable retention stub
- `E15-F04-T07` — Métricas token usage
- `E15-F04-T08` — Degradación si AI down
- `E15-F04-T09` — Definir Acceptance Criteria medibles para E15-F04 (Memory & multi-user light)
- `E15-F04-T10` — Agregar métricas RED/USE relevantes para E15-F04 (Memory & multi-user light)
- `E15-F04-T11` — Escribir ADR si hay desvío de arquitectura para E15-F04 (Memory & multi-user light)
- `E15-F04-T12` — Preparar feature flag + plan de rollback para E15-F04 (Memory & multi-user light)
- `E15-F04-T13` — Actualizar OpenAPI/event schema si aplica para E15-F04 (Memory & multi-user light)
- `E15-F04-T14` — Ejecutar checklist tenant isolation para E15-F04 (Memory & multi-user light)
- `E15-F04-T15` — Actualizar runbook operativo para E15-F04 (Memory & multi-user light)
- `E15-F04-T16` — Demo interna de 10 minutos documentada para E15-F04 (Memory & multi-user light)
- `E15-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E15-F04
- `E15-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E15-F04
- `E15-F04-T19` — Añadir tests de regresión golden si E15-F04 toca motores
- `E15-F04-T20` — Instrumentar traces spans para E15-F04
- `E15-F04-T21` — Documentar dependencias de eventos en E15-F04
- `E15-F04-T22` — Checklist seguridad secretos/PII en E15-F04
- `E15-F04-T23` — Validar performance budget preliminar de E15-F04
- `E15-F04-T24` — Actualizar mapping Architecture domain ↔ E15-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E15-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.16 E16 — AI Orchestrator / Guards / Eval

Prioridad P0 · Complejidad L · Depende de: E07, E10, E02, E04

#### E16-F01 — Orchestrator & tool allowlist

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E16` que avance el objetivo (Orquestador L3, tools read-only, policy guards (citation, no-geometry-write), AIProposal HITL, eval de alucinaciones, qu...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E16-F01-T01` — Pipeline retrieve→reason→tool→cite→answer
- `E16-F01-T02` — Tools read-only: get_takeoff, get_budget, get_element, search_entities
- `E16-F01-T03` — ToolCallLog audit
- `E16-F01-T04` — Timeouts/circuit break provider
- `E16-F01-T05` — Tests allowlist enforcement
- `E16-F01-T06` — Prohibir tool compute_geometry/set_price
- `E16-F01-T07` — Métricas tool error rate
- `E16-F01-T08` — Docs tool contracts
- `E16-F01-T09` — Definir Acceptance Criteria medibles para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T10` — Agregar métricas RED/USE relevantes para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T11` — Escribir ADR si hay desvío de arquitectura para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T12` — Preparar feature flag + plan de rollback para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T13` — Actualizar OpenAPI/event schema si aplica para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T14` — Ejecutar checklist tenant isolation para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T15` — Actualizar runbook operativo para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T16` — Demo interna de 10 minutos documentada para E16-F01 (Orchestrator & tool allowlist)
- `E16-F01-T17` — Revisar compatibilidad Free/Pro/Enterprise en E16-F01
- `E16-F01-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E16-F01
- `E16-F01-T19` — Añadir tests de regresión golden si E16-F01 toca motores
- `E16-F01-T20` — Instrumentar traces spans para E16-F01
- `E16-F01-T21` — Documentar dependencias de eventos en E16-F01
- `E16-F01-T22` — Checklist seguridad secretos/PII en E16-F01
- `E16-F01-T23` — Validar performance budget preliminar de E16-F01
- `E16-F01-T24` — Actualizar mapping Architecture domain ↔ E16-F01

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E16-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E16-F02 — Policy guards

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E16` que avance el objetivo (Orquestador L3, tools read-only, policy guards (citation, no-geometry-write), AIProposal HITL, eval de alucinaciones, qu...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E16-F02-T01` — Refuse-without-citation para claims cuantitativos
- `E16-F02-T02` — Block money claims sin proyección
- `E16-F02-T03` — PII/secrets scrub
- `E16-F02-T04` — PolicyDecision persist
- `E16-F02-T05` — Tests red-team prompts
- `E16-F02-T06` — Feature flag strict mode default on
- `E16-F02-T07` — Bypass solo internal eval
- `E16-F02-T08` — Dashboard refuse rate
- `E16-F02-T09` — Definir Acceptance Criteria medibles para E16-F02 (Policy guards)
- `E16-F02-T10` — Agregar métricas RED/USE relevantes para E16-F02 (Policy guards)
- `E16-F02-T11` — Escribir ADR si hay desvío de arquitectura para E16-F02 (Policy guards)
- `E16-F02-T12` — Preparar feature flag + plan de rollback para E16-F02 (Policy guards)
- `E16-F02-T13` — Actualizar OpenAPI/event schema si aplica para E16-F02 (Policy guards)
- `E16-F02-T14` — Ejecutar checklist tenant isolation para E16-F02 (Policy guards)
- `E16-F02-T15` — Actualizar runbook operativo para E16-F02 (Policy guards)
- `E16-F02-T16` — Demo interna de 10 minutos documentada para E16-F02 (Policy guards)
- `E16-F02-T17` — Revisar compatibilidad Free/Pro/Enterprise en E16-F02
- `E16-F02-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E16-F02
- `E16-F02-T19` — Añadir tests de regresión golden si E16-F02 toca motores
- `E16-F02-T20` — Instrumentar traces spans para E16-F02
- `E16-F02-T21` — Documentar dependencias de eventos en E16-F02
- `E16-F02-T22` — Checklist seguridad secretos/PII en E16-F02
- `E16-F02-T23` — Validar performance budget preliminar de E16-F02
- `E16-F02-T24` — Actualizar mapping Architecture domain ↔ E16-F02

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E16-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E16-F03 — AIProposal HITL

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E16` que avance el objetivo (Orquestador L3, tools read-only, policy guards (citation, no-geometry-write), AIProposal HITL, eval de alucinaciones, qu...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E16-F03-T01` — AIProposal con changeops sugeridos + citations
- `E16-F03-T02` — Estados draft/accepted/rejected
- `E16-F03-T03` — Eventos creada/resuelta
- `E16-F03-T04` — Apply solo tras accept vía ChangeSet engine
- `E16-F03-T05` — UI review
- `E16-F03-T06` — Tests no auto-apply
- `E16-F03-T07` — AuthZ
- `E16-F03-T08` — Audit
- `E16-F03-T09` — Definir Acceptance Criteria medibles para E16-F03 (AIProposal HITL)
- `E16-F03-T10` — Agregar métricas RED/USE relevantes para E16-F03 (AIProposal HITL)
- `E16-F03-T11` — Escribir ADR si hay desvío de arquitectura para E16-F03 (AIProposal HITL)
- `E16-F03-T12` — Preparar feature flag + plan de rollback para E16-F03 (AIProposal HITL)
- `E16-F03-T13` — Actualizar OpenAPI/event schema si aplica para E16-F03 (AIProposal HITL)
- `E16-F03-T14` — Ejecutar checklist tenant isolation para E16-F03 (AIProposal HITL)
- `E16-F03-T15` — Actualizar runbook operativo para E16-F03 (AIProposal HITL)
- `E16-F03-T16` — Demo interna de 10 minutos documentada para E16-F03 (AIProposal HITL)
- `E16-F03-T17` — Revisar compatibilidad Free/Pro/Enterprise en E16-F03
- `E16-F03-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E16-F03
- `E16-F03-T19` — Añadir tests de regresión golden si E16-F03 toca motores
- `E16-F03-T20` — Instrumentar traces spans para E16-F03
- `E16-F03-T21` — Documentar dependencias de eventos en E16-F03
- `E16-F03-T22` — Checklist seguridad secretos/PII en E16-F03
- `E16-F03-T23` — Validar performance budget preliminar de E16-F03
- `E16-F03-T24` — Actualizar mapping Architecture domain ↔ E16-F03

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E16-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E16-F04 — Embeddings index

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E16` que avance el objetivo (Orquestador L3, tools read-only, policy guards (citation, no-geometry-write), AIProposal HITL, eval de alucinaciones, qu...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E16-F04-T01` — Chunking projections/docs
- `E16-F04-T02` — EmbeddingsActualizados event
- `E16-F04-T03` — Tenant-scoped index
- `E16-F04-T04` — Rebuild job
- `E16-F04-T05` — Tests isolation vectors
- `E16-F04-T06` — Cost controls
- `E16-F04-T07` — Freshness lag metric
- `E16-F04-T08` — Docs what is indexed
- `E16-F04-T09` — Definir Acceptance Criteria medibles para E16-F04 (Embeddings index)
- `E16-F04-T10` — Agregar métricas RED/USE relevantes para E16-F04 (Embeddings index)
- `E16-F04-T11` — Escribir ADR si hay desvío de arquitectura para E16-F04 (Embeddings index)
- `E16-F04-T12` — Preparar feature flag + plan de rollback para E16-F04 (Embeddings index)
- `E16-F04-T13` — Actualizar OpenAPI/event schema si aplica para E16-F04 (Embeddings index)
- `E16-F04-T14` — Ejecutar checklist tenant isolation para E16-F04 (Embeddings index)
- `E16-F04-T15` — Actualizar runbook operativo para E16-F04 (Embeddings index)
- `E16-F04-T16` — Demo interna de 10 minutos documentada para E16-F04 (Embeddings index)
- `E16-F04-T17` — Revisar compatibilidad Free/Pro/Enterprise en E16-F04
- `E16-F04-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E16-F04
- `E16-F04-T19` — Añadir tests de regresión golden si E16-F04 toca motores
- `E16-F04-T20` — Instrumentar traces spans para E16-F04
- `E16-F04-T21` — Documentar dependencias de eventos en E16-F04
- `E16-F04-T22` — Checklist seguridad secretos/PII en E16-F04
- `E16-F04-T23` — Validar performance budget preliminar de E16-F04
- `E16-F04-T24` — Actualizar mapping Architecture domain ↔ E16-F04

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E16-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E16-F05 — Eval service & quotas

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E16` que avance el objetivo (Orquestador L3, tools read-only, policy guards (citation, no-geometry-write), AIProposal HITL, eval de alucinaciones, qu...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E16-F05-T01` — EvalCase golden LATAM
- `E16-F05-T02` — CI subset + nightly full
- `E16-F05-T03` — Gate regressions alucinación
- `E16-F05-T04` — AIQuotaExcedida
- `E16-F05-T05` — Meters tokens
- `E16-F05-T06` — Degradación graceful
- `E16-F05-T07` — Admin dashboard
- `E16-F05-T08` — Runbook provider outage
- `E16-F05-T09` — Definir Acceptance Criteria medibles para E16-F05 (Eval service & quotas)
- `E16-F05-T10` — Agregar métricas RED/USE relevantes para E16-F05 (Eval service & quotas)
- `E16-F05-T11` — Escribir ADR si hay desvío de arquitectura para E16-F05 (Eval service & quotas)
- `E16-F05-T12` — Preparar feature flag + plan de rollback para E16-F05 (Eval service & quotas)
- `E16-F05-T13` — Actualizar OpenAPI/event schema si aplica para E16-F05 (Eval service & quotas)
- `E16-F05-T14` — Ejecutar checklist tenant isolation para E16-F05 (Eval service & quotas)
- `E16-F05-T15` — Actualizar runbook operativo para E16-F05 (Eval service & quotas)
- `E16-F05-T16` — Demo interna de 10 minutos documentada para E16-F05 (Eval service & quotas)
- `E16-F05-T17` — Revisar compatibilidad Free/Pro/Enterprise en E16-F05
- `E16-F05-T18` — Verificar que no se rompe wedge color→qty→moneda local tras E16-F05
- `E16-F05-T19` — Añadir tests de regresión golden si E16-F05 toca motores
- `E16-F05-T20` — Instrumentar traces spans para E16-F05
- `E16-F05-T21` — Documentar dependencias de eventos en E16-F05
- `E16-F05-T22` — Checklist seguridad secretos/PII en E16-F05
- `E16-F05-T23` — Validar performance budget preliminar de E16-F05
- `E16-F05-T24` — Actualizar mapping Architecture domain ↔ E16-F05

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E16-F05-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.17 E17 — Timeline / Progress / Certifications

Prioridad P2 · Complejidad M · Depende de: E07, E10, E13

#### E17-F01 — Milestones & sequence MVP

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E17` que avance el objetivo (Hitos, secuencia constructiva ligera y certificaciones inmutables ligadas a snapshots del twin....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E17-F01-T01` — Milestone entity dates/links
- `E17-F01-T02` — WorkSequence ordered packs
- `E17-F01-T03` — Eventos HitoCreado/SecuenciaActualizada
- `E17-F01-T04` — UI board simple
- `E17-F01-T05` — Tests links element_ids exist
- `E17-F01-T06` — i18n
- `E17-F01-T07` — Limits Free
- `E17-F01-T08` — Docs no-Gantt-promise

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E17-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E17-F02 — Progress notes light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E17` que avance el objetivo (Hitos, secuencia constructiva ligera y certificaciones inmutables ligadas a snapshots del twin....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E17-F02-T01` — ProgressNote on milestone/element
- `E17-F02-T02` — Media attach opcional
- `E17-F02-T03` — AuthZ field roles
- `E17-F02-T04` — Tests
- `E17-F02-T05` — UI
- `E17-F02-T06` — Notifications
- `E17-F02-T07` — Retention
- `E17-F02-T08` — Métricas

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E17-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E17-F03 — Certifications immutable

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E17` que avance el objetivo (Hitos, secuencia constructiva ligera y certificaciones inmutables ligadas a snapshots del twin....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E17-F03-T01` — Issue certification period snapshot
- `E17-F03-T02` — Hash + freeze
- `E17-F03-T03` — Evento CertificacionEmitida
- `E17-F03-T04` — PDF via E13 template
- `E17-F03-T05` — Tests immutability
- `E17-F03-T06` — HITL roles
- `E17-F03-T07` — Vault UI
- `E17-F03-T08` — Runbook dispute

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E17-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.18 E18 — Procurement light / Purchase Orders

Prioridad P2 · Complejidad M · Depende de: E10, E09, E02

#### E18-F01 — PO from budget lines

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E18` que avance el objetivo (Órdenes de compra ligeras desde takeoff/budget lines, con aprobación HITL y estados básicos (no ERP completo)....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E18-F01-T01` — Generar líneas desde BudgetLine/TakeoffLine
- `E18-F01-T02` — Editable qty ≤ takeoff unless override reason
- `E18-F01-T03` — Evento OrdenCompraCreada
- `E18-F01-T04` — UI editor
- `E18-F01-T05` — Tests linkage
- `E18-F01-T06` — Currency consistency
- `E18-F01-T07` — Plan gate Pro+
- `E18-F01-T08` — Docs

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E18-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E18-F02 — Approvals HITL

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E18` que avance el objetivo (Órdenes de compra ligeras desde takeoff/budget lines, con aprobación HITL y estados básicos (no ERP completo)....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E18-F02-T01` — Approval entity
- `E18-F02-T02` — OrdenCompraAprobada
- `E18-F02-T03` — Roles
- `E18-F02-T04` — Notifications
- `E18-F02-T05` — Tests
- `E18-F02-T06` — UI queue
- `E18-F02-T07` — Audit
- `E18-F02-T08` — No AI auto-approve

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E18-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E18-F03 — Cancel & export

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E18` que avance el objetivo (Órdenes de compra ligeras desde takeoff/budget lines, con aprobación HITL y estados básicos (no ERP completo)....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E18-F03-T01` — Cancel flow
- `E18-F03-T02` — Export PDF/Excel light
- `E18-F03-T03` — Tests state machine
- `E18-F03-T04` — Métricas cycle time
- `E18-F03-T05` — Soft locks
- `E18-F03-T06` — Integration stub supplier email
- `E18-F03-T07` — Runbook
- `E18-F03-T08` — Anti-scope ERP note

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E18-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.19 E19 — Plugin Host & Module SDK

Prioridad P2 · Complejidad XL · Depende de: E07, E08, E01, E02

#### E19-F01 — Manifest & registry

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E19` que avance el objetivo (Host de plugins con manifest, capability contracts, sandbox, versionado e instalación org/project....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E19-F01-T01` — PluginManifest fields capabilities/permissions/semver
- `E19-F01-T02` — Registry storage signed artifacts
- `E19-F01-T03` — Validation PluginValidacionFallida
- `E19-F01-T04` — API registry
- `E19-F01-T05` — Tests schema
- `E19-F01-T06` — Docs SDK overview
- `E19-F01-T07` — CI publish internal
- `E19-F01-T08` — SBOM light

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E19-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E19-F02 — Host runtime sandbox

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E19` que avance el objetivo (Host de plugins con manifest, capability contracts, sandbox, versionado e instalación org/project....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E19-F02-T01` — Execution host allowlist
- `E19-F02-T02` — CPU/mem/time limits
- `E19-F02-T03` — No network default
- `E19-F02-T04` — Tests escape attempts
- `E19-F02-T05` — Audit executions
- `E19-F02-T06` — Metrics runtime
- `E19-F02-T07` — Kill switch disable
- `E19-F02-T08` — Runbook malicious plugin

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E19-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E19-F03 — Install lifecycle

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E19` que avance el objetivo (Host de plugins con manifest, capability contracts, sandbox, versionado e instalación org/project....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E19-F03-T01` — Install org/project
- `E19-F03-T02` — Eventos instalado/actualizado/deshabilitado
- `E19-F03-T03` — Compat check core version
- `E19-F03-T04` — UI manager
- `E19-F03-T05` — Entitlements plan
- `E19-F03-T06` — Tests rollback version
- `E19-F03-T07` — Config per installation
- `E19-F03-T08` — Docs

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E19-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E19-F04 — SDK & sample plugin

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E19` que avance el objetivo (Host de plugins con manifest, capability contracts, sandbox, versionado e instalación org/project....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E19-F04-T01` — SDK packaging
- `E19-F04-T02` — Sample typology plugin
- `E19-F04-T03` — Dev docs + examples
- `E19-F04-T04` — Contract tests SDK
- `E19-F04-T05` — Versioning guide
- `E19-F04-T06` — Local emulator light
- `E19-F04-T07` — Feature flag host
- `E19-F04-T08` — Support policy

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E19-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.20 E20 — Domain Plugins (Steel/HA/Gas/Fire/etc packs)

Prioridad P2 · Complejidad L · Depende de: E19, E08, E09

#### E20-F01 — Steel Frame pack

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E20` que avance el objetivo (Empaquetar tipologías/fórmulas de disciplinas como plugins first-party: Steel Frame, Hormigón Armado, Gas, Fire, etc....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E20-F01-T01` — Tipologías SF + fórmulas
- `E20-F01-T02` — Fixtures golden
- `E20-F01-T03` — Params schema
- `E20-F01-T04` — Tests
- `E20-F01-T05` — Docs ES
- `E20-F01-T06` — Pricebook mapping hints
- `E20-F01-T07` — Beta flag
- `E20-F01-T08` — Expert checklist signoff

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E20-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E20-F02 — Hormigón Armado pack

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E20` que avance el objetivo (Empaquetar tipologías/fórmulas de disciplinas como plugins first-party: Steel Frame, Hormigón Armado, Gas, Fire, etc....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E20-F02-T01` — Tipologías HA
- `E20-F02-T02` — Fórmulas + waste
- `E20-F02-T03` — Golden
- `E20-F02-T04` — Tests
- `E20-F02-T05` — Docs
- `E20-F02-T06` — UI param presets
- `E20-F02-T07` — Beta flag
- `E20-F02-T08` — Signoff

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E20-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E20-F03 — Gas pack

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E20` que avance el objetivo (Empaquetar tipologías/fórmulas de disciplinas como plugins first-party: Steel Frame, Hormigón Armado, Gas, Fire, etc....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E20-F03-T01` — Tipologías gas
- `E20-F03-T02` — Fórmulas conteos/longitudes
- `E20-F03-T03` — Golden
- `E20-F03-T04` — Tests
- `E20-F03-T05` — Docs normativa disclaimer
- `E20-F03-T06` — HITL warnings
- `E20-F03-T07` — Beta
- `E20-F03-T08` — Signoff

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E20-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E20-F04 — Fire / otras packs pipeline

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E20` que avance el objetivo (Empaquetar tipologías/fórmulas de disciplinas como plugins first-party: Steel Frame, Hormigón Armado, Gas, Fire, etc....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E20-F04-T01` — Template repo pack
- `E20-F04-T02` — Fire pack MVP
- `E20-F04-T03` — Backlog HVAC/electrical future
- `E20-F04-T04` — Release train process
- `E20-F04-T05` — Compat CI
- `E20-F04-T06` — Support matrix
- `E20-F04-T07` — Commercial packaging
- `E20-F04-T08` — Anti-scope infinite packs

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E20-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.21 E21 — Marketplace

Prioridad P3 · Complejidad XL · Depende de: E18, E19, E09, E02

#### E21-F01 — Provider & catalog sync

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E21` que avance el objetivo (Marketplace light: catálogo proveedores, cotizaciones, órdenes básicas, sync precios; solo después de MDO/PO estables....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E21-F01-T01` — Provider entity
- `E21-F01-T02` — Sync job CatalogoProveedorSincronizado
- `E21-F01-T03` — Mapping material_code
- `E21-F01-T04` — Tests
- `E21-F01-T05` — UI browse
- `E21-F01-T06` — Freshness SLA light
- `E21-F01-T07` — Curated LATAM seed
- `E21-F01-T08` — Docs onboarding provider

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E21-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E21-F02 — Quotes

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E21` que avance el objetivo (Marketplace light: catálogo proveedores, cotizaciones, órdenes básicas, sync precios; solo después de MDO/PO estables....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E21-F02-T01` — CotizacionCreada
- `E21-F02-T02` — Compare quotes UI
- `E21-F02-T03` — Link takeoff lines
- `E21-F02-T04` — Tests
- `E21-F02-T05` — Expiry
- `E21-F02-T06` — Notifications
- `E21-F02-T07` — AuthZ
- `E21-F02-T08` — No AI invent price

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E21-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E21-F03 — Orders & payments light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E21` que avance el objetivo (Marketplace light: catálogo proveedores, cotizaciones, órdenes básicas, sync precios; solo después de MDO/PO estables....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E21-F03-T01` — CompraRealizada / OrdenCancelada
- `E21-F03-T02` — HITL confirm
- `E21-F03-T03` — Status machine
- `E21-F03-T04` — Tests
- `E21-F03-T05` — Integration payment stub
- `E21-F03-T06` — Audit
- `E21-F03-T07` — Meters
- `E21-F03-T08` — Runbook failed order

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E21-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E21-F04 — Trust & compliance light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E21` que avance el objetivo (Marketplace light: catálogo proveedores, cotizaciones, órdenes básicas, sync precios; solo después de MDO/PO estables....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E21-F04-T01` — Provider verification flags
- `E21-F04-T02` — Tax display LATAM disclaimer
- `E21-F04-T03` — Abuse reporting
- `E21-F04-T04` — Tests
- `E21-F04-T05` — Admin tools
- `E21-F04-T06` — Docs legal stub
- `E21-F04-T07` — Feature flags regions
- `E21-F04-T08` — Anti-scope full B2B network

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E21-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.22 E22 — Enterprise (SSO, RBAC fine, multi-company, audit export, DR)

Prioridad P2 · Complejidad XL · Depende de: E02, E01, E07, E10

#### E22-F01 — SSO/SAML/OIDC

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E22` que avance el objetivo (Capacidades Enterprise: SSO/SAML/OIDC, RBAC/ABAC fino, multi-company, audit export, retención/DR, residency options....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E22-F01-T01` — SsoConnection entity
- `E22-F01-T02` — Login flows
- `E22-F01-T03` — JIT provisioning light
- `E22-F01-T04` — Tests matrix IdP
- `E22-F01-T05` — UI setup
- `E22-F01-T06` — Fallback local breakglass
- `E22-F01-T07` — Runbook SSO down
- `E22-F01-T08` — Docs

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E22-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E22-F02 — RBAC/ABAC fino

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E22` que avance el objetivo (Capacidades Enterprise: SSO/SAML/OIDC, RBAC/ABAC fino, multi-company, audit export, retención/DR, residency options....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E22-F02-T01` — OrgUnit/Team
- `E22-F02-T02` — RoleBinding resource scopes
- `E22-F02-T03` — Policy checks MDO/costs/reports
- `E22-F02-T04` — Tests denials
- `E22-F02-T05` — UI matrix
- `E22-F02-T06` — Migration from base roles
- `E22-F02-T07` — Perf cache
- `E22-F02-T08` — Audit decisions optional sample

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E22-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E22-F03 — Audit export & legal hold

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E22` que avance el objetivo (Capacidades Enterprise: SSO/SAML/OIDC, RBAC/ABAC fino, multi-company, audit export, retención/DR, residency options....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E22-F03-T01` — AuditExportJob
- `E22-F03-T02` — LegalHold
- `E22-F03-T03` — PoliticaRetencionCambiada
- `E22-F03-T04` — Tests completeness
- `E22-F03-T05` — UI
- `E22-F03-T06` — Encryption at rest confirm
- `E22-F03-T07` — Access controls exports
- `E22-F03-T08` — Docs retention

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E22-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E22-F04 — Multi-company & DR light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E22` que avance el objetivo (Capacidades Enterprise: SSO/SAML/OIDC, RBAC/ABAC fino, multi-company, audit export, retención/DR, residency options....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E22-F04-T01` — Multi-company within org
- `E22-F04-T02` — Data boundaries
- `E22-F04-T03` — Backup/restore runbook
- `E22-F04-T04` — DR RPO/RTO targets documentados
- `E22-F04-T05` — Drill anual/ semestral
- `E22-F04-T06` — Residency preference field
- `E22-F04-T07` — Tests company isolation
- `E22-F04-T08` — Anti-scope global multi-active

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E22-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.23 E23 — Public API & Integrations

Prioridad P2 · Complejidad L · Depende de: E07, E10, E02, E04

#### E23-F01 — API keys & public resources

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E23` que avance el objetivo (API pública estable Pro/Enterprise, keys, webhooks, quotas, OpenAPI, integraciones contables light....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E23-F01-T01` — ApiKey hashed storage
- `E23-F01-T02` — Scopes
- `E23-F01-T03` — Resources projects/takeoff/budgets read
- `E23-F01-T04` — Writes limitadas documentadas
- `E23-F01-T05` — Tests
- `E23-F01-T06` — Portal keys UI
- `E23-F01-T07` — Meter api calls
- `E23-F01-T08` — Docs OpenAPI

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E23-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E23-F02 — Webhooks

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E23` que avance el objetivo (API pública estable Pro/Enterprise, keys, webhooks, quotas, OpenAPI, integraciones contables light....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E23-F02-T01` — Endpoint CRUD
- `E23-F02-T02` — Signatures
- `E23-F02-T03` — Retries/DLQ
- `E23-F02-T04` — Tests
- `E23-F02-T05` — Event allowlist
- `E23-F02-T06` — UI deliveries
- `E23-F02-T07` — Security SSRF protect
- `E23-F02-T08` — Runbook

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E23-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E23-F03 — Integrations accounting light

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E23` que avance el objetivo (API pública estable Pro/Enterprise, keys, webhooks, quotas, OpenAPI, integraciones contables light....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E23-F03-T01` — Export adapters stub
- `E23-F03-T02` — Mapping accounts optional
- `E23-F03-T03` — Tests
- `E23-F03-T04` — Pilot one integration
- `E23-F03-T05` — Docs
- `E23-F03-T06` — Feature flag
- `E23-F03-T07` — Support boundary
- `E23-F03-T08` — Anti-scope full ERP

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E23-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.24 E24 — Data Platform / Analytics (later)

Prioridad P3 · Complejidad L · Depende de: E01, E04, E07, E02

#### E24-F01 — Event ingestion to lake

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E24` que avance el objetivo (Warehouse analítico desacoplado de OLTP para product analytics y métricas de negocio; no confundir con audit legal....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E24-F01-T01` — Sink from bus
- `E24-F01-T02` — Schema registry evolve
- `E24-F01-T03` — PII policy
- `E24-F01-T04` — Tests
- `E24-F01-T05` — Docs
- `E24-F01-T06` — Access controls
- `E24-F01-T07` — Cost monitors
- `E24-F01-T08` — Retention

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E24-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E24-F02 — Marts wedge & quality

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E24` que avance el objetivo (Warehouse analítico desacoplado de OLTP para product analytics y métricas de negocio; no confundir con audit legal....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E24-F02-T01` — Funnel upload→sign
- `E24-F02-T02` — Quality confidence marts
- `E24-F02-T03` — Tests reconciliación samples
- `E24-F02-T04` — Dashboards
- `E24-F02-T05` — Alerts business
- `E24-F02-T06` — Docs definitions
- `E24-F02-T07` — No PII in marts default
- `E24-F02-T08` — Owner PM+Eng

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E24-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E24-F03 — Self-serve later

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E24` que avance el objetivo (Warehouse analítico desacoplado de OLTP para product analytics y métricas de negocio; no confundir con audit legal....) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E24-F03-T01` — Explore tool limited
- `E24-F03-T02` — Enterprise export BI stub
- `E24-F03-T03` — Tests
- `E24-F03-T04` — Governance
- `E24-F03-T05` — Feature flag
- `E24-F03-T06` — Support model
- `E24-F03-T07` — Anti-scope customer arbitrary SQL early
- `E24-F03-T08` — Roadmap note

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E24-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

### 3.25 E25 — Mobile Site Ops (later)

Prioridad P3 · Complejidad L · Depende de: E12, E17, E03, E02

#### E25-F01 — Mobile auth & project picker

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E25` que avance el objetivo (App móvil light para obra: progreso, fotos, hitos, consulta takeoff/presupuesto; offline-ish; no reemplaza Studio deskto...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E25-F01-T01` — Login
- `E25-F01-T02` — Project list entitlements
- `E25-F01-T03` — Tests
- `E25-F01-T04` — Biometrics optional later
- `E25-F01-T05` — SSO enterprise later
- `E25-F01-T06` — UI
- `E25-F01-T07` — Telemetry
- `E25-F01-T08` — Docs

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E25-F01-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E25-F02 — Read models field

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E25` que avance el objetivo (App móvil light para obra: progreso, fotos, hitos, consulta takeoff/presupuesto; offline-ish; no reemplaza Studio deskto...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E25-F02-T01` — Takeoff/budget read
- `E25-F02-T02` — Milestone list
- `E25-F02-T03` — Caching
- `E25-F02-T04` — Tests
- `E25-F02-T05` — Offline read
- `E25-F02-T06` — Perf
- `E25-F02-T07` — UX low bandwidth
- `E25-F02-T08` — i18n

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E25-F02-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E25-F03 — Capture media & progress

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E25` que avance el objetivo (App móvil light para obra: progreso, fotos, hitos, consulta takeoff/presupuesto; offline-ish; no reemplaza Studio deskto...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E25-F03-T01` — Camera upload E03
- `E25-F03-T02` — Progress note
- `E25-F03-T03` — Offline queue
- `E25-F03-T04` — Conflict policy
- `E25-F03-T05` — Tests
- `E25-F03-T06` — Notifications
- `E25-F03-T07` — Compression
- `E25-F03-T08` — Prohibir geometry edit

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E25-F03-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

#### E25-F04 — Distribution & ops

**Intent de la feature.** Entregar un incremento testeable y desplegable dentro de `E25` que avance el objetivo (App móvil light para obra: progreso, fotos, hitos, consulta takeoff/presupuesto; offline-ish; no reemplaza Studio deskto...) sin acoplar innecesariamente otras features.

**Independencia.** Debe poder mergearse detrás de flag aunque otras Fxx de la épica sigan abiertas, salvo dependencia explícita declarada en tasks.

**Tasks.**

- `E25-F04-T01` — PWA or store decision ADR
- `E25-F04-T02` — Crash reporting
- `E25-F04-T03` — Feature flags remote
- `E25-F04-T04` — Tests device matrix light
- `E25-F04-T05` — Support runbook
- `E25-F04-T06` — Beta program
- `E25-F04-T07` — Metrics DAU field
- `E25-F04-T08` — Anti-scope full BIM mobile

**Checklist transversal de la feature.**
- Entidad/modelo actualizado con tenant + provenance si aplica
- Servicio de dominio con AuthZ
- Eventos outbox / consumers idempotentes si hay side-effects
- API conceptual documentada
- UI mínima o explícitamente N/A
- Migraciones expand/contract
- Tests unit + integration + aislamiento
- Métricas + logs + traces
- Docs/runbook
- Flag + rollback

**Criterio de done de la feature.**
- Todas las tasks `E25-F04-T*` cerradas o movidas a debt ticketed
- CI verde incluyendo tests nuevos
- No regresión wedge golden
- Observabilidad básica en dashboards
- Revisión de seguridad tenant OK

---

## 4. Matriz Feature × Capability

Matriz de trazabilidad entre features prioritarias y capabilities de arquitectura/producto.

| Feature | MDO SoT | L1 Evidence | L2 Engines | L3 AI Guards | Events/Outbox | Tenant/Billing | Wedge UX | Reports/Sign | Plugins | Enterprise |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| E01-F01 | x |  |  |  | x |  |  |  |  |  |
| E01-F03 |  |  |  |  |  | x | x |  |  |  |
| E02-F03 |  |  |  |  |  | x | x |  |  | x |
| E02-F04 |  |  |  |  | x | x |  |  |  |  |
| E03-F01 |  | x |  |  | x | x | x |  |  |  |
| E04-F02 | x |  |  |  | x |  |  |  |  |  |
| E05-F03 |  | x |  |  | x |  | x |  |  |  |
| E06-F02 | x |  | x |  | x |  | x |  |  |  |
| E07-F03 | x |  | x |  | x | x |  |  |  |  |
| E07-F05 | x | x | x |  | x |  | x |  |  |  |
| E08-F03 | x |  | x |  | x |  | x |  |  |  |
| E09-F03 | x |  | x |  | x | x | x |  |  |  |
| E10-F02 | x |  | x |  | x | x | x | x |  |  |
| E11-F02 | x |  | x |  | x |  | x |  |  |  |
| E12-F04 | x | x | x |  |  | x | x | x |  |  |
| E13-F02 | x |  |  |  | x | x |  | x |  |  |
| E14-F01 |  |  |  |  | x | x | x |  |  |  |
| E15-F02 | x |  |  | x |  | x | x |  |  |  |
| E16-F02 | x |  |  | x | x | x |  |  |  |  |
| E16-F03 | x |  | x | x | x |  |  |  |  |  |
| E17-F03 | x |  |  |  | x |  |  | x |  | x |
| E19-F02 | x |  | x |  |  | x |  |  | x |  |
| E20-F01 | x |  | x |  |  |  |  |  | x |  |
| E21-F03 |  |  |  |  | x | x |  |  | x |  |
| E22-F01 |  |  |  |  |  | x |  |  |  | x |
| E23-F01 | x |  |  |  | x | x |  |  |  | x |

### 4.1 Matriz épica × etapa de arquitectura

| Épica | Etapa 1 | Etapa 2 | Etapa 3 | Etapa 4 | Etapa 5 |
|-------|-------|-------|-------|-------|-------|
| E01 | ██ | ░ | ░ | ░ | ░ |
| E02 | ██ | █ | █ | █ | █ |
| E03 | ██ | ░ | ░ | ░ | ░ |
| E04 | ██ | █ | █ | █ | █ |
| E05 | ██ | █ | ░ | ░ | ░ |
| E06 | ░ | ██ | ░ | ░ | ░ |
| E07 | ██ | █ | █ | █ | █ |
| E08 | ░ | ██ | ░ | █ | ░ |
| E09 | ░ | ██ | ░ | ░ | ░ |
| E10 | ░ | ██ | █ | ░ | ░ |
| E11 | ░ | ██ | ░ | ░ | ░ |
| E12 | █ | ██ | █ | ░ | ░ |
| E13 | ░ | ░ | ██ | ░ | ░ |
| E14 | █ | ░ | █ | ░ | ░ |
| E15 | ░ | ░ | ██ | ░ | ░ |
| E16 | ░ | ░ | ██ | ░ | ░ |
| E17 | ░ | ░ | ██ | ░ | ░ |
| E18 | ░ | ░ | ░ | █ | ░ |
| E19 | ░ | ░ | ░ | ██ | ░ |
| E20 | ░ | ░ | ░ | ██ | ░ |
| E21 | ░ | ░ | ░ | ██ | ░ |
| E22 | ░ | ░ | ░ | ░ | ██ |
| E23 | ░ | ░ | ░ | ░ | ██ |
| E24 | ░ | ░ | ░ | ░ | █ |
| E25 | ░ | ░ | ░ | ░ | █ |

Leyenda: ██ foco principal · █ soporte significativo · ░ no foco.

---

## 5. Detalle de Tasks transversales y checklists

Tasks y checklists que aplican a casi toda épica P0/P1. Deben copiarse al brief de feature.

### 5.1 Checklist de entidad de dominio
- Campos id, org_id/project_id, created_at, updated_at, deleted_at (soft) según política
- Provenance/confidence si la entidad representa hecho cuantitativo
- Índices de lookup tenant-scoped
- No hard-delete si es hecho comercial o lineage
- Serialización estable para eventos
- Tests de validación de invariantes
- Documentar ownership de escritura
- Migración expand antes de contract

### 5.2 Checklist de servicio de dominio
- AuthZ al inicio del use-case (deny by default)
- Idempotency keys en mutaciones relevantes
- Outbox en la misma unidad de trabajo que la mutación
- Errores de dominio mapeados a error model API
- Timeouts a dependencias externas
- Logs estructurados con correlation ids
- Métricas de latencia/error
- Prohibir imports cross-domain de infraestructura ajena

### 5.3 Checklist de eventos
- Nombre estable DomainEventoPastTense
- Envelope completo (id, type, version, tenant, correlation)
- Schema versionado; cambios breaking → nueva version
- Consumer idempotente (dedup store o natural key)
- Ordering documentado por aggregate
- DLQ + runbook
- Contract test productor/consumidor
- No usar eventos como RPC síncrono oculto

### 5.4 Checklist de API
- Rutas bajo /v1
- AuthN + AuthZ
- Validación input
- Paginación/filtrado donde listas
- ETags en proyecciones si aplica
- Rate limits por plan en rutas sensibles
- OpenAPI actualizada
- Tests de contrato y aislamiento

### 5.5 Checklist de frontend
- No tratar UI state como SoT del MDO
- Version badge visible en flujos wedge
- Estados loading/error/empty
- i18n ES
- Respeto entitlements/flags
- Accesibilidad mínima teclado en flujos críticos
- E2E smoke del path tocado
- Performance: evitar re-render storms en canvas/tree

### 5.6 Checklist de tests mínimos por épica
- Unit motores deterministas
- Integration outbox→consumer
- Tenant isolation (mín. 3 casos negativos)
- Plan matrix smoke si hay entitlements
- Golden wedge si toca perception/materials/costs/UI
- Immurability tests si toca signed/cert
- Eval IA si toca L3
- Migraciones up/down o expand/contract verified

### 5.7 Checklist de migraciones
- Expand primero (columnas/tablas nuevas nullable)
- Backfill job si necesario
- Dual-read si strangler
- Contract solo tras verificación
- Nunca rewrite destructivo de signed snapshots
- Seeds tipologías/pricebooks versionados
- Rollback script o flag off path
- Documentar tiempo estimado de migrate en prod

### 5.8 Checklist de métricas
- Latencia p50/p95 use-case
- Error rate
- Queue depth / lag outbox
- Business: uploads, takeoff lines, signed budgets
- Quality: low_confidence_pct
- AI: refuse_rate, token_cost
- Billing: quota hits
- Frontend: TTI workspace (sampled)

### 5.9 Catálogo extendido de tasks transversales numeradas

- `TX-001` — Task transversal genérica #1: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-002` — Task transversal genérica #2: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-003` — Task transversal genérica #3: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-004` — Task transversal genérica #4: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-005` — Task transversal genérica #5: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-006` — Task transversal genérica #6: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-007` — Task transversal genérica #7: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-008` — Task transversal genérica #8: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-009` — Task transversal genérica #9: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-010` — Task transversal genérica #10: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-011` — Task transversal genérica #11: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-012` — Task transversal genérica #12: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-013` — Task transversal genérica #13: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-014` — Task transversal genérica #14: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-015` — Task transversal genérica #15: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-016` — Task transversal genérica #16: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-017` — Task transversal genérica #17: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-018` — Task transversal genérica #18: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-019` — Task transversal genérica #19: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-020` — Task transversal genérica #20: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-021` — Task transversal genérica #21: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-022` — Task transversal genérica #22: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-023` — Task transversal genérica #23: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-024` — Task transversal genérica #24: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-025` — Task transversal genérica #25: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-026` — Task transversal genérica #26: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-027` — Task transversal genérica #27: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-028` — Task transversal genérica #28: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-029` — Task transversal genérica #29: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-030` — Task transversal genérica #30: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-031` — Task transversal genérica #31: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-032` — Task transversal genérica #32: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-033` — Task transversal genérica #33: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-034` — Task transversal genérica #34: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-035` — Task transversal genérica #35: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-036` — Task transversal genérica #36: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-037` — Task transversal genérica #37: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-038` — Task transversal genérica #38: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-039` — Task transversal genérica #39: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-040` — Task transversal genérica #40: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-041` — Task transversal genérica #41: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-042` — Task transversal genérica #42: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-043` — Task transversal genérica #43: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-044` — Task transversal genérica #44: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-045` — Task transversal genérica #45: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-046` — Task transversal genérica #46: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-047` — Task transversal genérica #47: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-048` — Task transversal genérica #48: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-049` — Task transversal genérica #49: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-050` — Task transversal genérica #50: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-051` — Task transversal genérica #51: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-052` — Task transversal genérica #52: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-053` — Task transversal genérica #53: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-054` — Task transversal genérica #54: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-055` — Task transversal genérica #55: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-056` — Task transversal genérica #56: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-057` — Task transversal genérica #57: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-058` — Task transversal genérica #58: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-059` — Task transversal genérica #59: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-060` — Task transversal genérica #60: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-061` — Task transversal genérica #61: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-062` — Task transversal genérica #62: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-063` — Task transversal genérica #63: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-064` — Task transversal genérica #64: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-065` — Task transversal genérica #65: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-066` — Task transversal genérica #66: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-067` — Task transversal genérica #67: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-068` — Task transversal genérica #68: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-069` — Task transversal genérica #69: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-070` — Task transversal genérica #70: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-071` — Task transversal genérica #71: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-072` — Task transversal genérica #72: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-073` — Task transversal genérica #73: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-074` — Task transversal genérica #74: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-075` — Task transversal genérica #75: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-076` — Task transversal genérica #76: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-077` — Task transversal genérica #77: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-078` — Task transversal genérica #78: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-079` — Task transversal genérica #79: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).
- `TX-080` — Task transversal genérica #80: aplicar si la épica introduce superficie nueva (seguridad, obs, docs, flags, tests, perf, i18n, planes, runbooks, ADRs).

### 5.10 Matriz de obligatoriedad transversal × prioridad de épica

| Checklist §5.x | P0 | P1 | P2 | P3 |
|-------|-------|-------|-------|-------|
| 5.1 Entidad | Obligatorio | Obligatorio | Obligatorio | Recomendado |
| 5.2 Servicio | Obligatorio | Obligatorio | Obligatorio | Recomendado |
| 5.3 Eventos | Obligatorio si mute | Obligatorio si mute | Si aplica | Si aplica |
| 5.4 API | Obligatorio | Obligatorio | Obligatorio | Si hay API |
| 5.5 Frontend | Si hay UI | Si hay UI | Si hay UI | Si hay UI |
| 5.6 Tests | Obligatorio | Obligatorio | Obligatorio | Smoke+unit |
| 5.7 Migraciones | Obligatorio | Obligatorio | Obligatorio | Si schema |
| 5.8 Métricas | Obligatorio | Obligatorio | Mínimas | Mínimas |

---

## 6. Dependencias

### 6.1 Grafo ASCII de dependencias entre épicas

```
E01 Platform/Obs
 ├── E02 Identity/Billing
 │    ├── E03 Media
 │    │    └── E05 Perception
 │    ├── E04 Jobs/Outbox/Bus
 │    │    ├── E05 Perception
 │    │    ├── E07 MDO Core ←──── also needs E01
 │    │    ├── E13 Reports
 │    │    ├── E14 Notifications
 │    │    └── E16 AI Orchestrator
 │    ├── E09 Costs (entitlements)
 │    ├── E14 Notifications
 │    ├── E16 AI (quotas)
 │    ├── E22 Enterprise
 │    └── E23 Public API
 ├── E04 (obs for queues)
 └── E07 (obs/flags)

E07 MDO Core
 ├── E06 Geometry (needs E05+E07)
 ├── E08 Materials (needs E06+E07)
 ├── E09 Costs (needs E08)
 ├── E10 Projections+Signed (needs E09+E07)
 ├── E11 Scenarios (needs E07+E08+E09)
 ├── E12 Frontend Workspace (needs E05/E07/E08/E09/E04)
 ├── E16 AI Guards (needs E07+E10)
 ├── E15 Chat (needs E16+E07+E10)
 ├── E17 Timeline/Cert (needs E07+E10+E13)
 ├── E19 Plugin Host (needs E07+E08)
 └── E23 Public API

E10 Signed/Projections
 ├── E13 Reports
 ├── E18 Procurement light
 └── E21 Marketplace (also E18+E19)

E19 Plugin Host
 ├── E20 Domain Packs
 └── E21 Marketplace (plugins/providers)

E12 Frontend
 └── E25 Mobile (later; also E17+E03)

E01+E04+E07+E02
 └── E24 Analytics (later)
```

### 6.2 Tracks paralelos recomendados (equipo 2–3 eng)

| Track | Épicas | Notas |
|-------|-------|-------|
| Track A — Platform | E01 → E02 → E04 → (E14) | Desbloquea async y tenancy |
| Track B — Twin/Wedge | E03 → E05 → E07 → E06 → E08 → E09 → E10 | Camino crítico del wedge |
| Track C — Experience | E12 paralelo desde E05/E07; luego E13 | UI strangler |
| Track D — Intelligence | E16 → E15 tras E10 | Nunca antes de guards+proyecciones |
| Track E — Extend | E11; luego E19→E20; E18→E21 | Post MVP comercial |
| Track F — Enterprise | E22+E23; E24/E25 late | Con pilots |

### 6.3 Critical path (qué bloquea el MVP comercial)

```
E01 → E02 → E03 → E04 → E07 → E05 → E06 → E08 → E09 → E10 → E12(harden) → MVP
                 ↘________↗
```

Bloqueadores duros:
- E07 bloquea casi todo L2/L3 serio
- E05/E06/E08 bloquean cantidades confiables
- E09/E10 bloquean cierre comercial firmado
- E04 bloquea perception/reports/ai async seguros
- E16 bloquea E15 (chat) — no negociable
- E19 bloquea E20/E21

### 6.4 Matriz de bloqueo (extracto)

| Si falta… | No se puede completar bien… |
|-------|-------|
| E01 | Operar cualquier épica en prod con evidencia |
| E02 | E03 quotas, E09 plans, E15/E16 meters, E22 |
| E03 | E05, parte E12, E25 |
| E04 | E05, E13, E14 scale, E16 embeddings jobs |
| E05 | E06 útil, wedge automatizado |
| E07 | E06 write, E08, E11, E15, E16 proposals |
| E08 | E09, E10, E20 |
| E09 | E10, E13 budget PDF, E18 |
| E10 | E13 signed annex, E15 commercial insert, E17 cert |
| E16 | E15 |
| E19 | E20, parte E21 |

### 6.5 Dependencias peligrosas / atajos prohibidos
- Marketplace (E21) o IA generativa de cantidades antes de MDO (E07) — prohibido
- Chat (E15) antes de Guards/Eval (E16) — prohibido
- Plugins (E19) antes de contracts Materials (E08) estables — alto riesgo
- Microservicios split físico antes de dolor medido — prohibido (P22)
- SignedBudget sin provenance/confidence gates — prohibido comercialmente

---

## 7. Riesgos

### 7.1 Riesgos consolidados por épica (síntesis)

#### Riesgos E01

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Over-instrumentation prematura | SLIs mínimos por clase; expandir con dolor medido |
| Arch | Acoplar app a vendor APM | OpenTelemetry como abstracción |
| Perf | Sampling inadecuado | Tail-based + muestreo tenant-aware |
| Scale | Cardinality explosion en labels | Allowlist estricta de labels |
| Commercial | Retrasar wedge por plataforma perfecta | Cap ≤20% capacidad del equipo en E01 |

#### Riesgos E02

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Roles ad-hoc en frontend | AuthZ server-side obligatoria en dominio |
| Arch | Billing acoplado a UI | Billing domain + eventos de uso |
| Perf | Checks AuthZ caros | Cache membership con invalidación por evento |
| Scale | Orgs grandes | Paginación memberships + búsqueda |
| Commercial | Upgrade path confuso | Entitlements claros + UX plan |

#### Riesgos E03

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Uploads grandes fallan | Multipart + resume |
| Arch | URLs firmadas mal scoped | Prefijo org/project + TTL corto |
| Perf | Derivados bloquean request | Job async DerivadoGenerado |
| Scale | Costos de storage | Lifecycle + retención |
| Commercial | Límites Free poco claros | Quotas en entitlements |

#### Riesgos E04

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Dual-write sin outbox | Outbox obligatorio |
| Arch | Bus como RPC | Eventos de hecho + envelope estándar |
| Perf | Poison messages | DLQ + circuit break |
| Scale | Noisy neighbor | Fairness multi-tenant |
| Commercial | Jobs stuck sin UX | WS progress + timeouts |

#### Riesgos E05

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Nondeterminism / model drift | pipeline_version + golden fixtures LATAM |
| Arch | Perception escribe costos | Prohibido; solo Evidence/ColorRegion |
| Perf | Costo CPU/GPU | Cola dedicada + quotas plan |
| Scale | Picos de upload | Fairness + backpressure |
| Commercial | Scans LATAM de baja calidad | Confidence UI + mapping humano |

#### Riesgos E06

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Escala mal calibrada | UX calibración + blockers de compute |
| Arch | Mutación silenciosa MDO | Solo ChangeSet/ChangeOp |
| Perf | Polígonos pesados | Jobs + spatial index |
| Scale | Multi-sheet | Incremental por sheet |
| Commercial | UX difícil | Calibración guiada < 2 minutos |

#### Riesgos E07

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Schema incompleto eterno | Cerrar MDO schema v1 + evolve |
| Arch | God aggregate | Entidades + ChangeOps acotados |
| Perf | Proyecciones stale | Invalidación event-driven |
| Scale | Explosión de versions | Snapshots lógicos + diffs |
| Commercial | Migración mental usuario | Wedge sobre MDO sin romper UX |

#### Riesgos E08

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | DSL demasiado poderoso | Sandbox de expresiones limitado |
| Arch | Materials lee Perception | Solo geometría tipada MDO |
| Perf | Recalc full lento | Incremental por ChangeSet |
| Scale | Catálogo grande | Índices + lazy |
| Commercial | Edge LATAM | Overrides + feedback |

#### Riesgos E09

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | FX/multimoneda | CurrencyRate as_of + freeze on sign |
| Arch | Costs←Perception | Solo TakeoffLine |
| Perf | Recalc | Incremental + cache totals |
| Scale | Pricebooks grandes | Import async |
| Commercial | Precios viejos | source metadata + import |

#### Riesgos E10

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Snapshot incompleto | Freeze takeoff+prices+FX+versions |
| Arch | Mutar budget firmado | Inmutabilidad enforce + tests |
| Perf | Snapshots pesados | Object store + hash |
| Scale | Muchos signs | Retención política |
| Commercial | Firma UX fricción | Flujo corto + roles claros |

#### Riesgos E11

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Merge conflicts complejos | MVP compare+promote; merge limitado |
| Arch | Scenario como copia full pesada | Versions + diffs |
| Perf | Compare lento | Projections diff |
| Scale | Branches zombie | Soft-delete + límites plan |
| Commercial | Confusión UX | Metáfora Git suave para constructores |

#### Riesgos E12

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Estado UI duplica MDO | Server SoT; UI cache descartable |
| Arch | BFF god | BFF solo agrega proyecciones |
| Perf | Bundle/TTI | Code-split panels |
| Scale | Proyectos grandes tree | Virtualización |
| Commercial | UX regresa a file-centric | Version badge siempre visible |

#### Riesgos E13

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Templates frágiles | Fixtures + visual/pdf hash tests |
| Arch | Report lee DB alien | Solo projections/APIs |
| Perf | PDF grandes | Cola reports + timeouts |
| Scale | Abuse Free | Quotas |
| Commercial | Brand weak en PDF | Template LATAM marca ARQ-IA |

#### Riesgos E14

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Duplicados | Idempotency keys notif |
| Arch | Emails con datos sensibles | Minimize payload + AuthZ links |
| Perf | Burst | Queue notify + batch |
| Scale | Provider limits | Backoff |
| Commercial | Spam | Preferences + digests |

#### Riesgos E15

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Alucinaciones | Guards E16 + refuse |
| Arch | Chat escribe geometría | Tools read-only + AIProposal HITL |
| Perf | Latencia/tokens | Cache retrieval + quotas |
| Scale | Costo Free abuse | Hard meters |
| Commercial | Overpromise IA | Copy UX honesto |

#### Riesgos E16

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Guard bypass | Defense in depth + tests red team |
| Arch | LLM escribe stores | Allowlist tools + repo writes solo proposal |
| Perf | Eval flaky | Golden prompts estables |
| Scale | Costo tokens | Cache + plan limits |
| Commercial | Ship chat before guards | E16 antes o junto a E15 hard gate |

#### Riesgos E17

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Certificación sin freeze correcto | Reusar snapshot pattern SignedBudget |
| Arch | Timeline como Gantt completo prematuro | MVP hitos + links elementos |
| Perf | Snapshots frecuentes | On-demand + retención |
| Scale | Obra grande | Paginación hitos |
| Commercial | Scope creep scheduling | Anti-scope: no MS Project clone |

#### Riesgos E18

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Estados PO complejos | MVP draft/submitted/approved/ordered/cancelled |
| Arch | ERP scope creep | Anti-scope lista dura |
| Perf | OK | N/A early |
| Scale | Integraciones proveedor | Manual first |
| Commercial | Marketplace confusion | PO local antes de marketplace |

#### Riesgos E19

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Sandbox escape | Allowlist APIs + resource limits |
| Arch | Plugins write arbitrary MDO | Capability contracts only |
| Perf | Plugin lento | Timeouts + isolation |
| Scale | Compat matrix | Semver + CI compat tests |
| Commercial | SDK antes de demanda | 1–2 plugins first-party primero |

#### Riesgos E20

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Fórmulas incorrectas dominio | Expert review + golden cases |
| Arch | Plugin depende de APIs inestables | Contracts versionados |
| Perf | Packs pesados | Lazy load |
| Scale | Muchos packs | Release trains |
| Commercial | Pack incompleto daña marca | Beta labeled + HITL |

#### Riesgos E21

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Integraciones frágiles | Provider adapter interface |
| Arch | Marketplace antes de MDO | Gate dependencia dura |
| Perf | Sync catálogos | Jobs + incremental |
| Scale | Ops proveedores | Onboarding limitado piloto |
| Commercial | Cold start suppliers | First-party curated LATAM |

#### Riesgos E22

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | SSO edge cases | Pilot IdP matrix |
| Arch | Over-compliance theater | Priorizar controles pedidos por pilots |
| Perf | AuthZ fino costoso | Caching + policy engine |
| Scale | Multi-region cost | DR warm standby opcional no multi-active early |
| Commercial | Custom forever | Packaging estándar + extras pagos |

#### Riesgos E23

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Breaking changes | Versioning estricto + contract tests |
| Arch | API expone internals | Resources de dominio estables |
| Perf | Abuse | Quotas + rate limits |
| Scale | Webhook storms | Backoff + DLQ |
| Commercial | API Free abuse | Pro+ only |

#### Riesgos E24

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | ETL fragile | Managed pipelines + contracts |
| Arch | Analytics como SoT | Prohibido; solo lecturas derivadas |
| Perf | CDC load | Incremental |
| Scale | Cost warehouse | Start narrow marts |
| Commercial | Vanity metrics | North-star wedge funnels |

#### Riesgos E25

| Tipo | Riesgo | Mitigación |
|-------|-------|-------|
| Tech | Offline sync conflicts | Append notes first; limited edits |
| Arch | Mobile escribe geometría | Prohibido; solo progress/media |
| Perf | Media mobile | Compression pipeline |
| Scale | Device fragmentation | RN/Flutter choice ADR |
| Commercial | App store tax early | PWA first option evaluate |

### 7.2 Matriz de riesgos de portafolio

| ID | Riesgo portafolio | Prob | Impacto | Severidad | Mitigación | Owner |
|-------|-------|-------|-------|-------|-------|-------|
| R-P01 | Reescritura file→MDO rompe wedge | M | A | Crítica | Strangler + flag + e2e golden | TL |
| R-P02 | IA alucina cantidades en prod | M | A | Crítica | E16 antes E15; eval gates | AI Eng |
| R-P03 | Fuga cross-tenant | B | A | Crítica | Isolation suite + reviews | Security |
| R-P04 | Outbox/colas inestables | M | A | Alta | E04 primero; DLQ runbooks | Platform |
| R-P05 | Percepción baja calidad LATAM scans | A | M | Alta | Confidence UI + HITL map | Engines |
| R-P06 | Scope creep Marketplace/ERP/Gantt | A | M | Alta | Anti-scope §H + DoR | PM/CTO |
| R-P07 | Deuda silenciosa acumula | A | M | Alta | P04 gates; debt board | TL |
| R-P08 | Costos LLM explotan en Free | M | M | Media | Meters duros + degradación | Billing |
| R-P09 | Plugin sandbox escape | B | A | Alta | Allowlist+limits; review | Platform |
| R-P10 | Enterprise custom infinito | M | M | Media | Packaging estándar E22 | CTO |
| R-P11 | Perf twin en proyectos grandes | M | M | Media | Projections+virtualización | Staff |
| R-P12 | 1 solo dev en critical path | A | M | Alta | Orden §15; WIP=1 epic | CTO |
| R-P13 | Multimoneda/FX errores money | M | A | Alta | Decimal+freeze on sign | Costs Eng |
| R-P14 | Compliance theater retrasa | M | B | Media | Pilot-driven E22 | CTO |
| R-P15 | Golden fixtures insuficientes | M | A | Alta | Invertir en set LATAM | QA/Eng |

### 7.3 Riesgos técnicos adicionales detallados

1. **Determinismo pipelines CV.** Variación de OCR/segmentación entre versiones de libs; mitigar con pin de versiones y pipeline_version inmutable.
2. **Consistencia eventual proyecciones.** UI puede mostrar stale; mitigar version badges + WS invalidate + ETags.
3. **Poison messages.** Consumers que fallan siempre; DLQ + quarantine + replay tools.
4. **Schema migration hotspots.** Tablas grandes takeoff_lines; backfill batch + expand/contract.
5. **WS fanout.** Muchas conexiones por project; authz handshake + limits.
6. **Vector index isolation.** Embeddings mal scoped; tests obligatorios E16-F04.
7. **PDF determinism.** Fuentes/layout; golden hash tolerante + pinned fonts.
8. **Idempotencia meters.** Double charge quotas; idempotency keys + reconciliación.
9. **Merge scenarios.** Conflicts money lines; no auto-merge; HITL.
10. **Mobile offline.** Duplicar progress notes; client ids idempotentes.

### 7.4 Plan de respuesta a riesgos críticos

| Severidad | Acción inmediata | Escalación |
|-------|-------|-------|
| Crítica | Flag off + hotfix o rollback | CTO + owner dominio < 2h |
| Alta | Mitigar en 48h o disable feature | TL |
| Media | Ticket P1 con fecha | TL en planning |
| Baja | Backlog | PM |

---

## 8. Criterio de calidad (Definition of Done global)

Ninguna épica P0/P1 se declara Done sin cumplir este DoD global, además de su criterio local.

### 8.1 Tests
- Unit tests de motores tocados con fixtures
- Integration tests del path outbox/API/DB
- E2E smoke wedge si el cambio toca el path comercial
- Isolation suite tenant en verde
- Contract tests de eventos/API modificados
- Eval IA si toca L3 (refuse-without-citation)

### 8.2 Types / lint / supply chain
- Typecheck + lint CI verdes
- Dependency audit sin críticos nuevos
- Secrets scan limpio
- Lockfiles actualizados conscientemente

### 8.3 Deuda
- Cero deuda P0 abierta introducida por el cambio
- Deuda P1 con issue, owner y fecha
- ADRs para desvíos

### 8.4 Docs
- Brief epic/feature actualizado
- OpenAPI/event schemas
- Runbook si hay ops surface
- Notas de migración

### 8.5 Performance budgets
- No regresiones fuera de budget sin waiver
- Benchmarks motores si aplica
- Queue SLO no degradado materialmente

### 8.6 Logs / metrics / traces
- Correlation ids presentes
- Métricas del use-case en dashboard
- Alertas básicas si path crítico

### 8.7 Rollback
- Flag off path verificado
- Migraciones no dejan sistema irrecuperable
- Plan escrito en PR/brief

### 8.8 Security checklist
- AuthZ deny-by-default en endpoints nuevos
- Signed URLs scoped
- Validación input
- Least privilege workers
- Threat notes para features XL

### 8.9 Tenant isolation proof
- Al menos 3 tests negativos cross-tenant
- Storage key prefix verified
- Vector/index/search scoped if used
- Admin tools también scoped

### 8.10 Product / commercial integrity
- Wedge color→qty→moneda local intacto
- IA no inventa geometría/cantidades
- HITL en firmas/compras/proposals
- Entitlements Free/Pro/Enterprise respetados

### 8.11 Rubrica de score de calidad pre-release

| Área | 0 | 1 | 2 | Mínimo merge P0 |
|-------|-------|-------|-------|-------|
| Tests | No hay | Parcial | Completo+e2e | 2 |
| Obs | No hay | Logs only | Logs+metrics+traces | 2 |
| Security | No revisado | Checklist parcial | Checklist+isolation | 2 |
| Rollback | No | Flag only | Flag+migrate plan | 2 |
| Docs | No | README corto | Brief+runbook+schemas | 1 |
| Perf | Desconocido | Spot check | Budget verified | 1 |

---

## 9. Roadmap visual

Secuencia recomendada por fases conceptuales (rangos de meses para equipo pequeño 1–3 eng). No son fechas de calendario absolutas.

### 9.1 Fases

| Fase | Rango meses | Etapa arch | Épicas foco | Outcome |
|-------|-------|-------|-------|-------|
| Phase A | M0–M3 | 1 | E01 E02 E03 E04 E07 (slice) E12 (shell) | Cimientos + MDO v1 + async |
| Phase B | M3–M7 | 1–2 | E05 E06 E08 E09 E10 E12 (harden) E14 | Wedge completo sobre MDO + sign |
| Phase C | M7–M11 | 2–3 | E11 E13 E16 E15 E17 | Scenarios + IA grounded + reports/cert |
| Phase D | M11–M16 | 4 | E18 E19 E20 (packs) E21 (piloto) | Extensibilidad + procurement/marketplace light |
| Phase E | M16–M24+ | 5 | E22 E23 E24 E25 | Enterprise + API + analytics + mobile |

### 9.2 Gantt ASCII (conceptual)

```
Mes     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 18 20 22 24
E01     ████
E02       ██████
E03         ████
E04       ██████
E07         ████████
E05             ████████
E12         ████████████
E06                 ████████
E08                   ██████
E09                     ██████
E10                       ████
E14               ████
E11                           ██████
E13                           ████
E16                             ██████
E15                               ██████
E17                                 ████
E18                                     ████
E19                                     ████████
E20                                         ████████
E21                                           ████████
E22                                               ████████████
E23                                                 ██████
E24                                                     ██████
E25                                                       ████████
```

### 9.3 Hitos de arquitectura ↔ releases producto

| Hito | Fase | Evidencia |
|-------|-------|-------|
| H1 MDO+Events vivos | A | ChangeSet + outbox + upload async |
| H2 Wedge on MDO | B | Color→qty→ARS/local + SignedBudget |
| H3 Scenarios MVP | C | Branch/compare/promote |
| H4 AI grounded | C | Chat con citas + eval gate |
| H5 Plugins first-party | D | 2 packs instalables |
| H6 Marketplace piloto | D | Quote→order con N providers |
| H7 Enterprise ready | E | SSO+RBAC fino+audit export+DR drill |

### 9.4 Capacidad sugerida por fase (1–3 eng)

| Fase | 1 eng | 2 eng | 3 eng |
|-------|-------|-------|-------|
| A | Critical path serial | A+B tracks | A+B+C shell UI |
| B | Engines serial | Engines || UI | Engines || UI || polish billing |
| C | AI then chat | AI || reports | AI || reports || scenarios |
| D | Plugins first | Plugins || PO | Plugins || PO || marketplace prep |
| E | Enterprise SSO first | Ent || API | Ent || API || mobile/analytics |

---

## 10. Backlog MoSCoW

### 10.1 Must
| ID | Item | Épica/Feature |
|-------|-------|-------|
| M1 | Obs+flags+CI gates | E01-F01..F04 |
| M2 | Tenant isolation + entitlements base | E02-F02..F04 |
| M3 | Media upload seguro | E03-F01 |
| M4 | Jobs+outbox+WS progress | E04-F01..F04 |
| M5 | MDO schema v1 + ChangeSets | E07-F01..F03 |
| M6 | Perception color segmentation | E05-F03 |
| M7 | Geometry calibrate+compute | E06-F01..F02 |
| M8 | Materials takeoff formulas core | E08-F01..F03 |
| M9 | Costs pricebook+budget moneda local | E09-F01..F03 |
| M10 | SignedBudget HITL | E10-F02 |
| M11 | Studio wedge panels | E12-F02..F04 |
| M12 | AI guards before any chat money claims | E16-F01..F02 |

### 10.2 Should
| ID | Item | Épica/Feature |
|-------|-------|-------|
| S1 | Notifications email/in-app | E14 |
| S2 | Reports PDF/Excel | E13 |
| S3 | Scenarios compare/promote | E11 |
| S4 | Chat grounded | E15 |
| S5 | AIProposal HITL | E16-F03 |
| S6 | Overrides takeoff auditados | E08-F04 |
| S7 | Billing provider Pro checkout | E02-F05 |
| S8 | Certifications | E17-F03 |
| S9 | Eval nightly alucinaciones | E16-F05 |
| S10 | Quality dashboards twin trust | E07-F06 + E01 |

### 10.3 Could
| ID | Item | Épica/Feature |
|-------|-------|-------|
| C1 | Procurement PO light | E18 |
| C2 | Plugin host SDK | E19 |
| C3 | Steel/HA packs | E20-F01..F02 |
| C4 | Gas/Fire packs | E20-F03..F04 |
| C5 | Public API keys | E23-F01 |
| C6 | Webhooks | E23-F02 |
| C7 | Timeline board full | E17-F01 |
| C8 | Merge scenarios avanzado | E11-F03 |
| C9 | Symbol assist advanced | E05-F04 |
| C10 | Accounting integration light | E23-F03 |

### 10.4 Future
| ID | Item | Épica/Feature |
|-------|-------|-------|
| FUT1 | Marketplace red providers | E21 |
| FUT2 | Enterprise SSO/RBAC/DR | E22 |
| FUT3 | Analytics warehouse | E24 |
| FUT4 | Mobile site ops | E25 |
| FUT5 | Multi-region active-active | E22-F04 late |
| FUT6 | Customer arbitrary SQL BI | E24-F03 |
| FUT7 | Full ERP procurement | Anti-scope |
| FUT8 | LLM geometry generation | Prohibido |

---

## 11. MVP comercial

Mínimo indispensable para primer lanzamiento comercial LATAM (cobrar Pro / convertir Free→Pro) sin romper la promesa del wedge.

### 11.1 Subset de épicas MVP
- E01 (mínimo operable)
- E02 (auth + entitlements + meters esenciales)
- E03 (upload)
- E04 (async jobs + progress)
- E05 (color segmentation usable)
- E06 (calibración + medidas)
- E07 (MDO v1 + versions/changesets mínimos)
- E08 (fórmulas core tipologías wedge)
- E09 (pricebook + budget moneda local)
- E10 (proyección takeoff + SignedBudget)
- E12 (workspace suficiente para flujo completo)
- E14 (notificaciones mínimas job/invite/quota) — strongly recommended

Fuera de MVP (aunque deseable): E11 scenarios avanzados, E13 reports fancy (export CSV mínimo puede colarse), E15/E16 chat (salvo demos internas gated), E17–E25.

### 11.2 Flujo MVP obligatorio

```
Registro/Login → Crear proyecto (currency local) → Upload plano
→ Perception color regions → Mapear colores→tipologías
→ Calibrar escala → Geometry compute → Materials takeoff
→ Pricebook → Budget → Revisar confidence → Firmar presupuesto
→ (opcional) export CSV/PDF simple
```

### 11.3 Criterios de aceptación MVP
- E2E < X minutos en plano sample LATAM (definir X con PM; target aspiracional 15–30)
- Totales en moneda del proyecto correctos vs golden
- SignedBudget inmutable con hash
- Free limits enforced; upgrade path Pro
- Cero writes de IA a geometría/cantidades (IA puede estar off)
- Aislamiento tenant verificado
- Jobs fallidos visibles + reintento/soporte runbook

### 11.4 Métricas de éxito MVP
- Activation: % trials que alcanzan primer budget
- Time-to-first-signed-budget
- Override rate tipologías (calidad)
- Job failure rate perception
- Conversion Free→Pro
- Support tickets por crash/job stuck

---

## 12. Versión 1.0

### 12.1 Definición
Versión 1.0 = MVP comercial endurecido + estabilidad operativa suficiente para clientes Pro pagando en LATAM.

### 12.2 Contenidos
- Todo el MVP §11
- E13 reports PDF/Excel takeoff+budget
- E14 completo prefs
- E10 vault signed budgets
- Hardening E05/E06 golden sets ampliados
- Billing checkout Pro estable (E02-F05)
- Dashboards obs productivos (E01)
- Docs onboarding usuario ES

### 12.3 No contenidos en 1.0
- Chat IA producción
- Scenarios merge avanzado (compare light opcional beta)
- Plugins/Marketplace
- SSO Enterprise
- Mobile nativo
- Warehouse analytics

### 12.4 Exit criteria 1.0
- Error budget API/jobs en verde 30 días
- N clientes Pro piloto satisfechos (definir N con negocio)
- Restore backup drill OK
- P0 debt absoluta = 0

---

## 13. Versión 2.0

### 13.1 Definición
Versión 2.0 = MDO maduro + scenarios + chat grounded + reports/certificaciones + AI proposals HITL.

### 13.2 Contenidos
- E11 Scenarios branch/compare/promote
- E16 Orchestrator+guards+eval+embeddings+proposals
- E15 Chat grounded citation-first
- E17 Timeline + Certifications
- E13 templates avanzados / compare exports
- Mejoras quality flags y twin trust dashboards
- E08-F05 contracts listos para plugins

### 13.3 Exit criteria 2.0
- Eval alucinación gate en CI
- Chat refuse-without-citation medido
- Scenarios usados por % usuarios Pro
- CertificacionEmitida en flujo piloto
- No incidentes de money-claim inventado

---

## 14. Versión 3.0

### 14.1 Definición
Versión 3.0 = plataforma extensible: plugins, packs de dominio, marketplace, enterprise, public API; analytics/mobile según demanda.

### 14.2 Contenidos
- E19 Plugin Host & SDK
- E20 Domain packs (Steel/HA/Gas/Fire…)
- E18 Procurement light
- E21 Marketplace piloto→GA
- E22 Enterprise SSO/RBAC/audit/DR
- E23 Public API & webhooks
- E24 Analytics (internal→select enterprise)
- E25 Mobile site ops MVP

### 14.3 Exit criteria 3.0
- ≥2 packs first-party GA
- Marketplace con proveedores curados LATAM
- Cliente Enterprise en SSO
- Public API con SLA documentado
- Compat matrix plugins publicada

---

## 15. Conclusión — un solo desarrollador

Orden óptimo si solo hay **1 desarrollador**. Cada decisión es pragmática: maximizar aprendizaje comercial del wedge y minimizar superficie que no vende.

### 15.1 Orden serial recomendado
1. E01 mínimo (logs, health, flags, CI) — sin esto operás a ciegas.
2. E02 mínimo (auth, org, roles, entitlements Free/Pro) — sin esto no hay producto multi-tenant vendible.
3. E04 mínimo (jobs+outbox) — perception síncrona te va a matar.
4. E03 upload — input del wedge.
5. E07 MDO v1 thin — SoT; strangler temprano evita reescritura doble.
6. E05 color segmentation — corazón del wedge LATAM.
7. E12 shell+canvas+mapper — sin UI no hay feedback real de usuarios.
8. E06 calibración+compute — cantidades reales.
9. E08 fórmulas core — takeoff.
10. E09 pricebooks+budget — dinero.
11. E10 signed budget — cierre comercial.
12. E14 notificaciones mínimas — reduce soporte.
13. E13 export PDF/Excel — entrega al cliente del usuario.
14. E16 guards+eval — solo cuando el twin está estable.
15. E15 chat grounded — diferenciador Pro después de guards.
16. E11 scenarios — upsell cuando el núcleo no se cae.
17. E17 certs — si hay demanda obra.
18. E18 PO light — si piden compras.
19. E19/E20 plugins — cuando el core se vuelve intocable por pedidos de tipologías.
20. E21 marketplace — último entre extensiones comerciales.
21. E22/E23 enterprise/API — con pilots que pagan.
22. E24/E25 — solo con señal clara.

### 15.2 Reglas brutales para 1 eng
- WIP=1 épica (o 1 feature) en vuelo
- Cada 2 semanas: demo wedge o no cuenta
- No chat antes de signed budget
- No marketplace antes de plugins contracts + PO
- No microservicios
- Decir no a custom Enterprise hasta E10 estable
- Invertir en golden fixtures temprano (paga intereses negativos si no)
- Documentar debt; no esconderla

### 15.3 Qué recortar primero si el tiempo aprieta
| Recorte | Impacto | Cuándo está OK |
|-------|-------|-------|
| E11 scenarios | Menos upsell | OK post-MVP |
| E15 chat | Menos wow | OK si guards no listos |
| E13 PDF fancy | CSV basta | OK early |
| E17 timeline | Obra espera | OK |
| Symbol assist avanzado | Mapper manual | OK |
| Billing provider full | Manual upgrade | Solo muy early; no en 1.0 |

### 15.4 Cierre
El norte no es «plataforma perfecta»: es un twin MDO event-driven donde la cuña coloreado→cantidades→presupuesto local sigue siendo el camino feliz, con IA solo como L3 citada, y crecimiento por plugins cuando el core ya es aburridamente confiable.

---

## Apéndice A — Glosario

| Término | Definición |
|-------|-------|
| MDO | Modelo Digital de la Obra; fuente de verdad L2. |
| L1 / Percepción | Capa que extrae evidencias desde medios; no costos finales. |
| L2 / Twin | Grafo tipado versionado de la obra + motores deterministas. |
| L3 / Inteligencia | Orquestación IA, chat, explicación; no inventa geometría/cantidades. |
| Evidence | Hecho percibido con confidence y lineage a media. |
| ChangeSet / ChangeOp | Commit y operaciones atómicas sobre el twin. |
| ProjectVersion | Snapshot lógico inmutable al cerrar. |
| Scenario | Branch Git-like sobre el MDO. |
| TakeoffLine | Cantidad material con provenance/fórmula. |
| Pricebook | Lista de precios tipada por moneda/región. |
| SignedBudget | Presupuesto firmado HITL con snapshot+hash inmutable. |
| Outbox | Patrón para publicar eventos consistentemente tras mutar. |
| DLQ | Dead Letter Queue para mensajes poison. |
| Entitlement | Capacidad habilitada por plan Free/Pro/Enterprise. |
| Meter | Contador de uso facturable/cuotable. |
| Provenance | Origen auditable de un hecho (evidence, fórmula, usuario). |
| Confidence | Score de confiabilidad de percepción/medida/línea. |
| HITL | Human-in-the-Loop; aprobación humana obligatoria. |
| AIProposal | Sugerencia de ChangeOps por IA; requiere accept humano. |
| Citation | Referencia a entity/version/proyección en respuesta IA. |
| Plugin Manifest | Descriptor versionado de capabilities de un módulo. |
| Wedge | Cuña comercial: plano coloreado → cantidades → presupuesto local. |
| Golden set | Fixtures canónicos LATAM para regresión. |
| Strangler | Patrón de reemplazo gradual del legacy file-centric. |
| BFF | Backend-for-frontend; agrega proyecciones UI sin contaminar dominio. |
| ABAC/RBAC | Control de acceso por roles/atributos. |
| Residency | Preferencia/restricción de región de datos Enterprise. |
| Projection | Read model materializado desde el MDO/eventos. |

## Apéndice B — Plantilla de Epic brief

```
Epic ID: Exx
Título:
Owner:
Prioridad: P0|P1|P2|P3
Complejidad: S|M|L|XL
Etapa arquitectura: 1-5
Objetivo:
Problema:
Beneficio medible:
Dependencias:
Anti-scope:
Eventos:
Entidades:
API:
UI:
Migraciones:
Tests:
Flags:
Rollback:
Riesgos:
DoD local:
Demo script:
```

- Campo opcional extendido B-1: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-2: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-3: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-4: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-5: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-6: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-7: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-8: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-9: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-10: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-11: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-12: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-13: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-14: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-15: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-16: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-17: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-18: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-19: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.
- Campo opcional extendido B-20: notas de capacidad, partners, costo infra, owners secundarios, links ADR, etc.

## Apéndice C — Plantilla de Feature brief

```
Feature ID: Exx-Fyy
Épica padre:
Título:
Intent:
Usuario/job-to-be-done:
Dependencias features:
Tasks (Txx):
Contratos tocados:
Plan entitlements:
Observabilidad:
Seguridad:
DoD:
QA notes:
```

- Variante C-1: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-2: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-3: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-4: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-5: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-6: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-7: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-8: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-9: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-10: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-11: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-12: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-13: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-14: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-15: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-16: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-17: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-18: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-19: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.
- Variante C-20: agregar estimación horas, reviewer, riesgo, fixture ids, screenshots, feature flag key.

## Apéndice D — RACI sugerido

| Actividad | CTO | Tech Lead | Staff Eng | Domain Eng | AI Eng | PM | QA |
|-------|-------|-------|-------|-------|-------|-------|-------|
| Prioridad épicas | A | R | C | C | C | R | I |
| ADR arquitectura | A | R | R | C | C | I | I |
| Diseño MDO | A | C | R | R | I | C | C |
| Perception/Geometry | I | A | C | R | I | C | R |
| Costs/Sign | I | A | C | R | I | R | R |
| AI guards/eval | A | C | C | C | R | C | R |
| Plugins host | A | R | R | C | I | C | C |
| Enterprise SSO | A | R | C | C | I | R | C |
| Release gate | A | R | C | C | C | C | R |
| Incident Sev1 | A | R | C | R | C | I | C |

R=Responsible, A=Accountable, C=Consulted, I=Informed

## Apéndice E — Métricas de engineering health

| Métrica | Target inicial | Notas |
|-------|-------|-------|
| CI verde main | >95% días | Flakes ticketed |
| Lead time feature P0 | < 2 semanas slice | Partir si más |
| MTTR Sev1 | < 4h | Con flags |
| Change fail rate | <10% | DORA-ish |
| P0 debt count | 0 | Gate release |
| Isolation tests | 100% pass | Bloqueante |
| Wedge e2e | 100% RC | Bloqueante |
| Eval refuse precision | Alta / sin regresiones | Desde E16 |
| DLQ depth | 0 sostenido | Alert |
| Outbox lag p95 | SLO definido E04 | Alert |
| Low confidence takeoff % | Monitorear tendencia | Product+Eng |
| Token cost / project | Dentro budget plan | Billing |

- Señal adicional E-01: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-02: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-03: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-04: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-05: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-06: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-07: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-08: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-09: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-10: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-11: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-12: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-13: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-14: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-15: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-16: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-17: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-18: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-19: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-20: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-21: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-22: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-23: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-24: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-25: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-26: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-27: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-28: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-29: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).
- Señal adicional E-30: revisar en monthly engineering review (latencias, costos infra, overrides, churn técnico, etc.).

## Apéndice F — Checklist release

1. [ ] Changelog escrito
2. [ ] Migraciones probadas en staging
3. [ ] Flags configuradas default seguro
4. [ ] Dashboards/alerts OK
5. [ ] Runbooks linkeados
6. [ ] Wedge e2e staging pass
7. [ ] Isolation suite pass
8. [ ] Perf smoke
9. [ ] Security checklist §8.8
10. [ ] Rollback ensayado (flag off)
11. [ ] Support notified
12. [ ] Comm owners oncall
13. [ ] OpenAPI/events publicados
14. [ ] Seed data tipologías/pricebooks OK
15. [ ] Billing meters verified
16. [ ] Backups recientes verified
17. [ ] Feature demo interna
18. [ ] Debt P0 = 0
19. [ ] Known issues documentados
20. [ ] LATAM locale/currency smoke

21. [ ] Item extendido de release checklist #21 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
22. [ ] Item extendido de release checklist #22 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
23. [ ] Item extendido de release checklist #23 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
24. [ ] Item extendido de release checklist #24 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
25. [ ] Item extendido de release checklist #25 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
26. [ ] Item extendido de release checklist #26 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
27. [ ] Item extendido de release checklist #27 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
28. [ ] Item extendido de release checklist #28 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
29. [ ] Item extendido de release checklist #29 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
30. [ ] Item extendido de release checklist #30 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
31. [ ] Item extendido de release checklist #31 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
32. [ ] Item extendido de release checklist #32 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
33. [ ] Item extendido de release checklist #33 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
34. [ ] Item extendido de release checklist #34 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
35. [ ] Item extendido de release checklist #35 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
36. [ ] Item extendido de release checklist #36 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
37. [ ] Item extendido de release checklist #37 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
38. [ ] Item extendido de release checklist #38 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
39. [ ] Item extendido de release checklist #39 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
40. [ ] Item extendido de release checklist #40 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
41. [ ] Item extendido de release checklist #41 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
42. [ ] Item extendido de release checklist #42 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
43. [ ] Item extendido de release checklist #43 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
44. [ ] Item extendido de release checklist #44 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
45. [ ] Item extendido de release checklist #45 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
46. [ ] Item extendido de release checklist #46 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
47. [ ] Item extendido de release checklist #47 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
48. [ ] Item extendido de release checklist #48 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
49. [ ] Item extendido de release checklist #49 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
50. [ ] Item extendido de release checklist #50 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
51. [ ] Item extendido de release checklist #51 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
52. [ ] Item extendido de release checklist #52 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
53. [ ] Item extendido de release checklist #53 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
54. [ ] Item extendido de release checklist #54 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
55. [ ] Item extendido de release checklist #55 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
56. [ ] Item extendido de release checklist #56 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
57. [ ] Item extendido de release checklist #57 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
58. [ ] Item extendido de release checklist #58 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
59. [ ] Item extendido de release checklist #59 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).
60. [ ] Item extendido de release checklist #60 (verificar según superficie: AI, plugins, enterprise, mobile, etc.).

## Apéndice G — Mapping Epic → Architecture domains

| Épica | Dominios arquitectura principales |
|-------|-------|
| E01 | Platform / Settings / Audit light |
| E02 | Identity / Billing / Audit |
| E03 | Media / Projects |
| E04 | Platform Jobs / Eventing / WS |
| E05 | Vision-Perception / Media |
| E06 | Geometry / Construction |
| E07 | Construction-MDO / Projects / Scenarios min |
| E08 | Materials / Plugins contracts |
| E09 | Costs / Materials |
| E10 | Costs / Audit / Reports |
| E11 | Scenarios / MDO / Costs |
| E12 | Frontend Studio / BFF / all read models |
| E13 | Reports / Costs / Media |
| E14 | Notifications / Identity |
| E15 | Chat / AI / MDO projections |
| E16 | AI / Billing / Eval |
| E17 | Timeline / Reports / Audit |
| E18 | Procurement / Costs / Audit |
| E19 | Plugins-Registry / Materials |
| E20 | Plugins packs / Materials / Costs |
| E21 | Marketplace / Procurement / Billing |
| E22 | Identity / Audit / Settings / Platform |
| E23 | API Gateway / Identity / Webhooks |
| E24 | Analytics / Platform |
| E25 | Mobile / Timeline / Media / Identity |

### G.1 Mapping capa L1/L2/L3 × épicas
| Capa | Épicas |
|-------|-------|
| L1 | E03 E05 (E12 overlays) |
| L2 | E06 E07 E08 E09 E10 E11 E17 E18 E19 E20 |
| L3 | E15 E16 (E13 narrativa) |
| Transversal | E01 E02 E04 E12 E14 E22 E23 E24 E25 |

## Apéndice H — Anti-scope creep list

Si aparece en un ticket sin ADR y sin pago explícito de oportunidad, **rechazar**:

1. LLM que genera geometría o cantidades autoritativas
2. Marketplace antes de MDO+PO+plugin contracts
3. ERP completo (inventario, contabilidad dual, nómina)
4. MS Project / Primavera clone
5. BIM Autodesk-complete parity
6. Microservicios por tabla
7. Multi-region active-active temprano
8. App móvil nativa antes de Studio estable
9. Analytics customer arbitrary SQL temprano
10. Hard-delete de signed/cert/usage
11. Chat sin citation guards
12. Auto-approve AIProposal
13. Perception escribiendo Costs
14. Costs leyendo Perception directo
15. Fork del core por tipología (usar plugin)
16. Custom Enterprise one-off sin packaging
17. Reescritura total big-bang del wedge
18. Síncrono CV en HTTP 'temporal para siempre'
19. Shared DB cross-domain sin ownership
20. Feature flags eternas sin expiry
21. Dark mode redesign distraction
22. Rediseño visual completo no pedido durante engines
23. Integraciones contables múltiples simultáneas
24. Soporte offline total Studio desktop
25. Realtime collaborative CRDT completo temprano
26. Marketplace de plugins abiertos sin sandbox
27. Data science notebooks sobre prod OLTP
28. Generative fill de planos
29. Crypto/blockchain provenance theater
30. Reemplazar motores deterministas por LLM 'más fácil'

### H.1 Frases que activan alarma de scope creep
- «Mientras estamos acá, agreguemos…»
- «Es igual de fácil hacer el Gantt completo»
- «El LLM ya lo saca de una»
- «Necesitamos microservicio aparte para esta tabla»
- «Marketplace light = marketplace real»
- «Enterprise pidió un custom único para ayer»
- «Saquemos el outbox y publicamos directo»
- «Firmemos el presupuesto automático si confidence alta»

---

## Registro de control del documento

| Campo | Valor |
|-------|-------|
| Versión documento | ARQ-IA 3.1 Engineering Roadmap |
| Fecha | 2026-08-02 |
| Estado | Plan de ingeniería oficial |
| Supersede | Cualquier roadmap informal previo no versionado |
| Alineado a | ARQ-IA 3.0 Arquitectura Definitiva + Master Plan + Auditoría aprobados |
| Mantenimiento | Actualizar al cerrar cada Phase A–E y al crear ADR material |
| Owner | CTO / Tech Lead |

### Fin del documento

*Documento de planificación. No contiene código de implementación. Cualquier implementación debe respetar MDO como SoT, L1→L2→L3, event-driven+plugins, Free/Pro/Enterprise, LATAM first, etapas 1–5, y la cuña comercial coloreado→cantidades→presupuesto moneda local, sin romper funcionalidad existente.*

## Apéndice I — Desglose mensual ilustrativo por épica P0 (equipo pequeño)

### I.E01 Plan de olas

Épica **E01 Platform Foundations & Observability** — 1–2 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E01 hacia «Dashboards core vivos; trace_id en request→job; flags con audit; CI bloquea P0 debt; runbook health/…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Over-instrumentation prematura
- Mitigación activa: SLIs mínimos por clase; expandir con dolor medido
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E01 hacia «Dashboards core vivos; trace_id en request→job; flags con audit; CI bloquea P0 debt; runbook health/…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Over-instrumentation prematura
- Mitigación activa: SLIs mínimos por clase; expandir con dolor medido
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E01 hacia «Dashboards core vivos; trace_id en request→job; flags con audit; CI bloquea P0 debt; runbook health/…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Over-instrumentation prematura
- Mitigación activa: SLIs mínimos por clase; expandir con dolor medido
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E01 hacia «Dashboards core vivos; trace_id en request→job; flags con audit; CI bloquea P0 debt; runbook health/…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Over-instrumentation prematura
- Mitigación activa: SLIs mínimos por clase; expandir con dolor medido
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E02 Plan de olas

Épica **E02 Identity, Tenancy & Billing hardening** — 1.5–3 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E02 hacia «Aislamiento CI verde; meters registran upload/AI/export; upgrade Free→Pro sin downtime; roles base e…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Roles ad-hoc en frontend
- Mitigación activa: AuthZ server-side obligatoria en dominio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E02 hacia «Aislamiento CI verde; meters registran upload/AI/export; upgrade Free→Pro sin downtime; roles base e…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Roles ad-hoc en frontend
- Mitigación activa: AuthZ server-side obligatoria en dominio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E02 hacia «Aislamiento CI verde; meters registran upload/AI/export; upgrade Free→Pro sin downtime; roles base e…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Roles ad-hoc en frontend
- Mitigación activa: AuthZ server-side obligatoria en dominio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E02 hacia «Aislamiento CI verde; meters registran upload/AI/export; upgrade Free→Pro sin downtime; roles base e…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Roles ad-hoc en frontend
- Mitigación activa: AuthZ server-side obligatoria en dominio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E03 Plan de olas

Épica **E03 Media & Object Storage** — 1–2 meses (1 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E03 hacia «Upload→evento→listo observable; soft-delete; quotas Free; signed URLs scoped; retention dry-run.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Uploads grandes fallan
- Mitigación activa: Multipart + resume
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E03 hacia «Upload→evento→listo observable; soft-delete; quotas Free; signed URLs scoped; retention dry-run.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Uploads grandes fallan
- Mitigación activa: Multipart + resume
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E03 hacia «Upload→evento→listo observable; soft-delete; quotas Free; signed URLs scoped; retention dry-run.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Uploads grandes fallan
- Mitigación activa: Multipart + resume
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E03 hacia «Upload→evento→listo observable; soft-delete; quotas Free; signed URLs scoped; retention dry-run.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Uploads grandes fallan
- Mitigación activa: Multipart + resume
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E04 Plan de olas

Épica **E04 Async Jobs & Event Bus (Outbox)** — 1.5–3 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E04 hacia «Flujo async observable; DLQ runbook; idempotencia demostrada; WS progress en Studio.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Dual-write sin outbox
- Mitigación activa: Outbox obligatorio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E04 hacia «Flujo async observable; DLQ runbook; idempotencia demostrada; WS progress en Studio.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Dual-write sin outbox
- Mitigación activa: Outbox obligatorio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E04 hacia «Flujo async observable; DLQ runbook; idempotencia demostrada; WS progress en Studio.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Dual-write sin outbox
- Mitigación activa: Outbox obligatorio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E04 hacia «Flujo async observable; DLQ runbook; idempotencia demostrada; WS progress en Studio.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Dual-write sin outbox
- Mitigación activa: Outbox obligatorio
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E05 Plan de olas

Épica **E05 Perception Engine (CV/OCR) modernization** — 2–4 meses (1–3 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E05 hacia «Evidence pack + confidence; color map UX; replay por pipeline_version; eventos listos para Geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Nondeterminism / model drift
- Mitigación activa: pipeline_version + golden fixtures LATAM
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E05 hacia «Evidence pack + confidence; color map UX; replay por pipeline_version; eventos listos para Geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Nondeterminism / model drift
- Mitigación activa: pipeline_version + golden fixtures LATAM
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E05 hacia «Evidence pack + confidence; color map UX; replay por pipeline_version; eventos listos para Geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Nondeterminism / model drift
- Mitigación activa: pipeline_version + golden fixtures LATAM
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E05 hacia «Evidence pack + confidence; color map UX; replay por pipeline_version; eventos listos para Geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Nondeterminism / model drift
- Mitigación activa: pipeline_version + golden fixtures LATAM
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E06 Plan de olas

Épica **E06 Geometry Engine** — 2–4 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E06 hacia «Compute→ChangeOps; issues visibles; golden verde; cero path LLM→geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Escala mal calibrada
- Mitigación activa: UX calibración + blockers de compute
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E06 hacia «Compute→ChangeOps; issues visibles; golden verde; cero path LLM→geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Escala mal calibrada
- Mitigación activa: UX calibración + blockers de compute
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E06 hacia «Compute→ChangeOps; issues visibles; golden verde; cero path LLM→geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Escala mal calibrada
- Mitigación activa: UX calibración + blockers de compute
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E06 hacia «Compute→ChangeOps; issues visibles; golden verde; cero path LLM→geometry.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Escala mal calibrada
- Mitigación activa: UX calibración + blockers de compute
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E07 Plan de olas

Épica **E07 MDO Core (entities, versions, changesets)** — 2–5 meses (1–3 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E07 hacia «Wedge sobre ProjectVersion; versions inmutables al cerrar; lineage evidence→element; AuthZ API.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Schema incompleto eterno
- Mitigación activa: Cerrar MDO schema v1 + evolve
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E07 hacia «Wedge sobre ProjectVersion; versions inmutables al cerrar; lineage evidence→element; AuthZ API.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Schema incompleto eterno
- Mitigación activa: Cerrar MDO schema v1 + evolve
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E07 hacia «Wedge sobre ProjectVersion; versions inmutables al cerrar; lineage evidence→element; AuthZ API.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Schema incompleto eterno
- Mitigación activa: Cerrar MDO schema v1 + evolve
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E07 hacia «Wedge sobre ProjectVersion; versions inmutables al cerrar; lineage evidence→element; AuthZ API.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Schema incompleto eterno
- Mitigación activa: Cerrar MDO schema v1 + evolve
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E08 Plan de olas

Épica **E08 Materials Engine** — 1.5–3 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E08 hacia «Color→typology→formula→TakeoffLine con provenance; overrides HITL; MaterialCalculado emitido.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: DSL demasiado poderoso
- Mitigación activa: Sandbox de expresiones limitado
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E08 hacia «Color→typology→formula→TakeoffLine con provenance; overrides HITL; MaterialCalculado emitido.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: DSL demasiado poderoso
- Mitigación activa: Sandbox de expresiones limitado
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E08 hacia «Color→typology→formula→TakeoffLine con provenance; overrides HITL; MaterialCalculado emitido.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: DSL demasiado poderoso
- Mitigación activa: Sandbox de expresiones limitado
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E08 hacia «Color→typology→formula→TakeoffLine con provenance; overrides HITL; MaterialCalculado emitido.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: DSL demasiado poderoso
- Mitigación activa: Sandbox de expresiones limitado
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E09 Plan de olas

Épica **E09 Costs & PriceBooks** — 1.5–3 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E09 hacia «Budget total en Project.currency; CostoActualizado; precision tests; pricebook org/project.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: FX/multimoneda
- Mitigación activa: CurrencyRate as_of + freeze on sign
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E09 hacia «Budget total en Project.currency; CostoActualizado; precision tests; pricebook org/project.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: FX/multimoneda
- Mitigación activa: CurrencyRate as_of + freeze on sign
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E09 hacia «Budget total en Project.currency; CostoActualizado; precision tests; pricebook org/project.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: FX/multimoneda
- Mitigación activa: CurrencyRate as_of + freeze on sign
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E09 hacia «Budget total en Project.currency; CostoActualizado; precision tests; pricebook org/project.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: FX/multimoneda
- Mitigación activa: CurrencyRate as_of + freeze on sign
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E10 Plan de olas

Épica **E10 Takeoff Projections & Signed Budgets** — 1–2 meses (1 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E10 hacia «Sign crea snapshot+hash; no mutate; evento PresupuestoFirmado; proyección takeoff estable post-sign.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Snapshot incompleto
- Mitigación activa: Freeze takeoff+prices+FX+versions
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E10 hacia «Sign crea snapshot+hash; no mutate; evento PresupuestoFirmado; proyección takeoff estable post-sign.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Snapshot incompleto
- Mitigación activa: Freeze takeoff+prices+FX+versions
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E10 hacia «Sign crea snapshot+hash; no mutate; evento PresupuestoFirmado; proyección takeoff estable post-sign.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Snapshot incompleto
- Mitigación activa: Freeze takeoff+prices+FX+versions
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E10 hacia «Sign crea snapshot+hash; no mutate; evento PresupuestoFirmado; proyección takeoff estable post-sign.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Snapshot incompleto
- Mitigación activa: Freeze takeoff+prices+FX+versions
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E12 Plan de olas

Épica **E12 Frontend Workspace & Model Explorer** — 2–4 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E12 hacia «Flujo wedge completo en Studio sobre MDO; progress jobs; explorer navega entidades; no inventa datos…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Estado UI duplica MDO
- Mitigación activa: Server SoT; UI cache descartable
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E12 hacia «Flujo wedge completo en Studio sobre MDO; progress jobs; explorer navega entidades; no inventa datos…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Estado UI duplica MDO
- Mitigación activa: Server SoT; UI cache descartable
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E12 hacia «Flujo wedge completo en Studio sobre MDO; progress jobs; explorer navega entidades; no inventa datos…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Estado UI duplica MDO
- Mitigación activa: Server SoT; UI cache descartable
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E12 hacia «Flujo wedge completo en Studio sobre MDO; progress jobs; explorer navega entidades; no inventa datos…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Estado UI duplica MDO
- Mitigación activa: Server SoT; UI cache descartable
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

### I.E16 Plan de olas

Épica **E16 AI Orchestrator / Guards / Eval** — 2–3.5 meses (1–2 eng)

#### Ola 1 — Contratos y skeleton

- Objetivo de ola: avanzar E16 hacia «Guards en path; proposals HITL; eval nightly; quotas; cero write autoritativo desde LLM.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Guard bypass
- Mitigación activa: Defense in depth + tests red team
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 2 — Vertical slice usable

- Objetivo de ola: avanzar E16 hacia «Guards en path; proposals HITL; eval nightly; quotas; cero write autoritativo desde LLM.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Guard bypass
- Mitigación activa: Defense in depth + tests red team
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 3 — Hardening tests/obs/flags

- Objetivo de ola: avanzar E16 hacia «Guards en path; proposals HITL; eval nightly; quotas; cero write autoritativo desde LLM.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Guard bypass
- Mitigación activa: Defense in depth + tests red team
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

#### Ola 4 — Rollout y DoD

- Objetivo de ola: avanzar E16 hacia «Guards en path; proposals HITL; eval nightly; quotas; cero write autoritativo desde LLM.…»
- Entregables: al menos una feature F* mergeada o flag-ready
- Riesgo a vigilar: Guard bypass
- Mitigación activa: Defense in depth + tests red team
- Demo interna al cierre de ola
- Actualizar critical path §6 si hay deslizamiento

## Apéndice J — Inventario completo Feature IDs

- `E01-F01` — Observabilidad base (logs/traces/metrics) (prioridad épica P0)
- `E01-F02` — Health, readiness y degradación (prioridad épica P0)
- `E01-F03` — Feature flags & config dinámica (prioridad épica P0)
- `E01-F04` — CI quality gates & engineering standards (prioridad épica P0)
- `E01-F05` — Runbooks y operabilidad inicial (prioridad épica P0)
- `E02-F01` — AuthN sesiones y recuperación (prioridad épica P0)
- `E02-F02` — Organizations & memberships (prioridad épica P0)
- `E02-F03` — Entitlements Free/Pro/Enterprise (prioridad épica P0)
- `E02-F04` — Usage meters & quotas (prioridad épica P0)
- `E02-F05` — Billing provider integration light (prioridad épica P0)
- `E02-F06` — Audit identity actions (prioridad épica P0)
- `E03-F01` — Upload sessions & signed URLs (prioridad épica P0)
- `E03-F02` — Derivatives pipeline (prioridad épica P0)
- `E03-F03` — MediaAsset lifecycle & retention (prioridad épica P0)
- `E03-F04` — Security & malware light (prioridad épica P0)
- `E04-F01` — Jobs API & state machine (prioridad épica P0)
- `E04-F02` — Outbox pattern (prioridad épica P0)
- `E04-F03` — Queues, retries, DLQ, fairness (prioridad épica P0)
- `E04-F04` — WebSocket progress & presence light (prioridad épica P0)
- `E04-F05` — Event envelope & schema registry light (prioridad épica P0)
- `E05-F01` — Pipeline versioning & job orchestration (prioridad épica P0)
- `E05-F02` — Normalize + OCR (prioridad épica P0)
- `E05-F03` — Color segmentation (wedge crítico) (prioridad épica P0)
- `E05-F04` — Symbol assist & evidence pack (prioridad épica P0)
- `E05-F05` — Replay, golden sets & quality gates (prioridad épica P0)
- `E06-F01` — Calibration de escala (prioridad épica P0)
- `E06-F02` — Compute measures determinista (prioridad épica P0)
- `E06-F03` — Validators & GeometryIssue (prioridad épica P0)
- `E06-F04` — Spatial relations light (prioridad épica P0)
- `E06-F05` — Integration contract con MDO (prioridad épica P0)
- `E07-F01` — MDO schema v1 entities (prioridad épica P0)
- `E07-F02` — ProjectVersion lifecycle (prioridad épica P0)
- `E07-F03` — ChangeSet / ChangeOp engine (prioridad épica P0)
- `E07-F04` — Projections materializadas (prioridad épica P0)
- `E07-F05` — Strangler: wedge escribe a MDO (prioridad épica P0)
- `E07-F06` — Quality flags & provenance on entities (prioridad épica P0)
- `E08-F01` — Typology & catalog core LATAM (prioridad épica P0)
- `E08-F02` — Formula engine versionado (prioridad épica P0)
- `E08-F03` — Takeoff compute & lines (prioridad épica P0)
- `E08-F04` — Overrides HITL (prioridad épica P0)
- `E08-F05` — Plugin-ready formula contracts (prioridad épica P0)
- `E09-F01` — Pricebook management (prioridad épica P0)
- `E09-F02` — Currency & FX (prioridad épica P0)
- `E09-F03` — Budget compute (prioridad épica P0)
- `E09-F04` — Plan gates on costs features (prioridad épica P0)
- `E10-F01` — Takeoff/Cost projections API (prioridad épica P0)
- `E10-F02` — SignedBudget HITL (prioridad épica P0)
- `E10-F03` — Commercial audit trail (prioridad épica P0)
- `E11-F01` — Scenario CRUD & head versions (prioridad épica P1)
- `E11-F02` — Compare takeoff/cost (prioridad épica P1)
- `E11-F03` — Merge MVP & conflicts (prioridad épica P1)
- `E11-F04` — Promote to baseline (prioridad épica P1)
- `E12-F01` — Workspace shell & layout (prioridad épica P0)
- `E12-F02` — Canvas plano + overlays (prioridad épica P0)
- `E12-F03` — Model Explorer & Inspector (prioridad épica P0)
- `E12-F04` — Takeoff & Budget panels (prioridad épica P0)
- `E12-F05` — Jobs tray & notifications UI (prioridad épica P0)
- `E13-F01` — Report job pipeline (prioridad épica P1)
- `E13-F02` — PDF budget/takeoff (prioridad épica P1)
- `E13-F03` — Excel exports (prioridad épica P1)
- `E13-F04` — Entitlements & abuse controls (prioridad épica P1)
- `E14-F01` — In-app notifications (prioridad épica P1)
- `E14-F02` — Email templates ES (prioridad épica P1)
- `E14-F03` — Preferences & digests (prioridad épica P1)
- `E15-F01` — Threads & messages (prioridad épica P1)
- `E15-F02` — Context assembly & retrieval UX (prioridad épica P1)
- `E15-F03` — Insert to doc / commercial use (prioridad épica P1)
- `E15-F04` — Memory & multi-user light (prioridad épica P1)
- `E16-F01` — Orchestrator & tool allowlist (prioridad épica P0)
- `E16-F02` — Policy guards (prioridad épica P0)
- `E16-F03` — AIProposal HITL (prioridad épica P0)
- `E16-F04` — Embeddings index (prioridad épica P0)
- `E16-F05` — Eval service & quotas (prioridad épica P0)
- `E17-F01` — Milestones & sequence MVP (prioridad épica P2)
- `E17-F02` — Progress notes light (prioridad épica P2)
- `E17-F03` — Certifications immutable (prioridad épica P2)
- `E18-F01` — PO from budget lines (prioridad épica P2)
- `E18-F02` — Approvals HITL (prioridad épica P2)
- `E18-F03` — Cancel & export (prioridad épica P2)
- `E19-F01` — Manifest & registry (prioridad épica P2)
- `E19-F02` — Host runtime sandbox (prioridad épica P2)
- `E19-F03` — Install lifecycle (prioridad épica P2)
- `E19-F04` — SDK & sample plugin (prioridad épica P2)
- `E20-F01` — Steel Frame pack (prioridad épica P2)
- `E20-F02` — Hormigón Armado pack (prioridad épica P2)
- `E20-F03` — Gas pack (prioridad épica P2)
- `E20-F04` — Fire / otras packs pipeline (prioridad épica P2)
- `E21-F01` — Provider & catalog sync (prioridad épica P3)
- `E21-F02` — Quotes (prioridad épica P3)
- `E21-F03` — Orders & payments light (prioridad épica P3)
- `E21-F04` — Trust & compliance light (prioridad épica P3)
- `E22-F01` — SSO/SAML/OIDC (prioridad épica P2)
- `E22-F02` — RBAC/ABAC fino (prioridad épica P2)
- `E22-F03` — Audit export & legal hold (prioridad épica P2)
- `E22-F04` — Multi-company & DR light (prioridad épica P2)
- `E23-F01` — API keys & public resources (prioridad épica P2)
- `E23-F02` — Webhooks (prioridad épica P2)
- `E23-F03` — Integrations accounting light (prioridad épica P2)
- `E24-F01` — Event ingestion to lake (prioridad épica P3)
- `E24-F02` — Marts wedge & quality (prioridad épica P3)
- `E24-F03` — Self-serve later (prioridad épica P3)
- `E25-F01` — Mobile auth & project picker (prioridad épica P3)
- `E25-F02` — Read models field (prioridad épica P3)
- `E25-F03` — Capture media & progress (prioridad épica P3)
- `E25-F04` — Distribution & ops (prioridad épica P3)

## Apéndice K — Inventario de eventos por épica

### K.E01
- SettingsActualizados
- UsoRegistrado (meter platform opcional)

### K.E02
- UsuarioRegistrado
- UsuarioInvitado
- MiembroRolCambiado
- SuscripcionCambiada
- UsoRegistrado
- UsoConsumido
- QuotaUmbralAlcanzado
- PagoFallido

### K.E03
- PlanoSubido
- MediaAssetListo
- DerivadoGenerado
- MediaRetencionAplicada

### K.E04
- job.progress
- job.completed
- job.failed
- eventos dominio vía envelope

### K.E05
- PercepcionIniciada
- PlanoProcesado
- PercepcionFallida
- EvidenciaCreada
- ColorMapActualizado

### K.E06
- CalibracionActualizada
- GeometriaCalculada
- GeometriaInvalidaDetectada
- ModeloActualizado

### K.E07
- ModeloActualizado
- ElementoCreado
- ElementoTipificado
- EspacioActualizado
- ProyeccionInvalidada
- ChangeSetCreado
- ChangeSetConfirmado

### K.E08
- MaterialCalculado
- TakeoffOverrideAplicado
- FormulaVersionPublicada
- TipologiaMapeada

### K.E09
- CostoActualizado
- PresupuestoCreado
- PricebookActualizado
- CurrencyRatesActualizadas

### K.E10
- PresupuestoFirmado
- ProyeccionInvalidada

### K.E11
- EscenarioCreado
- EscenarioMerged
- EscenarioPromovido
- EscenarioEliminado
- ConflictoDetectado

### K.E12
- (consume) job.*, ModeloActualizado, CostoActualizado

### K.E13
- ReporteSolicitado
- ReporteGenerado
- ReporteFallido

### K.E14
- NotificacionEnviada
- NotificacionFallida

### K.E15
- ChatIniciado
- MensajeChatRegistrado
- ChatRespuestaUsadaEnDoc

### K.E16
- AIProposalCreada
- AIProposalResuelta
- EmbeddingsActualizados
- AIQuotaExcedida

### K.E17
- HitoCreado
- SecuenciaActualizada
- CertificacionEmitida

### K.E18
- OrdenCompraCreada
- OrdenCompraAprobada
- OrdenCompraCancelada

### K.E19
- PluginInstalado
- PluginActualizado
- PluginDeshabilitado
- PluginValidacionFallida

### K.E20
- FormulaVersionPublicada (por pack)
- PluginInstalado

### K.E21
- ProveedorSeleccionado
- CotizacionCreada
- CompraRealizada
- OrdenCancelada
- CatalogoProveedorSincronizado

### K.E22
- MiembroRolCambiado (fine)
- PoliticaRetencionCambiada
- SuscripcionCambiada

### K.E23
- WebhookDelivery*
- UsoRegistrado (api)

### K.E24
- (consume domain events to lake)

### K.E25
- HitoCreado (mobile)
- MediaAssetListo
- Progress notes events

## Apéndice L — Inventario de entidades por épica

### L.E01
- FeatureFlag
- ReleaseMarker
- HealthCheckRecord
- SliSnapshot

### L.E02
- Organization
- User
- Membership
- Session
- PlanEntitlement
- UsageMeter
- InvoiceRef

### L.E03
- MediaAsset
- MediaDerivative
- UploadSession
- RetentionPolicy

### L.E04
- Job
- JobAttempt
- OutboxMessage
- DeadLetter
- ConsumerCheckpoint

### L.E05
- PerceptionJob
- Evidence
- ColorRegion
- OcrBlock
- PipelineVersion

### L.E06
- ElementGeometry
- Calibration
- GeometryIssue
- MeasureSet

### L.E07
- Site
- Building
- Level
- Space
- System
- Element
- ProjectVersion
- ChangeSet
- ChangeOp
- Connection
- ParameterSet

### L.E08
- Typology
- Formula
- TakeoffLine
- MaterialCatalogItem
- WasteFactor
- TakeoffOverride

### L.E09
- Pricebook
- PriceItem
- Budget
- BudgetLine
- CurrencyRate

### L.E10
- SignedBudget
- TakeoffProjection
- CostProjection
- SignatureMeta

### L.E11
- Scenario
- ScenarioCompare
- MergeConflict

### L.E12
- UiPreference
- WorkspaceLayout

### L.E13
- ReportJob
- ReportArtifact
- ReportTemplate

### L.E14
- Notification
- NotificationPreference
- EmailDelivery

### L.E15
- ChatThread
- ChatMessage
- ChatCitation
- ChatMemorySlice

### L.E16
- AIProposal
- ToolCallLog
- EvalCase
- EmbeddingChunk
- PolicyDecision

### L.E17
- Milestone
- WorkSequence
- Certification
- ProgressNote

### L.E18
- PurchaseOrder
- PurchaseOrderLine
- Approval

### L.E19
- PluginManifest
- PluginInstallation
- PluginVersion
- CapabilityGrant

### L.E20
- PackTypology set
- PackFormula set
- PackFixture

### L.E21
- Provider
- CatalogItem
- Quote
- MarketplaceOrder

### L.E22
- OrgUnit
- Team
- RoleBinding
- SsoConnection
- LegalHold
- AuditExportJob

### L.E23
- ApiKey
- WebhookEndpoint
- WebhookDelivery

### L.E24
- AnalyticsEvent
- MartWedgeFunnel
- MartQuality

### L.E25
- MobileSession
- OfflineQueue

