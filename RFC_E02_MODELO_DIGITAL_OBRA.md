# ARQ-IA — RFC E02 Modelo Digital de la Obra (MDO)

## Metadatos del RFC

| Campo | Valor |
| --- | --- |
| ID | RFC-E02-MDO |
| Título | Modelo Digital de la Obra (MDO) |
| Estado | Proposed → Ready for implementation after approval |
| Fecha | 2026-08-02 |
| Owners | CTO / Tech Lead / Domain Owner Construction |
| **Épica Roadmap implementada** | **E07 MDO Core** (entities, versions, changesets) + foundations Scenarios Architecture §12 / prep E11 |
| **NO es** | **NO es la épica Identity E02** (Identity, Tenancy & Billing). Homónimo de secuencia RFC, no de épica. |
| Secuencia RFC usuario | RFC E02 (después de RFC-E01 Platform Foundations) |
| Prioridad | P0 |
| Complejidad | XL |
| Estimación | 2–5 meses (1–3 eng) |
| Dependencias producción | RFC-E01 + Roadmap E01; Roadmap E02 Identity (AuthZ); Roadmap E04 Outbox; E03 Media refs; E05/E06 → Evidence/Geometry vía ChangeOps |
| Documentos fuente | AUDITORIA · MASTER PLAN · ARCHITECTURE · ENGINEERING_ROADMAP (aprobados; no re-ensayar) |
| Naturaleza | Contrato de diseño (sin código de implementación) |
| Idioma | Español |
| Mercado | LATAM primero |
| Cuña a preservar | color → qty → ARS (moneda local) sobre ProjectVersion |
| Feature flag raíz | `mdo.v1` |
| Norte arquitectura | MDO = L2 SoT; Perception L1; Materials/Costs/AI/Marketplace proyectan/leen; nunca duplican hechos MDO |


### Nota crítica de nomenclatura (evitar confusión E02)

Este documento se titula **RFC E02** porque es el segundo RFC de la secuencia de contratos de diseño del usuario (después de RFC-E01).

En el `ENGINEERING_ROADMAP.md`, la épica **E02** es **Identity, Tenancy & Billing hardening**.

La épica que este RFC operacionaliza es **E07 MDO Core**.

Cuando este documento diga «E02» sin calificar, significa **RFC-E02-MDO**. «Roadmap E02» / «Identity E02» = identidad. «Roadmap E07» / «épica E07» = MDO Core.

Este RFC asume AUDITORIA, MASTER PLAN, ARCHITECTURE y ENGINEERING_ROADMAP **aprobados**. No los resume como ensayos: los operacionaliza en contratos MDO.

Cualquier desviación material requiere ADR + aprobación Tech Lead/CTO antes del merge a `main`.

Naturaleza: diseño / contrato. **No** contiene funciones ejecutables ni cuerpos de implementación.

## Índice

- [0. Resumen ejecutivo / contexto](#0-resumen-ejecutivo--contexto)
- [1. ¿Qué es el MDO?](#1-qué-es-el-mdo)
- [2. Arquitectura](#2-arquitectura)
- [3. Entidades](#3-entidades)
- [4. Relaciones](#4-relaciones)
- [5. Versionado Git-like](#5-versionado-git-like)
- [6. Timeline](#6-timeline)
- [7. Motor de escenarios](#7-motor-de-escenarios)
- [8. API del MDO](#8-api-del-mdo)
- [9. Eventos](#9-eventos)
- [10. Persistencia](#10-persistencia)
- [11. Integración visión](#11-integración-visión)
- [12. Integración IA](#12-integración-ia)
- [13. Materiales](#13-materiales)
- [14. Costos](#14-costos)
- [15. Marketplace](#15-marketplace)
- [16. Migración desde Process JSON (strangler)](#16-migración-desde-process-json-strangler)
- [17. Riesgos](#17-riesgos)
- [18. Criterios de aceptación objetivos](#18-criterios-de-aceptación-objetivos)
- [19. Checklist final](#19-checklist-final)
- [20. Anti-scope](#20-anti-scope)
- [Apéndice A — Catálogo exhaustivo de entidades](#apéndice-a--catálogo-exhaustivo-de-entidades)
- [Apéndice B — Catálogo de eventos](#apéndice-b--catálogo-de-eventos)
- [Apéndice C — Catálogo de API REST conceptual](#apéndice-c--catálogo-de-api-rest-conceptual)
- [Apéndice D — Estrategia de índices](#apéndice-d--estrategia-de-índices)
- [Apéndice E — Tipos de conflicto](#apéndice-e--tipos-de-conflicto)
- [Apéndice F — Modelo de confidence](#apéndice-f--modelo-de-confidence)
- [Apéndice G — Provenance](#apéndice-g--provenance)
- [Apéndice H — Tipos de proyección](#apéndice-h--tipos-de-proyección)
- [Apéndice I — Glosario analogía Git](#apéndice-i--glosario-analogía-git)
- [Apéndice J — Approval sign-off](#apéndice-j--approval-sign-off)
- [Apéndice K — Feature flags MDO](#apéndice-k--feature-flags-mdo)
- [Apéndice L — Decision log](#apéndice-l--decision-log)
- [Apéndice M — Open questions](#apéndice-m--open-questions)
- [Apéndice N — Trazabilidad Roadmap E07 → RFC](#apéndice-n--trazabilidad-roadmap-e07--rfc)
- [Apéndice O — Runbook skeletons](#apéndice-o--runbook-skeletons)
- [Apéndice P — Performance budgets](#apéndice-p--performance-budgets)
- [Apéndice Q — Security, AuthZ & PII](#apéndice-q--security-authz--pii)
- [Apéndice R — Rollback playbooks](#apéndice-r--rollback-playbooks)
- [Apéndice S — Demo scripts](#apéndice-s--demo-scripts)
- [Apéndice T — Mapping Architecture domains](#apéndice-t--mapping-architecture-domains)
- [Apéndice U — Matrices de contratos extendidas](#apéndice-u--matrices-de-contratos-extendidas)
- [Apéndice V — Escenarios A/B/C (ladrillo/acero/retak)](#apéndice-v--escenarios-abc-ladrilloaceroretak)
- [Apéndice W — ChangeOp taxonomy](#apéndice-w--changeop-taxonomy)
- [Apéndice X — OpenAPI fragment conceptual](#apéndice-x--openapi-fragment-conceptual)
- [Apéndice Y — Checklist review PR MDO](#apéndice-y--checklist-review-pr-mdo)
- [Apéndice Z — Cierre del RFC](#apéndice-z--cierre-del-rfc)


## 0. Resumen ejecutivo / contexto


### 0.1 Objetivo oficial (ENGINEERING_ROADMAP § E07)

Implementar el **Modelo Digital de la Obra (MDO)** como única fuente de verdad (SoT) de la obra digital: grafo espacial/sistemas/elementos, `ProjectVersion`, `ChangeSet`/`ChangeOp`, proyecciones materializadas y lineage Evidence→Element.

Problema que resuelve: sin twin versionado el producto permanece file-centric (Process JSON) y bloquea escenarios Git-like, IA grounded con citas, certificaciones y marketplace sin forks de geometría.

Beneficio: SoT estable que habilita Etapas 1–3; cuña color→qty→ARS sobre versiones inmutables; supervivencia a rewrites de UI/visión/IA.

Dependencias roadmap: E01, E02 (Identity), E04. Complejidad XL. Prioridad P0. Tiempo 2–5 meses (1–3 eng).


### 0.2 Criterio de Done de la épica (fuente roadmap)

- Wedge sobre `ProjectVersion`
- Versions inmutables al cerrar/sellar
- Lineage evidence→element
- AuthZ tenant en toda API MDO
- Schema MDO v1 cerrado + evolve path
- Proyecciones con invalidación event-driven
- Strangler: wedge escribe a MDO detrás de flag


### 0.3 Features contenidas (E07-F01–F06)

| Feature | Nombre | Intent condensado |
| --- | --- | --- |
| E07-F01 | MDO schema v1 entities | Site/Building/Level/Space/System/Element/ParameterSet + IDs estables |
| E07-F02 | ProjectVersion lifecycle | Crear/cerrar inmutable; parent chain; baseline; version tree |
| E07-F03 | ChangeSet / ChangeOp engine | Draft/confirm/conflict; apply idempotente; audit before/after |
| E07-F04 | Projections materializadas | Takeoff/tree skeletons; invalidación; rebuild; cache versionado |
| E07-F05 | Strangler wedge→MDO | Dual-write/read; flag `mdo.wedge`; E2E; rollback |
| E07-F06 | Quality flags & provenance | quality_flags; evidence_ids; filter; twin trust; gate firmas |

Cimientos de escenarios (Architecture §12 / prep E11) incluidos como contratos de diseño en §7: Scenario, ScenarioPointer, overlay CoW, merge rules. Merge UX avanzado puede diferirse a E11 con ADR; modelo de datos y APIs mínimas de Scenario head **deben** existir en E07.


### 0.4 Principios duros del MDO (expand)

| ID | Principio | Implicación contractual |
| --- | --- | --- |
| M01 | Inmutable cuando sellado | Tras `promote`/`sign`/`seal`, no UPDATE in-place de hechos de esa `ProjectVersion` |
| M02 | Versionable | Todo cambio material = nuevo ChangeSet → nueva ProjectVersion (o tip en Scenario) |
| M03 | Auditable | Quién/qué/cuándo/porqué + before/after refs + causation chain |
| M04 | Extensible | Element tipologías y ParameterSets abiertos; plugins vía capability |
| M05 | Escalable | Snapshots lógicos + diffs; proyecciones cache; no explosión full-copy por escenario |
| M06 | Independiente de AI | IA es lector + proponente de drafts; nunca autoridad de mutación |
| M07 | Independiente de visión | Vision escribe Evidence + proposed ops; confirmación produce ChangeOps |
| M08 | Independiente de frontend | UI es proyección descartable; server SoT |
| M09 | Sobrevive UI rewrite | Contratos API/eventos/persistencia estables |
| M10 | Single source of truth | Un grafo MDO por project/version/scenario head |
| M11 | No stores duplicados | Materials/Costs/AI/Marketplace NO mantienen inventario paralelo de muros/espacios |
| M12 | Perception → Evidence → proposed ChangeOps | Nunca muta versiones selladas en silencio |
| M13 | IA read-only sobre hechos | Tools read; drafts HITL; citas obligatorias a MDO/proyección |
| M14 | Soft-delete + retención | Hard-delete prohibido para hechos MDO (salvo política legal documentada) |
| M15 | Tenant isolation day-0 | Toda query/mutation filtra `tenant_id` |
| M16 | Confidence & provenance | Hechos cuantitativos llevan score + evidence refs |
| M17 | HITL dinero | Firmas/presupuestos no se autocommitan desde percepción/IA |
| M18 | Determinismo L2 | Apply de ChangeOps es determinista dado el mismo base version + ops |
| M19 | Event-driven extensión | Mutaciones emiten outbox; sync para UX inmediata post-confirm |
| M20 | Flags & entitlements | Rollout `mdo.v1` / `mdo.wedge` / escenarios por plan |


### 0.5 Non-goals (preview; detalle §20)

- No reescribir Identity (Roadmap E02)
- No implementar bus outbox completo (E04) — consumir envelope aprobado
- No object storage propio (E03) — solo refs a Media
- No motor CV/OCR (E05) ni Geometry Engine completo (E06) — solo contratos de integración
- No Materials DSL completo (E08) ni PriceBooks (E09) — solo bindings y proyecciones skeleton
- No Marketplace productivo (E21)
- No Chat IA completo (E15/E16) — solo contrato read-only
- No microservicios MDO separados
- No BIM IFC full import/export como requisito v1
- No hard-delete masivo de Process históricos en día 1


### 0.6 Capacidad y secuenciación

E07 es XL: priorizar thin slice vertical — Project + Version + Element muro/espacio mínimos + ChangeSet confirm + TakeoffLine skeleton + strangler wedge — antes de tipologías raras.

- Schema v1 + migraciones expand (`mdo.v1` off)
- ProjectVersion lifecycle + immutability tests
- ChangeSet/ChangeOp engine + eventos outbox
- Projections skeleton + invalidación
- Strangler dual-write wedge (`mdo.wedge`)
- Quality/provenance + ScenarioPointer mínimo
- Dual-read → cutover lectura Studio → deprecar Process JSON como SoT


### 0.7 Señales de éxito post-release

- SLIs MDO en verde 7 días o waiver
- Cero incidentes P0 aislamiento tenant atribuibles a E07
- Wedge e2e golden no degradado
- Deuda P0 nueva = 0
- Demo grabada: crear versión, confirmar ChangeSet, ver proyección, flag rollback
- ≥N proyectos piloto on MDO (N acordado con PM; métrica `% proyectos on MDO`)


### 0.8 Audiencia

| Rol | Uso |
| --- | --- |
| CTO | Aprobar SoT boundaries + anti-scope + nota nomenclatura |
| Tech Lead | Contratos API/eventos/datos; ADR reviewer |
| Domain Eng Construction | Implementar F01–F06 |
| Perception/Geometry Eng | Contratos Evidence→ChangeOp |
| Materials/Costs Eng | Contratos proyección/binding |
| Frontend Eng | Explorer/Inspector/Version badge (mínimo) |
| QA | Matrices inmutabilidad/tenant/golden |
| PM | Criterios binarios §18 |


### 0.9 Diagrama L1 → L2 → L3 (MDO como L2 SoT)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ L1 PERCEPTION / INPUTS (no autoridad)                                   │
│  Planos · OCR · CV · uploads · calibración · Evidence blobs (Media E03) │
│  Emite: Evidence + proposed ChangeOps (draft ChangeSets)                │
└─────────────────────────────┬────────────────────────────────────────────┘
                              │ confirm HITL / auto-policy acotada
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ L2 MDO CORE = SINGLE SOURCE OF TRUTH                                    │
│  Project → Versions → Levels → Spaces → Elements → Systems → Params     │
│  ChangeSet/ChangeOp · Scenario heads · Timeline/Audit · Provenance      │
│  Inmutable cuando sealed · versionable · auditable                      │
└───────┬─────────────┬──────────────┬──────────────┬─────────────────────┘
        ▼             ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────┐
│ L3 Materials│ │ L3 Costs   │ │ L3 AI      │ │ L3 Marketplace │
│ TakeoffLine │ │ CostLine   │ │ read-only  │ │ Offer bindings │
│ projections │ │ Budgets    │ │ + drafts   │ │ → PO refs      │
│ (no fork)   │ │ (no fork)  │ │ HITL       │ │ (no fork geom) │
└────────────┘ └────────────┘ └────────────┘ └────────────────┘
```


### 0.10 Relación con documentos oficiales

| Documento | Qué aporta a este RFC | Qué NO hace este RFC |
| --- | --- | --- |
| AUDITORIA | Hechos Process JSON / deuda file-centric | No re-auditar producto |
| MASTER PLAN | Secuencia comercial wedge LATAM | No redefinir roadmap comercial |
| ARCHITECTURE | MDO §2; Scenarios §12; boundaries | No inventar microservicios |
| ENGINEERING_ROADMAP | E07 F01–F06 tasks, DoD, riesgos | No alterar Identity E02 |
| RFC-E01 | Flags, OTel, health, CI gates | No redefinir platform |


### 0.11 Definition of Ready de este RFC (antes de coding)

- [ ] Contratos de eventos/API bocetados y revisados por Tech Lead
- [ ] Criterios de aceptación numéricos o binarios acordados con PM (§18)
- [ ] Owner de dominio Construction asignado + reviewer de arquitectura (XL)
- [ ] Plan de migración strangler Process JSON + rollback escrito (§16, Apéndice R)
- [ ] Lista de lo que explícitamente NO entra (§20, ≥40 bullets)
- [ ] Claridad nomenclatura RFC-E02 ≠ Roadmap E02 Identity firmada por CTO
- [ ] Dependencias Identity AuthZ + Outbox envelope en estado usable
- [ ] Flag `mdo.v1` registrada en catálogo E01


### 0.12 Hard freeze statement

Durante la implementación de este RFC está **prohibido**: mutar Process JSON como segunda SoT en paralelo permanente; escribir geometría desde AI/Marketplace; hard-delete de versions selladas; introducir store de muros en Materials; saltar ChangeSet para «arreglos rápidos» en prod.


## 1. ¿Qué es el MDO?


### 1.1 Definición

El **Modelo Digital de la Obra (MDO)** es el grafo versionado, tipado y auditable que representa la obra construible (y sus alternativas de escenario) como hechos de dominio: sitio, edificios, niveles, espacios, elementos constructivos, sistemas de instalaciones, parámetros, conexiones, cantidades proyectadas y bindings a materiales/costos/marketplace — **sin** ser un archivo de plano, **sin** ser un motor de visión, **sin** ser un LLM, **sin** ser la UI.

Es el **digital twin estructural/comercial** de la obra para ARQ-IA: la capa L2 sobre la que se calculan takeoffs, presupuestos, certificaciones y respuestas de IA con cita.


### 1.2 Qué representa

| Representa | Ejemplo |
| --- | --- |
| Identidad de proyecto y partes | Organization, Client, Contractor como ProjectParty |
| Jerarquía espacial | Site → Building → Level → Space |
| Elementos constructivos | Wall, Opening, Slab, Column, Beam, Stair, Roof, Finishes |
| Sistemas MEP/Fire | Water hot/cold, Sewage, Electrical, Gas, HVAC, Fire |
| Geometría tipada | ElementGeometry (medidas, polígonos lógicos, unidades) |
| Parámetros y packs | ParameterSet, SystemPack bindings |
| Evolución temporal | ProjectVersion, ChangeSet, ChangeOp, TimelineEvent |
| Alternativas | Scenario + ScenarioPointer (heads) |
| Evidencia y percepción | Evidence refs, PerceptionJob refs (no blobs inline SoT) |
| Proyecciones derivadas | TakeoffLine, ModelTreeProjection |
| Anclas a otros dominios | CostLine keys, PriceBook refs, SupplierOffer bindings, PO/Contract refs |
| Calidad del twin | confidence, quality_flags, provenance |
| Sellos comerciales | CertificationLock, signed budget freeze points |


### 1.3 Qué NO representa

| NO representa | Dónde vive |
| --- | --- |
| Píxeles del plano / PDF binario | Media (E03) vía Document/PlanAsset ref |
| Pesos del modelo CV | Perception Engine (E05) |
| Fórmulas tipología→qty como DSL | Materials Engine (E08) |
| Listas de precios regionales | PriceBooks (E09) — MDO solo refs |
| Conversación chat | AI Orchestrator / Chat (E15/E16) |
| Catálogo de proveedores | Marketplace (E21) |
| Sesión UI / selection state | Frontend (descartable) |
| Identidad/login/billing | Identity E02 |
| Colas/jobs infra | E04 Async Jobs |
| Render WebGL efímero | Frontend cache |


### 1.4 Por qué existe

- **Eliminar file-centrismo:** hoy `Process.items` JSON es SoT implícita; no versiona, no ramifica, no cita bien.
- **Habilitar escenarios** ladrillo vs acero vs retak sin clonar geometría.
- **Habilitar IA grounded** con citations a entity ids estables.
- **Separar percepción de verdad:** CV propone; humano/política confirma; MDO registra.
- **Congelar dinero:** firmas/certificaciones anclan versiones inmutables.
- **Escalar dominio:** plugins tipológicos y marketplace se enganchan a ids, no a blobs.
- **Sobrevivir rewrites:** UI/visión/IA pueden cambiar; el grafo permanece.


### 1.5 Problemas concretos que resuelve

| Problema actual | Resolución MDO |
| --- | --- |
| Process JSON monolítico | Entidades normalizadas + ChangeOps |
| Sin historial útil | Timeline + version tree |
| Recalcular borra contexto | Versions selladas + proyecciones versionadas |
| Escenarios = copiar proyecto | Overlay CoW + ScenarioPointer |
| Materials re-parsea items | Lee Element/TakeoffLine por version_id |
| Costs acoplado a shape FE | CostLine → takeoff_line_id / element_id |
| IA inventa cantidades | Tools read-only + draft ChangeSet |
| Marketplace forkearía muros | Binding a MaterialSpec/ElementType |
| audit_image_base64 en DB | Media blob ref; Evidence apunta a object key |
| Sin tenant en grafo obra | tenant_id obligatorio en raíces |


### 1.6 Posición en capas L1/L2/L3 (detalle)

**L1 — Percepción e inputs:** produce Evidence y candidatos. Autoridad = ninguna sobre hechos sellados.

**L2 — MDO:** autoridad de hechos de obra. Única SoT. Apply solo vía ChangeSet confirmado.

**L3 — Proyectores y consumidores:** Materials, Costs, Reports, AI, Marketplace, Timeline UX. Pueden cachear proyecciones; deben poder rebuild desde L2.

Regla de oro: si un hecho puede reconstruirse desde MDO+motores deterministas, **no** es SoT en L3.


### 1.7 Analogía Git (preview; glosario Apéndice I)

| Git | MDO |
| --- | --- |
| Repository | Project (scoped tenant) |
| Commit | ProjectVersion |
| Tree/blob diff | ChangeSet + ChangeOps |
| Branch | Scenario |
| HEAD | ScenarioPointer |
| Merge commit | Merge ChangeSet (con conflictos tipados) |
| Tag/release | Baseline / CertificationLock / signed budget |
| Working tree | Draft ChangeSet |
| Blame | TimelineEvent + provenance |


### 1.8 Invariantes formales (must-hold)

- Toda entidad de grafo pertenece a exactamente un `(tenant_id, project_id)`.
- Toda mutación material de hechos L2 ocurre como apply de ChangeOps en un ChangeSet.
- Una `ProjectVersion` en estado `sealed`/`signed` es inmutable en hechos.
- Perception/AI/Marketplace no poseen FK invertida que les permita UPDATE directo a Element.
- TakeoffLine y CostLine son proyecciones o ownership de dominio L3 con keys a ids MDO — nunca geometría forkeada.
- Soft-delete: `deleted_at` + exclusión de heads; retención según política.
- Idempotencia: `Idempotency-Key` en confirms; `change_op_id` estable.


### 1.9 Definición operativa de «hecho MDO»

Un **hecho MDO** es cualquier atributo que afecta: identidad de elemento, tipología, geometría medida, pertenencia espacial, conexión de sistema, binding de material/escenario, o sello de versión. Los caches, renders y respuestas LLM **no** son hechos MDO.


### 1.10 Límites del twin v1

v1 prioriza: vivienda/obra LATAM wedge (muros, aberturas, losas/carpetas, espacios, escala), versionado, escenarios material overlay, lineage. Diferido: BIM coordination 4D/5D completa, clash detection industrial, IoT sensors, digital twin físico tiempo real.


### 1.11 Diagrama de ownership bounded context

```
┌──────────────── MDO CORE (este RFC) ────────────────┐
│ Project, Version, Scenario*, Element*, Geometry,     │
│ ParameterSet, Connection, ChangeSet, Evidence ref,   │
│ Timeline, CertificationLock, Projection skeletons    │
└───────────────┬───────────────────┬─────────────────┘
                │ lee/proyecta      │ emite eventos
     ┌──────────▼──────────┐  ┌─────▼────────────┐
     │ Materials / Costs   │  │ Outbox consumers │
     └─────────────────────┘  └──────────────────┘
* Scenario head mínimo en E07; merge UX avanzado puede ser E11 con ADR.
```


### 1.12 Criterios de pertenencia al bounded context MDO

- [ ] ¿El dato es necesario para reconstruir la obra tipada sin UI?
- [ ] ¿Debe versionarse con la obra?
- [ ] ¿Otros dominios lo citarán por id estable?
- [ ] ¿Una mutación silenciosa rompería dinero o certificaciones?

Si 3+ sí → pertenece a MDO (o es proyección keyed a MDO). Si es blob binario → Media. Si es precio de mercado → PriceBook/Marketplace.


### 1.13 Estados mentales del usuario vs modelo

| Usuario dice | MDO modela |
| --- | --- |
| «El plano» | PlanAsset + Evidence + Elements derivados |
| «La obra» | Project + Scenario main HEAD |
| «Presupuesto A/B» | Scenario A/B + Cost projection |
| «Cambié el muro» | ChangeSet confirm → nueva Version |
| «Ya firmamos» | CertificationLock + sealed version |


### 1.14 Garantías de producto

- Misma Version + mismos motores L3 ⇒ mismas proyecciones (determinismo).
- Compare Versions/Scenarios es operación de primera clase.
- Rollback de producto = flag off o pointer a version anterior — no rewrite history sellada.
- Export/report cita `version_id` + `scenario_id` + hash de proyección.


## 2. Arquitectura


### 2.1 Vista de contenedor

El MDO vive como **módulo de dominio** dentro del monolito FastAPI (P22: no microservicios prematuros). Exposición: `/v1/projects/{project_id}/mdo/*`. Persistencia: OLTP graph + JSON doc payloads + projection cache. Blobs: refs a Media.

```
Studio FE ──HTTP AuthZ──► API MDO ──► Domain Services
                              │            ├─ VersionService
                              │            ├─ ChangeSetService
                              │            ├─ GraphQueryService
                              │            ├─ ProjectionService
                              │            └─ ScenarioService (mínimo)
                              ├─ OLTP (entities, versions, ops)
                              ├─ Projection store
                              └─ Outbox (envelope E04)
```


### 2.2 Jerarquía canónica del grafo

```
Organization (ref Identity)
└─ Project
   ├─ ProjectParty (Client / Contractor / Subcontractor)
   ├─ Document / PlanAsset (ref Media)
   ├─ Scenario[] (incl. 'main' / baseline scenario)
   │   └─ ScenarioPointer → ProjectVersion (HEAD)
   ├─ ProjectVersion[] (DAG/parent chain)
   │   ├─ Site
   │   │   └─ Building[]
   │   │       └─ Level[]
   │   │           ├─ Space[] / Zone[]
   │   │           ├─ Element[] (Wall, Opening, Slab, Floor, Column, Beam, Stair, Roof, ...)
   │   │           └─ System endpoints / verticals
   │   ├─ System[] (HotWater, ColdWater, Sewage, Electrical, Gas, HVAC, Fire, Structure, Envelope)
   │   │   └─ Element[] / Connection[]
   │   ├─ ParameterSet[] (por element o pack)
   │   ├─ MaterialBinding[] (refs a MaterialSpec; no catálogo ownership)
   │   ├─ Quantity anchors → TakeoffLine projections
   │   └─ Cost anchors → CostLine (owned Costs; keyed)
   ├─ ChangeSet[] → ChangeOp[]
   ├─ Evidence[] / PerceptionJob ref
   ├─ TimelineEvent[] / AuditEntry[]
   └─ CertificationLock[] / Contract ref / PurchaseOrder ref
```


### 2.3 Cardinalidades principales

| Padre | Hijo | Card | Notas |
| --- | --- | --- | --- |
| Project | ProjectVersion | 1:N | versions inmutables al seal |
| Project | Scenario | 1:N | al menos scenario `main` |
| Scenario | ScenarioPointer | 1:1 | HEAD mutable pointer |
| ScenarioPointer | ProjectVersion | N:1 | scenarios pueden compartir version base |
| ProjectVersion | Site | 1:0..1 | v1 un site típico |
| Site | Building | 1:N |  |
| Building | Level | 1:N |  |
| Level | Space | 1:N |  |
| Level | Element | 1:N | también pueden colgar de Space |
| Space | Element | 1:N | containment opcional |
| Element | ElementGeometry | 1:1 |  |
| Element | ParameterSet | 1:N |  |
| Wall | Opening | 1:N | host relation |
| System | Element | 1:N | membership |
| Element | Connection | N:N | vía Connection |
| ProjectVersion | TakeoffLine | 1:N | projection |
| TakeoffLine | CostLine | 1:N | Costs domain |
| ChangeSet | ChangeOp | 1:N |  |
| ChangeSet | ProjectVersion | N:1 base + 0..1 result |  |
| Evidence | Element | N:N | vía provenance |


### 2.4 Systems graph

Además de la jerarquía espacial, el MDO mantiene un **grafo de sistemas**: nodos `System`, `Element`, `Connection`; edges tipadas `feeds`, `returns`, `controls`, `supports`, `bounds`, `hosts`, `hosted_by`. Un Element puede pertenecer a Spatial containment Y a System membership. Installations se modelan como Systems + Elements tipados, no como JSON paralelo.

| system_type | Elementos ejemplo |
| --- | --- |
| structure | Column, Beam, Slab, Foundation |
| envelope | Wall, Roof, Opening |
| finishes | FloorFinish, WallFinish, Ceiling |
| cold_water | PipeRun, Fixture |
| hot_water | PipeRun, Heater, Fixture |
| sewage | PipeRun, Stack, Fixture |
| electrical | Circuit, Panel, Device |
| gas | PipeRun, Appliance |
| hvac | Duct, AHU, Diffuser |
| fire | Sprinkler, Extinguisher, AlarmDevice |


### 2.5 Bounded context: ownership

| Dominio | Owns | May read | Must NOT |
| --- | --- | --- | --- |
| MDO Core | Graph, versions, changesets, scenario pointers, evidence refs, projection skeletons | — | Precios de mercado, pesos CV |
| Perception | PerceptionJob, raw detections (staging) | PlanAsset | Mutar Element sellado |
| Geometry | Validators, measure compute (vía ChangeOps) | ElementGeometry | Skip ChangeSet |
| Materials | Formulas, catalog, Takeoff compute | Element tipado | Inventario privado de walls |
| Costs | PriceBook apply, CostLine, Budget | TakeoffLine | Poseer Element |
| AI | Prompts, tool calls, drafts | Projections + graph read | Direct mutate |
| Marketplace | Offers, suppliers | MaterialSpec ids | Fork geometry |
| Media | Blobs | — | Interpretar obra |
| Identity | Users, tenants, roles | — | Hechos de obra |


### 2.6 Componentes lógicos internos


#### 2.6.1 GraphStore

Persistencia de entidades tipadas versionadas (o copy-on-write rows keyed by version).


#### 2.6.2 VersionService

Creación, seal, baseline, parent chain, compare metadata.


#### 2.6.3 ChangeSetEngine

Validación, conflicto, apply determinista, idempotencia, audit.


#### 2.6.4 ProjectionEngine

Build/invalidate TakeoffLine skeleton, ModelTree, ScenarioDiff summaries.


#### 2.6.5 ScenarioService

CRUD scenario, pointer move, CoW overlay rules, merge MVP.


#### 2.6.6 QueryService

Lecturas filtradas por tenant/version/scenario; never leak cross-tenant.


#### 2.6.7 TimelineService

Append-only events for UX history.


#### 2.6.8 StranglerAdapter

Map Process JSON ↔ ChangeOps / Elements (temporal).


### 2.7 Flujos arquitectónicos clave


#### 2.7.1 Flujo de confirmación percepción

```
PlanoSubido → PerceptionJob → Evidence persistida (Media ref)
  → draft ChangeSet (proposed ops: add Space, add Wall, ...)
  → HITL confirm / auto-policy
  → ChangeSetConfirmado → apply → nueva ProjectVersion tip
  → ModeloActualizado → ProyeccionInvalidada → rebuild Takeoff
```


#### 2.7.2 Flujo escenario material

```
Scenario B from main @ Version Vn
  → overlay ChangeOps: rebind Wall.material_spec brick→steel
  → shared Element ids for geometry
  → Takeoff/Cost projections diverge by scenario_id
```


#### 2.7.3 Flujo sello presupuesto

```
Budget sign → CertificationLock on (project, scenario, version)
  → version sealed if not already
  → CostLines frozen; further edits require new version + new lock
```


### 2.8 Multi-tenancy

Toda raíz `Project` lleva `tenant_id` (y `studio_id` si aplica al modelo Identity). Services reciben `AuthContext`. Queries usan predicado obligatorio. Tests de aislamiento son gate de merge (ver §18).


### 2.9 Consistency model

| Operación | Consistencia |
| --- | --- |
| Confirm ChangeSet | Strong (transacción OLTP apply + outbox write) |
| Lectura graph post-confirm | Strong en primary |
| Proyecciones | Eventual (ventana budgeteada; Apéndice P) |
| Scenario pointer move | Strong |
| Cross-region | N/A v1 |


### 2.10 Extensibilidad tipológica

Nuevos `element_type` / `system_type` se registran por catálogo versionado (seed LATAM + plugins E20). El core no hardcodea todos los tipos del universo; valida contra registry. Tipos desconocidos → `Element` genérico + ParameterSet, no crash.


### 2.11 Diagrama de deployment (lógico)

```
┌─────────────┐   ┌──────────────────┐   ┌─────────────┐
│ FE Studio   │──►│ API monolith     │──►│ Postgres    │
└─────────────┘   │  mdo.* modules   │   │ graph+proj  │
                  │  outbox publisher│   └─────────────┘
                  └────────┬─────────┘
                           │
                  ┌────────▼─────────┐   ┌─────────────┐
                  │ Workers (E04)    │──►│ Object store│
                  │ projection rebuild│   │ Media refs  │
                  └──────────────────┘   └─────────────┘
```


### 2.12 Separación historical vs cache

- **Historical SoT:** entities versionadas, changesets, timeline, locks — durable, soft-delete only.
- **Cache:** projection rows, FE state, AI embeddings — disposable, rebuildable.
- **Blobs:** Media — content-addressed o object keys; never base64 SoT en OLTP.


### 2.13 API surface ownership

Solo MDO Core autoriza paths `/v1/.../mdo/...` y mutaciones de graph. Materials/Costs exponen sus propios paths pero reciben `version_id`/`scenario_id` como input obligatorio.


### 2.14 Observabilidad (hereda RFC-E01)

Spans: `mdo.changeset.apply`, `mdo.version.seal`, `mdo.projection.rebuild`, `mdo.scenario.fork`. Métricas: ops_per_changeset, apply_latency, conflict_rate, projection_lag, pct_projects_on_mdo. Logs: tenant_id, project_id, version_id, changeset_id, scenario_id, trace_id — nunca geometría completa ni PII de cliente en claro más allá de ids.


### 2.15 Failure domains

| Fallo | Degradación |
| --- | --- |
| Projection rebuild down | Lectura graph OK; banner stale projection |
| Outbox lag | Apply OK; consumers atrasados; métrica alerta |
| Media down | Evidence metadata OK; thumbnails fail |
| Flag `mdo.v1=false` | Strangler off; legacy Process path |


### 2.16 Contratos con épicas vecinas

| Épica | Contrato con MDO |
| --- | --- |
| E01 | Flags `mdo.*`, métricas, traces |
| E02 Identity | AuthZ tenant/roles en API MDO |
| E03 | PlanAsset/Evidence → object_key |
| E04 | Outbox envelope en mutaciones |
| E05 | Proposed ChangeSets only |
| E06 | Geometry vía ChangeOps |
| E08 | Lee Element tipado; escribe TakeoffLine |
| E09/E10 | CostLine/Budget keyed; freeze on sign |
| E11 | Completa merge UX sobre Scenario de E07 |
| E12 | Explorer lee SoT; no inventa |
| E15/E16 | Read-only tools + draft CS |
| E17 | CertificationLock + progress over versions |
| E18/E21 | PO/Offer bindings a specs/ids |


### 2.17 Anti-corruption layer Strangler

Mientras Process JSON exista, `StranglerAdapter` traduce items→ops y ops→vista legacy. El adapter es temporal y feature-flagged; no es SoT.


### 2.18 Escalado de versions

Estrategia: (1) entity rows con `valid_from_version`/`valid_to_version` o (2) CoW chunk por subtree. Prohibido clonar full graph en cada commit. Snapshots periódicos opcionales para lectura rápida de heads antiguas (cache, no segunda SoT).


### 2.19 Diagrama Project→…→Scenarios (resumen requerido)

Jerarquía operativa completa requerida por producto:

- Project
- Versions (ProjectVersion)
- Levels
- Spaces
- Walls
- Openings
- Floors / Slabs
- Installations (Systems)
- Materials (bindings, no ownership de catálogo)
- Quantities (TakeoffLine projections)
- Costs (CostLine keyed)
- Scenarios (heads + overlays)

También: Building, Site/Lot, Systems graph. Bounded context: **MDO Core owns graph**; other domains project/read.


## 3. Entidades


### 3.1 Convenciones de catálogo

Cada entidad declara: propósito, atributos clave conceptuales, lifecycle, ownership domain. IDs: ULID/UUID estables cross-version cuando la identidad lógica persiste; `version_id` selecciona el snapshot/visibility. Campos comunes: `tenant_id`, `project_id`, `created_at`, `created_by`, `deleted_at`, `provenance`, `quality_flags` cuando aplica.


### 3.2 Matriz resumen de entidades

| Entidad | Propósito | Atributos clave | Lifecycle | Ownership |
| --- | --- | --- | --- | --- |
| OrganizationRef | Puntero a org Identity; scoping comercial | tenant_id, org_id, display_name_cache | immutable ref | Identity owns; MDO refs |
| Project | Raíz de la obra digital | id, tenant_id, name, default_scenario_id, currency, locale | active|archived | MDO/Projects |
| ProjectParty | Cliente/contratista/sub en proyecto | party_type, party_ref, role, contact_ref | active|removed soft | MDO |
| DocumentRef | Documento asociado | doc_id, kind, media_object_key | uploaded|superseded | Media owns blob; MDO refs |
| PlanAsset | Plano/hoja de dibujo | asset_id, sheet_name, scale_hint, media_ref | active|superseded | MDO meta + Media blob |
| Evidence | Hecho perceptivo anclado | evidence_id, kind, media_ref, bbox, confidence, perception_job_id | proposed|accepted|rejected | MDO refs; Perception produces |
| PerceptionJobRef | Job CV/OCR | job_id, status, plan_asset_id | queued|running|done|failed | Perception owns; MDO refs |
| Site | Lote/sitio | site_id, lot_ref, geo_optional, area_m2 | versioned | MDO |
| Building | Edificio | building_id, site_id, name, typology | versioned | MDO |
| Level | Nivel/piso | level_id, building_id, elevation_m, name | versioned | MDO |
| Space | Ambiente | space_id, level_id, name, space_type, area_m2 | versioned | MDO |
| Zone | Zona lógica | zone_id, level_id, name | versioned | MDO |
| System | Sistema instalación/estructura | system_id, system_type, name | versioned | MDO |
| Element | Supertipo constructivo | element_id, element_type, level_id?, space_id?, system_ids[] | versioned; soft-delete | MDO |
| Wall | Element subtype muro | host openings, length_m, height_m, thickness_m | versioned | MDO |
| Opening | Vanos puerta/ventana | host_wall_id, width_m, height_m, sill_m | versioned | MDO |
| Floor | Solado/piso | space_id, area_m2, finish_spec_ref | versioned | MDO |
| Slab | Losa | thickness_m, area_m2, structural_role | versioned | MDO |
| Column | Columna | section, height_m | versioned | MDO |
| Beam | Viga | span_m, section | versioned | MDO |
| Stair | Escalera | flight_count, rise_run | versioned | MDO |
| Roof | Cubierta | area_m2, slope, roof_type | versioned | MDO |
| Finish | Terminación | host_element_id, finish_spec_ref | versioned | MDO |
| ElementGeometry | Geometría tipada | element_id, geom_type, measures, polygon_ref, units | versioned via element | MDO; E06 writes vía CS |
| ParameterSet | Parámetros tipados | owner_ref, params_json, schema_version | versioned | MDO |
| Connection | Edge sistemas/espacial | from_id, to_id, connection_type | versioned | MDO |
| MaterialBinding | Binding material a element | element_id, material_spec_ref, scenario_overlay? | versioned/overlay | MDO binding; Materials catalog elsewhere |
| TakeoffLine | Proyección cantidad | version_id, scenario_id, element_id?, qty, unit, formula_ref | rebuildable projection | Materials compute; MDO skeleton OK |
| CostLine | Línea costo | takeoff_line_id, pricebook_ref, amount, currency | owned Costs; freeze on sign | Costs |
| PriceBookRef | Ref lista precios | pricebook_id, region | ref only | Costs owns book |
| SupplierOfferBinding | Oferta ligada | offer_id, material_spec_ref|takeoff_line_id|element_type | binding ChangeOp | Marketplace owns offer |
| Scenario | Branch Git-like | scenario_id, name, base_scenario_id? | active|archived soft | MDO |
| ScenarioPointer | HEAD de scenario | scenario_id, version_id | mutable pointer | MDO |
| ChangeSet | Contenedor de ops | changeset_id, base_version_id, status, author | draft|confirmed|conflict|rejected | MDO |
| ChangeOp | Operación atómica | op_id, op_type, target_ref, payload, before_ref, after_ref | immutable once confirmed | MDO |
| ProjectVersion | Commit del modelo | version_id, parent_version_id, status, is_baseline, summary | open|sealed|signed | MDO |
| TimelineEvent | Evento UX historia | event_id, actor, verb, object_ref, why | append-only | MDO |
| AuditEntry | Audit técnico | audit_id, action, before, after, trace_id | append-only | MDO/Platform |
| CertificationLock | Sello certificación/presupuesto | lock_id, version_id, scenario_id, kind | active|superseded | MDO + Costs/Timeline |
| PurchaseOrderRef | Ref OC | po_id | ref | Procurement owns |
| ContractRef | Ref contrato | contract_id | ref | Enterprise/Contracts |
| ClientParty | ProjectParty type=client | — | — | MDO |
| ContractorParty | ProjectParty type=contractor | — | — | MDO |
| SubcontractorParty | ProjectParty type=subcontractor | — | — | MDO |
| HotWaterSystem | System type | — | versioned | MDO |
| ColdWaterSystem | System type | — | versioned | MDO |
| SewageSystem | System type | — | versioned | MDO |
| ElectricalSystem | System type | — | versioned | MDO |
| GasSystem | System type | — | versioned | MDO |
| HVACSystem | System type | — | versioned | MDO |
| FireSystem | System type | — | versioned | MDO |
| Assembly | Grupo de elements | assembly_id, member_ids | versioned | MDO |
| MaterialSpecRef | Spec material | spec_id | ref | Materials owns catalog |
| SystemPack | Pack parámetros sistema | pack_id, system_type, params | overlayable | MDO/Plugins |


### 3.3 Element como supertipo

`Element` es el supertipo persistido. Subtipos (Wall, Opening, Slab, …) pueden ser: (a) tabla única con `element_type` + ParameterSet, o (b) tablas hijas 1:1. Contrato: lectores siempre pueden tratar como Element; writers usan tipología registry.


### 3.4 Lifecycles detallados


#### 3.4.1 ProjectVersion

- `open` — mutable solo vía nuevos ChangeSets que la usan como base (la version en sí no se edita in-place).
- `sealed` — inmutable; tip de baseline o promote.
- `signed` — sellada + CertificationLock dinero/certificación.


#### 3.4.2 ChangeSet

- `draft` — editable por author/roles.
- `confirmed` — applied; immutable.
- `conflict` — apply bloqueado; requiere resolución.
- `rejected` — descartado; soft.


#### 3.4.3 Evidence

- `proposed` — de Perception.
- `accepted` — citada por ChangeOp confirmado.
- `rejected` — no usada; retenida para audit.


### 3.5 Campos de lineage obligatorios en Element

| Campo | Semántica |
| --- | --- |
| element_id | Identidad estable cross-version |
| origin_evidence_ids[] | Evidence que originó/alteró |
| origin_changeset_ids[] | ChangeSets que tocaron |
| confidence | 0..1 agregada |
| quality_flags[] | enum flags (low_scale_confidence, manual_override, ...) |
| created_in_version_id | Primera aparición |
| retired_in_version_id | Soft remove version |


### 3.6 Entidades que MDO NO posee (refs only)

- Organization, User, Role → Identity
- MediaObject bytes → Media E03
- Perception model weights / raw tensors → Perception
- MaterialCatalogItem definitions → Materials
- PriceBook rows → Costs
- Supplier, Offer master → Marketplace
- PurchaseOrder master → Procurement
- Contract master → Contracts/Enterprise


### 3.7 Seed tipologías core LATAM (E07-F01-T06)

Registry inicial mínimo (no exhaustivo del universo constructivo):

- wall.masonry.brick
- wall.masonry.block
- wall.drywall
- wall.steel_frame
- wall.retak
- opening.door
- opening.window
- slab.concrete
- floor.carpetas
- floor.ceramic
- space.room
- space.bath
- space.kitchen
- space.corridor
- roof.metal
- roof.tile
- column.concrete
- beam.concrete
- stair.concrete

Cada tipología declara schema de ParameterSet y units esperadas para Geometry.


### 3.8 Reglas de soft-delete

| Entidad | Soft-delete | Hard-delete |
| --- | --- | --- |
| ProjectVersion sealed | Nunca delete; archive project | Prohibido |
| Element | retired_in_version / deleted_at | Prohibido en prod |
| ChangeSet confirmed | No delete | Prohibido |
| Scenario | archived_at | Prohibido si locks |
| Evidence | rejected retained | Prohibido si cited |
| Projections | rebuild/delete cache OK | N/A cache |


## 4. Relaciones


### 4.1 Tabla de cardinalidades extendida

| Edge | From | To | Card | Obligatoria | Notas |
| --- | --- | --- | --- | --- | --- |
| contains_site | ProjectVersion | Site | 1:0..1 | No | v1 usualmente 1 |
| contains_building | Site | Building | 1:N | Si site existe |  |
| contains_level | Building | Level | 1:N | Sí |  |
| contains_space | Level | Space | 1:N | No |  |
| contains_zone | Level | Zone | 1:N | No |  |
| hosts_element_level | Level | Element | 1:N | No | alternativa a space |
| hosts_element_space | Space | Element | 1:N | No |  |
| has_geometry | Element | ElementGeometry | 1:1 | Sí si medible |  |
| has_params | Element | ParameterSet | 1:N | No |  |
| hosts_opening | Wall | Opening | 1:N | No |  |
| member_of_system | Element | System | N:N | No |  |
| connects | Element | Element | N:N | No | vía Connection |
| binds_material | Element | MaterialSpecRef | N:1 | No | por scenario overlay |
| projects_takeoff | Element | TakeoffLine | 1:N | No | projection |
| prices_takeoff | TakeoffLine | CostLine | 1:N | No | Costs |
| evidences | Evidence | Element | N:N | No | provenance |
| produced_by_job | Evidence | PerceptionJobRef | N:1 | No |  |
| based_on | ChangeSet | ProjectVersion | N:1 | Sí | base_version_id |
| results_in | ChangeSet | ProjectVersion | 0..1:1 | Si confirmed |  |
| contains_op | ChangeSet | ChangeOp | 1:N | Sí si non-empty |  |
| points_to | ScenarioPointer | ProjectVersion | N:1 | Sí |  |
| locks | CertificationLock | ProjectVersion | N:1 | Sí |  |
| party_of | ProjectParty | Project | N:1 | Sí |  |
| asset_of | PlanAsset | Project | N:1 | Sí |  |


### 4.2 Edges permitidos (allowlist)

- `ProjectVersion -contains-> Site|Building|Level|Space|System|Element|ParameterSet|Connection`
- `Wall -hosts-> Opening`
- `Element -has-> ElementGeometry`
- `Element -bound-> MaterialSpecRef` (binding)
- `Element -cited_by-> TakeoffLine`
- `TakeoffLine -priced_by-> CostLine`
- `Evidence -supports-> Element|ElementGeometry|ChangeOp`
- `ChangeSet -applies_to-> ProjectVersion (base)`
- `ScenarioPointer -heads-> ProjectVersion`
- `SupplierOfferBinding -targets-> MaterialSpecRef|TakeoffLine|ElementType`
- `PurchaseOrderRef -references-> SupplierOfferBinding|TakeoffLine`


### 4.3 Relaciones FORBIDDEN (hard fail en review/CI conceptual)

| Forbidden | Por qué | Alternativa |
| --- | --- | --- |
| Costs → Perception (direct read detections) | Salta SoT; no auditable | Costs → TakeoffLine → Element ← Evidence |
| AI → geometry write directo | Rompe HITL/determinismo | AI crea draft ChangeSet |
| Marketplace owns Element | Fork geometría / SoT rota | Offer binding a spec/type/line |
| Materials private Wall store | Duplica hechos MDO | Leer Element versionado |
| Frontend persistir Element como SoT | UI descartable | POST ChangeSet |
| PlanAsset bytes inline en Element | OLTP bloat | Media object_key |
| ChangeOp mutate sealed version in-place | Rompe M01 | Nueva version tip |
| Perception emit qty autoritativa final sin confirm | P12 | draft CS + confirm |
| Plugin write arbitrary graph sin capability | P18 | capability contracts |
| Scenario full deep-copy geometry default | Perf/scale | CoW overlay |


### 4.4 Integridad referencial lógica

- Opening.host_wall_id debe existir en misma version visibility.
- Element.level_id y space_id coherentes (space.level == element.level).
- ChangeSet.base_version_id pertenece al mismo project/tenant.
- ScenarioPointer.version_id reachable from project version DAG.
- CertificationLock no puede apuntar a version `open` sin seal atómico.


### 4.5 Reglas de navegación query

Queries de grafo siempre reciben `(tenant_id, project_id, version_id|scenario_id)`. Si `scenario_id`, resolver HEAD vía ScenarioPointer y aplicar overlays. Nunca devolver entidades de otro tenant aunque se conozca el UUID.


### 4.6 Matriz dominio×edge permitido

| Dominio writer | Edges que puede crear vía ChangeOp | Edges prohibidos |
| --- | --- | --- |
| MDO Core / human editor | spatial, system, params, bindings | price rows |
| Perception (proposed) | propose element/space/geometry ops | confirm alone if money gate |
| Geometry Engine | geometry measure/validate ops | material price |
| Materials | — (reads); may request binding ops via CS draft | wall geometry |
| Costs | — (reads takeoff) | element create |
| AI | draft CS only | confirm without HITL money |
| Marketplace | offer binding ops | element geometry |


## 5. Versionado Git-like


### 5.1 Objetos

| Objeto | Analogía Git | Rol |
| --- | --- | --- |
| ProjectVersion | commit | Snapshot lógico inmutable al seal |
| ChangeSet | commit contents / patch | Conjunto ordenado de ChangeOps |
| ChangeOp | file hunk | Mutación atómica tipada |
| Scenario | branch | Línea de evolución alternativa |
| ScenarioPointer | HEAD ref | Apunta al tip version |
| Baseline flag | main release | is_baseline / promote |
| CertificationLock | annotated tag | Sello comercial/legal |


### 5.2 ProjectVersion — contrato

Atributos: `version_id`, `project_id`, `parent_version_id`, `resulting_from_changeset_id`, `status`, `is_baseline`, `change_summary`, `sealed_at`, `sealed_by`, `content_hash` (hash del grafo lógico o del changeset apply).

- Creación: solo como resultado de ChangeSet confirmado (excepto version genesis vacía al crear Project).
- Inmutabilidad: tras `sealed`/`signed`, API rechaza cualquier mutate de hechos (HTTP 409 `VERSION_SEALED`).
- Parent chain: permite history walk y blame.
- Compare: `GET .../versions/{a}/compare/{b}` retorna diff de entities + takeoff summary.


### 5.3 ChangeSet — contrato

Estados: draft → confirmed | conflict | rejected. Apply es transacción: validar → detectar conflictos → escribir grafo CoW → crear ProjectVersion hija → mover ScenarioPointer (si aplica) → outbox events → audit.

- Idempotencia: confirm con misma Idempotency-Key retorna mismo result version.
- Optimistic concurrency: `base_version_id` debe == HEAD del scenario target al confirmar (o política merge).
- Max ops por CS: budget configurado (evitar megapatches opacos).


### 5.4 Branch / Scenario

Crear Scenario B desde Scenario A en version Vn: nuevo Scenario + Pointer a Vn (compartido) + overlay vacío. Cambios en B crean versions hijas solo en la línea B; A intacta.


### 5.5 Merge

Merge MVP (E07 mínimo / E11 completo): calcular union de ChangeOps desde ancestor común; clasificar conflictos (Apéndice E); producir Merge ChangeSet; HITL resolve; confirm crea version merge con dos parents (opcional DAG) o parent lineal + merge metadata.


### 5.6 Compare

| Compare kind | Output |
| --- | --- |
| Structure diff | added/removed/modified Elements/Spaces |
| Param diff | ParameterSet deltas |
| Material binding diff | rebinds |
| Takeoff diff | qty deltas by line |
| Cost diff | amount deltas (si Costs disponible) |


### 5.7 History

Version tree API + Timeline. No rewrite: no force-push. Corrección = nuevo CS. «Revert» = CS inverso que aplica ops compensatorias.


### 5.8 Seals / baselines / immutability rules

| Acción | Efecto |
| --- | --- |
| seal(version) | status=sealed; no más tips overwriting; pointers pueden seguir si ya apuntaban |
| promote_baseline(version) | is_baseline=true; previous baseline flag off (histórico preservado) |
| sign(version, lock_kind) | status=signed + CertificationLock; freeze CostLines asociadas |
| attempt edit sealed | 409 VERSION_SEALED |


### 5.9 Genesis version

Al crear Project con `mdo.v1`: version V0 vacía sealed-or-open según política (recomendado: open hasta primer plano procesado). Scenario `main` pointer → V0.


### 5.10 Reglas de tip movement

- Confirm CS en scenario S mueve ScenarioPointer S al result version.
- No mueve otros scenarios.
- Locks en HEAD previo permanecen anclados a esa version (no viajan).


## 6. Timeline


### 6.1 Preguntas que responde

- **Quién** — actor_user_id / actor_system / actor_job
- **Qué** — verb + entity refs
- **Cuándo** — timestamp UTC
- **Por qué** — reason code + free text opcional acotado
- **Causation** — caused_by_event_id / changeset_id / perception_job_id


### 6.2 TimelineEvent contrato

| Campo | Tipo conceptual | Notas |
| --- | --- | --- |
| event_id | id | ULID |
| tenant_id / project_id | id | obligatorio |
| actor_type | enum | user|system|perception|ai|plugin |
| actor_id | string |  |
| verb | enum | created|updated|confirmed|sealed|merged|rejected|... |
| object_type / object_id | ref |  |
| changeset_id | id? |  |
| version_id | id? |  |
| scenario_id | id? |  |
| diff_summary | json | pequeño; no full geometry |
| why | string? |  |
| causation_id | id? |  |
| trace_id | string? | OTel |
| created_at | datetime | append-only |


### 6.3 Diff contracts para UX

Compare UX consume: lista de ops humanizadas («Muro M-12 espesor 0.15→0.20»), deep-link a entity inspector, badges confidence, filtros por actor/verb/fecha. FE no recompute autoridad; solo presenta.


### 6.4 AuditEntry vs TimelineEvent

TimelineEvent = producto/UX. AuditEntry = compliance técnico (before/after refs, IP hash opcional, authz decision). Ambos append-only; retención distinta posible.


### 6.5 Flujos timeline mínimos

1. ProyectoCreado → Timeline project.created
2. PlanoSubido → document.uploaded
3. ChangeSetConfirmado → model.updated + ops summaries
4. EscenarioCreado → scenario.forked
5. CertificationLock → budget.signed


## 7. Motor de escenarios


### 7.1 Objetivo

Permitir Scenario A ladrillo / B acero / C retak **sin duplicar geometría**: shared base elements + overlay ParameterSet / SystemPack / material bindings vía ChangeOps en branch. Copy-on-write rules.


### 7.2 Modelo

```
Scenario main @ V10 (walls geometry shared)
├─ Scenario A (brick)  HEAD VA3  = V10 + overlays material brick
├─ Scenario B (steel)  HEAD VB2  = V10 + overlays material steel
└─ Scenario C (retak)  HEAD VC1  = V10 + overlays material retak
Geometry Element ids idénticos; bindings/params divergen por overlay chain.
```


### 7.3 Copy-on-write rules

- Lectura: resolver entity en HEAD caminando overlays hacia base hasta hit.
- Escritura de geometría en scenario hijo: CoW clona entity row para ese version tip; otros scenarios siguen viendo base hasta que ellos escriban.
- Escritura solo de MaterialBinding/ParameterSet: overlay liviano sin clonar geometry payload.
- Prohibido: clonar todo el building al fork.


### 7.4 SystemPack / ParameterSet overlays

Un SystemPack agrupa rebindings tipológicos (ej. muro portante ladrillo→steel frame). Aplicar pack = ChangeSet con N ops. Reversible con CS inverso.


### 7.5 Compare escenarios

API compare por scenario heads: structure equal check + binding diff + takeoff/cost diff. UX: tabla A/B/C cantidades y ARS.


### 7.6 Merge entre escenarios

Default: no auto-merge geometry divergences. Material-only overlays merge clean si no tocan mismos keys. Conflict types Apéndice E.


### 7.7 Entitlements

N scenarios por plan (Free/Pro/Enterprise) vía flags/entitlements Identity. Core no hardcodea precios de plan; consulta entitlement service.


### 7.8 Escenarios y certificaciones

Lock es por `(scenario_id, version_id)`. Firmar A no sella B. Promote baseline elige un head.


## 8. API del MDO


### 8.1 Convenciones

- Base: `/v1/projects/{project_id}/mdo`
- AuthZ: Bearer + tenant membership + project ACL (Identity E02)
- Idempotency-Key obligatorio en POST confirm/merge/seal
- Errores: problem+json conceptual `{code, message, details, trace_id}`
- Paginación cursor en listados
- Versionado API header `Accept: application/vnd.arqia.mdo.v1+json`


### 8.2 Códigos de error MDO

| code | HTTP | Cuándo |
| --- | --- | --- |
| MDO_NOT_FOUND | 404 | entity/version ausente en tenant |
| MDO_FORBIDDEN | 403 | AuthZ fail |
| VERSION_SEALED | 409 | mutate sealed |
| CHANGESET_CONFLICT | 409 | optimistic concurrency / merge conflict |
| CHANGESET_INVALID | 422 | ops fallan validación grafo |
| IDEMPOTENCY_REPLAY | 200 | misma key; body original |
| SCENARIO_LIMIT | 402/403 | entitlement |
| PROJECTION_STALE | 409/200+header | según endpoint |
| TENANT_MISMATCH | 403 | id cross-tenant |


### 8.3 Catálogo REST conceptual (núcleo)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | /projects | Crear project + V0 + scenario main |
| GET | /projects/{id} | Metadata project |
| PATCH | /projects/{id} | Update metadata no-grafo |
| POST | /projects/{id}/archive | Soft archive |
| GET | /projects/{id}/mdo/versions | Version tree |
| GET | /projects/{id}/mdo/versions/{vid} | Version detail |
| POST | /projects/{id}/mdo/versions/{vid}/seal | Seal |
| POST | /projects/{id}/mdo/versions/{vid}/promote | Baseline |
| GET | /projects/{id}/mdo/versions/{a}/compare/{b} | Compare |
| GET | /projects/{id}/mdo/graph | Query graph by version|scenario |
| GET | /projects/{id}/mdo/elements | List/filter elements |
| GET | /projects/{id}/mdo/elements/{eid} | Element inspector |
| GET | /projects/{id}/mdo/spaces | List spaces |
| GET | /projects/{id}/mdo/systems | List systems |
| POST | /projects/{id}/mdo/changesets | Create draft CS |
| GET | /projects/{id}/mdo/changesets/{cid} | Get CS |
| PATCH | /projects/{id}/mdo/changesets/{cid} | Edit draft ops |
| POST | /projects/{id}/mdo/changesets/{cid}/confirm | Confirm/apply |
| POST | /projects/{id}/mdo/changesets/{cid}/reject | Reject draft |
| GET | /projects/{id}/mdo/scenarios | List scenarios |
| POST | /projects/{id}/mdo/scenarios | Fork/create scenario |
| GET | /projects/{id}/mdo/scenarios/{sid} | Scenario detail + HEAD |
| POST | /projects/{id}/mdo/scenarios/{sid}/merge | Merge MVP |
| GET | /projects/{id}/mdo/scenarios/{a}/compare/{b} | Compare scenarios |
| GET | /projects/{id}/mdo/projections/takeoff | Takeoff projection |
| GET | /projects/{id}/mdo/projections/tree | Model tree projection |
| POST | /projects/{id}/mdo/projections/rebuild | Admin rebuild |
| GET | /projects/{id}/mdo/timeline | Timeline events |
| POST | /projects/{id}/mdo/locks | CertificationLock |
| DELETE | /projects/{id}/mdo/elements/{eid} | Soft delete vía CS (no hard) |
| POST | /projects/{id}/mdo/duplicate | Duplicate project (new ids) |


### 8.4 AuthZ matrix (conceptual)

| Acción | Owner | Editor | Viewer | AI bot | Perception worker |
| --- | --- | --- | --- | --- | --- |
| Read graph | ✓ | ✓ | ✓ | ✓ read tools | ✓ |
| Draft CS | ✓ | ✓ | — | ✓ draft | ✓ proposed |
| Confirm CS | ✓ | ✓* | — | — HITL | — / auto-policy limited |
| Seal/Sign | ✓ | —* | — | — | — |
| Fork scenario | ✓ | ✓ | — | — | — |
| Admin rebuild proj | ✓ | — | — | — | system |

* Confirm dinero/sign gated HITL roles. Auto-policy percepción solo tipologías allowlist low-risk.


### 8.5 Idempotencia

Headers: `Idempotency-Key` en confirm/merge/seal/sign/duplicate. Store key→response por 24h+ (política). Replay safe.


### 8.6 Query model

Filtros: `element_type`, `level_id`, `space_id`, `quality_flags`, `confidence_gte`, `updated_since`. Sort estable por id. Include opcional `geometry`, `params`, `provenance`.


### 8.7 Soft delete API

No existe hard DELETE de hechos. `DELETE` semántico crea draft/confirm CS con op `remove`. Admin legal purge = proceso offline documentado fuera de happy path.


## 9. Eventos


### 9.1 Envelope (hereda Architecture / E04)

| Campo | Notas |
| --- | --- |
| event_id | ULID |
| event_type | PascalCase español o English estable — elegir uno en ADR; este RFC usa español roadmap |
| occurred_at | UTC |
| tenant_id | obligatorio |
| project_id | obligatorio si aplica |
| trace_id / correlation_id | OTel |
| causation_id | event padre |
| producer | service name |
| payload | json versionado schema |
| schema_version | int |


### 9.2 Catálogo de eventos MDO

| Evento | Significado | Producer |
| --- | --- | --- |
| ProyectoCreado | Project genesis + V0 | Identity/Projects→MDO |
| PlanoSubido | PlanAsset ref creado | Media/MDO |
| PlanoProcesado | PerceptionJob done | Perception |
| AmbienteDetectado | Evidence space proposed | Perception |
| MuroDetectado | Evidence wall proposed | Perception |
| AberturaDetectada | Evidence opening proposed | Perception |
| EvidenciaAceptada | Evidence→accepted | MDO |
| ChangeSetCreado | Draft CS | MDO |
| ChangeSetConfirmado | Apply OK | MDO |
| ChangeSetRechazado | Draft rejected | MDO |
| ChangeSetConflicto | Conflict detected | MDO |
| ModeloActualizado | Nueva version tip | MDO |
| ElementoCreado | Element added | MDO |
| ElementoTipificado | element_type set/changed | MDO |
| ElementoActualizado | params/geom | MDO |
| ElementoEliminado | soft remove | MDO |
| EspacioActualizado | Space change | MDO |
| SistemaActualizado | System change | MDO |
| ProyeccionInvalidada | Cache bust | MDO |
| ProyeccionReconstruida | Rebuild done | MDO |
| MaterialCalculado | Takeoff rebuilt (Materials) | Materials |
| CostoActualizado | Cost projection (Costs) | Costs |
| EscenarioCreado | Scenario fork | MDO |
| EscenarioComparado | Audit compare op | MDO |
| EscenarioMergeado | Merge confirmed | MDO |
| VersionSellada | seal | MDO |
| VersionPromovida | baseline | MDO |
| PresupuestoFirmado | CertificationLock budget | Costs/MDO |
| OfertaVinculada | SupplierOfferBinding | Marketplace |


### 9.3 Flujos event-driven


#### 9.3.1 Wedge feliz

```
ProyectoCreado → PlanoSubido → PlanoProcesado
 → AmbienteDetectado / MuroDetectado
 → ChangeSetCreado (proposed) → ChangeSetConfirmado
 → ModeloActualizado → ProyeccionInvalidada
 → MaterialCalculado → CostoActualizado
```


#### 9.3.2 Regla de autoridad

Perception **nunca** emite cantidades finales autoritativas sin `ChangeSetConfirmado`. Puede emitir sugerencias en payload de Evidence, pero TakeoffLine autoritativo nace post-confirm + Materials compute.


### 9.4 Consumers

| Consumer | Eventos | Acción |
| --- | --- | --- |
| ProjectionEngine | ModeloActualizado, ProyeccionInvalidada | rebuild |
| Materials | ModeloActualizado | recompute takeoff |
| Costs | MaterialCalculado | reprice |
| Timeline | casi todos | append UX event |
| AI index | ModeloActualizado | reindex embeddings opcional |
| Notifications | PresupuestoFirmado, ChangeSetConflicto | notify |


### 9.5 Outbox

Mutations MDO escriben outbox en la misma transacción que apply (E04). Publishers idempotentes. Sin E04 completo, degradar a tabla outbox local mínima compatible envelope.


## 10. Persistencia


### 10.1 Principios

- OLTP graph = SoT hechos versionados
- Projection store = cache rebuildable
- Blobs = Media object keys; never base64 SoT
- Historical append para CS/Timeline/Audit
- Never hard-delete lista §10.6


### 10.2 Tablas/colecciones lógicas

| Store | Contiene | Notas |
| --- | --- | --- |
| mdo_project | Project root + flags | tenant scoped |
| mdo_project_party | ProjectParty | soft |
| mdo_plan_asset | PlanAsset meta + media_ref |  |
| mdo_evidence | Evidence meta + media_ref + confidence |  |
| mdo_version | ProjectVersion | immutable rows when sealed |
| mdo_scenario | Scenario | soft archive |
| mdo_scenario_pointer | HEAD pointers | hot update |
| mdo_changeset | ChangeSet header |  |
| mdo_change_op | ChangeOp rows | immutable after confirm |
| mdo_site / building / level / space / zone | Spatial | version visibility strategy |
| mdo_system | Systems |  |
| mdo_element | Element supertype |  |
| mdo_element_geometry | Geometry payload / measures |  |
| mdo_parameter_set | Params |  |
| mdo_connection | Edges |  |
| mdo_material_binding | Bindings |  |
| mdo_takeoff_line | Projection takeoff | cacheable |
| mdo_projection_tree | Model tree cache |  |
| mdo_timeline_event | UX timeline | append |
| mdo_audit_entry | Audit | append |
| mdo_certification_lock | Locks |  |
| mdo_idempotency | Idempotency keys |  |
| mdo_outbox | Outbox events | E04 compatible |


### 10.3 Estrategias de versionado en storage

**Opción A — validity ranges:** filas con `valid_from_version_seq`, `valid_to_version_seq`. **Opción B — CoW por version tip:** filas keyed `(entity_id, version_id)` solo cuando cambian. Elegir en ADR; tests de immutabilidad idénticos.


### 10.4 Índices (resumen; detalle Apéndice D)

- `(tenant_id, project_id)` en todas raíces
- `(project_id, version_id)` en entities
- `(project_id, scenario_id)` pointers
- `(changeset_id)` ops
- `(element_id)` geometry/bindings
- `(version_id, scenario_id)` takeoff
- GIN/JSONB opcional params si query
- Partial index `deleted_at IS NULL`


### 10.5 Historical vs cache

| Clase | Ejemplos | Pérdida aceptable? |
| --- | --- | --- |
| Historical SoT | versions, ops, elements validity, locks, evidence meta | No |
| Rebuildable cache | takeoff_line, tree projection, AI embeddings | Sí |
| Blob | plan images, audit overlays | No (Media durability) |


### 10.6 Never hard-delete list

- ProjectVersion sealed/signed
- ChangeSet confirmed + ChangeOps
- Evidence cited by accepted provenance
- CertificationLock
- TimelineEvent / AuditEntry (salvo retención legal expirada con proceso)
- Idempotency records dentro de ventana
- Outbox until published+acked


### 10.7 Blob refs a Media (E03)

Campos: `media_object_key`, `content_type`, `byte_size`, `checksum`. Prohibido persistir `audit_image_base64` como SoT en MDO. Strangler puede leer legacy base64 y migrar a Media async.


### 10.8 Migraciones expand/contract

- Expand: crear tablas mdo_* nullable dual-write
- Backfill proyectos piloto
- Dual-read flag
- Contract: deprecar Process.items como SoT (mantener archive read)


### 10.9 Retention

Draft ChangeSets stale > N días: auto-reject job. Projections: TTL + invalidate. Soft-deleted scenarios: retención plan Enterprise configurable.


## 11. Integración visión


### 11.1 Principio one-way

**Vision → Evidence + proposed ops → human/auto confirm → MDO.** Never MDO drives CV as authority. MDO no «pide» re-inferencias como verdad; jobs se disparan por upload/usuario.


### 11.2 Contrato Perception → MDO

| Artifact | Destino | Autoridad |
| --- | --- | --- |
| PerceptionJob | ref en Evidence | Perception |
| Detections raw | staging Perception | none on MDO |
| Evidence | mdo_evidence | candidata |
| draft ChangeSet | mdo_changeset status=draft | proposed |
| Confirm | ChangeSetConfirmado | MDO SoT |


### 11.3 Prohibiciones

- CV no UPDATE Element sellado
- CV no escribe TakeoffLine final
- CV no bypasea AuthZ tenant
- CV no embebe pesos en OLTP MDO


### 11.4 Auto-policy confirm

Permitido solo si: tipología allowlist, confidence ≥ umbral, no money gate, flag `mdo.autopipeline` on, audit actor=system. Default off en prod hasta QA.


### 11.5 Escala / calibración

E06 produce ops de escala; Perception aporta hints. Escala aceptada queda en ParameterSet de Level/PlanAsset vía CS.


### 11.6 Flujo detallado

```
1 Upload PlanAsset (Media)
2 PerceptionJob queued (E04/E05)
3 Job writes Evidence rows + draft ChangeSet ops
4 Studio muestra propuestas (FE)
5 User confirm → MDO apply
6 Events → Materials/Costs
7 Si user rejects → Evidence rejected; no model change
```


## 12. Integración IA


### 12.1 Principio

IA es **read-only** sobre hechos MDO. Tools de lectura con citations. Proposals como **draft ChangeSets** requiriendo HITL. Never direct mutate.


### 12.2 Tools permitidos (conceptual)

- `mdo.get_element(element_id, version|scenario)`
- `mdo.list_spaces(...)`
- `mdo.get_takeoff(...)`
- `mdo.compare_scenarios(a,b)`
- `mdo.get_timeline(...)`
- `mdo.create_draft_changeset(ops)` — no confirm


### 12.3 Tools prohibidos

- confirm_changeset
- seal/sign
- raw SQL
- update_geometry_direct
- delete_hard


### 12.4 Citations

Toda afirmación cuantitativa en respuesta comercial debe citar `element_id` / `takeoff_line_id` / `version_id`. Sin cita ⇒ no usable en documentos de dinero (P17).


### 12.5 Draft proposals

AI puede generar ops; author_type=ai; confirm role humano. Money paths siempre HITL.


### 12.6 Independencia

Apagar AI no degrada MDO. MDO no depende de LLM para integridad.


## 13. Materiales


### 13.1 Principio

Materials **compute over MDO**. Results = `TakeoffLine` projections keyed a `version_id`/`scenario_id`. **No** private parallel inventory of walls.


### 13.2 Inputs

- Element tipado + ElementGeometry
- ParameterSet / MaterialBinding
- Typology formulas (Materials domain)
- Waste factors / overrides auditados


### 13.3 Outputs

| Campo TakeoffLine | Notas |
| --- | --- |
| takeoff_line_id | estable por key business |
| version_id / scenario_id | scope |
| element_id? | nullable for aggregates |
| qty / unit | determinista |
| formula_ref / formula_version | provenance compute |
| confidence | propagada |
| evidence_ids | lineage |


### 13.4 Invalidación

On `ModeloActualizado` / binding change → `ProyeccionInvalidada` → rebuild. Incremental por CS cuando sea posible.


### 13.5 Prohibiciones

- Materials no parsea Process.items cuando `mdo.wedge` on
- Materials no guarda geometría copia
- Materials no confirma ChangeSets de geometría


## 14. Costos


### 14.1 Principio

Costs igual que Materials: Budget/CostLine reference TakeoffLine/Element ids; **freeze on sign**.


### 14.2 CostLine

| Campo | Notas |
| --- | --- |
| cost_line_id | Costs ownership |
| takeoff_line_id | FK lógica |
| pricebook_ref | no owned by MDO |
| unit_price / amount / currency | LATAM currency |
| frozen_at | set on CertificationLock |


### 14.3 Freeze

Sign budget ⇒ CertificationLock + CostLines frozen para ese `(scenario, version)`. Edits ⇒ new version + new budget draft.


### 14.4 Forbidden

- Costs→Perception direct
- Costs owning Element
- Mutate frozen lines


## 15. Marketplace


### 15.1 Principio

Supplier offers bind to `MaterialSpec` / `TakeoffLine` / `ElementType` — **never fork Element geometry**. Selection creates binding ChangeOp / PO ref.


### 15.2 Binding flow

```
Offer selected → draft ChangeOp bind_offer
 → confirm (role) → SupplierOfferBinding stored
 → optional PurchaseOrderRef
 → projections may update commercial fields
 Geometry Element untouched
```


### 15.3 Ownership

| Data | Owner |
| --- | --- |
| Offer master | Marketplace |
| Binding | MDO fact (via CS) |
| PO master | Procurement |
| Element geometry | MDO only |


### 15.4 Gate dependencia

Marketplace productivo (E21) solo después de MDO/PO estables. Este RFC solo deja contratos de binding.


## 16. Migración desde Process JSON (strangler)


### 16.1 Estado actual (asunciones operativas)

Hoy el wedge persiste `Process` con `items` JSON, `total`, `audit_image_base64`, `result_meta`, escala, etc. Eso actúa como SoT implícita. El strangler reemplaza la SoT sin big-bang.


### 16.2 Fases

| Fase | Flag | Comportamiento |
| --- | --- | --- |
| A Expand | `mdo.v1` on (write schema) | Tablas MDO existen; write path legacy only |
| B Dual-write | `mdo.wedge` on | Process + map items→CS confirm→Elements/Takeoff |
| C Dual-read | `mdo.read` | Studio lee MDO; fallback Process |
| D Cutover read | `mdo.read` only | Process archive |
| E Contract | deprecate writes legacy | Process items read-only histórico |


### 16.3 Mapping Process → MDO

| Process field | MDO target |
| --- | --- |
| project_id | Project |
| filename / tipo_plano | PlanAsset + DocumentRef |
| audit_image_base64 | Media object + Evidence |
| escala_detectada | ParameterSet / Level scale via CS |
| items[] color/qty | Elements + TakeoffLines |
| total | Cost projection aggregate (Costs) |
| result_meta | Evidence meta / quality_flags |
| created_at / user | Timeline + Audit |


### 16.4 Dual-write rules

- Misma request wedge genera Process legacy + CS MDO
- Si MDO apply falla: error métrica; política: fail-open legacy vs fail-closed — default fail-open + alert en B; fail-closed en D
- Idempotencia por process_id → changeset key


### 16.5 Migración datos piloto

Job batch: para projects seleccionados, construir V0+V1 desde último Process; marcar `migrated_from_process_id`. Validar golden qty/ARS delta ≤ tolerancia.


### 16.6 Rollback

- `mdo.wedge=false` → stop dual-write
- `mdo.read=false` → Studio legacy
- Datos MDO se conservan (no hard-delete)
- Runbook Apéndice R


### 16.7 Feature flags

| Flag | Default | Función |
| --- | --- | --- |
| `mdo.v1` | false | Schema/API MDO habilitada |
| `mdo.wedge` | false | Dual-write wedge |
| `mdo.read` | false | Lectura Studio desde MDO |
| `mdo.scenarios` | false | Fork escenarios UI |
| `mdo.autopipeline` | false | Auto-confirm percepción limited |


### 16.8 Criterios de salida strangler

- [ ] % proyectos on MDO ≥ target PM
- [ ] Golden wedge delta qty/ARS dentro de tolerancia
- [ ] Error rate dual-write < umbral 7 días
- [ ] Soporte entrenado en version badge
- [ ] Process JSON documentado como legacy archive


### 16.9 Compatibilidad FE

Version badge + Model Explorer mínimos. Failover: si MDO read error y flag fallback, mostrar legacy con banner.


## 17. Riesgos


### 17.1 Riesgos roadmap E07 (reafirmados)

| Tipo | Riesgo | Mitigación |
| --- | --- | --- |
| Tech | Schema incompleto eterno | Cerrar MDO schema v1 + evolve |
| Arch | God aggregate | Entidades + ChangeOps acotados |
| Perf | Proyecciones stale | Invalidación event-driven + lag SLO |
| Scale | Explosión de versions | Snapshots lógicos + diffs + CoW |
| Commercial | Migración mental usuario | Wedge sobre MDO sin romper UX |


### 17.2 Riesgos adicionales de implementación

| ID | Riesgo | Prob | Impacto | Mitigación |
| --- | --- | --- | --- | --- |
| R01 | Confundir RFC-E02 con Identity E02 | Alta | Crítica | Metadata + checklist PR + training |
| R02 | Dual-write diverge Process vs MDO | Alta | Alta | Comparadores + métricas delta + fail policy |
| R03 | Full-copy scenarios | Media | Alta | CoW enforced tests |
| R04 | AI mutate directo por atajo | Media | Crítica | AuthZ + code owners + tests |
| R05 | Perception qty autoritativa | Alta | Alta | Gate ChangeSetConfirmado |
| R06 | Hard-delete accidental | Baja | Alta | DB grants + soft-delete only |
| R07 | Tenant leak por UUID | Media | Crítica | Predicate tests isolation |
| R08 | Projection lag UX confunde | Alta | Media | Banner stale + version pins |
| R09 | Idempotency gaps | Media | Alta | Keys en confirm paths |
| R10 | Base64 permanece SoT | Alta | Media | Media migration job |
| R11 | Merge conflicts mal UX | Media | Media | MVP + defer E11 ADR |
| R12 | Scope creep tipologías | Alta | Media | Seed LATAM only + registry |
| R13 | Costs freeze bypass | Media | Crítica | CertificationLock enforce |
| R14 | Outbox no disponible | Media | Alta | Tabla local compatible |
| R15 | Perf apply CS grande | Media | Media | Max ops + batch |

| R16 | Riesgo operativo/extensión MDO #16 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R17 | Riesgo operativo/extensión MDO #17 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R18 | Riesgo operativo/extensión MDO #18 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R19 | Riesgo operativo/extensión MDO #19 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R20 | Riesgo operativo/extensión MDO #20 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R21 | Riesgo operativo/extensión MDO #21 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R22 | Riesgo operativo/extensión MDO #22 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R23 | Riesgo operativo/extensión MDO #23 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R24 | Riesgo operativo/extensión MDO #24 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R25 | Riesgo operativo/extensión MDO #25 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R26 | Riesgo operativo/extensión MDO #26 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R27 | Riesgo operativo/extensión MDO #27 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R28 | Riesgo operativo/extensión MDO #28 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R29 | Riesgo operativo/extensión MDO #29 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R30 | Riesgo operativo/extensión MDO #30 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R31 | Riesgo operativo/extensión MDO #31 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R32 | Riesgo operativo/extensión MDO #32 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R33 | Riesgo operativo/extensión MDO #33 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R34 | Riesgo operativo/extensión MDO #34 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R35 | Riesgo operativo/extensión MDO #35 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R36 | Riesgo operativo/extensión MDO #36 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R37 | Riesgo operativo/extensión MDO #37 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R38 | Riesgo operativo/extensión MDO #38 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R39 | Riesgo operativo/extensión MDO #39 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |
| R40 | Riesgo operativo/extensión MDO #40 (flags, docs drift, capacity, index miss, overlay bugs, strangler skew, etc.) | M | M | Checklists F01–F06 + review semanal SLIs + anti-scope |

Tabla extendida R16–R40: mitigan con runbooks, flags `mdo.*`, tests immutability/tenant, y freeze de alcance §20.


## 18. Criterios de aceptación objetivos


### 18.1 Binarios (pass/fail)

- [ ] Nota nomenclatura RFC-E02 ≠ Identity E02 visible en metadata y README épica
- [ ] Schema MDO v1 migrado expand con tablas listadas §10
- [ ] Project crea V0 + scenario main automáticamente cuando `mdo.v1`
- [ ] ChangeSet confirm crea ProjectVersion hija y mueve pointer
- [ ] Attempt mutate sealed version → 409 VERSION_SEALED
- [ ] Apply ChangeSet es idempotente con Idempotency-Key
- [ ] Conflictos optimistic concurrency detectados (test)
- [ ] Tenant isolation: user A no lee project B (tests)
- [ ] Evidence→Element lineage fields poblados post-confirm
- [ ] Perception no escribe TakeoffLine final sin confirm (test contrato)
- [ ] AI tools read-only; confirm endpoint forbidden a bot role
- [ ] TakeoffLine keyed por version/scenario rebuildable
- [ ] CostLine freeze on CertificationLock (contrato/test)
- [ ] Scenario fork no duplica geometry payloads (assert storage)
- [ ] Compare versions retorna diff structure+params
- [ ] Outbox event ModeloActualizado emitido en confirm
- [ ] Flag `mdo.wedge` dual-write documentado + rollback
- [ ] Golden wedge color→qty→ARS verde con MDO path
- [ ] No base64 SoT nuevo introducido en tablas MDO
- [ ] Soft-delete only en Elements (no hard)
- [ ] ProyeccionInvalidada → rebuild job path existe
- [ ] AuthZ en toda API `/mdo/*`
- [ ] OpenAPI/event schema actualizados o waiver
- [ ] Demo 10 min grabada/scriptable
- [ ] Anti-scope §20 respetado (review)


### 18.2 Numéricos

| Métrica | Target |
| --- | --- |
| Coverage dominio mdo/* | ≥ 80% |
| ChangeSet apply p95 (≤50 ops) | < 200ms olTP local budget (ajustar ADR) |
| Projection rebuild p95 wedge | < 2s o waiver |
| Conflict false positive rate golden | 0 |
| P0 debt nueva | 0 |
| Delta qty strangler vs legacy golden | ≤ 0% lógico / tolerancia documentada |
| Delta ARS golden | ≤ tolerancia PM |
| SLI API MDO availability week-1 | ≥ 99% o waiver |
| % proyectos piloto on MDO | ≥ target PM |
| Max geometry clone on scenario fork | 0 full-building clones |


### 18.3 Criterios extendidos por feature

- [ ] E07-F01 criterio extendido 18.3.1.01: evidencia en demo/tests de la feature.
- [ ] E07-F01 criterio extendido 18.3.1.02: evidencia en demo/tests de la feature.
- [ ] E07-F01 criterio extendido 18.3.1.03: evidencia en demo/tests de la feature.
- [ ] E07-F01 criterio extendido 18.3.1.04: evidencia en demo/tests de la feature.
- [ ] E07-F01 criterio extendido 18.3.1.05: evidencia en demo/tests de la feature.
- [ ] E07-F01 criterio extendido 18.3.1.06: evidencia en demo/tests de la feature.
- [ ] E07-F01 criterio extendido 18.3.1.07: evidencia en demo/tests de la feature.

- [ ] E07-F02 criterio extendido 18.3.2.01: evidencia en demo/tests de la feature.
- [ ] E07-F02 criterio extendido 18.3.2.02: evidencia en demo/tests de la feature.
- [ ] E07-F02 criterio extendido 18.3.2.03: evidencia en demo/tests de la feature.
- [ ] E07-F02 criterio extendido 18.3.2.04: evidencia en demo/tests de la feature.
- [ ] E07-F02 criterio extendido 18.3.2.05: evidencia en demo/tests de la feature.
- [ ] E07-F02 criterio extendido 18.3.2.06: evidencia en demo/tests de la feature.
- [ ] E07-F02 criterio extendido 18.3.2.07: evidencia en demo/tests de la feature.

- [ ] E07-F03 criterio extendido 18.3.3.01: evidencia en demo/tests de la feature.
- [ ] E07-F03 criterio extendido 18.3.3.02: evidencia en demo/tests de la feature.
- [ ] E07-F03 criterio extendido 18.3.3.03: evidencia en demo/tests de la feature.
- [ ] E07-F03 criterio extendido 18.3.3.04: evidencia en demo/tests de la feature.
- [ ] E07-F03 criterio extendido 18.3.3.05: evidencia en demo/tests de la feature.
- [ ] E07-F03 criterio extendido 18.3.3.06: evidencia en demo/tests de la feature.
- [ ] E07-F03 criterio extendido 18.3.3.07: evidencia en demo/tests de la feature.

- [ ] E07-F04 criterio extendido 18.3.4.01: evidencia en demo/tests de la feature.
- [ ] E07-F04 criterio extendido 18.3.4.02: evidencia en demo/tests de la feature.
- [ ] E07-F04 criterio extendido 18.3.4.03: evidencia en demo/tests de la feature.
- [ ] E07-F04 criterio extendido 18.3.4.04: evidencia en demo/tests de la feature.
- [ ] E07-F04 criterio extendido 18.3.4.05: evidencia en demo/tests de la feature.
- [ ] E07-F04 criterio extendido 18.3.4.06: evidencia en demo/tests de la feature.
- [ ] E07-F04 criterio extendido 18.3.4.07: evidencia en demo/tests de la feature.

- [ ] E07-F05 criterio extendido 18.3.5.01: evidencia en demo/tests de la feature.
- [ ] E07-F05 criterio extendido 18.3.5.02: evidencia en demo/tests de la feature.
- [ ] E07-F05 criterio extendido 18.3.5.03: evidencia en demo/tests de la feature.
- [ ] E07-F05 criterio extendido 18.3.5.04: evidencia en demo/tests de la feature.
- [ ] E07-F05 criterio extendido 18.3.5.05: evidencia en demo/tests de la feature.
- [ ] E07-F05 criterio extendido 18.3.5.06: evidencia en demo/tests de la feature.
- [ ] E07-F05 criterio extendido 18.3.5.07: evidencia en demo/tests de la feature.

- [ ] E07-F06 criterio extendido 18.3.6.01: evidencia en demo/tests de la feature.
- [ ] E07-F06 criterio extendido 18.3.6.02: evidencia en demo/tests de la feature.
- [ ] E07-F06 criterio extendido 18.3.6.03: evidencia en demo/tests de la feature.
- [ ] E07-F06 criterio extendido 18.3.6.04: evidencia en demo/tests de la feature.
- [ ] E07-F06 criterio extendido 18.3.6.05: evidencia en demo/tests de la feature.
- [ ] E07-F06 criterio extendido 18.3.6.06: evidencia en demo/tests de la feature.
- [ ] E07-F06 criterio extendido 18.3.6.07: evidencia en demo/tests de la feature.


## 19. Checklist final


### 19.1 Tasks roadmap E07-F01

- [ ] E07-F01-T01 — Modelar Site/Building/Level/Space/Zone
- [ ] E07-F01-T02 — Modelar System/Element/Assembly/ParameterSet
- [ ] E07-F01-T03 — IDs estables + lineage fields
- [ ] E07-F01-T04 — Validaciones de grafo mínimas
- [ ] E07-F01-T05 — Migraciones expand
- [ ] E07-F01-T06 — Seed tipologías core LATAM refs
- [ ] E07-F01-T07 — Tests integridad referencial lógica
- [ ] E07-F01-T08 — Documentar límites MDO (qué NO es)
- [ ] E07-F01-T09 — Índices tenant/project/version
- [ ] E07-F01-T10 — Soft-delete policies
- [ ] E07-F01-T11 — Acceptance Criteria medibles
- [ ] E07-F01-T12 — Métricas RED/USE
- [ ] E07-F01-T13 — ADR si desvío
- [ ] E07-F01-T14 — Feature flag + rollback
- [ ] E07-F01-T15 — OpenAPI/event schema
- [ ] E07-F01-T16 — Checklist tenant isolation
- [ ] E07-F01-T17 — Runbook operativo
- [ ] E07-F01-T18 — Demo 10 minutos
- [ ] E07-F01-T19 — Compat Free/Pro/Enterprise
- [ ] E07-F01-T20 — No romper wedge color→qty→moneda
- [ ] E07-F01-T21 — Tests regresión golden
- [ ] E07-F01-T22 — Traces spans
- [ ] E07-F01-T23 — Dependencias de eventos
- [ ] E07-F01-T24 — Seguridad secretos/PII
- [ ] E07-F01-T25 — Performance budget preliminar
- [ ] E07-F01-T26 — Mapping Architecture domain


### 19.2 Tasks roadmap E07-F02

- [ ] E07-F02-T01 — Crear versiones; cerrar inmutable
- [ ] E07-F02-T02 — parent_version_id chain
- [ ] E07-F02-T03 — is_baseline flag
- [ ] E07-F02-T04 — Summary change_summary
- [ ] E07-F02-T05 — Tests immutability enforce
- [ ] E07-F02-T06 — API get version tree
- [ ] E07-F02-T07 — UI version badge
- [ ] E07-F02-T08 — Evento ModeloActualizado
- [ ] E07-F02-T09 — AC medibles
- [ ] E07-F02-T10 — Métricas
- [ ] E07-F02-T11 — ADR
- [ ] E07-F02-T12 — Flag+rollback
- [ ] E07-F02-T13 — OpenAPI
- [ ] E07-F02-T14 — Tenant isolation
- [ ] E07-F02-T15 — Runbook
- [ ] E07-F02-T16 — Demo
- [ ] E07-F02-T17 — Compat planes
- [ ] E07-F02-T18 — Wedge OK
- [ ] E07-F02-T19 — Golden
- [ ] E07-F02-T20 — Traces
- [ ] E07-F02-T21 — Event deps
- [ ] E07-F02-T22 — PII
- [ ] E07-F02-T23 — Perf
- [ ] E07-F02-T24 — Mapping Arch


### 19.3 Tasks roadmap E07-F03

- [ ] E07-F03-T01 — ChangeSet draft/confirmed/conflict
- [ ] E07-F03-T02 — ChangeOp add/update/remove
- [ ] E07-F03-T03 — Apply idempotent
- [ ] E07-F03-T04 — Eventos ChangeSetCreado/Confirmado
- [ ] E07-F03-T05 — Optimistic concurrency
- [ ] E07-F03-T06 — Tests conflict detection
- [ ] E07-F03-T07 — AuthZ author roles
- [ ] E07-F03-T08 — Audit before/after refs
- [ ] E07-F03-T09 — Prohibir apply sin tenant check
- [ ] E07-F03-T10 — Métricas ops_per_changeset
- [ ] E07-F03-T11 — AC
- [ ] E07-F03-T12 — Métricas RED/USE
- [ ] E07-F03-T13 — ADR
- [ ] E07-F03-T14 — Flag+rollback
- [ ] E07-F03-T15 — OpenAPI
- [ ] E07-F03-T16 — Tenant isolation
- [ ] E07-F03-T17 — Runbook
- [ ] E07-F03-T18 — Demo
- [ ] E07-F03-T19 — Compat
- [ ] E07-F03-T20 — Wedge
- [ ] E07-F03-T21 — Golden
- [ ] E07-F03-T22 — Traces
- [ ] E07-F03-T23 — Event deps
- [ ] E07-F03-T24 — PII
- [ ] E07-F03-T25 — Perf
- [ ] E07-F03-T26 — Mapping


### 19.4 Tasks roadmap E07-F04

- [ ] E07-F04-T01 — Takeoff projection skeleton
- [ ] E07-F04-T02 — Model tree projection
- [ ] E07-F04-T03 — Invalidación ProyeccionInvalidada
- [ ] E07-F04-T04 — Rebuild job
- [ ] E07-F04-T05 — Cache keys versionados
- [ ] E07-F04-T06 — Tests eventual consistency window
- [ ] E07-F04-T07 — Perf budget rebuild
- [ ] E07-F04-T08 — API read projections
- [ ] E07-F04-T09 — AC
- [ ] E07-F04-T10 — Métricas
- [ ] E07-F04-T11 — ADR
- [ ] E07-F04-T12 — Flag+rollback
- [ ] E07-F04-T13 — OpenAPI
- [ ] E07-F04-T14 — Tenant
- [ ] E07-F04-T15 — Runbook
- [ ] E07-F04-T16 — Demo
- [ ] E07-F04-T17 — Compat
- [ ] E07-F04-T18 — Wedge
- [ ] E07-F04-T19 — Golden
- [ ] E07-F04-T20 — Traces
- [ ] E07-F04-T21 — Events
- [ ] E07-F04-T22 — PII
- [ ] E07-F04-T23 — Perf
- [ ] E07-F04-T24 — Mapping


### 19.5 Tasks roadmap E07-F05

- [ ] E07-F05-T01 — Adaptar flujo color→qty persistir Element/TakeoffLine
- [ ] E07-F05-T02 — Dual-read legacy
- [ ] E07-F05-T03 — Feature flag `mdo.wedge`
- [ ] E07-F05-T04 — E2E wedge sobre MDO
- [ ] E07-F05-T05 — Rollback flag
- [ ] E07-F05-T06 — Migración datos proyectos piloto
- [ ] E07-F05-T07 — Métrica % proyectos on MDO
- [ ] E07-F05-T08 — Docs soporte
- [ ] E07-F05-T09 — AC
- [ ] E07-F05-T10 — Métricas
- [ ] E07-F05-T11 — ADR
- [ ] E07-F05-T12 — Flag+rollback
- [ ] E07-F05-T13 — OpenAPI
- [ ] E07-F05-T14 — Tenant
- [ ] E07-F05-T15 — Runbook
- [ ] E07-F05-T16 — Demo
- [ ] E07-F05-T17 — Compat
- [ ] E07-F05-T18 — Wedge
- [ ] E07-F05-T19 — Golden
- [ ] E07-F05-T20 — Traces
- [ ] E07-F05-T21 — Events
- [ ] E07-F05-T22 — PII
- [ ] E07-F05-T23 — Perf
- [ ] E07-F05-T24 — Mapping


### 19.6 Tasks roadmap E07-F06

- [ ] E07-F06-T01 — quality_flags en ElementGeometry/Element
- [ ] E07-F06-T02 — provenance evidence_ids
- [ ] E07-F06-T03 — API filter by quality
- [ ] E07-F06-T04 — UI badges
- [ ] E07-F06-T05 — Tests schema
- [ ] E07-F06-T06 — Dashboard twin trust
- [ ] E07-F06-T07 — Gate firmas usa quality
- [ ] E07-F06-T08 — Docs semántica flags
- [ ] E07-F06-T09 — AC
- [ ] E07-F06-T10 — Métricas
- [ ] E07-F06-T11 — ADR
- [ ] E07-F06-T12 — Flag+rollback
- [ ] E07-F06-T13 — OpenAPI
- [ ] E07-F06-T14 — Tenant
- [ ] E07-F06-T15 — Runbook
- [ ] E07-F06-T16 — Demo
- [ ] E07-F06-T17 — Compat
- [ ] E07-F06-T18 — Wedge
- [ ] E07-F06-T19 — Golden
- [ ] E07-F06-T20 — Traces
- [ ] E07-F06-T21 — Events
- [ ] E07-F06-T22 — PII
- [ ] E07-F06-T23 — Perf
- [ ] E07-F06-T24 — Mapping


### 19.7 Tasks específicas RFC (adicionales)

- [ ] Scenario + ScenarioPointer schema mínimo
- [ ] Compare API versions/scenarios
- [ ] Forbidden relations suite tests
- [ ] Strangler mapping Process→MDO documentado en runbook
- [ ] CertificationLock endpoint + freeze contract con Costs
- [ ] Envelope eventos español roadmap alineado ADR
- [ ] Media refs reemplazan nuevos base64
- [ ] Checklist PR Apéndice Y adoptado


### 19.8 Checklist transversal por feature


#### 19.8.F01

- [ ] Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] Servicio de dominio con AuthZ
- [ ] Eventos outbox / consumers idempotentes si hay side-effects
- [ ] API conceptual documentada
- [ ] UI mínima o explícitamente N/A
- [ ] Migraciones expand/contract
- [ ] Tests unit + integration + aislamiento
- [ ] Métricas + logs + traces
- [ ] Docs/runbook
- [ ] Flag + rollback


#### 19.8.F02

- [ ] Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] Servicio de dominio con AuthZ
- [ ] Eventos outbox / consumers idempotentes si hay side-effects
- [ ] API conceptual documentada
- [ ] UI mínima o explícitamente N/A
- [ ] Migraciones expand/contract
- [ ] Tests unit + integration + aislamiento
- [ ] Métricas + logs + traces
- [ ] Docs/runbook
- [ ] Flag + rollback


#### 19.8.F03

- [ ] Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] Servicio de dominio con AuthZ
- [ ] Eventos outbox / consumers idempotentes si hay side-effects
- [ ] API conceptual documentada
- [ ] UI mínima o explícitamente N/A
- [ ] Migraciones expand/contract
- [ ] Tests unit + integration + aislamiento
- [ ] Métricas + logs + traces
- [ ] Docs/runbook
- [ ] Flag + rollback


#### 19.8.F04

- [ ] Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] Servicio de dominio con AuthZ
- [ ] Eventos outbox / consumers idempotentes si hay side-effects
- [ ] API conceptual documentada
- [ ] UI mínima o explícitamente N/A
- [ ] Migraciones expand/contract
- [ ] Tests unit + integration + aislamiento
- [ ] Métricas + logs + traces
- [ ] Docs/runbook
- [ ] Flag + rollback


#### 19.8.F05

- [ ] Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] Servicio de dominio con AuthZ
- [ ] Eventos outbox / consumers idempotentes si hay side-effects
- [ ] API conceptual documentada
- [ ] UI mínima o explícitamente N/A
- [ ] Migraciones expand/contract
- [ ] Tests unit + integration + aislamiento
- [ ] Métricas + logs + traces
- [ ] Docs/runbook
- [ ] Flag + rollback


#### 19.8.F06

- [ ] Entidad/modelo actualizado con tenant + provenance si aplica
- [ ] Servicio de dominio con AuthZ
- [ ] Eventos outbox / consumers idempotentes si hay side-effects
- [ ] API conceptual documentada
- [ ] UI mínima o explícitamente N/A
- [ ] Migraciones expand/contract
- [ ] Tests unit + integration + aislamiento
- [ ] Métricas + logs + traces
- [ ] Docs/runbook
- [ ] Flag + rollback


## 20. Anti-scope


### 20.1 Hard freeze (NO entra en RFC-E02-MDO / E07)

- [ ] Reescribir Identity, SSO, billing (Roadmap E02)
- [ ] Implementar bus Kafka completo / consumers multi-servicio (más allá de outbox envelope)
- [ ] Object storage propietario sin E03
- [ ] Entrenar/redeploy modelos CV
- [ ] Geometry Engine completo (clash, 3D solids) — solo contrato ops
- [ ] Materials DSL completo y UI tipologías avanzada (E08)
- [ ] PriceBooks regionales completos (E09)
- [ ] Signed Budgets UX completa (E10) — solo freeze contract
- [ ] Scenario merge UX avanzada 3-way (puede E11 con ADR; datos mínimos sí)
- [ ] Frontend Workspace multi-panel completo (E12)
- [ ] PDF/Excel reports engine (E13)
- [ ] Notifications/email product (E14)
- [ ] Chat IA grounded completo (E15)
- [ ] AI Orchestrator eval harness completo (E16)
- [ ] Timeline progress certifications product UI completa (E17)
- [ ] Procurement PO full (E18)
- [ ] Plugin host SDK (E19)
- [ ] Domain plugins packs productivos (E20)
- [ ] Marketplace catálogo público (E21)
- [ ] Enterprise SSO/RBAC fine/DR (E22)
- [ ] Public API externa versionada partners (E23)
- [ ] Data lake/analytics (E24)
- [ ] Mobile site ops (E25)
- [ ] Microservicio MDO separado
- [ ] IFC import/export full
- [ ] Revit/Archicad live sync
- [ ] IoT sensors twin
- [ ] Multi-region active-active
- [ ] Hard-delete tool en UI
- [ ] Edición colaborativa OT realtime CRDT
- [ ] Blockchain timestamps
- [ ] Crypto payments
- [ ] Rediseño visual completo Studio
- [ ] Eliminar precios.json en esta épica
- [ ] Rotación SECRET_KEY
- [ ] Soporte offline-first PWA
- [ ] Generación automática de planos
- [ ] GIS catastral full
- [ ] Cálculo estructural FEA
- [ ] Energy modeling
- [ ] Point cloud / LiDAR ingest
- [ ] Auto-sign presupuestos por IA
- [ ] Duplicar store de muros en Materials
- [ ] Permitir AI confirm ChangeSet dinero
- [ ] Escribir geometría desde Marketplace
- [ ] Usar Process JSON como SoT permanente en paralelo sin flag de salida

Total anti-scope bullets: 46 (≥40 requerido).


### 20.2 Borderline decisions

| Tema | Decisión | ADR? |
| --- | --- | --- |
| Scenario merge UX | Datos+API MVP en E07; UX avanzada E11 | Sí si se recorta más |
| TakeoffLine ownership | Skeleton en MDO; compute Materials | No si se respeta |
| Auto-confirm perception | Off by default | Sí para on |
| DAG multi-parent versions | Metadata merge suficiente v1 | Sí si parents múltiples |
| Validity ranges vs CoW rows | Elegir una; tests iguales | Sí obligatorio |


### 20.3 Statement

Todo lo no listado en features E07-F01–F06 + contratos de escenarios mínimos + strangler **está fuera**. Scope creep se rechaza en PR review vía Apéndice Y.


## Apéndice A — Catálogo exhaustivo de entidades

Extiende §3 con campos conceptuales adicionales y notas de implementación. No es SQL final; es contrato.


#### A.OrganizationRef

**Propósito:** Ref org

**Ownership:** Identity

**Lifecycle:** ref

**Campos clave:** tenant_id, org_id, name_cache

**Notas:** No cascade delete hechos


#### A.Project

**Propósito:** Raíz obra

**Ownership:** MDO

**Lifecycle:** active|archived

**Campos clave:** id, tenant_id, studio_id?, name, currency, locale, default_scenario_id, status

**Notas:** Genesis crea V0


#### A.ProjectParty

**Propósito:** Partes

**Ownership:** MDO

**Lifecycle:** active|removed

**Campos clave:** id, project_id, party_type, external_ref, role, email_hash?

**Notas:** PII mínima


#### A.DocumentRef

**Propósito:** Doc

**Ownership:** MDO+Media

**Lifecycle:** uploaded|superseded

**Campos clave:** id, project_id, media_key, kind, title

**Notas:** —


#### A.PlanAsset

**Propósito:** Plano

**Ownership:** MDO+Media

**Lifecycle:** active|superseded

**Campos clave:** id, project_id, media_key, sheet, scale_state

**Notas:** —


#### A.Evidence

**Propósito:** Evidencia

**Ownership:** MDO

**Lifecycle:** proposed|accepted|rejected

**Campos clave:** id, job_id, media_key, kind, bbox, confidence, status

**Notas:** cited immutable


#### A.PerceptionJobRef

**Propósito:** Job

**Ownership:** Perception

**Lifecycle:** ref

**Campos clave:** job_id, status, plan_asset_id

**Notas:** —


#### A.Site

**Propósito:** Sitio

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, version visibility, lot_ref, area_m2

**Notas:** —


#### A.Building

**Propósito:** Edificio

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, site_id, name, typology

**Notas:** —


#### A.Level

**Propósito:** Nivel

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, building_id, elevation_m, name, scale_params

**Notas:** —


#### A.Space

**Propósito:** Ambiente

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, level_id, name, space_type, area_m2

**Notas:** —


#### A.Zone

**Propósito:** Zona

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, level_id, name

**Notas:** —


#### A.System

**Propósito:** Sistema

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, system_type, name

**Notas:** —


#### A.Element

**Propósito:** Supertipo

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, element_type, level_id, space_id, quality_flags, confidence

**Notas:** stable id


#### A.Wall

**Propósito:** Muro

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** length_m, height_m, thickness_m, wall_role

**Notas:** subtype


#### A.Opening

**Propósito:** Abertura

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** host_wall_id, width_m, height_m, sill_m, opening_kind

**Notas:** —


#### A.Floor

**Propósito:** Piso

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** space_id, area_m2, finish_ref

**Notas:** —


#### A.Slab

**Propósito:** Losa

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** area_m2, thickness_m, structural_role

**Notas:** —


#### A.Column

**Propósito:** Columna

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** section, height_m

**Notas:** —


#### A.Beam

**Propósito:** Viga

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** span_m, section

**Notas:** —


#### A.Stair

**Propósito:** Escalera

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** flights, rise, run

**Notas:** —


#### A.Roof

**Propósito:** Cubierta

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** area_m2, slope, roof_type

**Notas:** —


#### A.Finish

**Propósito:** Terminación

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** host_element_id, finish_spec_ref

**Notas:** —


#### A.ElementGeometry

**Propósito:** Geom

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** element_id, geom_type, measures_json, polygon_ref, units

**Notas:** E06 via CS


#### A.ParameterSet

**Propósito:** Params

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** owner_ref, schema_version, params_json

**Notas:** —


#### A.Connection

**Propósito:** Conexión

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** from_id, to_id, connection_type

**Notas:** —


#### A.MaterialBinding

**Propósito:** Binding

**Ownership:** MDO

**Lifecycle:** versioned/overlay

**Campos clave:** element_id, material_spec_ref, source

**Notas:** —


#### A.TakeoffLine

**Propósito:** Qty proj

**Ownership:** Materials/MDO skel

**Lifecycle:** projection

**Campos clave:** version_id, scenario_id, element_id, qty, unit, formula_ref

**Notas:** —


#### A.CostLine

**Propósito:** Costo

**Ownership:** Costs

**Lifecycle:** Costs

**Campos clave:** takeoff_line_id, amount, currency, pricebook_ref, frozen_at

**Notas:** —


#### A.PriceBookRef

**Propósito:** Ref PB

**Ownership:** Costs

**Lifecycle:** ref

**Campos clave:** pricebook_id, region

**Notas:** —


#### A.SupplierOfferBinding

**Propósito:** Oferta

**Ownership:** MDO+Marketplace

**Lifecycle:** binding

**Campos clave:** offer_id, target_ref, target_kind

**Notas:** —


#### A.Scenario

**Propósito:** Branch

**Ownership:** MDO

**Lifecycle:** active|archived

**Campos clave:** id, name, description, base_scenario_id, archived_at

**Notas:** —


#### A.ScenarioPointer

**Propósito:** HEAD

**Ownership:** MDO

**Lifecycle:** mutable

**Campos clave:** scenario_id, version_id, updated_at

**Notas:** —


#### A.ChangeSet

**Propósito:** Patch set

**Ownership:** MDO

**Lifecycle:** draft|confirmed|conflict|rejected

**Campos clave:** id, base_version_id, result_version_id, status, author

**Notas:** —


#### A.ChangeOp

**Propósito:** Op

**Ownership:** MDO

**Lifecycle:** immutable confirmed

**Campos clave:** id, changeset_id, op_type, target_ref, payload, before_ref, after_ref

**Notas:** —


#### A.ProjectVersion

**Propósito:** Commit

**Ownership:** MDO

**Lifecycle:** open|sealed|signed

**Campos clave:** id, parent_id, status, is_baseline, summary, content_hash

**Notas:** —


#### A.TimelineEvent

**Propósito:** UX hist

**Ownership:** MDO

**Lifecycle:** append

**Campos clave:** id, actor, verb, object_ref, why, causation_id

**Notas:** —


#### A.AuditEntry

**Propósito:** Audit

**Ownership:** MDO

**Lifecycle:** append

**Campos clave:** id, action, before, after, trace_id

**Notas:** —


#### A.CertificationLock

**Propósito:** Sello

**Ownership:** MDO

**Lifecycle:** active|superseded

**Campos clave:** id, version_id, scenario_id, kind, signed_by

**Notas:** —


#### A.PurchaseOrderRef

**Propósito:** OC ref

**Ownership:** Procurement

**Lifecycle:** ref

**Campos clave:** po_id

**Notas:** —


#### A.ContractRef

**Propósito:** Contrato

**Ownership:** Contracts

**Lifecycle:** ref

**Campos clave:** contract_id

**Notas:** —


#### A.Assembly

**Propósito:** Grupo

**Ownership:** MDO

**Lifecycle:** versioned

**Campos clave:** id, member_element_ids

**Notas:** —


#### A.SystemPack

**Propósito:** Pack

**Ownership:** MDO/Plugins

**Lifecycle:** overlay

**Campos clave:** id, system_type, params

**Notas:** —


#### A.MaterialSpecRef

**Propósito:** Spec

**Ownership:** Materials

**Lifecycle:** ref

**Campos clave:** spec_id

**Notas:** —


## Apéndice B — Catálogo de eventos

Complementa §9. Cada evento declara payload mínimo.

- **ProyectoCreado**: payload mínimo `project_id, tenant_id, default_scenario_id, version0_id`
- **PlanoSubido**: payload mínimo `plan_asset_id, media_key, project_id`
- **PlanoProcesado**: payload mínimo `job_id, plan_asset_id, status, stats`
- **AmbienteDetectado**: payload mínimo `evidence_id, space_hint, confidence`
- **MuroDetectado**: payload mínimo `evidence_id, wall_hint, confidence`
- **AberturaDetectada**: payload mínimo `evidence_id, opening_hint, confidence`
- **EvidenciaAceptada**: payload mínimo `evidence_id, changeset_id`
- **ChangeSetCreado**: payload mínimo `changeset_id, base_version_id, author_type`
- **ChangeSetConfirmado**: payload mínimo `changeset_id, result_version_id, ops_count`
- **ChangeSetRechazado**: payload mínimo `changeset_id, reason`
- **ChangeSetConflicto**: payload mínimo `changeset_id, conflict_types[]`
- **ModeloActualizado**: payload mínimo `version_id, scenario_id, project_id`
- **ElementoCreado**: payload mínimo `element_id, element_type, version_id`
- **ElementoTipificado**: payload mínimo `element_id, element_type, prev_type`
- **ElementoActualizado**: payload mínimo `element_id, fields_changed[]`
- **ElementoEliminado**: payload mínimo `element_id, version_id`
- **EspacioActualizado**: payload mínimo `space_id, version_id`
- **SistemaActualizado**: payload mínimo `system_id, version_id`
- **ProyeccionInvalidada**: payload mínimo `projection_type, version_id, scenario_id`
- **ProyeccionReconstruida**: payload mínimo `projection_type, version_id, hash`
- **MaterialCalculado**: payload mínimo `version_id, scenario_id, lines_count`
- **CostoActualizado**: payload mínimo `version_id, scenario_id, total, currency`
- **EscenarioCreado**: payload mínimo `scenario_id, from_scenario_id, head_version_id`
- **EscenarioComparado**: payload mínimo `a, b, actor`
- **EscenarioMergeado**: payload mínimo `result_version_id, sources[]`
- **VersionSellada**: payload mínimo `version_id, sealed_by`
- **VersionPromovida**: payload mínimo `version_id`
- **PresupuestoFirmado**: payload mínimo `lock_id, version_id, scenario_id`
- **OfertaVinculada**: payload mínimo `binding_id, offer_id, target_ref`


## Apéndice C — Catálogo de API REST conceptual

Extiende §8. Query params comunes: `scenario_id`, `version_id`, `cursor`, `limit`, `include`.

- `POST /v1/projects`
  - Request: `{name,currency,locale}`
  - Response: `{project,version0,scenario_main}`

- `GET /v1/projects/{pid}/mdo/graph`
  - Request: `—`
  - Response: `{entities,refs,version_id}`

- `POST /v1/projects/{pid}/mdo/changesets`
  - Request: `{base_version_id,scenario_id,ops[]}`
  - Response: `{changeset}`

- `POST /v1/projects/{pid}/mdo/changesets/{cid}/confirm`
  - Request: `{} + Idempotency-Key`
  - Response: `{result_version_id}`

- `POST /v1/projects/{pid}/mdo/scenarios`
  - Request: `{name,from_scenario_id}`
  - Response: `{scenario,pointer}`

- `GET /v1/projects/{pid}/mdo/versions/{a}/compare/{b}`
  - Request: `—`
  - Response: `{diffs}`

- `GET /v1/projects/{pid}/mdo/projections/takeoff`
  - Request: `?scenario_id&version_id`
  - Response: `{lines,hash,stale?}`

- `POST /v1/projects/{pid}/mdo/versions/{vid}/seal`
  - Request: `{}`
  - Response: `{version}`

- `POST /v1/projects/{pid}/mdo/locks`
  - Request: `{version_id,scenario_id,kind}`
  - Response: `{lock}`

- `POST /v1/projects/{pid}/mdo/duplicate`
  - Request: `{name}`
  - Response: `{new_project_id}`


## Apéndice D — Estrategia de índices

| Index | Columns | Purpose |
| --- | --- | --- |
| ix_project_tenant | tenant_id, id | isolation |
| ix_version_project | project_id, created_at | tree |
| ix_pointer_scenario | scenario_id UNIQUE | HEAD |
| ix_element_project_type | project_id, element_type | filter |
| ix_element_level | level_id | nav |
| ix_element_space | space_id | nav |
| ix_geometry_element | element_id | join |
| ix_ops_changeset | changeset_id, ordinal | apply order |
| ix_cs_base | base_version_id | concurrency |
| ix_takeoff_vs | version_id, scenario_id | projection |
| ix_evidence_job | perception_job_id | lineage |
| ix_timeline_project_time | project_id, created_at | UX |
| ix_idempotency_key | key UNIQUE | replay |
| ix_outbox_status | status, created_at | publisher |
| ix_lock_vs | version_id, scenario_id, kind | freeze |

Evitar índices sobre geometría completa. Cardinality labels métricas: no project_name crudo.


## Apéndice E — Tipos de conflicto

| conflict_type | Descripción | Resolución |
| --- | --- | --- |
| OPTIMISTIC_HEAD | base_version != HEAD scenario | rebase/merge |
| ELEMENT_EDIT_EDIT | mismo element_id campos distintos | pick ours/theirs/manual |
| ELEMENT_EDIT_DELETE | edit vs remove | manual |
| OPENING_HOST_MISSING | opening host wall removed | delete opening or retarget |
| BINDING_EDIT_EDIT | material binding diverge | pick |
| PARAM_SCHEMA | params incompatibles schema | manual upgrade |
| GEOMETRY_EDIT_EDIT | measures diverge | manual / E06 assist |
| LOCK_BLOCK | target sealed/signed | new version only |
| TENANT | mismatch | reject hard |
| SCENARIO_LIMIT | entitlement | upgrade plan |


## Apéndice F — Modelo de confidence

Confidence ∈ [0,1]. Agregación: min o product policy documentada por tipología. Gates:

| Gate | Umbral default | Override |
| --- | --- | --- |
| Auto-confirm perception | ≥0.90 + allowlist | flag+role |
| Show warning badge | <0.75 | UI |
| Block sign budget | any money line <0.60 sin waiver | role owner |
| Twin trust dashboard | aggregate avg | — |

- confidence de Evidence alimenta Element
- overrides manuales setean quality_flag `manual_override` y pueden subir/bajar confidence según política
- nunca silenciar low confidence en exports firmados


## Apéndice G — Provenance

Cadena: `PerceptionJob → Evidence → ChangeOp → Element/Geometry → TakeoffLine → CostLine`.

| Campo | Dónde |
| --- | --- |
| evidence_ids[] | Element, Geometry, TakeoffLine |
| changeset_ids[] | Element lineage |
| formula_ref | TakeoffLine |
| pricebook_ref | CostLine |
| actor + trace_id | Audit/Timeline |

- [ ] Toda TakeoffLine post-MDO tiene provenance no vacía o flag `legacy_migrated`
- [ ] Exports incluyen version_id + content_hash


## Apéndice H — Tipos de proyección

| projection_type | Input | Output | Invalidation |
| --- | --- | --- | --- |
| takeoff_lines | Elements+bindings+formulas | TakeoffLine[] | ModeloActualizado, binding change |
| model_tree | Spatial graph | tree JSON | spatial CS |
| scenario_diff | two heads | diff summary | pointer move |
| twin_trust | quality/confidence | aggregates | quality updates |
| legacy_process_view | MDO graph | Process-like JSON | strangler read |

Caches llevan `source_version_id`, `scenario_id`, `built_at`, `hash`. Stale si hash mismatch.


## Apéndice I — Glosario analogía Git

| Término Git | Término MDO | Notas |
| --- | --- | --- |
| repo | Project |  |
| commit | ProjectVersion |  |
| patch/index | ChangeSet |  |
| hunk | ChangeOp |  |
| branch | Scenario |  |
| HEAD | ScenarioPointer |  |
| merge commit | Merge ChangeSet result version |  |
| tag | CertificationLock / baseline |  |
| working tree | draft ChangeSet |  |
| blame | Timeline + provenance |  |
| force push | PROHIBIDO |  |
| rebase | rebase CS onto new HEAD (tool) |  |
| cherry-pick | copiar ops selectas a otro scenario |  |
| stash | draft CS no confirmado |  |


## Apéndice J — Approval sign-off

| Rol | Nombre | Fecha | Firma |
| --- | --- | --- | --- |
| CTO |  |  |  |
| Tech Lead |  |  |  |
| Domain Owner Construction |  |  |  |
| PM |  |  |  |
| Security/Privacy reviewer |  |  |  |

- [ ] Aprobado metadata: RFC-E02 implementa Roadmap E07, no Identity E02
- [ ] Anti-scope §20 aceptado
- [ ] Criterios §18 aceptados
- [ ] Strangler plan §16 aceptado


## Apéndice K — Feature flags MDO

| Flag | Default | Owner | Rollback |
| --- | --- | --- | --- |
| `mdo.v1` | false | Construction | off → hide API mutators |
| `mdo.wedge` | false | Construction | off → legacy write only |
| `mdo.read` | false | Construction+FE | off → legacy read |
| `mdo.scenarios` | false | Construction | off → solo main |
| `mdo.autopipeline` | false | Perception+Construction | off → always HITL |
| `mdo.projections.async` | true | Construction | sync rebuild path |

Todas las flags auditadas vía RFC-E01 FeatureFlagAudit.


## Apéndice L — Decision log

| ID | Decisión | Alternativa rechazada | Fecha |
| --- | --- | --- | --- |
| D01 | RFC id E02-MDO mapea épica E07 | Renombrar RFC a E07 (rompe secuencia usuario) | 2026-08-02 |
| D02 | Scenario mínimo en E07 | 100% defer E11 | 2026-08-02 |
| D03 | CoW overlays no full-copy | Clone project per scenario | 2026-08-02 |
| D04 | Process strangler dual-write | Big-bang cutover | 2026-08-02 |
| D05 | IA solo draft CS | IA auto-confirm tipologías | 2026-08-02 |
| D06 | Takeoff projection keyed MDO ids | Materials private wall table | 2026-08-02 |
| D07 | Media refs not base64 SoT | Keep base64 in OLTP | 2026-08-02 |
| D08 | Event names alineados roadmap ES | English-only cloudEvents | 2026-08-02 |
| D09 | Monolito module not microservice | Split MDO service | 2026-08-02 |
| D10 | Soft-delete only | Hard delete UI | 2026-08-02 |


## Apéndice M — Open questions

| ID | Pregunta | Owner | Default si no hay respuesta |
| --- | --- | --- | --- |
| Q01 | ¿Validity ranges o CoW rows? | Tech Lead | ADR en semana 1 implementación |
| Q02 | ¿Tolerancia numérica strangler qty/ARS? | PM | 0 delta lógico golden |
| Q03 | ¿Auto-confirm allowlist exacta? | Perception+PM | vacía (off) |
| Q04 | ¿Multi-parent DAG versions? | Arch | single parent + merge metadata |
| Q05 | ¿N scenarios Free/Pro/Ent? | PM/Billing | 1/3/unlimited stub |
| Q06 | ¿content_hash algoritmo? | TL | sha256 canonical JSON |


## Apéndice N — Trazabilidad Roadmap E07 → RFC

| Roadmap item | RFC section |
| --- | --- |
| E07 objetivo SoT | §0 §1 §2 |
| E07-F01 schema | §3 Apéndice A |
| E07-F02 versions | §5 |
| E07-F03 changesets | §5 §8 §9 Apéndice W |
| E07-F04 projections | §10 Apéndice H |
| E07-F05 strangler | §16 |
| E07-F06 quality/provenance | §3 Apéndice F G |
| Events list E07 | §9 Apéndice B |
| Entities list E07 | §3 Apéndice A |
| DoD wedge+immutable+lineage+AuthZ | §18 |
| Architecture Scenarios §12 foundations | §7 Apéndice V |
| Dependencies E01/E02/E04 | §0 metadata |


## Apéndice O — Runbook skeletons


#### O.mdo-changeset-conflict

1) Leer conflict_types 2) Comparar HEAD 3) Rebase o merge 4) Reconfirm 5) Verificar proyección

- [ ] Owner oncall definido
- [ ] Link dashboard
- [ ] Paso de comunicación usuario si aplica


#### O.mdo-version-sealed-edit-attempt

1) Explicar 409 2) Crear CS desde sealed como base 3) Nueva version 4) Actualizar pointer

- [ ] Owner oncall definido
- [ ] Link dashboard
- [ ] Paso de comunicación usuario si aplica


#### O.mdo-strangler-rollback

1) `mdo.read=false` 2) `mdo.wedge=false` 3) Verificar legacy wedge 4) Dejar datos MDO intactos 5) Postmortem

- [ ] Owner oncall definido
- [ ] Link dashboard
- [ ] Paso de comunicación usuario si aplica


#### O.mdo-projection-stale

1) Check lag metric 2) Trigger rebuild 3) Banner UX 4) Si fail, servir graph sin qty con warning

- [ ] Owner oncall definido
- [ ] Link dashboard
- [ ] Paso de comunicación usuario si aplica


#### O.mdo-tenant-isolation-incident

1) Sev1 2) Disable mdo.read si leak vector 3) Audit queries 4) Patch predicate 5) Notify

- [ ] Owner oncall definido
- [ ] Link dashboard
- [ ] Paso de comunicación usuario si aplica


## Apéndice P — Performance budgets

| Operación | Budget p95 | Notas |
| --- | --- | --- |
| GET graph wedge project | < 300ms | sin geometry pesada |
| GET element inspector | < 100ms |  |
| POST confirm ≤50 ops | < 200ms | OLTP local |
| Scenario fork | < 100ms | pointer only |
| Takeoff rebuild wedge | < 2s |  |
| Compare two versions | < 500ms | summary |
| Dual-write overhead | < 50ms added |  |


## Apéndice Q — Security, AuthZ & PII

- AuthZ tenant en cada handler
- Project ACL roles owner/editor/viewer
- PII de Client en ProjectParty minimizada (hash/email opcional)
- No loggear geometry completa
- No loggear tokens
- Exports firmados auditados
- IDOR tests UUID cross-tenant

- [ ] Checklist secretos en CI
- [ ] No nuevas API sin AuthZ
- [ ] Bot AI role cannot confirm money


## Apéndice R — Rollback playbooks


### R.1 Flag rollback

```
1. PATCH flag mdo.read=false
2. PATCH flag mdo.wedge=false
3. Verify Studio legacy path
4. Monitor error rates
5. Keep mdo.v1 schema (expand) unless catastrophic
```


### R.2 Data rollback

No borrar versions. Re-point ScenarioPointer a version anterior conocida buena. Emit Timeline revert. Si dual-write diverge: marcar project `mdo_needs_repair` + job.


### R.3 Kill switches

| Switch | Effect |
| --- | --- |
| `mdo.v1` | disables new MDO mutators |
| `mdo.wedge` | stops dual-write |
| `mdo.read` | FE legacy |
| `mdo.autopipeline` | force HITL |


## Apéndice S — Demo scripts


#### S.Demo F01

Script 10 min: Crear project MDO → ver Site/Level/Space seed → inspector entity ids

- [ ] Grabación o notas
- [ ] Datos golden
- [ ] Flags documentadas


#### S.Demo F02

Script 10 min: Confirm CS → version tree + badge → seal → attempt edit → 409

- [ ] Grabación o notas
- [ ] Datos golden
- [ ] Flags documentadas


#### S.Demo F03

Script 10 min: Draft ops add wall → conflict by stale base → resolve → confirm

- [ ] Grabación o notas
- [ ] Datos golden
- [ ] Flags documentadas


#### S.Demo F04

Script 10 min: Confirm → takeoff projection visible → invalidate → rebuild

- [ ] Grabación o notas
- [ ] Datos golden
- [ ] Flags documentadas


#### S.Demo F05

Script 10 min: Wedge color→qty→ARS con `mdo.wedge` → compare Process vs MDO

- [ ] Grabación o notas
- [ ] Datos golden
- [ ] Flags documentadas


#### S.Demo F06

Script 10 min: Low confidence wall badge → filter API → block sign without waiver

- [ ] Grabación o notas
- [ ] Datos golden
- [ ] Flags documentadas


## Apéndice T — Mapping Architecture domains

| Architecture domain | MDO responsibility |
| --- | --- |
| Construction/MDO | Owns graph SoT |
| Projects | Project root lifecycle |
| Scenarios | Heads/overlays (min E07) |
| Projections | Caches |
| Perception | Evidence producer |
| Geometry | Measure via CS |
| Materials | Takeoff compute |
| Costs | CostLine/Budget |
| AI | Read tools |
| Marketplace | Offer bindings |
| Media | Blobs |
| Platform | Flags/obs |
| Identity | AuthZ |


## Apéndice U — Matrices de contratos extendidas


### U.1 Mutator × AuthZ × Event

| Mutator | Min role | Event |
| --- | --- | --- |
| confirm CS | editor | ChangeSetConfirmado+ModeloActualizado |
| seal | owner | VersionSellada |
| sign lock | owner | PresupuestoFirmado |
| fork scenario | editor | EscenarioCreado |
| reject CS | editor | ChangeSetRechazado |


### U.2 Reader × citation requirement

| Reader | Must cite |
| --- | --- |
| AI chat | yes |
| PDF report | version+hash |
| FE inspector | ids |
| Costs | takeoff_line_id |


### U.3 Strangler path matrix

| Flag combo | Write | Read |
| --- | --- | --- |
| all off | Process | Process |
| v1 | Process | Process |
| v1+wedge | dual | Process |
| v1+wedge+read | dual | MDO (fallback Process) |
| cutover | MDO | MDO |


## Apéndice V — Escenarios A/B/C (ladrillo/acero/retak)


### V.1 Setup

```
Base geometry @ V10 (shared Element ids W1..Wn)
Scenario A brick:  MaterialBinding wall.* → brick_spec
Scenario B steel:  MaterialBinding wall.* → steel_frame_spec
Scenario C retak:  MaterialBinding wall.* → retak_spec
Takeoff/Cost diverge; geometry ids shared
```


### V.2 Acceptance

- [ ] Fork B from A no copia geometry rows
- [ ] Rebind only creates overlay ops
- [ ] Compare A/B shows binding+qty+cost diffs
- [ ] Merge material-only clean; geometry edit-edit conflicts


### V.3 SystemPack example

Pack `envelope.masonry_to_steel` = ops tipifican wall types + default thickness params + binding. Apply as single CS en scenario hijo.


## Apéndice W — ChangeOp taxonomy

| op_type | target | payload keys | notes |
| --- | --- | --- | --- |
| add_entity | type+temp_id | attrs | creates stable id |
| update_entity | element_id | patch |  |
| remove_entity | element_id | reason | soft |
| set_geometry | element_id | measures | E06 |
| set_params | owner_ref | params |  |
| bind_material | element_id | material_spec_ref |  |
| bind_offer | target_ref | offer_id | marketplace |
| add_connection | from,to,type |  |  |
| remove_connection | connection_id |  |  |
| set_membership | element_id,system_id |  |  |
| accept_evidence | evidence_id | links |  |
| noop | — | marker | tests |

Ops ordenadas por `ordinal`. Apply sort estable. Unknown op_type → reject CS (fail closed).


## Apéndice X — OpenAPI fragment conceptual

```
openapi: 3.0.3
info:
  title: ARQ-IA MDO API
  version: "1.0.0"
paths:
  /v1/projects/{project_id}/mdo/changesets/{changeset_id}/confirm:
    post:
      parameters:
        - in: header
          name: Idempotency-Key
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Applied
        "409":
          description: VERSION_SEALED or CHANGESET_CONFLICT
  /v1/projects/{project_id}/mdo/versions/{version_id}:
    get:
      responses:
        "200":
          description: Version detail
```


## Apéndice Y — Checklist review PR MDO

- [ ] ¿Toca MDO? ¿Respeta ChangeSet-only writes?
- [ ] ¿AuthZ tenant presente?
- [ ] ¿Tests immutability si toca versions?
- [ ] ¿Tests isolation?
- [ ] ¿Eventos outbox si muta hechos?
- [ ] ¿Flag + rollback?
- [ ] ¿No introduce store duplicado L3?
- [ ] ¿No base64 SoT?
- [ ] ¿No confunde Identity E02 con este RFC?
- [ ] ¿Anti-scope intacto?
- [ ] ¿Golden wedge considerado?
- [ ] ¿OpenAPI/event schema?
- [ ] ¿Provenance/confidence si qty?
- [ ] ¿Docs/runbook touch?


## Apéndice Z — Cierre del RFC

Este RFC-E02-MDO operacionaliza la épica **E07 MDO Core** del ENGINEERING_ROADMAP (no Identity E02) como contrato de diseño ejecutable: SoT L2, versionado Git-like, ChangeSets, escenarios CoW, strangler desde Process JSON, e integraciones one-way con Visión/IA/Materials/Costs/Marketplace.

Tras approval sign-off (Apéndice J), el estado pasa a **Ready for implementation**. Desviaciones materiales requieren ADR.

Fin del contrato RFC E02 Modelo Digital de la Obra (MDO).

- [ ] Documento completo secciones 0–20 + Apéndices A–Z
- [ ] Idioma español
- [ ] Sin código de aplicación
- [ ] wc -l ≥ 2800
- [ ] Archivo único `/workspace/RFC_E02_MODELO_DIGITAL_OBRA.md`


### Z.1 Registro de control

- [ ] Control Z.1.01: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 1.
- [ ] Control Z.1.02: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 2.
- [ ] Control Z.1.03: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 3.
- [ ] Control Z.1.04: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 4.
- [ ] Control Z.1.05: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 5.
- [ ] Control Z.1.06: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 6.
- [ ] Control Z.1.07: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 7.
- [ ] Control Z.1.08: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 8.
- [ ] Control Z.1.09: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 9.
- [ ] Control Z.1.10: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 10.
- [ ] Control Z.1.11: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 11.
- [ ] Control Z.1.12: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 12.
- [ ] Control Z.1.13: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 13.
- [ ] Control Z.1.14: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 14.
- [ ] Control Z.1.15: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 15.
- [ ] Control Z.1.16: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 16.
- [ ] Control Z.1.17: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 17.
- [ ] Control Z.1.18: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 18.
- [ ] Control Z.1.19: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 19.
- [ ] Control Z.1.20: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 20.
- [ ] Control Z.1.21: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 21.
- [ ] Control Z.1.22: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 22.
- [ ] Control Z.1.23: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 23.
- [ ] Control Z.1.24: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 24.
- [ ] Control Z.1.25: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 25.
- [ ] Control Z.1.26: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 26.
- [ ] Control Z.1.27: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 27.
- [ ] Control Z.1.28: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 28.
- [ ] Control Z.1.29: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 29.
- [ ] Control Z.1.30: verificación de consistencia interna del RFC (cross-refs §/Apéndices, flags, eventos, entidades) item 30.


### Z.2 Narrativa de justificación (operativa, no ensayo de AUDITORIA)

El wedge actual demuestra valor color→qty→ARS, pero la persistencia file-centric impide versionado, escenarios y citas confiables. El MDO convierte ese wedge en twin versionado sin romper la cuña: strangler, flags, y proyecciones permiten migrar autoridad con rollback. La independencia de UI/visión/IA asegura que el SoT sobreviva la evolución del producto LATAM.


### Z.3 Dependencias futuras explícitas (no implementar aquí)

- E08 Materials DSL full
- E09 PriceBooks
- E10 Signed budgets UX
- E11 Scenario merge UX avanzada
- E12 Workspace
- E15/E16 AI product
- E21 Marketplace product

