# ARQ-IA 3.0 — ARQUITECTURA DEFINITIVA

| Campo | Valor |
|-------|-------|
| Documento | ARQ-IA 3.0 — Arquitectura Definitiva |
| Fecha | 2026-08-02 |
| Estado | Arquitectura objetivo aprobada para diseño |
| Audiencia | Ingeniería / Arquitectura de software |
| Naturaleza | Diseño (sin código de implementación) |
| Alcance | Sistema completo ARQ-IA 3.0 para años de evolución |
| Fuente de verdad de producto | MDO (Modelo Digital de la Obra) |
| Capas canónicas | Percepción → Twin → Inteligencia |
| Principio IA | La IA nunca reemplaza motores de CV/geometría |
| Modelo de crecimiento | Event-driven + módulos plugin |
| Monetización | Free / Pro / Enterprise |
| Mercado primario | LATAM primero |

---

## Índice

1. [Arquitectura general](#1-arquitectura-general)
   - 1.1 [Visión sistémica](#11-visión-sistémica)
   - 1.2 [Diagrama de contexto (C4 L1)](#12-diagrama-de-contexto-c4-l1)
   - 1.3 [Diagrama de contenedores (C4 L2)](#13-diagrama-de-contenedores-c4-l2)
   - 1.4 [Patrones de comunicación](#14-patrones-de-comunicación)
   - 1.5 [Flujos request vs eventos](#15-flujos-request-vs-eventos)
   - 1.6 [Bounded contexts](#16-bounded-contexts)
   - 1.7 [Topología de despliegue conceptual](#17-topología-de-despliegue-conceptual)
   - 1.8 [Principios arquitectónicos innegociables](#18-principios-arquitectónicos-innegociables)
2. [Modelo Digital de la Obra (MDO)](#2-modelo-digital-de-la-obra-mdo)
   - 2.1 [Definición y rol](#21-definición-y-rol)
   - 2.2 [Catálogo de entidades](#22-catálogo-de-entidades)
   - 2.3 [Relaciones canónicas](#23-relaciones-canónicas)
   - 2.4 [Ciclo de vida y evolución](#24-ciclo-de-vida-y-evolución)
   - 2.5 [Versionado: ProjectVersion, ChangeSet, Scenario](#25-versionado-projectversion-changeset-scenario)
   - 2.6 [Estrategia de almacenamiento](#26-estrategia-de-almacenamiento)
   - 2.7 [Patrones de consulta](#27-patrones-de-consulta)
   - 2.8 [Interacción con IA](#28-interacción-con-ia)
3. [Dominios](#3-dominios)
4. [Módulos (detalle por dominio)](#4-módulos-detalle-por-dominio)
5. [Eventos](#5-eventos)
6. [Base de datos](#6-base-de-datos)
7. [API](#7-api)
8. [Colas](#8-colas)
9. [Almacenamiento](#9-almacenamiento)
10. [IA (arquitectura)](#10-ia-arquitectura)
11. [Chat](#11-chat)
12. [Escenarios (Git-like)](#12-escenarios-git-like)
13. [Plugins](#13-plugins)
14. [Enterprise](#14-enterprise)
15. [Escalabilidad](#15-escalabilidad)
16. [Roadmap técnico](#16-roadmap-técnico)
17. [Qué NO hacer](#17-qué-no-hacer)
18. [Conclusión](#18-conclusión)
- [Apéndice A — Glosario arquitectónico](#apéndice-a--glosario-arquitectónico)
- [Apéndice B — Contratos entre capas L1/L2/L3](#apéndice-b--contratos-entre-capas-l1l2l3)
- [Apéndice C — Matriz dominio × store](#apéndice-c--matriz-dominio--store)
- [Apéndice D — Matriz evento × consumidores](#apéndice-d--matriz-evento--consumidores)
- [Apéndice E — Checklist onboarding de nuevo ingeniero](#apéndice-e--checklist-onboarding-de-nuevo-ingeniero)
- [Apéndice F — ADRs recomendados](#apéndice-f--adrs-recomendados)
- [Apéndice G — Criterios de aceptación arquitectónicos](#apéndice-g--criterios-de-aceptación-arquitectónicos)

---

## 1. Arquitectura general

### 1.1 Visión sistémica

ARQ-IA 3.0 es una plataforma de **ingeniería de obra asistida por software determinista**, donde la inteligencia artificial actúa como capa de orquestación, explicación y asistencia —nunca como fuente autoritativa de geometría, cantidades o costos. El sistema se organiza alrededor del **Modelo Digital de la Obra (MDO)** como única fuente de verdad de negocio.

La arquitectura separa tres capas canónicas:

| Capa | Nombre | Responsabilidad | Autoridad |
|------|--------|-----------------|-----------|
| L1 | Percepción | Extraer evidencia visual/geométrica desde planos y medios | Motores CV/OCR/segmentación |
| L2 | Twin (MDO) | Representar la obra como grafo tipado versionado | MDO + motores geométricos/materiales |
| L3 | Inteligencia | Asistir, explicar, recomendar, chat, reportes narrativos | Orquestador IA + políticas |

Flujo conceptual irreversible de autoridad:

```
[Planos / Medios]
        |
        v
 +--------------+     evidencias tipadas
 |  PERCEPCIÓN  | --------------------->  no inventa cantidades finales
 +--------------+
        |
        v
 +--------------+     entidades MDO
 |  TWIN (MDO)  | --------------------->  fuente de verdad
 +--------------+
        |
        v
 +--------------+     lecturas + citas
 | INTELIGENCIA | --------------------->  nunca escribe geometría cruda
 +--------------+
```

El producto comercial (wedge LATAM) permanece: plano coloreado → cantidades → costos en ARS (u otra moneda local), con fórmulas de dominio y planes Free/Pro/Enterprise. La arquitectura 3.0 generaliza ese wedge sin romperlo.

### 1.2 Diagrama de contexto (C4 L1)

```
                         +----------------------+
                         |   Usuarios LATAM     |
                         | Arquitectos, calc.,  |
                         | constructores, PM    |
                         +----------+-----------+
                                    |
                                    | HTTPS / WSS
                                    v
 +-------------+          +----------------------+          +------------------+
 | Proveedores | <------->|                      |<-------->| Contabilidad     |
 | Marketplace |  sync    |       ARQ-IA 3.0     |  light   | (Enterprise)     |
 +-------------+          |   Plataforma MDO     |          +------------------+
                          |                      |
 +-------------+          |  Percepción→Twin→IA  |          +------------------+
 | IdP SSO     | <------->|                      |<-------->| Pasarela pagos   |
 | OIDC/SAML   |          +----------+-----------+          | Billing          |
 +-------------+                     |                      +------------------+
                                     |
                     +---------------+---------------+
                     |               |               |
                     v               v               v
              Object Storage    Event Bus      Workers GPU/CPU
              Search Index      OLTP/Docs      Analytics (fase)
```

Actores externos:
- **Usuario final**: opera proyectos, planos, presupuestos, chat, reportes.
- **Administrador de organización**: RBAC, billing, retención, SSO.
- **Proveedor marketplace**: catálogos, cotizaciones, pedidos.
- **IdP**: identidad federada Enterprise.
- **Pasarela de pagos**: suscripciones Free→Pro→Enterprise.
- **Integraciones contables ligeras**: exportación de costos/certificaciones (no ERP completo en núcleo).

### 1.3 Diagrama de contenedores (C4 L2)

```
+===========================================================================+
|                              EDGE / CDN                                    |
|  static assets, thumbnails, signed URL media                               |
+====================================+======================================+
                                     |
                                     v
+===========================================================================+
|                         FRONTEND (SPA / Studio)                            |
|  Canvas planos · MDO explorer · Chat · Presupuestos · Escenarios · Admin  |
+====================================+======================================+
                                     | REST + WS
                                     v
+===========================================================================+
|                         API GATEWAY / BFF                                  |
|  AuthN/AuthZ · rate limit · idempotency · request routing · WS hub         |
+--+--------+--------+--------+--------+--------+--------+--------+---------+
   |        |        |        |        |        |        |        |
   v        v        v        v        v        v        v        v
Identity  Projects Vision  Geometry Materials Scenarios  AI/Chat  Marketplace
Billing   Media    Reports Costs   Timeline  Notify     Plugins  Audit
   |        |        |        |        |        |        |        |
   +--------+--------+--------+---+----+--------+--------+--------+
                                  |
                                  v
                    +-----------------------------+
                    |     MDO CORE SERVICE        |
                    | graph + versions + queries  |
                    +-------------+---------------+
                                  |
          +-----------------------+-----------------------+
          |                       |                       |
          v                       v                       v
   Relational OLTP         Geometry Docs            Object Storage
   Event Outbox            Search projections       Media / PDFs
                                  |
                                  v
                    +-----------------------------+
                    |        EVENT BUS            |
                    | domain + integration events |
                    +-------------+---------------+
                                  |
          +-----------+-----------+-----------+-----------+
          v           v           v           v           v
     Perception   Geometry    Materials    Reports     AI Indexer
     Workers      Workers     / Costs      / PDF       / Embeddings
                  Workers     Workers      Workers     Workers
```

Contenedores lógicos (no imponen vendor):

| Contenedor | Rol | Protocolo principal |
|------------|-----|---------------------|
| Frontend Studio | UX interactiva, canvas, chat | HTTPS, WSS |
| API Gateway/BFF | Entrada única, políticas | REST, WSS |
| Identity/Billing | Cuentas, orgs, planes, cuotas | REST sync |
| MDO Core | Grafo de obra, versiones, queries | REST interno + eventos |
| Perception Engine | CV, OCR, segmentación color | Jobs async |
| Geometry Engine | Mediciones, topología, takeoff geométrico | Jobs + sync queries |
| Materials Engine | Fórmulas de dominio → cantidades | Jobs + sync |
| Costs Engine | Pricebooks, presupuestos, moneda | Sync + eventos |
| Scenario Engine | Branches/changesets tipo Git | Sync + eventos |
| AI Orchestrator | Tools, RAG, citation/policy guards | Sync + streaming |
| Chat Service | Sesiones, memoria, streaming | WSS + REST |
| Marketplace | Catálogo, pedidos, sync proveedores | REST + jobs |
| Reports | PDF/Excel/certificaciones | Jobs |
| Notifications | Email, in-app, webhooks | Eventos |
| Media Service | Upload, derivados, firmas URL | REST + storage |
| Plugin Host | Manifests, capabilities, sandbox | REST interno |
| Job Workers | Ejecución background | Colas |
| Event Bus | Fan-out desacoplado | Pub/Sub |
| Storage tier | Objetos, blobs geométricos | SDK storage |
| Cache | Sesiones, proyecciones calientes | Key-value |
| Search | Índice textual/semántico MDO | Query API |

### 1.4 Patrones de comunicación

#### 1.4.1 Síncrono REST

Usar REST cuando:
- El cliente necesita respuesta inmediata para UI (CRUD proyecto, listar espacios, obtener presupuesto).
- La operación es de lectura o mutación corta (< pocos segundos).
- Se requiere contrato versionado público/privado estable.
- AuthZ debe evaluarse en el request path.

Anti-uso REST:
- OCR/CV de planos completos.
- Regeneración masiva de materiales.
- Generación de PDF grandes.
- Refresh de embeddings.

#### 1.4.2 WebSocket

Usar WSS para:
- Progreso de jobs (`job.progress`, `job.completed`, `job.failed`).
- Streaming de tokens/chunks de chat.
- Presencia colaborativa (quién edita qué hoja/escenario).
- Invalidaciones livianas de proyecciones abiertas en canvas.

No usar WSS como bus de dominio entre servicios backend.

#### 1.4.3 Eventos asíncronos

Usar eventos cuando:
- Un bounded context no debe conocer a sus consumidores.
- Hay fan-out (ModeloActualizado → materiales, costos, search, AI index, notificaciones).
- Se necesita resiliencia y reintentos.
- La consistencia eventual es aceptable y modelada.

```
Request path (sync):
Client -> Gateway -> Domain Service -> MDO/DB -> Response
                 \-> Outbox (si mutó estado)

Event path (async):
Outbox/Publisher -> Bus -> Consumers -> side effects -> maybe new events
```

#### 1.4.4 Matriz de decisión comunicación

| Caso | Patrón | Justificación |
|------|--------|---------------|
| Crear proyecto | REST | Respuesta inmediata |
| Subir plano | REST upload + event | Upload sync, proceso async |
| Segmentar colores | Cola + eventos | CPU intensivo |
| Consultar takeoff | REST sobre proyección MDO | Lectura |
| Recalcular costos | Evento o job | Puede ser largo |
| Chat respuesta | WSS stream + tools sync internos | UX |
| Certificación emitida | Evento + storage | Auditoría + fan-out |
| Plugin instalado | REST admin + evento integración | Propagación |

### 1.5 Flujos request vs eventos

#### Flujo request (lectura takeoff)

```
[UI] --GET /projects/{id}/takeoff?system=estructura-->
[Gateway AuthZ] -->
[Construction/Materials Read API] -->
[MDO Query: by system] -->
[Projection cache?] -->
[Response DTO + etag]
```

#### Flujo evento (plano → costos)

```
[UI] POST /media/planos
        |
        v
[Media] almacena original + emite PlanoSubido
        |
        v
[Perception Worker] procesa → PlanoProcesado (+ evidencias)
        |
        v
[Geometry Worker] actualiza geometría → ModeloActualizado
        |
        v
[Materials Worker] aplica fórmulas → MaterialCalculado
        |
        v
[Costs Worker] aplica pricebook → CostoActualizado
        |
        v
[Notify + Search + AI Indexer] consumen CostoActualizado / ModeloActualizado
        |
        v
[WS Hub] empuja progreso/completion al Studio
```

#### Flujo híbrido (chat con tools)

```
[UI Chat] WSS message
    |
    v
[Chat Service] ensambla contexto
    |
    v
[AI Orchestrator] plan estructurado
    |
    +--> Tool Router --> MDO Read APIs (sync interno)
    +--> Retriever RAG (proyecciones)
    |
    v
[Citation Guard] + [Policy Guard]
    |
    v
stream chunks --> UI
audit trail persistido
```

### 1.6 Bounded contexts

| Contexto | Lenguaje ubicuo | Frontera |
|----------|-----------------|----------|
| Identity & Access | usuario, org, rol, permiso, sesión | No conoce MDO |
| Projects | proyecto, obra, membresía, settings | Orquesta pertenencia, no geometría |
| Perception | plano, capa, máscara, evidencia, confianza CV | No escribe costos |
| Geometry | polígono, longitud, área, espesor, topología | No conoce pricebooks |
| Construction Twin (MDO) | espacio, elemento, sistema, vínculo | Núcleo |
| Materials | tipología, fórmula, cantidad, unidad | Lee geometría tipada |
| Costs | ítem, precio, moneda, presupuesto | No inventa cantidades |
| Scenarios | branch, changeset, merge, conflicto | Versiona MDO |
| Timeline | hito, secuencia constructiva | Proyección temporal |
| Reports | plantilla, artefacto, certificación | Solo lee + empaqueta |
| AI | tool, citation, confidence, eval | Read-mostly |
| Chat | thread, mensaje, memoria | UI conversacional |
| Marketplace | proveedor, SKU, pedido | Fuera del twin core |
| Billing | plan, cuota, uso, factura | Gates de capacidad |
| Notifications | canal, preferencia, delivery | Side-effect |
| Media | asset, derivado, retención | Bytes |
| Audit | acto, actor, before/after | Inmutable |
| Plugins | manifest, capability, sandbox | Extensión |

Mapa de acoplamiento permitido:

```
Identity --------> (gates) casi todos
Projects --------> MDO, Media, Scenarios
Perception ------> Media, MDO (evidencias)
Geometry --------> MDO
Materials -------> MDO (geo tipada)
Costs -----------> Materials projections, Pricebooks
Scenarios -------> MDO
AI/Chat ---------> MDO reads, Reports reads
Marketplace ----- > Costs (opcional), Identity
Reports ---------> MDO, Costs, Media
Billing ---------> Identity, Usage meters
Plugins ---------> host contracts only
```

### 1.7 Topología de despliegue conceptual

Diseño **cloud-portable**: contenedores/procesos lógicos, sin amarrar la arquitectura a un hiperescalador concreto.

```
Region Primaria (LATAM-friendly)
├── Edge/CDN
├── Gateway + Frontend hosting
├── Stateless API pods (autoscale HPA)
├── MDO/OLTP primary + read replicas
├── Document store / JSON geometry snapshots
├── Object storage buckets (tenant-prefixed)
├── Cache cluster
├── Search cluster
├── Event bus (partitioned by org_id/project_id)
├── Worker pools:
│   ├── perception-cpu
│   ├── perception-gpu (opcional)
│   ├── geometry
│   ├── materials-costs
│   ├── reports
│   ├── ai-embed
│   └── notify-mail
└── Observability stack (logs/metrics/traces)

Region Secundaria (Enterprise DR opcional)
├── Async replica DB
├── Object storage replication
└── Warm standby workers
```

Principios de topología:
1. APIs stateless; estado en stores.
2. Workers aislados por perfil de recurso (CPU vs I/O vs LLM).
3. Particionado de colas por `org_id` para fairness multi-tenant.
4. Object storage con prefijos `org/{orgId}/project/{projectId}/...`.
5. No compartir DB física obligatoriamente al inicio; sí límites lógicos por esquema/ownership.
6. Evolución a servicios desplegables independientes cuando el throughput lo exija — no antes.

### 1.8 Principios arquitectónicos innegociables

1. **MDO es la fuente de verdad** de la obra digital.
2. **Percepción produce evidencias**, no presupuestos finales.
3. **Geometría y materiales son motores deterministas** (o semi-deterministas versionados).
4. **IA es L3**: lee, explica, asiste; no inventa cantidades ni geometría.
5. **Event-driven para crecimiento**: nuevos consumidores sin reescribir productores.
6. **Plugins por capability contracts**, no forks del core.
7. **Multi-tenant desde día 0** en modelo de datos y authZ.
8. **Auditoría de hechos comerciales** (presupuestos firmados, certificaciones) es inmutable.
9. **LATAM-first**: moneda, unidades, flujos de estudio/constructor, offline-ish tolerante a latencia.
10. **Free/Pro/Enterprise** como ejes de cuota y capacidad, no como forks de código.
11. **Versionado de escenarios** tipo Git sobre el twin.
12. **Citation-first** en respuestas IA usadas comercialmente.
13. **Idempotencia** en mutaciones y consumers de eventos.
14. **Soft-delete + retención** sobre hard-delete en dominios críticos.
15. **Observabilidad de confianza**: cada cantidad lleva provenance + confidence cuando aplica.

### 1.9 Desglose por subsistema de plataforma

#### Frontend
- Studio multi-panel: canvas de plano, árbol MDO, inspector, chat, costos.
- Estado UI separado del MDO server; optimistic UI solo en ediciones no autoritativas.
- Suscripción WS a `project:{id}` para jobs y presencia.
- Feature flags por plan (Free/Pro/Enterprise) y por plugin instalado.
- Internacionalización ES-AR/ES-LATAM prioritaria; números y moneda localizados.

#### Backend / API Gateway
- Terminación TLS, CORS, auth bearer/session.
- Rate limits por plan y por ruta sensible (upload, AI, export).
- Correlación `X-Request-Id` / `traceparent`.
- Traducción de errores de dominio a error model estable.
- BFF opcional para agregar proyecciones de UI sin contaminar APIs de dominio.

#### Motor de visión (Perception)
- Pipelines: ingest → normalize → OCR → color segmentation → symbol assist → evidence pack.
- Salida: evidencias con bounding boxes, máscaras, labels, confidence, lineage a asset.
- Nunca calcula costo; puede sugerir tipologías candidatas con baja autoridad.

#### Motor geométrico
- Consume evidencias + calibración de escala.
- Produce longitudes, áreas, volúmenes, conteos, relaciones espaciales.
- Expone validadores (cierres de polígono, escala ausente, solapes).
- Escribe en MDO vía ChangeSets, no mutación silenciosa.

#### Motor de materiales
- Catálogo de tipologías y fórmulas versionadas.
- Input: geometría tipada + parámetros de sistema.
- Output: líneas de takeoff con unidad, cantidad, provenance.
- Plugins pueden aportar fórmulas (Steel Frame, Gas, etc.).

#### MDO
- Grafo + proyecciones.
- Versionado y escenarios.
- APIs de lectura ricas para IA y reportes.

#### Motor de escenarios
- Branches, commits/changesets, merge, compare, promote.
- Detección de conflictos por tipo de entidad.

#### Motor de IA
- Orquestador, tools read-only, RAG, guards, eval.
- Sin autoridad geométrica.

#### Chat
- Capa conversacional sobre motor IA + permisos proyecto.

#### Marketplace
- Catálogo y transacción comercial periférica al twin.
- Puede sugerir proveedores para líneas de costo; no altera geometría.

#### Reportes
- Renderizadores PDF/Excel; certificaciones firmadas lógicamente.
- Empaquetan snapshots MDO + costos + disclaimers.

#### Notificaciones
- Fan-out desde eventos; preferencias de usuario/org.

#### Identity / Billing
- Orgs, usuarios, planes, entitlements, usage meters.
- Gates antes de jobs costosos.

#### Media
- Upload multipart/resumable, virus scan conceptual, derivados, thumbnails.

#### Event bus
- Domain events (dentro del modelo) + integration events (entre contextos).

#### Job workers
- Escalables horizontalmente; heartbeats; cancelación cooperativa.

#### Storage
- Object storage + DB + docs + cache + search + outbox.

### 1.10 SLAs conceptuales por clase de operación

| Clase | Ejemplo | Objetivo UX |
|-------|---------|-------------|
| Interactivo | abrir proyecto, listar espacios | p95 < 300–500 ms (API) |
| Mutación corta | renombrar espacio, editar parámetro | p95 < 800 ms |
| Job corto | thumbnail, preview OCR page | < 30–60 s |
| Job medio | plano completo segmentado | minutos |
| Job largo | recálculo masivo + reportes pack | minutos a decenas |
| Chat token stream | primer token | pocos segundos |
| Export certificación | PDF firmado | job con progreso |

### 1.11 Seguridad transversal (alto nivel)

- AuthN: sesión + OIDC/SAML Enterprise.
- AuthZ: RBAC base + ABAC por atributos de proyecto/escenario.
- Tenant isolation en cada query (`org_id` obligatorio).
- Firmas URL temporales para media.
- Secrets fuera del MDO.
- Audit log de acciones privilegiadas y de respuestas IA usadas en docs comerciales.
- Sanitización de uploads; límites de tamaño por plan.

### 1.12 Observabilidad transversal

Señales mínimas:
- Métricas: latencia API, profundidad de cola, tasa DLQ, costo tokens, éxito percepción.
- Trazas: request → outbox → consumer.
- Logs estructurados con `org_id`, `project_id`, `job_id`, `event_id`.
- Product analytics separado de audit legal.

### 1.13 Modelo de tenancy

```
Organization
  ├── Users / Teams
  ├── Entitlements (plan)
  ├── Projects
  │     ├── Media
  │     ├── MDO Baseline
  │     ├── Scenarios
  │     └── Commercial docs
  └── Audit / Billing usage
```

Aislamiento:
- Hard boundary: organización.
- Soft boundary: proyecto y escenario.
- Plugins instalables a nivel org (Enterprise) o proyecto (según plan).

### 1.14 Consistencia

| Dato | Modelo de consistencia |
|------|------------------------|
| Membresía / roles | Fuerte (sync) |
| Metadata proyecto | Fuerte |
| Evidencias percepción | Eventual tras job |
| Geometría MDO | Fuerte dentro del changeset commit |
| Proyecciones search | Eventual |
| Costos derivados | Eventual tras materiales |
| Embeddings | Eventual |
| Notificaciones | Eventual at-least-once |

### 1.15 Diagrama de capas tecnológicas lógicas

```
+--------------------- EXPERIENCIA ----------------------+
| Studio Web · Admin · Public API clients · Mobile later |
+--------------------- APLICACIÓN -----------------------+
| Use-cases · Policies · DTOs · WS hubs · Job APIs       |
+--------------------- DOMINIO --------------------------+
| MDO aggregates · Domain services · Plugin contracts    |
+--------------------- INFRAESTRUCTURA ------------------+
| OLTP · Docs · Object · Cache · Search · Bus · Workers  |
+--------------------------------------------------------+
```

### 1.16 Relación Free / Pro / Enterprise con arquitectura

| Capacidad | Free | Pro | Enterprise |
|-----------|------|-----|------------|
| Proyectos activos | limitado | alto | custom |
| MPX / storage | bajo | medio | alto/custom |
| Jobs percepción concurrentes | 1 | N | N + prioridad |
| Escenarios | básico/ninguno avanzado | branches | branches + políticas |
| Chat IA | cupo bajo | cupo alto | cupo + SSO audit |
| Plugins | core | selectos | privados + SDK |
| SSO / DR / residencia | no | limitado | sí |
| API pública | no/limitada | sí | sí + SLA |

La arquitectura implementa entitlements como **policy checks** en Gateway y en enqueue de jobs — no como código duplicado por plan.

### 1.17 Mapa de ownership de escritura al MDO

| Actor | Puede escribir | Restricción |
|-------|----------------|-------------|
| Geometry Engine | elementos geométricos, medidas | vía ChangeSet |
| Materials Engine | líneas takeoff materiales | vía ChangeSet / proyección material |
| Costs Engine | ítems costo derivados | store de costos ligado a versión |
| Usuario (Studio) | anotaciones, parámetros, tipologías elegidas | validadas |
| Scenarios | branches/merges | reglas merge |
| AI | **no** escribe geometría; puede proponer ChangeSet draft | requiere aceptación humana |
| Marketplace | **no** escribe MDO core | solo vínculos comerciales opcionales |
| Reports | **no** escribe twin | snapshots de salida |

### 1.18 Diagrama ASCII de anti-corrupción hacia IA

```
          +------------------+
          |  AI Orchestrator |
          +--------+---------+
                   |
                   | solo tools read + propose
                   v
          +------------------+
          |  Anti-Corruption |
          |  - schema validate
          |  - citation required
          |  - no raw geom write
          +--------+---------+
                   |
                   v
          +------------------+
          |   MDO Read API   |
          +------------------+
```

---

## 2. Modelo Digital de la Obra (MDO)

### 2.1 Definición y rol

El **Modelo Digital de la Obra (MDO)** es el agregado central de ARQ-IA 3.0: una representación tipada, versionada y consultable de la obra, construida a partir de evidencia de percepción y decisiones de ingeniería, enriquecida por motores geométricos y de materiales, y consumida por costos, escenarios, reportes e IA.

Propiedades esenciales:
- **Canónico**: cualquier cantidad comercial debe poder trazarse a entidades MDO (o declararse explícitamente manual).
- **Versionado**: baseline + scenarios + changesets.
- **Multi-proyección**: vistas por espacio, sistema, takeoff, costo, timeline.
- **Provenance-aware**: cada hecho relevante conoce origen (percepción, usuario, fórmula, plugin).
- **IA-ready**: APIs de lectura y citas estables.

El MDO **no es** un archivo BIM completo obligatorio ni un dump de píxeles. Es un grafo de dominio de construcción + payloads geométricos asociados.

### 2.2 Catálogo de entidades

#### 2.2.1 Entidades raíz y de organización

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| Organization | id, name, plan, region_preference, retention_policy | Tenant root |
| User | id, email, display_name, status | Identity |
| Membership | user_id, org_id, roles[], status | |
| Project | id, org_id, name, code, location, currency, unit_system, status | Obra |
| ProjectSettings | project_id, defaults tipología, escalas, plugins_enabled[] | |

#### 2.2.2 Versionado

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| ProjectVersion | id, project_id, label, parent_version_id, is_baseline, created_by, created_at, summary | Snapshot lógico |
| Scenario | id, project_id, branch_name, head_version_id, status, description | Branch |
| ChangeSet | id, scenario_id, base_version_id, result_version_id?, message, author, status, conflicts[] | Commit |
| ChangeOp | id, changeset_id, op_type (add/update/remove), entity_type, entity_id, payload_diff, confidence? | Operación atómica |

#### 2.2.3 Medios y percepción

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| MediaAsset | id, project_id, kind (plano/foto/pdf), storage_key, checksum, pages, mime | |
| PlanSheet | id, asset_id, page_index, name, scale_ratio, calibration_status | |
| PerceptionJob | id, asset_id, status, pipeline_version, metrics | |
| Evidence | id, sheet_id, kind, label, geom_ref, confidence, raw_features_ref | Salida L1 |
| ColorRegion | id, sheet_id, color_key, mask_ref, area_px, mapped_typology_candidate? | Wedge color |

#### 2.2.4 Espacio y estructura del twin

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| Site | id, project_id, name, geo_location? | |
| Building | id, site_id, name, levels_count | |
| Level | id, building_id, elevation, name | |
| Space | id, level_id, name, use_type, area_m2, perimeter_m, polygon_ref | |
| Zone | id, level_id, name, purpose | Agrupación |
| Grid / Axis | id, level_id, label, geometry_ref | Opcional |

#### 2.2.5 Sistemas y elementos

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| System | id, project_id, discipline (estructura/instalaciones/…), name | |
| Element | id, system_id, space_id?, typology_code, name, status | Nodo central |
| ElementGeometry | element_id, geom_type, payload_ref, measures{L,A,V,count}, units, quality_flags | Doc/blob |
| Connection | id, from_element_id, to_element_id, connection_type | Topología |
| Assembly | id, name, member_element_ids[] | Compuesto |
| ParameterSet | id, owner_ref, params{} versioned | Dimensiones tipológicas |

#### 2.2.6 Materiales y takeoff

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| Typology | code, discipline, plugin_id?, params_schema, default_formula_id | Catálogo |
| Formula | id, typology_code, version, expression_ref, unit_out, inputs[] | Determinista |
| TakeoffLine | id, version_id, element_id, material_code, qty, unit, formula_id, provenance | |
| MaterialCatalogItem | code, name, unit, category, region_tags | |
| WasteFactor | typology_code, factor, rationale | |

#### 2.2.7 Costos

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| Pricebook | id, org_id/project_id, currency, valid_from, source | |
| PriceItem | pricebook_id, material_code, unit_price, taxes?, provider_ref? | |
| Budget | id, project_id, version_id, scenario_id?, status, total | |
| BudgetLine | budget_id, takeoff_line_id, unit_price, amount, adjustments | |
| CurrencyRate | from, to, rate, as_of | LATAM |
| SignedBudget | budget_id, signature_meta, immutable_snapshot_ref | Comercial |

#### 2.2.8 Escenarios extendidos y timeline

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| ScenarioCompare | left_version, right_version, diff_summary | |
| Milestone | id, project_id, name, date, linked_elements[] | |
| WorkSequence | id, ordered_system_ids / packs | |
| Certification | id, project_id, period, snapshot_ref, status, hash | Inmutable al emitir |

#### 2.2.9 Colaboración, IA, plugins

| Entidad | Atributos conceptuales | Notas |
|---------|------------------------|-------|
| Annotation | id, target_ref, author, body, severity | |
| AIProposal | id, proposed_changeops[], citations[], status (draft/accepted/rejected) | |
| ChatThread | id, project_id, scope_ref, participants | |
| ChatMessage | id, thread_id, role, content, citations[], tools_used[] | |
| PluginInstallation | org_id/project_id, plugin_id, version, config | |
| AuditEvent | actor, action, entity_ref, before, after, ts | Append-only |

### 2.3 Relaciones canónicas

```
Organization 1--* Project
Project 1--* ProjectVersion
Project 1--* Scenario
Scenario *--1 ProjectVersion (head)
ProjectVersion 1--* ChangeSet (resulting)
ChangeSet 1--* ChangeOp

Project 1--* MediaAsset 1--* PlanSheet 1--* Evidence
Project 1--1 Site? 1--* Building 1--* Level 1--* Space

Project 1--* System 1--* Element
Element 1--1 ElementGeometry
Element *--* Space (ubicación)
Element *--* Element (Connection)
Element 1--* TakeoffLine
TakeoffLine *--1 Formula
TakeoffLine 1--* BudgetLine
Budget 1--* BudgetLine
Budget 0--1 SignedBudget

Project 1--* Certification (sobre version snapshot)
PluginInstallation --> Typology/Formula contribution
```

Reglas de integridad conceptuales:
1. Toda `TakeoffLine` apunta a `ProjectVersion` concreta.
2. Todo `Budget` cuelga de versión/escenario.
3. `Evidence` puede vincularse a `Element` pero la ausencia no bloquea elemento manual.
4. `ChangeOp` es la unidad de merge/conflicto.
5. Soft-delete marca `status=deleted` sin borrar lineage comercial.

### 2.4 Ciclo de vida y evolución

Estados de proyecto (simplificado):

```
draft -> active -> bidding -> in_construction -> certified_periods... -> archived
```

Estados de hoja/plano:

```
uploaded -> queued -> perceiving -> needs_calibration -> geometrizing -> ready -> stale
```

Estados de elemento:

```
detected -> classified -> measured -> materialized -> costed -> locked_in_certification
```

Evolución típica:
1. Upload de planos coloreados / documentación.
2. Percepción genera evidencias.
3. Usuario calibra escala y mapea colores→tipologías (wedge).
4. Geometría consolida medidas en elementos.
5. Materiales aplican fórmulas → takeoff.
6. Costos aplican pricebook → presupuesto.
7. Escenarios exploran alternativas (p.ej. steel vs hormigón).
8. Promote a baseline.
9. Reportes/certificaciones congelan snapshots.
10. IA explica y asiste en todo el ciclo sin romper determinismo.

### 2.5 Versionado: ProjectVersion, ChangeSet, Scenario

Analogía Git (ver también §12):

| Git | MDO |
|-----|-----|
| Repository | Project |
| Branch | Scenario |
| Commit | ChangeSet |
| Tree/Blob | Entity graph + geometry payloads |
| Main | Baseline scenario/version |
| Tag | Certification / SignedBudget snapshot |
| Merge | Scenario merge con reglas por conflict type |
| Working copy | Draft ChangeSet abierto en Studio |

Reglas:
- `ProjectVersion` es inmutable una vez cerrada.
- Editar = nuevo ChangeSet sobre un Scenario.
- Baseline promote copia/marca versión head como baseline.
- Compare materializa diff de ChangeOps + agregados takeoff/cost.

### 2.6 Estrategia de almacenamiento

Tres planos de persistencia del MDO:

```
+-------------------+     +----------------------+     +------------------+
| Relational Graph  |     | Document / JSON      |     | Object Storage   |
| ids, relations,   | <-> | geometry snapshots,  | <-> | masks, planos,   |
| measures summary, |     | param sets grandes,  |     | PDFs, embeddings |
| version pointers  |     | evidence feature packs|     | binaries         |
+-------------------+     +----------------------+     +------------------+
```

| Tipo de dato | Store | Razón |
|--------------|-------|-------|
| Project, Space, Element ids/relations | Relacional OLTP | Integridad, joins, authZ |
| Medidas resumidas (L/A/V/count) | Relacional (columnas/JSON tipado) | Takeoff queries rápidas |
| Polígonos detallados, meshes ligeros | Document/JSON | Payload variable |
| Máscaras, imágenes, PDF | Object storage | Binario grande |
| Proyección search | Índice | Texto + facetado |
| Eventos | Outbox + bus (+ opcional event store) | Integración |

### 2.7 Patrones de consulta

#### Por espacio
- Entrada: `space_id` + `version_id`
- Retorna: elementos contenidos, áreas, takeoff filtrado, costos parciales.
- Uso UI: inspector de ambiente; chat “¿qué hay en cocina?”.

#### Por sistema / disciplina
- Entrada: `system_id` o `discipline`
- Retorna: elementos, conexiones, cantidades agregadas.
- Uso: cómputo estructura, instalaciones.

#### Vistas takeoff
- Agregaciones `GROUP BY material_code, unit` sobre `TakeoffLine` de una versión.
- Filtros: scenario, building, level, plugin typology set.
- Export hacia Excel/PDF.

#### Vistas de confianza / provenance
- Filtrar elementos con `confidence < threshold` o sin calibración.
- Lista de trabajo de QA humana.

#### Diff de escenarios
- Compare takeoff y costos entre dos `ProjectVersion`.

APIs de lectura deben ser **estables para IA** (ver §2.8 y §10).

### 2.8 Interacción con IA

Contrato:
1. IA consume **Read APIs** y proyecciones RAG — no SQL libre sobre OLTP.
2. Toda afirmación cuantitativa requiere **citation** a entity refs (`takeoff_line`, `element`, `budget_line`).
3. `confidence` de percepción/geometría se **repasa** (passthrough), no se “mejora” retóricamente.
4. IA puede crear `AIProposal` con ChangeOps sugeridos; commit requiere rol humano.
5. Prohibido generar geometría autoritativa desde LLM.

```
Pregunta usuario
   -> Retriever (MDO projections)
   -> Tools (get_space, list_takeoff, get_budget_summary, ...)
   -> Draft respuesta
   -> Citation Guard
   -> Policy Guard (plan, permisos, PII)
   -> Respuesta + citations[]
```

### 2.9 Identificadores y lineage

- IDs opacos globales (ULID/UUID).
- `stable_business_key` opcional por elemento para merges (p.ej. código de muro).
- Lineage chain: `MediaAsset -> Evidence -> ElementGeometry -> TakeoffLine -> BudgetLine -> SignedBudget`.
- Cada eslabón puede auditarse.

### 2.10 Proyecciones materializadas del MDO

| Proyección | Contenido | Consumidores |
|------------|-----------|--------------|
| `proj_space_tree` | site/building/level/space | UI, chat |
| `proj_system_graph` | systems/elements/connections | UI, geometry |
| `proj_takeoff_agg` | cantidades por material | costs, reports |
| `proj_cost_agg` | montos por capítulo | UI, reports |
| `proj_confidence_heat` | scores por hoja/elemento | QA |
| `proj_search_docs` | chunks texto para RAG | AI |
| `proj_timeline` | hitos/secuencias | timeline |

Invalidación: por eventos `ModeloActualizado`, `MaterialCalculado`, `CostoActualizado`, `EscenarioMerged`.

### 2.11 Extensibilidad tipológica vía plugins

El MDO admite tipologías contribuidas:
- Plugin declara `Typology` + `Formula` + validators + UI panels.
- Core almacena instancias `Element` con `typology_code` namespaced (`steel_frame:montante`).
- Desinstalar plugin no borra historia; marca tipologías como `orphaned` con regla de lectura.

### 2.12 Límites del MDO

El MDO no intenta ser:
- ERP de obra completo.
- BIM Authoring Tool (Revit-killer) en v3.0 inicial.
- Marketplace ledger financiero global.
- Data lake analítico (eso es warehouse posterior).

Sí es:
- Twin operacional de cómputo y decisión de estudio/constructor LATAM.
- Base para escenarios, costos y certificaciones.
- Suelo firme para IA con citas.

### 2.13 Calidad de datos y flags

Flags conceptuales en entidades:
- `scale_missing`
- `geometry_degenerate`
- `typology_unmapped`
- `formula_fallback_used`
- `price_stale`
- `manual_override`
- `locked_by_certification`
- `plugin_unavailable`

Los reportes y el chat deben surfacear estos flags; nunca ocultarlos.

### 2.14 Multimoneda y unidades

- `Project.currency` (ARS default LATAM wedge; soporta otras).
- `unit_system` métrico prioritario.
- Conversiones de moneda versionadas por fecha para presupuestos históricos.
- Unidades de takeoff normalizadas (`m`, `m2`, `m3`, `kg`, `un`, `ml`).

### 2.15 Seguridad de acceso al MDO

Toda query MDO exige:
1. `org_id` del caller.
2. membresía al proyecto.
3. permiso de acción (`mdo:read`, `mdo:write`, `scenario:merge`, etc.).
4. filtro de escenario visible según rol.

AI tools heredan el token/usuario efectivo (no service account omnisciente en chat usuario).

---

## 3. Dominios

Esta sección define bounded contexts con ownership claro. El detalle de módulos aparece en §4.

### 3.1 Identity

| Aspecto | Definición |
|---------|------------|
| Propósito | Autenticar usuarios, gestionar organizaciones, membresías, roles base y sesiones |
| Posee | User, Organization, Membership, Role bindings, Session, API keys |
| Depende de | Billing (entitlements de plan), IdP externo opcional |
| No posee | MDO, planos, costos |

### 3.2 Projects

| Aspecto | Definición |
|---------|------------|
| Propósito | Ciclo de vida de obras/proyectos, settings, membresía a nivel proyecto |
| Posee | Project, ProjectSettings, ProjectMembership, labels |
| Depende de | Identity, Billing (cuotas de proyectos), Media (indirecto) |
| No posee | Geometría detallada ni fórmulas |

### 3.3 Vision / Perception

| Aspecto | Definición |
|---------|------------|
| Propósito | Extraer evidencias desde medios gráficos |
| Posee | PerceptionJob, Evidence, ColorRegion, pipeline metrics |
| Depende de | Media, Projects; escribe evidencias consumibles por Geometry/MDO |
| No posee | Presupuestos, pricebooks |

### 3.4 Geometry

| Aspecto | Definición |
|---------|------------|
| Propósito | Medir, topologizar, validar geometría de elementos |
| Posee | ElementGeometry measures, validators, calibration helpers |
| Depende de | Perception evidences, MDO structure, Media calibrations |
| No posee | Precios ni narrativas IA |

### 3.5 Construction (Twin estructural)

| Aspecto | Definición |
|---------|------------|
| Propósito | Mantener el grafo espacial/sistémico del MDO |
| Posee | Site, Building, Level, Space, System, Element, Connection, Assembly |
| Depende de | Projects, Geometry inputs, Plugins tipológicos |
| No posee | Ejecución CV ni LLM |

### 3.6 Materials

| Aspecto | Definición |
|---------|------------|
| Propósito | Transformar geometría tipada en cantidades de materiales |
| Posee | Typology (core), Formula, TakeoffLine, WasteFactor |
| Depende de | Construction/Geometry measures, Plugins |
| No posee | Pagos ni chat |

### 3.7 Costs

| Aspecto | Definición |
|---------|------------|
| Propósito | Valorizar takeoff con pricebooks y producir presupuestos |
| Posee | Pricebook, PriceItem, Budget, BudgetLine, SignedBudget, CurrencyRate |
| Depende de | Materials takeoff, Marketplace opcional, Billing moneda/plan |
| No posee | Máscaras de percepción |

### 3.8 Scenarios

| Aspecto | Definición |
|---------|------------|
| Propósito | Branching/versionado Git-like del MDO |
| Posee | Scenario, ChangeSet, ChangeOp, merge results, compares |
| Depende de | Construction/Materials/Costs versioned data |
| No posee | Rendering PDF final (usa Reports) |

### 3.9 Timeline

| Aspecto | Definición |
|---------|------------|
| Propósito | Hitos y secuencia constructiva ligados al twin |
| Posee | Milestone, WorkSequence, links a systems/elements |
| Depende de | Construction, Scenarios (opcional) |
| No posee | Motor CV |

### 3.10 Reports

| Aspecto | Definición |
|---------|------------|
| Propósito | Generar artefactos PDF/Excel/certificaciones |
| Posee | ReportTemplate, ReportJob, Certification packages |
| Depende de | MDO reads, Costs, Media, Audit |
| No posee | Mutación de tipologías |

### 3.11 AI

| Aspecto | Definición |
|---------|------------|
| Propósito | Orquestar asistencia inteligente con guards |
| Posee | AIProposal, tool traces, eval results, embedding indexes refs |
| Depende de | MDO read, Chat, Policy/Billing quotas |
| No posee | Autoridad geométrica |

### 3.12 Chat

| Aspecto | Definición |
|---------|------------|
| Propósito | UX conversacional y memoria de hilo |
| Posee | ChatThread, ChatMessage, short/long memory summaries |
| Depende de | AI, Identity permissions, Projects scope |
| No posee | Event bus infra global |

### 3.13 Marketplace

| Aspecto | Definición |
|---------|------------|
| Propósito | Proveedores, catálogos, selección y compras |
| Posee | Provider, SKU, Quote, Order |
| Depende de | Identity/org, Costs (links), Notifications |
| No posee | Twin geometry core |

### 3.14 Billing

| Aspecto | Definición |
|---------|------------|
| Propósito | Planes Free/Pro/Enterprise, usage, facturación |
| Posee | Plan, Subscription, UsageMeter, Invoice refs |
| Depende de | Identity, Payment provider |
| No posee | MDO entities |

### 3.15 Notifications

| Aspecto | Definición |
|---------|------------|
| Propósito | Entregar avisos multi-canal |
| Posee | Preference, Notification, DeliveryAttempt |
| Depende de | Events from many domains, Identity |
| No posee | Cálculo de cantidades |

### 3.16 Media

| Aspecto | Definición |
|---------|------------|
| Propósito | Assets binarios y derivados |
| Posee | MediaAsset, Derivative, Thumbnail, retention marks |
| Depende de | Projects, Storage, Billing quotas |
| No posee | Fórmulas de materiales |

### 3.17 Settings

| Aspecto | Definición |
|---------|------------|
| Propósito | Preferencias de usuario/org/proyecto |
| Posee | Setting bags tipadas, defaults |
| Depende de | Identity, Projects |
| No posee | Evidencias |

### 3.18 Audit

| Aspecto | Definición |
|---------|------------|
| Propósito | Registro inmutable de actos relevantes |
| Posee | AuditEvent stream |
| Depende de | Todos (como consumidor); Identity para actor |
| No posee | Lógica de negocio activa |

### 3.19 Plugins / Registry

| Aspecto | Definición |
|---------|------------|
| Propósito | Descubrir, versionar, instalar y hospedar módulos |
| Posee | PluginManifest, Capability grants, installations |
| Depende de | Identity/org entitlements; host APIs |
| No posee | Datos de obra salvo via contracts |

### 3.20 Mapa de dependencias entre dominios

```
Billing ----\ 
Identity ----+--> Projects --> Media --> Perception --> Geometry --> Construction(MDO)
                                      \                           |
                                       \--> Scenarios <-----------+
                                                                  |
Materials <--------------------------------------------------------+
    |
    v
  Costs --> Reports --> Certifications
    ^
    |
Marketplace (opcional link)

AI/Chat ---- read ----> MDO/Materials/Costs/Reports
Plugins ---- contribute --> Materials/Geometry validators/UI
Notifications <---- events ---- almost all
Audit <---- events/commands ---- almost all
Settings ---- config ---- many
```

### 3.21 Reglas de dependencia

1. Dependencias apuntan hacia adentro al MDO o lateralmente vía eventos — no ciclos sync.
2. AI/Chat solo dependen en lectura (salvo proposals explícitas).
3. Marketplace no es prerequisito del twin.
4. Plugins no acceden a DB de otros dominios: solo capability APIs.
5. Reports nunca son source of truth; solo empaquetan.

### 3.22 Lenguaje ubicuo compartido vs local

Compartido (kernel):
- `org_id`, `project_id`, `version_id`, `scenario_id`
- unidades, moneda, confidence, provenance

Local por dominio:
- Perception: `mask`, `color_key`, `ocr_token`
- Costs: `amount`, `pricebook`, `tax`
- Chat: `thread`, `citation`, `memory_summary`

Traducción entre lenguajes ocurre en anti-corruption layers / DTOs de integración.

### 3.23 Dominios y planes comerciales

| Dominio | Free | Pro | Enterprise extras |
|---------|------|-----|-------------------|
| Perception | cola low | prioridad | VPC/gpu options conceptuales |
| Scenarios | limitado | full | policies merge |
| AI/Chat | cupos | altos | retention/audit legal |
| Marketplace | browse limitado | trade | contratos org |
| Plugins | core | marketplace plugins | private registry |
| Audit | básico | extendido | export legal hold |

---

## 4. Módulos (detalle por dominio)

Para cada dominio: responsabilidades, dependencias, API pública conceptual, eventos, servicios internos, casos de uso, datos, y anti-corruption (qué NUNCA debería conocer).

### 4.1 Módulo Identity

#### Responsabilidades
- Registro/login, sesiones, MFA opcional, API keys.
- Organizaciones y membresías.
- Roles base: `owner`, `admin`, `estimator`, `viewer`, `auditor`.
- Federación OIDC/SAML (Enterprise).
- Emisión de claims para Gateway.

#### Dependencias
- Billing (plan features).
- Notifications (verificación email).
- Audit (login privilegios).

#### API pública (conceptual)
- `POST /auth/login`, `POST /auth/logout`, `POST /auth/refresh`
- `GET/POST /orgs`, `GET/PATCH /orgs/{id}`
- `GET/POST /orgs/{id}/members`
- `POST /orgs/{id}/sso/config` (Enterprise)
- `POST /api-keys`, `DELETE /api-keys/{id}`

#### Eventos emitidos / consumidos
- Emite: `UsuarioRegistrado`, `UsuarioInvitado`, `MiembroRolCambiado`, `SSOConfigurado`
- Consume: `SuscripcionCambiada` (para claims de plan), `UsuarioEliminadoSolicitado`

#### Servicios internos
- Password/IdP broker, RoleService, SessionStore, ClaimComposer.

#### Casos de uso
- Invitar estimador a org.
- Cambiar rol a viewer.
- Emitir API key con scopes.

#### Datos que maneja
- Users, credentials refs, memberships, sso configs.

#### Qué NUNCA debería conocer
- Estructura MDO, precios, máscaras, prompts, contenidos de planos.

### 4.2 Módulo Projects

#### Responsabilidades
- Crear/archivar proyectos; código interno; moneda; sistema de unidades.
- Membership por proyecto; settings por defecto.
- Contadores hacia Billing (proyectos activos).

#### Dependencias
- Identity, Billing, Settings, Media (cuota), Audit.

#### API pública
- `GET/POST /projects`
- `GET/PATCH /projects/{id}`
- `POST /projects/{id}/archive`
- `GET/PUT /projects/{id}/members`
- `GET/PATCH /projects/{id}/settings`

#### Eventos
- Emite: `ProyectoCreado`, `ProyectoArchivado`, `ProyectoConfigurado`, `MiembroProyectoCambiado`
- Consume: `SuscripcionCambiada` (enforcement), `PluginInstalado` (enable defaults)

#### Servicios internos
- ProjectPolicy, QuotaGuard, SettingsMerger.

#### Casos de uso
- Alta de obra nueva en ARS.
- Archivar proyecto Free al exceder cupo.

#### Datos
- Project, ProjectSettings, ProjectMembership.

#### NUNCA conocer
- Detalle de polígonos, ejecución OCR, tokens LLM.

### 4.3 Módulo Vision / Perception

#### Responsabilidades
- Encolar y ejecutar pipelines de percepción.
- Producir evidencias tipadas y métricas de calidad.
- Mapear colores a candidatos de tipología (sin cerrar decisión).

#### Dependencias
- Media, Projects, Construction (para adjuntar evidencias), Billing quotas, Event bus.

#### API pública
- `POST /projects/{id}/perception/jobs`
- `GET /perception/jobs/{jobId}`
- `POST /perception/jobs/{jobId}/cancel`
- `GET /sheets/{sheetId}/evidences`
- `POST /sheets/{sheetId}/color-map` (user mapping)

#### Eventos
- Emite: `PlanoSubido` (si orquesta con Media), `PercepcionIniciada`, `PlanoProcesado`, `PercepcionFallida`, `EvidenciaCreada`, `ColorMapActualizado`
- Consume: `MediaAssetListo`, `CalibracionActualizada`, `ProyectoArchivado` (cancel jobs)

#### Servicios internos
- PipelineOrchestrator, OcrService, ColorSegmenter, SymbolAssist, EvidenceWriter, QualityScorer.

#### Casos de uso
- Procesar plano coloreado wedge.
- Reprocesar con nueva versión de pipeline.
- Marcar regiones de baja confianza.

#### Datos
- PerceptionJob, Evidence, ColorRegion, metrics.

#### NUNCA conocer
- Pricebooks, totales de presupuesto, prompts de chat, pedidos marketplace.

### 4.4 Módulo Geometry

#### Responsabilidades
- Calibración de escala; medición; validaciones geométricas; escritura de `ElementGeometry`.
- Generar medidas L/A/V/count confiables.

#### Dependencias
- Perception evidences, Media sheets, Construction elements, Scenarios (changesets).

#### API pública
- `POST /sheets/{id}/calibration`
- `POST /projects/{id}/geometry/recompute`
- `GET /elements/{id}/geometry`
- `POST /geometry/validate`

#### Eventos
- Emite: `CalibracionActualizada`, `GeometriaCalculada`, `ModeloActualizado` (vía MDO ops), `GeometriaInvalidaDetectada`
- Consume: `PlanoProcesado`, `ColorMapActualizado`, `ChangeSetConfirmado`

#### Servicios internos
- ScaleService, MeasureService, TopologyBuilder, GeometryValidator.

#### Casos de uso
- Calcular m2 de locales.
- Detectar polígonos abiertos.
- Recalcular tras ajuste de escala.

#### Datos
- geometry payloads refs, measures, validation issues.

#### NUNCA conocer
- Costos unitarios, proveedores, texto de chat, billing.

### 4.5 Módulo Construction (MDO Core)

#### Responsabilidades
- CRUD tipado de espacios/sistemas/elementos.
- Mantener grafo y proyecciones.
- Exponer query patterns (§2.7).
- Aplicar ChangeOps commitados.

#### Dependencias
- Projects, Scenarios, Plugins (typology registry), Geometry/Materials as writers controlados.

#### API pública
- `GET /versions/{id}/spaces`
- `GET /versions/{id}/systems/{sysId}/elements`
- `POST /scenarios/{id}/elements` (draft ops)
- `GET /versions/{id}/graph`
- `GET /versions/{id}/takeoff` (proyección; puede vivir en Materials read)
- `GET /entities/{type}/{id}?version=`

#### Eventos
- Emite: `ModeloActualizado`, `ElementoCreado`, `ElementoTipificado`, `EspacioActualizado`, `ProyeccionInvalidada`
- Consume: `ChangeSetMerged`, `GeometriaCalculada`, `MaterialCalculado` (para enlaces), `PluginDesinstalado`

#### Servicios internos
- GraphService, ProjectionBuilder, EntityResolver, LineageService.

#### Casos de uso
- Explorar árbol de espacios.
- Resolver citas IA a entidades.
- Bloquear entidades certificadas.

#### Datos
- Site…Element, connections, projection tables.

#### NUNCA conocer
- Implementación CV, providers de LLM, HTML de emails, tarjetas de crédito.

### 4.6 Módulo Materials

#### Responsabilidades
- Catálogo tipológico core + hook plugins.
- Evaluación de fórmulas → TakeoffLine.
- Factores de desperdicio y overrides manuales auditados.

#### Dependencias
- Construction measures, Plugins, Scenarios versions.

#### API pública
- `GET /typologies`
- `POST /versions/{id}/materials/recompute`
- `GET /versions/{id}/takeoff-lines`
- `POST /takeoff-lines/{id}/override`
- `GET /formulas/{id}`

#### Eventos
- Emite: `MaterialCalculado`, `TakeoffOverrideAplicado`, `FormulaVersionPublicada`
- Consume: `ModeloActualizado`, `PluginInstalado`, `EscenarioCreado` (lazy compute), `TipologiaMapeada`

#### Servicios internos
- FormulaEngine, TakeoffAggregator, OverrideService, TypologyRegistry.

#### Casos de uso
- Calcular montantes steel frame.
- Override manual de cantidad con razón.
- Recompute selectivo por sistema.

#### Datos
- Formula, TakeoffLine, WasteFactor, typology metadata.

#### NUNCA conocer
- Segmentación de color raw, SSO, pasarelas de pago, embeddings.

### 4.7 Módulo Costs

#### Responsabilidades
- Pricebooks regionales/org.
- Presupuestos y firmas.
- Ajustes, impuestos simples, moneda.

#### Dependencias
- Materials takeoff, Marketplace (opcional precios), Billing (features), Scenarios.

#### API pública
- `GET/POST /pricebooks`
- `POST /versions/{id}/budgets/recompute`
- `GET /budgets/{id}`
- `POST /budgets/{id}/sign`
- `GET /budgets/{id}/export` (job)

#### Eventos
- Emite: `CostoActualizado`, `PresupuestoCreado`, `PresupuestoFirmado`, `PricebookActualizado`
- Consume: `MaterialCalculado`, `ProveedorSeleccionado` (precio), `CurrencyRatesActualizadas`

#### Servicios internos
- PricingEngine, BudgetAssembler, SignatureService, TaxSimpleRules.

#### Casos de uso
- Valorizar takeoff en ARS.
- Firmar presupuesto (inmutable snapshot).
- Comparar costo entre escenarios.

#### Datos
- Pricebook, Budget*, SignedBudget, rates.

#### NUNCA conocer
- Máscaras, OCR tokens, implementación de plugins UI, transcripts completos salvo refs.

### 4.8 Módulo Scenarios

#### Responsabilidades
- Branches, changesets, merge, compare, promote, soft delete.
- Clasificar conflictos.

#### Dependencias
- Construction/Materials/Costs versioned model, Identity roles.

#### API pública
- `GET/POST /projects/{id}/scenarios`
- `POST /scenarios/{id}/changesets`
- `POST /scenarios/{id}/merge`
- `POST /scenarios/{id}/promote`
- `GET /compare?left=&right=`
- `DELETE /scenarios/{id}` (soft)

#### Eventos
- Emite: `EscenarioCreado`, `ChangeSetCreado`, `ChangeSetConfirmado`, `EscenarioMerged`, `EscenarioPromovido`, `ConflictoDetectado`
- Consume: `ModeloActualizado` (en branch), `CertificacionEmitida` (locks)

#### Servicios internos
- BranchService, MergeEngine, ConflictClassifier, DiffService.

#### Casos de uso
- Branch “alternativa hormigón”.
- Merge a baseline con conflictos de costo.
- Promote para licitación.

#### Datos
- Scenario, ChangeSet, ChangeOp, conflict records.

#### NUNCA conocer
- Marketplace orders, email templates, GPU scheduling details.

### 4.9 Módulo Timeline

#### Responsabilidades
- Hitos; secuencias; vínculos a sistemas.
- Vista temporal no autoritaria de costos/certificaciones.

#### Dependencias
- Construction, Reports/Certifications (fechas), Projects.

#### API pública
- `GET/POST /projects/{id}/milestones`
- `GET/PUT /projects/{id}/work-sequence`
- `GET /projects/{id}/timeline`

#### Eventos
- Emite: `HitoCreado`, `SecuenciaActualizada`
- Consume: `CertificacionEmitida`, `EscenarioPromovido`

#### Servicios internos
- TimelineProjector, MilestoneService.

#### Casos de uso
- Definir orden de gremios.
- Marcar hito “estructura terminada”.

#### Datos
- Milestone, WorkSequence.

#### NUNCA conocer
- Fórmulas internas, blobs geométricos crudos, billing cards.

### 4.10 Módulo Reports

#### Responsabilidades
- Plantillas; render PDF/Excel; certificaciones; empaquetado scenario packs.

#### Dependencias
- MDO/Costs reads, Media storage, Audit, Identity permissions.

#### API pública
- `POST /reports/jobs`
- `GET /reports/jobs/{id}`
- `GET /report-templates`
- `POST /certifications`
- `GET /certifications/{id}`

#### Eventos
- Emite: `ReporteSolicitado`, `ReporteGenerado`, `CertificacionEmitida`, `ReporteFallido`
- Consume: `PresupuestoFirmado`, `EscenarioPromovido`, `CostoActualizado` (si scheduled)

#### Servicios internos
- TemplateRenderer, PdfEngine, ExcelEngine, CertificationPackager, SnapshotFreezer.

#### Casos de uso
- Export Excel takeoff.
- Emitir certificación de período.
- Pack de escenario para cliente.

#### Datos
- templates, report artifacts refs, certification hashes.

#### NUNCA conocer
- Entrenamiento ML, color segmentation internals, plugin sandboxes code.

### 4.11 Módulo AI

#### Responsabilidades
- Orquestación, tool routing, retrieval, citation/policy guards, eval, embeddings index.
- Proposals draft.

#### Dependencias
- MDO read APIs, Chat, Billing quotas, Audit, Search/Embeddings store.

#### API pública
- `POST /ai/completions` (interno/Chat)
- `POST /ai/proposals`
- `POST /ai/proposals/{id}/accept|reject`
- `GET /ai/evals/summary` (interno)
- `POST /ai/index/rebuild` (admin job)

#### Eventos
- Emite: `AIProposalCreada`, `AIProposalResuelta`, `EmbeddingsActualizados`, `AIQuotaExcedida`
- Consume: `ModeloActualizado`, `MaterialCalculado`, `CostoActualizado` (reindex), `SuscripcionCambiada`

#### Servicios internos
- Orchestrator, ToolRouter, Retriever, CitationGuard, PolicyGuard, EvalService, EmbeddingIndexer.

#### Casos de uso
- Responder con citas sobre takeoff.
- Proponer tipología alternativa (draft).
- Evaluar tasa de alucinación offline.

#### Datos
- proposals, traces, eval sets, embedding refs.

#### NUNCA conocer
- Escritura directa DB geometría, secretos de pago, bypass de AuthZ.

### 4.12 Módulo Chat

#### Responsabilidades
- Threads, streaming UX, context assembly, memorias, permisos.
- Auditoría de respuestas usadas en docs comerciales.

#### Dependencias
- AI, Identity, Projects, Audit, Notifications (opcional).

#### API pública
- `GET/POST /projects/{id}/chats`
- `GET /chats/{id}/messages`
- WSS `/ws/chat/{threadId}`
- `POST /messages/{id}/mark-used-in-doc`

#### Eventos
- Emite: `ChatIniciado`, `MensajeChatRegistrado`, `ChatRespuestaUsadaEnDoc`
- Consume: `AIQuotaExcedida`, `MiembroProyectoCambiado`

#### Servicios internos
- ContextAssembler, MemorySummarizer, StreamHub, PermissionFilter.

#### Casos de uso
- Preguntar cantidades por espacio.
- Mantener resumen de decisiones del proyecto.
- Marcar respuesta citada en presupuesto.

#### Datos
- threads, messages, memory summaries.

#### NUNCA conocer
- Algoritmos CV, estructura interna pricebook provider sync, DLQ internals.

### 4.13 Módulo Marketplace

#### Responsabilidades
- Onboarding proveedores; catálogo SKU; cotizaciones; órdenes.
- Sync periódica de precios opcional hacia pricebooks.

#### Dependencias
- Identity/org, Costs (link), Notifications, Billing (features).

#### API pública
- `GET /marketplace/providers`
- `GET /marketplace/skus`
- `POST /quotes`
- `POST /orders`
- `POST /orders/{id}/cancel`

#### Eventos
- Emite: `ProveedorSeleccionado`, `CotizacionCreada`, `CompraRealizada`, `OrdenCancelada`, `CatalogoProveedorSincronizado`
- Consume: `CostoActualizado` (sugerencias), `ProyectoArchivado`

#### Servicios internos
- CatalogService, QuoteEngine, OrderService, ProviderSyncWorker.

#### Casos de uso
- Elegir proveedor para ítem acero.
- Registrar compra.
- Sync pricebook regional.

#### Datos
- providers, skus, quotes, orders.

#### NUNCA conocer
- ElementGeometry payloads, perception masks, scenario merge internals.

### 4.14 Módulo Billing

#### Responsabilidades
- Planes Free/Pro/Enterprise; suscripciones; usage meters; enforcement hooks.
- Integración pasarela; invoices refs.

#### Dependencias
- Identity, Payment provider, Audit, Notifications.

#### API pública
- `GET /billing/plan`
- `POST /billing/upgrade`
- `GET /billing/usage`
- `GET /billing/invoices`
- Webhooks provider: `POST /billing/webhooks`

#### Eventos
- Emite: `SuscripcionCambiada`, `UsoRegistrado`, `QuotaUmbralAlcanzado`, `PagoFallido`
- Consume: meters desde Perception/AI/Reports/Media (`UsoConsumido`)

#### Servicios internos
- EntitlementService, MeterService, WebhookVerifier, PlanCatalog.

#### Casos de uso
- Upgrade a Pro.
- Bloquear job si cuota Free agotada.
- Reportar uso mensualmente.

#### Datos
- subscription, meters, plan catalog.

#### NUNCA conocer
- Contenido de planos, mensajes de chat, fórmulas, merge conflicts.

### 4.15 Módulo Notifications

#### Responsabilidades
- Preferencias; routing email/in-app/webhook; reintentos delivery.

#### Dependencias
- Identity, Event bus, Templates.

#### API pública
- `GET/PATCH /users/me/notification-preferences`
- `GET /notifications`
- `POST /notifications/{id}/read`
- `POST /orgs/{id}/webhooks` (Enterprise)

#### Eventos
- Emite: `NotificacionEnviada`, `NotificacionFallida`
- Consume: muchos (`PlanoProcesado`, `CostoActualizado`, `CompraRealizada`, `CertificacionEmitida`, `QuotaUmbralAlcanzado`, …)

#### Servicios internos
- Router, TemplateRenderer, EmailSender, WebhookDispatcher, DigestBatcher.

#### Casos de uso
- Avisar fin de procesamiento de plano.
- Digest diario Pro/Enterprise.

#### Datos
- preferences, notification records, delivery attempts.

#### NUNCA conocer
- Cómo se calcula un m2, embeddings, price formulas.

### 4.16 Módulo Media

#### Responsabilidades
- Upload, checksum, derivados, thumbnails, signed URLs, retención.

#### Dependencias
- Projects, Billing quotas, Storage, Perception (consumer), Audit.

#### API pública
- `POST /projects/{id}/media` (init/complete)
- `GET /media/{id}`
- `GET /media/{id}/url`
- `POST /media/{id}/derivatives`
- `DELETE /media/{id}` (soft/policy)

#### Eventos
- Emite: `PlanoSubido`, `MediaAssetListo`, `DerivadoGenerado`, `MediaRetencionAplicada`
- Consume: `ProyectoArchivado`, `PoliticaRetencionCambiada`

#### Servicios internos
- UploadSession, VirusScanHook, DerivativeWorker, SignedUrlService.

#### Casos de uso
- Subir PDF multipágina.
- Generar thumbnail página 1.
- Purgar según retención org.

#### Datos
- MediaAsset, Derivative metadata.

#### NUNCA conocer
- Takeoff math, chat memory, SSO assertions detail beyond actor id.

### 4.17 Módulo Settings

#### Responsabilidades
- Defaults de tipologías, unidades UI, locale, flags de features no-billing.
- Herencia org → project → user.

#### Dependencias
- Identity, Projects, Plugins (defaults).

#### API pública
- `GET/PATCH /orgs/{id}/settings`
- `GET/PATCH /projects/{id}/settings`
- `GET/PATCH /users/me/settings`

#### Eventos
- Emite: `SettingsActualizados`
- Consume: `PluginInstalado`, `SuscripcionCambiada`

#### Servicios internos
- SettingsResolver (layered merge), SchemaValidator.

#### Casos de uso
- Default color map por org.
- Locale es-AR.

#### Datos
- nested settings documents tipados.

#### NUNCA conocer
- Jobs GPU, bus partitions, budget signatures internals.

### 4.18 Módulo Audit

#### Responsabilidades
- Append-only log; consultas de cumplimiento; legal hold flags.
- Capturar usos de IA en docs comerciales.

#### Dependencias
- Identity (actor resolution); storage inmutable.

#### API pública
- `GET /orgs/{id}/audit` (filtrable)
- `GET /projects/{id}/audit`
- `POST /audit/legal-hold` (Enterprise)

#### Eventos
- Emite: `AuditExportSolicitado` (meta)
- Consume: practically all sensitive domain events + command audits

#### Servicios internos
- AuditWriter, QueryService, HashChain (conceptual), ExportJob.

#### Casos de uso
- ¿Quién firmó presupuesto?
- ¿Qué respuesta IA se insertó en certificación?

#### Datos
- AuditEvent immutable.

#### NUNCA conocer
- Cómo recompute materials; no re-ejecuta lógica.

### 4.19 Módulo Plugins / Registry

#### Responsabilidades
- Registry de manifests; instalación; versionado; capability grants; sandbox host.
- Validar contratos antes de enable.

#### Dependencias
- Billing entitlements, Identity admin, Materials/Geometry/UI hosts.

#### API pública
- `GET /plugins/registry`
- `POST /orgs/{id}/plugins/install`
- `POST /orgs/{id}/plugins/{id}/upgrade`
- `DELETE /orgs/{id}/plugins/{id}` (disable)
- `GET /plugins/{id}/manifest`

#### Eventos
- Emite: `PluginInstalado`, `PluginActualizado`, `PluginDeshabilitado`, `PluginValidacionFallida`
- Consume: `SuscripcionCambiada`, `FormulaVersionPublicada` (si plugin)

#### Servicios internos
- ManifestValidator, SandboxRunner, CapabilityBroker, CompatibilityMatrix.

#### Casos de uso
- Instalar Steel Frame.
- Upgrade plugin Gas con migración tipologías.
- Rechazar manifest incompatible.

#### Datos
- manifests, installations, grants.

#### NUNCA conocer
- Contenido completo de todos los proyectos; opera por callbacks/contracts.

### 4.20 Tabla resumen API × dominio

| Dominio | Prefijo conceptual | Sync | Async |
|---------|--------------------|------|-------|
| Identity | `/auth`, `/orgs` | sí | pocos eventos |
| Projects | `/projects` | sí | sí |
| Perception | `/perception` | status | jobs |
| Geometry | `/geometry` | parcial | recompute |
| Construction | `/versions`, `/entities` | sí | proyecciones |
| Materials | `/takeoff`, `/typologies` | sí | recompute |
| Costs | `/budgets`, `/pricebooks` | sí | recompute |
| Scenarios | `/scenarios` | sí | merge jobs complejos |
| Timeline | `/timeline` | sí | proyecciones |
| Reports | `/reports`, `/certifications` | status | jobs |
| AI | `/ai` | sí | reindex |
| Chat | `/chats` + WSS | mixto | — |
| Marketplace | `/marketplace` | sí | sync |
| Billing | `/billing` | sí | webhooks |
| Notifications | `/notifications` | sí | delivery |
| Media | `/media` | sí | derivatives |
| Settings | `/settings` | sí | — |
| Audit | `/audit` | sí | export jobs |
| Plugins | `/plugins` | sí | validation |

### 4.21 Orquestación entre módulos (ejemplo extremo a extremo)

1. Media emite `PlanoSubido`.
2. Perception consume y emite `PlanoProcesado`.
3. Geometry consume y escribe medidas; Construction emite `ModeloActualizado`.
4. Materials recompute → `MaterialCalculado`.
5. Costs recompute → `CostoActualizado`.
6. Notifications avisa usuario; AI Indexer refresca chunks; Search actualiza.
7. Usuario abre Chat y pregunta; AI cita takeoff lines.
8. Usuario crea Escenario alternativo; merge; Reports certifica.

Cada paso respeta ownership: ningún módulo “se mete” en el store del otro sin API/evento.

### 4.22 Contratos de error entre módulos

Errores tipados conceptuales:
- `QuotaExceeded`
- `ConflictMerge`
- `CalibrationRequired`
- `EntityLockedByCertification`
- `PluginIncompatible`
- `CitationMissing` (AI)
- `StalePricebook`
- `UnauthorizedTenant`

El Gateway normaliza; los módulos no retornan stack traces al cliente.

---

## 5. Eventos

### 5.1 Filosofía event-driven

ARQ-IA 3.0 crece por **nuevos consumidores**, no por reescritura de productores. El MDO y los motores emiten hechos de dominio; reportes, search, IA, notificaciones y marketplace reaccionan.

Beneficios:
- Desacoplar Perception de Costs.
- Insertar Plugins que escuchen `ModeloActualizado`.
- Escalar workers por tipo de evento.
- Auditar causalidad (`causation_id` / `correlation_id`).

### 5.2 Tipos de bus / eventos

| Tipo | Alcance | Ejemplo | Garantía típica |
|------|---------|---------|-----------------|
| Domain Event | Dentro del modelo de un contexto / MDO | `ElementoTipificado` | Productor confiable + outbox |
| Integration Event | Entre bounded contexts | `PlanoProcesado` | Contrato versionado estable |
| Signal / UI Event | WS a clientes | `job.progress` | Best-effort |
| System Event | Plataforma | `QuotaUmbralAlcanzado` | Operaciones |

No mezclar señales UI con contratos de integración duraderos.

### 5.3 Naming

Convención:
```
<EntidadPasadoPerfecto>  o  <EntidadAccion>
```
Ejemplos correctos: `PlanoSubido`, `MaterialCalculado`, `EscenarioMerged`.
Evitar: `DoRecompute`, `UpdateEverything`, nombres de tablas.

Namespace conceptual:
```
arqia.{domain}.{event_name}.v1
```

### 5.4 Envelope estándar

| Campo | Descripción |
|-------|-------------|
| `event_id` | UUID único (idempotencia) |
| `event_type` | nombre versionado |
| `occurred_at` | timestamp UTC |
| `org_id` | tenant |
| `project_id` | si aplica |
| `version_id` / `scenario_id` | si aplica |
| `actor` | user/service |
| `correlation_id` | request/job originario |
| `causation_id` | event padre |
| `payload` | datos mínimos + refs |
| `schema_version` | int |

Payloads llevan **referencias**, no blobs enormes.

### 5.5 Idempotencia

- Consumers persisten `event_id` procesados (dedupe store).
- Handlers son “at-least-once safe”.
- Recomputos usan claves idempotentes (`version_id` + `engine_version`).
- Mutaciones REST de entrada usan `Idempotency-Key` y pueden generar el mismo `event_id` lógico.

### 5.6 Ordering

- Orden total global: **no** garantizado.
- Orden por clave de partición: `org_id` o `project_id` para causalidad local.
- Consumers que necesiten secuencias usan `version_id` monotónico / check de `head`.
- Merges y certificaciones actúan como barreras de ordenamiento de negocio.

### 5.7 Outbox pattern (conceptual)

```
[Domain Service TX]
   |
   |-- write OLTP state
   |-- write Outbox row (same TX)
   v
[Outbox Publisher] --> Event Bus --> Consumers
   |
   v
 mark published
```

Reglas:
- Nunca publicar al bus antes del commit.
- Publisher con polling/CDC según infra.
- Retención outbox con archive.

### 5.8 Catálogo de eventos (ampliado)

#### Medios y percepción
| Evento | Payload clave | Emisor |
|--------|---------------|--------|
| `PlanoSubido` | asset_id, pages, checksum | Media |
| `MediaAssetListo` | asset_id | Media |
| `DerivadoGenerado` | derivative_id, kind | Media |
| `PercepcionIniciada` | job_id, pipeline_version | Perception |
| `PlanoProcesado` | job_id, sheet_ids, evidence_counts | Perception |
| `PercepcionFallida` | job_id, error_code | Perception |
| `EvidenciaCreada` | evidence_id, sheet_id | Perception |
| `ColorMapActualizado` | sheet_id, mapping | Perception/UI |
| `CalibracionActualizada` | sheet_id, scale_ratio | Geometry |

#### Modelo y geometría
| Evento | Payload clave | Emisor |
|--------|---------------|--------|
| `GeometriaCalculada` | sheet_id/element_ids | Geometry |
| `GeometriaInvalidaDetectada` | issues[] | Geometry |
| `ModeloActualizado` | version_id, change_summary | Construction |
| `ElementoCreado` | element_id, typology | Construction |
| `ElementoTipificado` | element_id, typology | Construction |
| `EspacioActualizado` | space_id | Construction |
| `ProyeccionInvalidada` | projection_keys[] | Construction |

#### Materiales y costos
| Evento | Payload clave | Emisor |
|--------|---------------|--------|
| `MaterialCalculado` | version_id, takeoff_stats | Materials |
| `TakeoffOverrideAplicado` | line_id, reason | Materials |
| `FormulaVersionPublicada` | formula_id, ver | Materials/Plugins |
| `TipologiaMapeada` | color_key→typology | Materials/UI |
| `CostoActualizado` | budget_id/version_id, totals | Costs |
| `PresupuestoCreado` | budget_id | Costs |
| `PresupuestoFirmado` | signed_id, hash | Costs |
| `PricebookActualizado` | pricebook_id | Costs |
| `CurrencyRatesActualizadas` | as_of | Costs |

#### Escenarios y timeline
| Evento | Payload clave | Emisor |
|--------|---------------|--------|
| `EscenarioCreado` | scenario_id, from_version | Scenarios |
| `ChangeSetCreado` | changeset_id | Scenarios |
| `ChangeSetConfirmado` | result_version_id | Scenarios |
| `ConflictoDetectado` | conflict_types[] | Scenarios |
| `EscenarioMerged` | scenario_id, into | Scenarios |
| `EscenarioPromovido` | version_id baseline | Scenarios |
| `EscenarioEliminado` | soft delete | Scenarios |
| `HitoCreado` | milestone_id | Timeline |
| `SecuenciaActualizada` | sequence_id | Timeline |

#### Marketplace y comercial
| Evento | Payload clave | Emisor |
|--------|---------------|--------|
| `ProveedorSeleccionado` | provider_id, line_refs | Marketplace |
| `CotizacionCreada` | quote_id | Marketplace |
| `CompraRealizada` | order_id, amounts | Marketplace |
| `OrdenCancelada` | order_id | Marketplace |
| `CatalogoProveedorSincronizado` | provider_id | Marketplace |

#### Reportes y certificaciones
| Evento | Payload clave | Emisor |
|--------|---------------|--------|
| `ReporteSolicitado` | report_job_id | Reports |
| `ReporteGenerado` | artifact_ref | Reports |
| `ReporteFallido` | error_code | Reports |
| `CertificacionEmitida` | certification_id, hash | Reports |

#### IA, chat, plugins, billing, notify
| Evento | Payload clave | Emisor |
|--------|---------------|--------|
| `AIProposalCreada` | proposal_id | AI |
| `AIProposalResuelta` | status | AI |
| `EmbeddingsActualizados` | project_id, ver | AI |
| `AIQuotaExcedida` | org_id | AI/Billing |
| `ChatIniciado` | thread_id | Chat |
| `MensajeChatRegistrado` | message_id | Chat |
| `ChatRespuestaUsadaEnDoc` | message_id, doc_ref | Chat |
| `PluginInstalado` | plugin_id, ver | Plugins |
| `PluginActualizado` | plugin_id | Plugins |
| `PluginDeshabilitado` | plugin_id | Plugins |
| `PluginValidacionFallida` | reasons | Plugins |
| `SuscripcionCambiada` | plan | Billing |
| `UsoRegistrado` | meter, amount | Billing |
| `UsoConsumido` | meter, amount | Workers→Billing |
| `QuotaUmbralAlcanzado` | meter, pct | Billing |
| `PagoFallido` | invoice_ref | Billing |
| `NotificacionEnviada` | channel | Notifications |
| `NotificacionFallida` | channel | Notifications |
| `UsuarioRegistrado` | user_id | Identity |
| `UsuarioInvitado` | email | Identity |
| `MiembroRolCambiado` | member_id | Identity |
| `ProyectoCreado` | project_id | Projects |
| `ProyectoArchivado` | project_id | Projects |
| `SettingsActualizados` | scope | Settings |
| `MediaRetencionAplicada` | counts | Media |
| `PoliticaRetencionCambiada` | org_id | Settings/Enterprise |

### 5.9 Diagrama: upload → perception → geometry → materials → costs → notify

```
[Studio] POST media
    | 200 upload accepted
    v
(Media) PlanoSubido ----+
                        v
              [Perception Worker]
                        |
                        +--> job.progress (WS)
                        v
                 PlanoProcesado
                        |
          +-------------+-------------+
          v                           v
   [Geometry Worker]            [Search preview]
          |
          v
   GeometriaCalculada / ModeloActualizado
          |
          v
   [Materials Worker] --> MaterialCalculado
          |
          v
   [Costs Worker] --> CostoActualizado
          |
          +--> [Notifications] email/in-app
          +--> [AI Indexer] EmbeddingsActualizados
          +--> [WS Hub] project refresh
```

### 5.10 Diagrama: scenario branch

```
Baseline version V1
        |
        | EscenarioCreado (branch "alt-steel")
        v
   Working Scenario head=V1
        |
        | user edits + engines recompute on branch
        | ChangeSetConfirmado -> V2'
        v
   Compare(V1, V2') --> diff takeoff/cost
        |
        | merge request
        v
   ConflictClassifier
     - geometry conflict?
     - materials conflict?
     - costs conflict?
        |
        +-- resolve --> EscenarioMerged --> new Version V3
        +-- promote --> EscenarioPromovido (baseline=V3)
```

### 5.11 Diagrama: certification

```
Budget/Takeoff on Version Vn (locked candidates)
        |
        v
POST /certifications --> ReporteSolicitado
        |
        v
SnapshotFreezer copies MDO+Costs+hashes --> object storage
        |
        v
CertificacionEmitida
        |
        +--> Audit append
        +--> lock entities flags
        +--> Notifications stakeholders
        +--> Timeline milestone optional
```

### 5.12 Semántica de entrega

| Aspecto | Política |
|---------|----------|
| Entrega | At-least-once |
| Dedupe | Por `event_id` |
| Reintentos | Exponenciales con jitter |
| DLQ | Tras N fallos + alerta |
| Poison messages | Aislar sin bloquear partición |
| Backpressure | Limitar prefetch workers |

### 5.13 Versionado de esquemas de eventos

- Campos nuevos opcionales: compatible.
- Cambios breaking: `*.v2` nuevo tipo; consumers dual-read temporal.
- Documentar en catálogo; pruebas de contrato en CI.

### 5.14 Event Storming mínimo por capability

Capacidades y eventos pivote:
1. Ingestión planos → `PlanoSubido`/`PlanoProcesado`
2. Twin build → `ModeloActualizado`
3. Takeoff → `MaterialCalculado`
4. Pricing → `CostoActualizado`
5. Alternativas → `EscenarioCreado`/`EscenarioMerged`
6. Cierre comercial → `PresupuestoFirmado`/`CertificacionEmitida`
7. Extensión → `PluginInstalado`
8. Asistencia → `AIProposalCreada`/`ChatRespuestaUsadaEnDoc`

---

## 6. Base de datos

> Arquitectura lógica — **sin SQL DDL**.

### 6.1 Stores lógicos

| Store | Rol | Ejemplos de contenido |
|-------|-----|----------------------|
| OLTP relacional | Identidad, grafo MDO, costos, memberships | Project, Element, Budget |
| Document/JSON | Snapshots geométricos, param sets grandes, evidence packs | ElementGeometry payload |
| Object storage | Binarios | planos, masks, PDFs, embeddings files |
| Cache | Sesiones, proyecciones calientes, rate limit | takeoff agg short-TTL |
| Search index | Texto + facets + chunks RAG | spaces names, notes, report text |
| Event outbox / event store | Publicación confiable (+ opcional historial) | outbox rows |
| Analytics warehouse (fase posterior) | BI, funnel, costos infra | eventos ETL |

### 6.2 Principios de modelado

1. Cada dominio tiene ownership lógico de tablas/colecciones.
2. Cross-domain solo por IDs + APIs/eventos — no joins libres eternamente sin boundary.
3. `org_id` en toda fila tenant-owned.
4. Versiones inmutables; heads mutables apuntan a versiones.
5. Soft-delete flags + retención; hard-delete excepcional y policy-driven.

### 6.3 Colecciones/tablas lógicas por dominio

#### Identity
- `users`, `organizations`, `memberships`, `roles`, `sessions`, `api_keys`, `sso_configs`

#### Projects / Settings
- `projects`, `project_members`, `project_settings`, `org_settings`, `user_settings`

#### Media
- `media_assets`, `media_derivatives`, `upload_sessions`

#### Perception
- `perception_jobs`, `evidences`, `color_regions`, `pipeline_runs`

#### Geometry / Construction MDO
- `sites`, `buildings`, `levels`, `spaces`, `zones`
- `systems`, `elements`, `connections`, `assemblies`
- `element_geometry_docs` (document)
- `project_versions`, `entity_version_index`

#### Materials
- `typologies`, `formulas`, `takeoff_lines`, `waste_factors`, `takeoff_overrides`

#### Costs
- `pricebooks`, `price_items`, `budgets`, `budget_lines`, `signed_budgets`, `currency_rates`

#### Scenarios
- `scenarios`, `changesets`, `change_ops`, `merge_conflicts`, `scenario_compares`

#### Timeline
- `milestones`, `work_sequences`

#### Reports
- `report_templates`, `report_jobs`, `certifications`, `report_artifacts`

#### AI / Chat
- `ai_proposals`, `ai_tool_traces`, `embedding_index_meta`, `eval_runs`
- `chat_threads`, `chat_messages`, `chat_memory_summaries`

#### Marketplace
- `providers`, `skus`, `quotes`, `orders`, `order_items`

#### Billing
- `plans`, `subscriptions`, `usage_meters`, `usage_events`, `invoices_ref`

#### Notifications
- `notification_preferences`, `notifications`, `delivery_attempts`, `org_webhooks`

#### Audit / Plugins
- `audit_events`, `legal_holds`
- `plugin_manifests`, `plugin_installations`, `capability_grants`

#### Platform
- `outbox_events`, `processed_events`, `jobs`, `job_attempts`, `feature_flags`

### 6.4 Estrategia de índices (conceptual)

| Patrón de query | Índice conceptual |
|-----------------|-------------------|
| Listar proyectos por org | `(org_id, status, updated_at)` |
| Elementos por version+system | `(version_id, system_id)` |
| Takeoff por version+material | `(version_id, material_code)` |
| Evidencias por sheet | `(sheet_id, kind)` |
| Jobs por proyecto/estado | `(project_id, status, created_at)` |
| Audit por org/tiempo | `(org_id, occurred_at)` |
| Mensajes chat por thread | `(thread_id, created_at)` |
| Dedupe eventos | `(consumer, event_id)` UNIQUE |
| Idempotency API | `(org_id, idempotency_key)` |

Evitar índices “por si acaso” en JSON gigante; indexar campos extraídos.

### 6.5 Qué es histórico / inmutable

Inmutable al cerrar/emitir:
- `ProjectVersion` cerrada
- `ChangeSet` confirmado
- `SignedBudget`
- `Certification`
- `AuditEvent`
- `usage_events` de billing (para disputa)
- Report artifacts hasheados
- Chat messages marcados `used_in_commercial_doc` (contenido preservado)

Mutables:
- Heads de scenario
- Draft changesets
- Settings
- Pricebooks vigentes (pero con historial de versiones de precio recomendado)

### 6.6 Qué es cacheable

| Dato | TTL / invalidación |
|------|--------------------|
| Proyección takeoff agg | invalidar por `MaterialCalculado` |
| Budget summary | invalidar por `CostoActualizado` |
| Typology catalog | TTL largo + event plugin |
| Signed URLs | TTL corto |
| Session entitlements | TTL corto / push revoke |
| Search | eventual |
| Embeddings | rebuild event-driven |

No cachear permissions sin invalidación de membresía.

### 6.7 Qué NUNCA hard-delete

1. Audit events  
2. Usage/billing events  
3. Certifications y sus snapshots  
4. Signed budgets  
5. ChangeSets que soportan lineage de certificaciones  
6. Mensajes chat usados en docs comerciales  
7. Evidence ligada a certificaciones (al menos soft + legal hold)  
8. Media originals referenciados por certificaciones  
9. Plugin installation history relevante a lineage tipológico  
10. Outbox published log (archive, no silently delete)

Hard-delete solo con policy de retención cumplida + doble control Enterprise.

### 6.8 Separación OLTP vs documentos

```
Element (OLTP)
  id, typology, system_id, space_id, measures_summary, version_id
    |
    +--> ElementGeometryDoc (Document)
           polygons, vertices, debug paths, engine_meta
```

Queries de negocio usan summary OLTP; editors cargan documentos bajo demanda.

### 6.9 Event store opcional

Fase temprana: outbox + logs bastan.  
Fase avanzada: event store para replay de proyecciones y auditoría temporal fina.  
No construir event sourcing total del MDO el día 1 salvo necesidad demostrada; el modelo ya es versionado por ChangeSets.

### 6.10 Warehouse analítico (después)

ETL desde:
- eventos de producto
- meters
- job metrics
- funnel Free→Pro

Prohibido que el warehouse se vuelva source of truth operacional.

### 6.11 Multi-tenant data patterns

- Row-level `org_id` obligatorio.
- Claves de shard futuras: `org_id`.
- Evitar secuencias globales expuestas por tenant.
- Jobs y bus partitions por `org_id` para ruido vecino.

### 6.12 Migraciones y compatibilidad

- Migraciones expand/contract.
- Proyecciones rebuildables desde versiones + eventos.
- Formula engine version pinning por `TakeoffLine`.

### 6.13 Backups lógicos

| Store | RPO/RTO conceptual |
|-------|--------------------|
| OLTP | RPO bajo (sync/async replica) |
| Object storage | versioning + replication |
| Search/Cache | rebuildable |
| Outbox | incluido en OLTP |

Certificaciones: backup verificado periódicamente (Enterprise).

---

## 7. API

### 7.1 Estilo general

- REST JSON como API primaria externa/interna.
- WSS para progreso, chat stream, presencia.
- Jobs API uniforme para procesos largos.
- Versionado URI: `/api/v1/...`

### 7.2 Mapa de recursos REST por dominio

#### Identity & orgs
- `/api/v1/auth/*`
- `/api/v1/orgs`
- `/api/v1/orgs/{orgId}/members`
- `/api/v1/orgs/{orgId}/roles`

#### Projects
- `/api/v1/projects`
- `/api/v1/projects/{projectId}`
- `/api/v1/projects/{projectId}/members`
- `/api/v1/projects/{projectId}/settings`

#### Media & perception
- `/api/v1/projects/{projectId}/media`
- `/api/v1/media/{mediaId}`
- `/api/v1/projects/{projectId}/perception/jobs`
- `/api/v1/sheets/{sheetId}/evidences`
- `/api/v1/sheets/{sheetId}/color-map`
- `/api/v1/sheets/{sheetId}/calibration`

#### MDO / geometry / materials / costs
- `/api/v1/projects/{projectId}/versions`
- `/api/v1/versions/{versionId}/spaces`
- `/api/v1/versions/{versionId}/systems`
- `/api/v1/versions/{versionId}/elements`
- `/api/v1/elements/{elementId}`
- `/api/v1/versions/{versionId}/takeoff`
- `/api/v1/versions/{versionId}/materials/recompute`
- `/api/v1/pricebooks`
- `/api/v1/versions/{versionId}/budgets`
- `/api/v1/budgets/{budgetId}/sign`

#### Scenarios / timeline
- `/api/v1/projects/{projectId}/scenarios`
- `/api/v1/scenarios/{scenarioId}/changesets`
- `/api/v1/scenarios/{scenarioId}/merge`
- `/api/v1/scenarios/{scenarioId}/promote`
- `/api/v1/compare`
- `/api/v1/projects/{projectId}/milestones`
- `/api/v1/projects/{projectId}/timeline`

#### Reports / certifications
- `/api/v1/report-templates`
- `/api/v1/reports/jobs`
- `/api/v1/certifications`

#### AI / chat
- `/api/v1/ai/proposals`
- `/api/v1/projects/{projectId}/chats`
- `/api/v1/chats/{chatId}/messages`

#### Marketplace / billing / notify / audit / plugins
- `/api/v1/marketplace/providers`
- `/api/v1/marketplace/skus`
- `/api/v1/quotes`
- `/api/v1/orders`
- `/api/v1/billing/plan`
- `/api/v1/billing/usage`
- `/api/v1/notifications`
- `/api/v1/orgs/{orgId}/audit`
- `/api/v1/plugins/registry`
- `/api/v1/orgs/{orgId}/plugins`

### 7.3 WebSockets

| Canal | Uso |
|-------|-----|
| `/ws/projects/{projectId}` | job progress, model refresh hints, presence |
| `/ws/chat/{threadId}` | token/chunk streaming, tool status |
| `/ws/org/{orgId}/admin` (opcional) | billing/quota alerts |

Mensajes tipados: `job.progress`, `job.completed`, `chat.chunk`, `chat.citation`, `presence.update`, `error`.

### 7.4 Cuándo REST vs WS vs Job

| Necesidad | Elección |
|-----------|----------|
| CRUD y queries | REST |
| Proceso > timeout HTTP cómodo | Job + WS progress |
| Stream token a token | WS |
| Fan-out server-side | Events (no WS bus) |
| Colaboración presencia | WS |

### 7.5 Background Jobs API

Recurso uniforme:
- `POST /api/v1/jobs` (o subrecursos domain-specific que crean job)
- `GET /api/v1/jobs/{jobId}`
- `POST /api/v1/jobs/{jobId}/cancel`
- `GET /api/v1/projects/{projectId}/jobs?status=`

Estados: `queued`, `running`, `cancel_requested`, `canceled`, `succeeded`, `failed`, `dead`.

Cada job expone: `type`, `progress_pct`, `steps[]`, `error`, `result_refs`.

### 7.6 Versionado API

- `/api/v1` estable para Studio y partners.
- Cambios breaking → `v2` en paralelo.
- Deprecation headers y ventana de migración.
- Contratos de eventos versionados aparte (§5.13).

### 7.7 AuthZ high level

Capas:
1. **AuthN** válida.
2. **Tenant**: org activa.
3. **Entitlement**: plan permite feature.
4. **RBAC**: rol org/proyecto.
5. **ABAC**: atributos (escenario locked, certification freeze, ownership).
6. **Resource scope**: project membership.

Ejemplos:
- `viewer` lee MDO; no merge.
- `estimator` recompute materials/costs; no billing.
- `admin` instala plugins org.
- AI tools ejecutan con permisos del usuario, no elevated.

### 7.8 Idempotency keys

- Header `Idempotency-Key` en POST mutantes (uploads, sign budget, create order, merge).
- Retención de resultados 24h+ .
- Replays devuelven mismo status/body.

### 7.9 Error model conceptual

```
{
  "error": {
    "code": "CalibrationRequired",
    "message": "human readable",
    "details": { "sheet_id": "..." },
    "correlation_id": "...",
    "retryable": false
  }
}
```

Códigos estables; `message` localizable; no filtrar datos cross-tenant en details.

HTTP mapping conceptual:
- 400 validation
- 401 authn
- 403 authz/entitlement
- 404 not found (sin leak)
- 409 conflict (merge, idempotency mismatch)
- 422 domain semantic
- 429 rate limit
- 503 dependency

### 7.10 Rate limits por plan

| Plan | API req/min (orden) | Uploads/día | AI req/día | Jobs concurrentes |
|------|---------------------|-------------|------------|-------------------|
| Free | bajo | bajo | bajo | 1 |
| Pro | medio-alto | medio | alto | N |
| Enterprise | alto / custom | custom | custom | N + priority lane |

Rutas sensibles (sign, export, perception) con buckets separados.

### 7.11 Paginación, filtrado, ETags

- Cursor pagination en listados grandes (elements, audit, messages).
- Filtros: `version_id`, `system`, `space`, `updated_since`.
- ETags en proyecciones takeoff/budget para cache condicional.

### 7.12 Public API (Pro/Enterprise)

Subconjunto estable:
- projects read
- takeoff read
- budgets read
- webhooks outbound
- jobs status

No exponer internals de perception masks ni tool traces crudos por defecto.

### 7.13 Compatibilidad Studio-BFF

BFF puede agregar:
- dashboard cards
- canvas bootstrap payload

Sin mover reglas de dominio al BFF.

---

## 8. Colas

### 8.1 Procesos background (catálogo)

| Proceso | Cola lógica | Prioridad base | Trigger |
|---------|-------------|----------------|---------|
| Plan processing (perception) | `perception` | alta (UX) | PlanoSubido |
| OCR page | `perception_ocr` | alta | pipeline |
| ML assist symbols | `perception_ml` | media | pipeline |
| Geometry recompute | `geometry` | alta | PlanoProcesado / calib |
| Materials recompute | `materials` | alta | ModeloActualizado |
| Costs recompute | `costs` | alta | MaterialCalculado |
| PDF generation | `reports_pdf` | media | user/cert |
| Excel export | `reports_xlsx` | media | user |
| Emails | `notify_email` | media | events |
| In-app notify fanout | `notify_inapp` | alta | events |
| Marketplace sync | `market_sync` | baja | schedule/event |
| Reports scheduled | `reports_sched` | baja | cron |
| AI embeddings refresh | `ai_embed` | media | Modelo/Material/Costo |
| Pricebook refresh | `price_refresh` | baja | schedule/providers |
| Derivative thumbnails | `media_deriv` | media | MediaAssetListo |
| Audit export | `audit_export` | baja | admin |
| Scenario merge heavy | `scenario_merge` | alta | user |
| Virus scan hook | `media_scan` | alta | upload |

### 8.2 Tipos de cola

| Tipo | Características | Uso |
|------|-----------------|-----|
| Work queue | competing consumers | perception, reports |
| Delayed / scheduled | ETA | digests, price refresh |
| Priority lanes | Free vs Pro vs Enterprise | fairness + SLA |
| Pub/sub topics | fan-out | integration events |
| DLQ | isolation | poison |

### 8.3 Prioridades y fairness multi-tenant

```
Enterprise > Pro > Free
```

pero con **fair scheduling** por `org_id` para evitar starvation (token bucket / weighted fair queue).

### 8.4 Retries y DLQ

- Reintentos: 5–10 con backoff exponencial + jitter (configurable por cola).
- Errores no retryable (`ValidationError`, `CalibrationRequired` persistente malformada) → fail fast.
- DLQ con replay manual tooling.
- Alertas en tasa DLQ > umbral.

### 8.5 SLO conceptual por cola

| Cola | Tiempo cola p95 (aprox) | Notas |
|------|-------------------------|-------|
| notify_inapp | segundos | |
| media_deriv | < 1 min | |
| perception (Pro) | minutos | depende tamaño |
| materials/costs | < pocos minutos post modelo | |
| reports_pdf | minutos | |
| ai_embed | eventual < decenas min | |
| market_sync | horario ok | |

### 8.6 Cancelación cooperativa

Jobs largos checkean `cancel_requested` entre steps.  
WS emite `job.canceled`.  
Side effects compensan si parcial (idempotente).

### 8.7 Poison & circuit breaking

Si dependency (storage/LLM/OCR) falla masivamente:
- circuit breaker en worker
- requeue delay
- degradación: AI offline mode; perception pause con mensaje UX

### 8.8 Observabilidad de colas

Métricas: depth, age of oldest, success rate, attempt count, per-org usage.  
Traza: `job_id` ↔ `correlation_id` ↔ `event_id`.

### 8.9 Relación colas ↔ eventos

No todo evento crea job; algunos consumers son livianos sync-in-process.  
Regla: si >100ms CPU o I/O externo inestable → job/cola.

---

## 9. Almacenamiento

### 9.1 Dónde vive cada artefacto

| Artefacto | Store | Path conceptual |
|-----------|-------|-----------------|
| Planos originals | Object | `org/{o}/project/{p}/media/originals/...` |
| Derivatives (tiles/normalized) | Object | `.../media/derived/...` |
| Thumbnails | Object + CDN | `.../media/thumbs/...` |
| Audit images / evidence overlays | Object | `.../perception/overlays/...` |
| Máscaras color | Object | `.../perception/masks/...` |
| PDFs reportes | Object | `.../reports/pdf/...` |
| Excel | Object | `.../reports/xlsx/...` |
| MDO geometry snapshots | Document + Object (si huge) | docs / `.../mdo/geom/...` |
| Scenario packs | Object | `.../scenarios/packs/...` |
| Certification snapshots | Object (WORM-ish) | `.../certs/...` |
| Signed budget snapshots | Object | `.../budgets/signed/...` |
| Chat transcripts | OLTP (+ archive object cold) | DB hot |
| Logs app | Log store | ops |
| Backups | Backup vault | ops |
| Embeddings | Vector index + object backup | `.../ai/embeddings/...` |
| Outbox archive | OLTP cold / object | ops |

### 9.2 Políticas de retención conceptuales

| Clase | Free | Pro | Enterprise |
|-------|------|-----|------------|
| Media originals | días/meses limitados | largo | custom + legal hold |
| Derivatives | regenerables; TTL | largo | custom |
| Chat | corto | medio | custom / export |
| Certifications | mínimo legal producto | largo | legal hold |
| Audit | medio | largo | largo + export |
| Embeddings | rebuildable | rebuildable | rebuildable |
| Logs ops | corto | corto/medio | SIEM export |

### 9.3 Principios de aislamiento tenant

1. Prefijos de storage por `org_id` (y `project_id`).
2. Signed URLs con scope mínimo y TTL corto.
3. Workers asumen credenciales que aún validan authZ de dominio antes de leer.
4. Prohibido bucket “global browsable”.
5. Encryption at rest (platform) + claves por tenant opcionales Enterprise.
6. Hardening: no filtrar listing cross-tenant en tools admin sin break-glass.

### 9.4 Ciclo de vida media

```
upload -> scan -> ready -> derive -> perceive -> (optional) cold storage -> retention purge
```

Si referenciada por certificación: **retention lock**.

### 9.5 CDN y hot paths

- Thumbnails y tiles de planos via CDN.
- APIs JSON no cachear en CDN salvo públicos.
- Invalidación puntual tras nuevo derivado.

### 9.6 Estimación de drivers de volumen

1. Planos alta resolución y máscaras.  
2. Snapshots de certificación repetidos.  
3. Embeddings por versión.  
4. Packs de escenarios.  

Política: regenerar derivados antes que almacenar infinitas variantes.

---

## 10. IA (arquitectura)

### 10.1 Rol de la capa L3

La IA **asiste**; no sustituye Perception, Geometry ni Materials. Respuestas cuantitativas deben anclarse al MDO.

### 10.2 Servicios componentes

| Servicio | Función |
|----------|---------|
| Orchestrator | Interpreta intención → plan estructurado de pasos |
| Tool Router | Ejecuta tools registradas con schemas |
| Retriever (RAG) | Busca chunks/proyecciones MDO relevantes |
| Citation Guard | Exige citas para claims cuantitativos/comerciales |
| Policy Guard | Permisos, plan quotas, PII, denylist acciones |
| Eval Service | Suites offline/online de calidad y regressión |
| Embedding Indexer | Mantiene índice semántico de proyecciones |

### 10.3 Tools read-only hacia MDO (ejemplos conceptuales)

- `get_project_summary`
- `list_spaces(version_id)`
- `get_space(space_id)`
- `list_takeoff(version_id, filters)`
- `get_element(element_id)`
- `get_budget_summary(budget_id)`
- `compare_scenarios(left, right)`
- `list_issues(confidence_lt=...)`
- `get_certification(cert_id)` metadatos

Tools de escritura **solo**:
- `create_ai_proposal(change_ops_draft)`  
Nunca `write_geometry_raw`.

### 10.4 Pipeline de respuesta

```
User message
  -> Policy Guard (authz/quota)
  -> Context assembly (Chat)
  -> Orchestrator: structured plan
  -> Retriever RAG
  -> Tool Router (parallelizable reads)
  -> Draft answer
  -> Citation Guard
  -> Policy Guard (egress)
  -> Stream to user
  -> Persist trace + citations
```

### 10.5 Arquitectura anti-alucinación

1. **No geometry from LLM**: prohibido emitir coordenadas/polígonos autoritativos.  
2. **Refuse without citation**: si claim numérico sin ref MDO → rechazar o pedir aclaración.  
3. **Confidence passthrough**: reportar confidence de evidencia/medida; no “redondear confianza”.  
4. **Deterministic engines win**: cantidades salen de TakeoffLine, no del modelo generativo.  
5. **Proposal vs fact**: propuestas etiquetadas como no aplicadas.  
6. **Eval gates**: regressiones bloquean deploy de orquestación.  
7. **Grounding chunks**: RAG solo sobre proyecciones firmadas por version_id.  
8. **Temperature/policy** como detalle de implementación — no arquitectura mandatoria de vendor.

### 10.6 Indexación semántica

Indexer consume `ModeloActualizado`, `MaterialCalculado`, `CostoActualizado`, `CertificacionEmitida` y construye documentos:
- space cards
- system summaries
- takeoff aggregates
- open issues
- budget chapter summaries

Cada chunk lleva metadata de cita (`entity_type`, `entity_id`, `version_id`).

### 10.7 Quotas y degradación

Si cuota AI agotada:
- chat responde con límite y sugiere upgrade
- tools MDO UI siguen funcionando sin LLM

Si retriever caído:
- modo tools-only limitado
- o fail closed en claims cuantitativos

### 10.8 Seguridad IA

- Prompt injection defenses en capa de policy (sin publicar prompts aquí).
- Separar instrucciones de sistema de documentos recuperados.
- No exponer secrets en tool results.
- Redactar PII según settings Enterprise.

### 10.9 Observabilidad IA

Traces: plan, tools, latencias, citation pass/fail, token usage meters → Billing.  
Eval dashboards: groundedness, refusal correctness, cost per successful answer.

### 10.10 Lo que la IA puede y no puede escribir

| Puede | No puede |
|-------|----------|
| Explicar takeoff | Inventar m2 |
| Señalar low confidence | “Arreglar” geometría silenciosamente |
| Crear AIProposal | Commit automático a baseline |
| Ayudar a redactar notas | Firmar presupuestos |
| Guiar mapping color→tipología | Persistir mapping sin confirmación si policy lo exige |

---

## 11. Chat

### 11.1 Propósito

El Chat es la interfaz conversacional de L3 sobre el MDO. No es un chatbot genérico: está **anclado a proyecto, rol, entidades seleccionadas y permisos**.

### 11.2 Arquitectura de componentes

```
+-------------+     +------------------+     +------------------+
| Studio Chat | WSS | Chat Service     | --> | AI Orchestrator  |
| UI          | <-- | Context/Memory   | <-- | Tools / Guards   |
+-------------+     +--------+---------+     +--------+---------+
                             |                        |
                             v                        v
                      Chat store                 MDO Read APIs
                      Audit hooks                Retriever
```

### 11.3 Context assembly

Orden de ensamblado:
1. **Identity scope**: user, roles, entitlements.
2. **Project scope**: project_id, currency, unit_system, baseline/scenario activo.
3. **Selection scope**: sheet, spaces, systems, elements seleccionados en UI.
4. **Task hints**: modo (takeoff QA, costos, explicación certificación).
5. **Memory**: short-session + long-project summary.
6. **Retrieved chunks**: RAG top-k con version_id coherente.
7. **Open issues**: flags de confianza relevantes.

El contexto nunca incluye proyectos de otro tenant.

### 11.4 Retrieval

- Filtra por `org_id`, `project_id`, `version_id`/`scenario_id`.
- Prefiere chunks con agregados firmados (takeoff/budget) sobre texto libre.
- Mezcla lexical + semántico cuando el índice lo permita.
- Devuelve candidatos con citation metadata obligatoria.

### 11.5 Tool use en chat

El Chat Service no ejecuta SQL; solicita al Orchestrator.  
UX streaming muestra estados: `thinking` (genérico), `tool:list_takeoff`, `grounding`, `answer`.

Límites:
- máximo tools por turno
- timeout por tool
- deny tools de escritura excepto proposal

### 11.6 Memoria

| Tipo | Contenido | Persistencia |
|------|-----------|--------------|
| Short session | últimos turnos, selecciones | thread hot |
| Long project memory | resúmenes de decisiones, preferencias tipológicas | summaries versionados |
| Ephemeral UI | viewport selection | no DB durable |

Summaries se regeneran por job periódico o al cerrar hilo largo.  
No deben contradecir MDO; si conflictúan, gana MDO y se invalida summary.

### 11.7 Formato de citas

Cada claim relevante adjunta:
```
citations: [
  { "entity_type": "takeoff_line", "entity_id": "...", "version_id": "...", "label": "Yeso 12.5mm - Living" }
]
```
UI deep-link al inspector MDO.  
Si el usuario inserta respuesta en doc comercial → `ChatRespuestaUsadaEnDoc` + audit.

### 11.8 Streaming UX

- Primer byte útil rápido (ack + plan corto).
- Chunks de texto; citas pueden llegar al final del turno o inline.
- Errores retryable vs terminales diferenciados.
- Cancelación de generación por usuario.

### 11.9 Permisos

- Sin `chat:use` → bloqueado.
- Viewer puede preguntar lecturas; no crear proposals si policy lo impide.
- Datos de costos sensibles pueden ocultarse a ciertos roles.
- Enterprise: retención y eDiscovery de transcripts según settings.

### 11.10 Auditoría comercial

Cuando una respuesta se usa en presupuesto/certificación:
1. Snapshot del mensaje + citations + model/orchestrator version refs.
2. Inmutable respecto a edits posteriores del thread.
3. Exportable en audit pack.

### 11.11 Modos de chat

| Modo | Objetivo |
|------|----------|
| Ask | preguntas grounded |
| QA confianza | recorrer low-confidence |
| Compare escenarios | explicar diffs |
| Redacción asistida | notas/report narrative con disclaimers |
| Proposal assist | borradores de ChangeOps |

### 11.12 Fallas y degradación

- Sin índice: tools only.
- Sin cuota: mensaje de upgrade; UI MDO intacta.
- Tool error: explicar limitación; no inventar números.

### 11.13 Relación con notificaciones

Chat no reemplaza notificaciones de jobs.  
Puede ofrecer “explicar este resultado” deep-link desde notify.

### 11.14 Multi-usuario

Presencia en thread opcional; no collaborative editing del mismo mensaje.  
Rate limit por usuario y org.

### 11.15 Internacionalización

Respuestas en español LATAM por defecto; números/moneda según project settings.  
Glosario de obra consistente (m2, tipologías).

---

## 12. Escenarios (Git-like)

### 12.1 Concepto

Los escenarios permiten explorar alternativas de diseño/cómputo sin corromper la baseline de licitación o certificación.

```
          main/baseline
             |
            V1
           /  \
          /    \ scenario: "steel-alt"
        V2      V1'
         |       |
        V3      V2'  (materials/costs diverge)
           \   /
            merge -> V4
             |
          promote baseline
```

### 12.2 Branches (Scenarios)

Atributos: nombre, descripción, head version, status (`open`, `merged`, `frozen`, `deleted_soft`), permisos.

Reglas:
- Nombre único por proyecto.
- Baseline protegida por roles.
- Free puede limitar #scenarios; Pro/Enterprise amplían.

### 12.3 Commits / ChangeSets

ChangeSet agrupa ChangeOps atómicos:
- add/update/remove entity
- tipify element
- override takeoff
- param changes
- geometry replace refs (desde engines)

Estados: `open`, `validated`, `confirmed`, `rejected`.

Mensaje obligatorio (como commit message) para trazabilidad.

### 12.4 Merge rules

1. Fast-forward si no hay divergencia.
2. 3-way merge usando ancestor version.
3. Auto-merge cambios no solapados por `entity_id` + campo.
4. Conflictos → bloqueo hasta resolución.
5. Post-merge: invalidar proyecciones; encolar materials/costs recompute si aplica.
6. Emitir `EscenarioMerged`.

### 12.5 Tipos de conflicto

| Tipo | Ejemplo | Resolución típica |
|------|---------|-------------------|
| Geometry | mismo muro con polígonos distintos | elegir lado / re-measure |
| Typology | tipología distinta en mismo element stable key | elegir tipología |
| Materials | override vs fórmula recompute | conservar override o recalcular |
| Costs | pricebook line distinta | política de precio |
| Structural graph | element borrado vs editado | revive o drop |
| Certification lock | edit vs entidad locked | denegar |

### 12.6 Compare

Compare produce:
- diff entidades
- diff takeoff agg
- diff costos
- lista conflictos potenciales
- confidence deltas

API: `GET /compare?left=&right=`.  
UI: vista lado a lado + deltas % ARS.

### 12.7 History

Log de changesets navegable; blame-like por entidad (quién tipificó / override).  
Certificaciones etiquetan versions (tags).

### 12.8 Promote to baseline

- Solo roles autorizados.
- Preconditions: sin conflictos abiertos; checks de calidad opcionales (no scale_missing crítico).
- Marca version como baseline; emite `EscenarioPromovido`.
- Puede disparar report pack.

### 12.9 Soft delete

Scenario soft-deleted oculta UI; conserva history si referenciado por compares/certs.  
GC posterior según retención.

### 12.10 Diagramas de conflictos

```
Ancestor A
  |- Branch B: Element X geom=G1
  |- Branch C: Element X geom=G2
Merge:
  conflict(geometry, X)
  resolution pick G2 -> ChangeOp explicit
```

```
Ancestor A takeoff cement=10
  |- B override cement=12
  |- C recompute cement=11
Merge policy:
  prefer_manual_override -> 12 with flag
```

### 12.11 Interacción con motores

Engines pueden correr **por escenario**:
- materials/costs listeners filtran `scenario_id`/`version_id`.
- No contaminar baseline sin promote.

### 12.12 Interacción con IA

IA puede explicar diffs y proponer resoluciones; no merge autónomo salvo feature futura con policy estricta (default OFF).

### 12.13 Permisos finos

- `scenario:create`, `scenario:commit`, `scenario:merge`, `scenario:promote`, `scenario:delete`.
- Enterprise: protected branches + required reviewers (concepto).

### 12.14 Performance

Diffs usan ChangeOps e índices por entidad; evitar deep compare de blobs salvo necesidad.  
Aggregates precomputados aceleran compare comercial.

---

## 13. Plugins

### 13.1 Motivación

El core no puede hardcodear todas las disciplinas (Steel Frame, Gas, Incendio, etc.). Los plugins extienden **capabilities** sin reescribir el núcleo.

### 13.2 Module Manifest (conceptual)

Campos:
- `plugin_id`, `name`, `version`, `min_core_version`
- `capabilities[]`
- `typologies[]`, `formulas[]`
- `validators[]`
- `ui_panels[]`
- `perception_color_maps[]` opcionales
- `permissions_requested[]`
- `sandbox_profile`
- `changelog`

Firmado/validado por Registry antes de instalar.

### 13.3 Capability contracts

| Capability | Contribuye | Host |
|------------|------------|------|
| `takeoff.lines` | produce líneas / fórmulas | Materials |
| `costs.formulas` | ajustes de costeo tipológicos | Costs |
| `ui.panel` | paneles inspector | Frontend host |
| `perception.color_map` | mapas color→typology defaults | Perception/UI |
| `validate.model` | reglas de consistencia | Construction/Geometry |
| `reports.section` | secciones de reporte | Reports |
| `chat.tools` | tools extra read-only | AI Tool Router |

Contratos versionados; plugins hablan APIs host, no DB.

### 13.4 Sandboxing

- Plugins **no** reciben credenciales OLTP globales.
- Ejecución de fórmulas en motor determinista host o WASM/isolate conceptual.
- Time/CPU/memory limits.
- Network deny-by-default; allowlist Enterprise.
- Audit de installs/upgrades.

### 13.5 Versionado e instalación

```
Registry -> Install (org/project) -> Validate manifest -> Grant capabilities -> Emit PluginInstalado
Upgrade -> Compat matrix -> Migrate typology codes if needed -> PluginActualizado
Disable -> PluginDeshabilitado (data orphaned gracefully)
```

Sin rewrite del core: hot-load de registries y feature flags.

### 13.6 Ejemplos de plugins

#### Steel Frame
- Typologies: montante, solera, rigidizador, placa OSB, etc.
- Formulas: cantidad de perfiles por longitud/espaciamiento; tornillería.
- UI: panel de espaciamiento y calibre.
- Validators: espaciamiento fuera de norma → warning.
- Color maps: color “estructura liviana”.

#### Hormigón
- Typologies: zapata, columna, viga, losa, pared.
- Formulas: m3 hormigón, kg acero (ratios), m2 encofrado.
- Validators: recubrimientos/params faltantes.
- Reports: capítulo estructura hormigón.

#### Gas
- Typologies: cañerías, artefactos, reguladores.
- Formulas: metros lineales + fittings factores.
- Validators: pendientes/diámetros params.
- Chat tools: `list_gas_runs` (read).

#### Incendio
- Typologies: matafuegos, hidrantes, detección.
- Formulas: conteos por superficie/reglas paramétricas.
- Validators: cobertura mínima (param packs).
- UI panel: riesgo/uso del espacio.

#### Paisajismo
- Typologies: solados exteriores, césped, riego, especies (conteo).
- Formulas: m2 + unidades.
- Perception maps: verdes/exteriores.
- Costs: pricebook items regionales.

#### Domótica
- Typologies: puntos de control, cableado, hubs.
- Formulas: por ambiente/punto.
- Depende de spaces más que de máscaras.
- Plugin chat tools para inventario de puntos.

#### Piscinas
- Typologies: vaso, borde, equipo filtrado, cañerías.
- Formulas: volumen, m2 revestimiento, equipos set.
- Validators: profundidad params.
- Scenario-friendly: comparar revestimientos.

### 13.7 Ciclo de vida de datos tipológicos

Al deshabilitar plugin:
- Elementos existentes quedan legibles (snapshot tipología).
- Recompute puede marcar `plugin_unavailable`.
- No borrar takeoff histórico certificado.

### 13.8 SDK conceptual para desarrolladores

Entregables del SDK (diseño):
- plantilla manifest
- schemas de tipología/fórmula
- harness de tests de fórmulas
- emulador de host capabilities
- guía de versionado semver

### 13.9 Seguridad marketplace de plugins

- Review manifests.
- Permission least privilege.
- Revocación remota si vulnerability.
- Enterprise private registry aislado.

### 13.10 Relación con Free/Pro/Enterprise

| Plan | Plugins |
|------|---------|
| Free | core tipologías wedge |
| Pro | plugins públicos selectos |
| Enterprise | privados + pin versions + policy |

---

## 14. Enterprise

### 14.1 Unidades organizativas

```
Organization
  ├── OrgUnits / Branches ( sucursales )
  ├── Teams
  ├── Projects (ACL por team/unit)
  └── External auditors (read)
```

Soporte multi-company: una cuenta holding con varias orgs o multi-org units según packaging.

### 14.2 RBAC / ABAC fino

RBAC roles + ABAC conditions:
- project.sensitivity
- scenario.protected
- certification.period
- region residency tag
- team membership

Policies evaluadas en Gateway y servicios.

### 14.3 Audit logs

- Append-only, consultable, exportable.
- Cobertura: auth events, ACL changes, sign budget, cert emit, plugin install, AI used-in-doc, merge/promote.
- Legal hold detiene purgas.

### 14.4 Retención y backups / DR

- Políticas por clase de dato (§9).
- Backups verificados; drills DR.
- RPO/RTO contractuales conceptuales por tier.
- Region secundaria warm (opcional).

### 14.5 Integraciones

| Integración | Uso |
|-------------|-----|
| SSO SAML/OIDC | AuthN enterprise |
| Accounting light | export asientos/costos (no ERP full) |
| Webhooks | eventos firmados outbound |
| Public API | automatizaciones |
| SIEM export | audit stream |

### 14.6 Public API & quotas

- Keys con scopes.
- Rate limits elevados.
- SLAs de disponibilidad API.

### 14.7 Multi-company y data residency

- Opciones de residencia (LATAM region preference).
- Restricciones de routing de workers/storage.
- Controles contractuales sobre subprocessors (nivel diseño).

### 14.8 SLA concepts

| Métrica | Idea |
|---------|------|
| Disponibilidad API | mensual |
| Soporte | canales/horarios |
| Job priority | lanes dedicadas |
| DR | RPO/RTO |

### 14.9 Compliance posture (alto nivel)

- Least privilege, encryption, auditability, retention, tenant isolation.
- No afirmar certificaciones legales específicas sin control externo.

### 14.10 Enterprise UX admin

- Consola org units/teams.
- Usage dashboards.
- Plugin allowlists.
- Retention policies UI.
- SSO config wizard.

---

## 15. Escalabilidad

### 15.1 Trayectoria de crecimiento

| Tier | Usuarios | Proyectos (orden) | Topología |
|------|----------|-------------------|-----------|
| T0 | ~100 | cientos | monorepo deploy modular; 1 región; OLTP single + backups; colas simples |
| T1 | ~1k | miles | API replicas; read replica; CDN thumbs; workers separados perception/reports |
| T2 | ~10k | decenas de miles | partición colas por org; cache proyecciones; search cluster; autoscale workers; outbox CDC |
| T3 | ~100k | cientos de miles | shard keys `org_id` (o pool tenancy); regionalization; rate limit distribuido; DLQ ops mature |
| T4 | ~1M projects | millones entidades | multi-región activa selectiva; warehouse; isolation noisy neighbors; plugin sandboxes a escala |

### 15.2 Bottlenecks esperados

1. **Perception CPU/GPU** — coste y latencia.  
2. **Object storage volumen** — planos/máscaras/certs.  
3. **Recompute fan-out** materials/costs en obras grandes.  
4. **LLM tokens** — chat masivo.  
5. **PDF generation** spikes.  
6. **OLTP hot rows** (heads, meters).  
7. **Search/embeddings reindex storms**.

### 15.3 Qué introducir en cada salto

| Transición | Introducir |
|------------|------------|
| 100→1k | workers split, CDN, basic replicas |
| 1k→10k | queue partitions, projection cache, autoscale, stronger observability |
| 10k→100k | sharding/pooling by org_id, priority lanes, regional storage, query budgets |
| 100k→1M projects | multi-region active patterns, tenant placement, event archive tiers, cost anomaly detection |

### 15.4 Cost drivers

| Driver | Por qué duele | Mitigación arquitectónica |
|--------|---------------|---------------------------|
| Perception CPU | CV por página | caches de pipeline, reproceso parcial, quotas Free |
| Storage blobs | originals+masks+certs | retention, regenerate derivatives, compression |
| LLM tokens | chat/evals | grounding tools-first, cupos, summarization |
| PDF gen | CPU + I/O | async jobs, templates lean, cache signed PDFs |

### 15.5 Escalado del MDO

- Summaries en OLTP; payloads fríos en docs/object.
- Particionar takeoff_lines por `project_id`/`version_id` hash futuro.
- Evitar rebuild full-project si cambia un sistema: recompute incremental.

### 15.6 Escalado event bus

- Partición `org_id`.
- Consumers horizontales con dedupe store scalable.
- Backpressure y load shedding en eventos no críticos (embeddings).

### 15.7 Escalado multi-tenant fairness

Weighted fair queuing; límites de concurrency por org; burst credits Pro/Enterprise.

### 15.8 Pruebas de carga conceptuales

Escenarios:
- 1k uploads concurrentes Free/Pro mix
- recompute storm tras pricebook refresh
- chat spikes
- merge conflicts heavy projects

SLOs alineados a §1.10 y §8.5.

---

## 16. Roadmap técnico

Etapas técnicas alineadas al Master Plan (sin resumirlo): hitos de arquitectura.

### Etapa 1 — Cimientos MDO + Eventing

| Campo | Contenido |
|-------|-----------|
| Objetivos | MDO schema v1 (grafo+versions), outbox+bus inicial, Media+Perception jobs desacoplados, AuthZ tenant, wedge color→qty→ARS sobre MDO |
| Tiempo estimado | 3–6 meses |
| Riesgos | migrar mentalidad file-centric→twin; performance perception; subestimar provenance |
| Dependencias | decisiones MDO aprobadas; definición tipologías core |
| Beneficio | source of truth estable; async real; base para todo lo demás |

Hitos: `ProjectVersion`/`ChangeSet` mínimos, `PlanoSubido→…→CostoActualizado`, jobs API, proyección takeoff.

### Etapa 2 — Motores duros + Escenarios básicos

| Campo | Contenido |
|-------|-----------|
| Objetivos | Geometry engine endurecido; Materials formulas versionadas; Costs pricebooks; Scenarios branch/compare MVP; WS progress maduro |
| Tiempo estimado | 3–5 meses |
| Riesgos | conflictos merge prematuros; fórmulas edge-case LATAM; escala calibración UX |
| Dependencias | Etapa 1 sólida; catálogo unidades/moneda |
| Beneficio | alternativas de cómputo; determinismo auditable |

Hitos: `EscenarioCreado`, compare takeoff/cost, override auditado, SignedBudget v1.

### Etapa 3 — IA grounded + Chat + Reports/Cert

| Campo | Contenido |
|-------|-----------|
| Objetivos | Orchestrator+tools read-only; Retriever; Citation/Policy guards; Chat memoria; Reports PDF/Excel; CertificacionEmitida locks |
| Tiempo estimado | 4–6 meses |
| Riesgos | alucinaciones si se salta guards; costos tokens; abuso Free |
| Dependencias | proyecciones MDO estables; meters billing |
| Beneficio | asistencia confiable; cierre comercial con lineage |

Hitos: refuse-without-citation, `ChatRespuestaUsadaEnDoc`, certification freezer, eval service baseline.

### Etapa 4 — Plugin Host + Marketplace light

| Campo | Contenido |
|-------|-----------|
| Objetivos | Plugin manifest/SDK; host capabilities; instalar Steel Frame/Hormigón/Gas como plugins; Marketplace catálogo+órdenes básico; price sync |
| Tiempo estimado | 4–7 meses |
| Riesgos | sandbox escapes; compat matrix; marketplace antes de demanda real |
| Dependencias | Materials contracts estables; billing entitlements plugins |
| Beneficio | extensión sin fork; monetización ecosistema |

Hitos: `PluginInstalado` flow, private registry Enterprise beta, `CompraRealizada` event.

### Etapa 5 — Enterprise scale + Multi-región options

| Campo | Contenido |
|-------|-----------|
| Objetivos | SSO/SAML/OIDC; RBAC/ABAC fino; audit export; DR; sharding/pool tenancy; public API SLA; residency options; warehouse analytics |
| Tiempo estimado | 6–12 meses (incremental) |
| Riesgos | over-compliance theater; costo multi-región prematuro; complejidad ops |
| Dependencias | métricas reales de T2/T3; clientes Enterprise piloto |
| Beneficio | contratos grandes LATAM/global selectivo; durabilidad a años |

Hitos: org units/teams, legal hold, shard-ready keys, automation API v1 estable.

### 16.1 Dependencias entre etapas (diagrama)

```
Etapa1 MDO+Events
    -> Etapa2 Engines+Scenarios
        -> Etapa3 AI+Chat+Cert
            -> Etapa4 Plugins+Marketplace
                -> Etapa5 Enterprise Scale
```

Atajos peligrosos (prohibidos): Marketplace o IA generativa de cantidades antes de MDO; microservicios extremos en Etapa 1.

### 16.2 Definition of Done arquitectónico por etapa

Cada etapa cierra con:
- ADRs actualizados
- contratos de eventos publicados
- runbooks de DLQ/jobs
- pruebas de carga del bottleneck principal
- checklist anti-alucinación (desde Etapa 3)

---

## 17. Qué NO hacer

Lista de anti-patrones (no exhaustiva pero operativa). Si aparece en PRs/diseños, rechazar.

1. Mantener un god monolith eterno sin boundaries lógicos.  
2. Dejar que el LLM invente cantidades o geometría.  
3. Usar blobs/PDF como única fuente de verdad.  
4. Ejecutar OCR/CV síncrono dentro del request HTTP para siempre.  
5. Shared DB cross-domain sin ownership ni anti-corruption.  
6. Microservicios prematuros (1 servicio = 1 tabla) antes de dolor real.  
7. Construir Marketplace antes de MDO estable.  
8. Acoplar Costs directamente a Perception.  
9. Hard-delete de certificaciones o usage events.  
10. Chat sin citation guard en modo comercial.  
11. Escribir desde AI a tablas de geometría “porque es más fácil”.  
12. Ignorar `org_id` en queries (IDOR time-bomb).  
13. Pricebooks globales mutables sin historial cuando hay presupuestos firmados.  
14. Mezclar señales WS con contratos de integración duraderos.  
15. Fan-out síncrono en cascada dentro de un solo request (perception→…→pdf).  
16. Duplicar fórmulas en Frontend como autoridad.  
17. Embeddings sobre datos de otro scenario/version por bug de filtro.  
18. Plugin con acceso SQL crudo al core.  
19. Versionar APIs solo “en la cabeza” sin `/v1`.  
20. Carecer de idempotencia en consumers.  
21. Publicar eventos antes del commit (sin outbox).  
22. Usar orden global de eventos como supuesto.  
23. Cachear permisos sin invalidación.  
24. Entregar signed URLs eternas.  
25. Tratar Free/Pro/Enterprise como forks de código.  
26. Meter lógica de billing dentro de Geometry.  
27. Reportes que mutan el twin.  
28. Escenarios sin ancestor (diff imposible).  
29. Auto-merge silencioso de conflictos de tipología.  
30. Certificar sin hash/snapshot freezer.  
31. Logs con PII de planos completos.  
32. “Temp tables” globales compartidas entre tenants en workers.  
33. Reprocess storms sin backoff/fairness.  
34. Evaluar IA solo con vibe checks (sin Eval Service).  
35. Ocultar flags `scale_missing` al usuario.  
36. Permitir promote a baseline con merge conflicts abiertos.  
37. Construir ERP completo dentro del núcleo.  
38. Vendor lock arquitectónico como premisa de diseño.  
39. Documentar arquitectura solo con slides; cero contratos.  
40. Subir tipologías nuevas solo en hardcoded enums sin plugin path.  
41. Mezclar moneda de project con conversiones silenciosas no versionadas.  
42. Usar search index como source of truth de takeoff.  
43. Colas únicas sin prioridad ni isolation de poison.  
44. Chat memory que contradice MDO sin invalidación.  
45. Exponer tool traces crudos en public API.  
46. Soft-delete inconsistente (algunas tablas sí, audit no).  
47. “Arreglar” datos certificados con update in place.  
48. Ignorar LATAM units/currency en defaults.  
49. Diseñar mobile offline-full antes que twin sync sólido (salvo research).  
50. Sustituir tests de motores deterministas por prompts.  
51. Acoplar Frontend al schema interno de documents geometry.  
52. Growth hacks que bypassen QuotaGuard en workers.  
53. Un solo usuario de DB con privilegios god en producción sin controles.  
54. Event names verbosos inestables que cambian cada sprint.  
55. Implementar ABAC Enterprise sin antes tener RBAC limpio.  
56. Guardar secretos de SSO en settings de proyecto.  
57. Dejar DLQ sin owner ni alerta.  
58. Hacer del warehouse el lugar donde “se corrigen” cantidades.  
59. Copiar MDO completo por cada tecla en canvas.  
60. Prometer realtime colaborativo CRDT global antes de WS presence básico.

---

## 18. Conclusión

### 18.1 Si se reconstruyera ARQ-IA desde cero hoy

Se construiría **alrededor del MDO versionado**, con Perception/Geometry/Materials como motores deterministas, Costs sobre takeoff, Scenarios tipo Git, y una capa IA estrictamente grounded. El sistema nacería event-driven con outbox, jobs para todo lo pesado, multi-tenant con `org_id`, y planes Free/Pro/Enterprise como entitlements — no como productos divergentes.

Orden de construcción:  
**Identity/Billing gates → Projects/Media → Perception async → Geometry → MDO → Materials → Costs → Scenarios → Reports/Cert → AI/Chat → Plugins → Marketplace → Enterprise scale**.

### 18.2 Qué conservar del producto actual (wedge y motion)

Conservar el wedge que ya demuestra valor en LATAM:
- Plano coloreado → cantidades → valorización en ARS (u moneda local).
- Fórmulas de dominio (no “magia” genérica).
- Motion comercial Free/Pro (y proyección Enterprise).
- Multi-tenant studio para estudios/constructores.
- Enfoque pragmático en cómputo usable, no en BIM authoring total.

### 18.3 Qué reemplazar

- Cualquier autoridad implícita de archivos/blobs sobre el twin.  
- Caminos síncronos frágiles de OCR/CV en request-response.  
- Acoplamientos que permitan a la IA o al UI convertirse en source of truth de cantidades.  
- Extensiones por forks/hardcode donde debería haber plugins.  
- Ausencia de versionado/escenarios cuando el negocio compara alternativas.

### 18.4 Qué hacer diferente

- Diseñar provenance y confidence desde el día 0.  
- Citation-first en asistencia.  
- ChangeSets como moneda de cambio del modelo.  
- Contratos de eventos estables para crecer por consumidores.  
- Plugin host antes de que el core se vuelva un cementerio de disciplinas.  
- Escala por partición `org_id` y fairness, no solo “más pods”.  
- Certificaciones y presupuestos firmados como datos sagrados e inmutables.

### 18.5 Norte durable

ARQ-IA 3.0 debe ser, por años:
- un **twin de obra consultable y versionado**,
- con **motores deterministas** que merecen confianza profesional,
- con **IA que explica y acelera** sin usurpar,
- extensible por **plugins**,
- vendible en **LATAM primero** y endurecible a **Enterprise**,
- y operable event-driven sin reescrituras existenciales cada trimestre.

Esta arquitectura es la base de diseño aprobada para guiar ADRs, implementación incremental y evaluación de PRs futuros.

---

## Apéndice A — Glosario arquitectónico

| Término | Definición |
|---------|------------|
| MDO | Modelo Digital de la Obra; source of truth del twin |
| L1 Percepción | Capa de extracción de evidencias desde medios |
| L2 Twin | Capa del MDO y motores geométricos/materiales |
| L3 Inteligencia | IA/chat/reportes narrativos asistidos |
| Evidence | Hecho percibido con confidence y lineage a media |
| TakeoffLine | Cantidad material tipada ligada a versión |
| Pricebook | Catálogo de precios versionable |
| ChangeSet | Commit de operaciones sobre el twin |
| Scenario | Branch de exploración del MDO |
| Baseline | Versión/scenario principal de la obra |
| Citation | Referencia a entidad MDO que soporta un claim |
| Capability | Contrato de extensión de plugin |
| Outbox | Tabla/patrón de publicación confiable de eventos |
| DLQ | Dead Letter Queue |
| Entitlement | Derecho de plan (Free/Pro/Enterprise) |
| Projection | Vista materializada del twin para query/UI/RAG |
| Provenance | Cadena de origen de un hecho |
| Soft delete | Borrado lógico reteniendo lineage |
| SignedBudget | Presupuesto congelado e inmutable |
| Certification | Paquete firmado/hasheado de período u obra |
| Tool Router | Componente que despacha tools de IA |
| Policy Guard | Control de políticas/permisos/cuotas en IA |
| Fair scheduling | Evitar que un tenant ahogue colas |
| Anti-corruption | Capa que evita contaminar un dominio con otro lenguaje |
| Wedge | Caso de uso estrecho de alto valor (color→qty→ARS) |

---

## Apéndice B — Contratos entre capas L1/L2/L3

### B.1 L1 → L2

Entrada L2 desde L1:
- evidences tipadas
- color regions
- confidence scores
- refs a masks/overlays
- pipeline_version

L2 puede rechazar evidencias inconsistentes; nunca L1 escribe Budget.

### B.2 L2 internos

Geometry → Construction measures  
Construction → Materials tipificados  
Materials → Costs takeoff  
Scenarios versiona todos  
Reports lee snapshots

### B.3 L2 → L3

L3 obtiene:
- read DTOs
- projections/chunks
- flags calidad
- compare diffs

L3 devuelve:
- narrativa citada
- AIProposal drafts
- nunca raw geometry authority

### B.4 Tabla de autoridad

| Claim type | Autoridad |
|------------|-----------|
| máscara color | L1 |
| m2 / m / m3 | L2 Geometry/Materials |
| precio unitario | L2 Costs/Pricebook |
| explicación | L3 |
| certificación hash | L2 Reports freezer |

---

## Apéndice C — Matriz dominio × store

| Dominio | OLTP | Document | Object | Cache | Search | Outbox |
|---------|------|----------|--------|-------|--------|--------|
| Identity | ● | ○ | ○ | ● | ○ | ● |
| Projects | ● | ○ | ○ | ○ | ● | ● |
| Media | ● | ○ | ● | ○ | ○ | ● |
| Perception | ● | ● | ● | ○ | ○ | ● |
| Geometry | ● | ● | ● | ○ | ○ | ● |
| Construction | ● | ● | ○ | ● | ● | ● |
| Materials | ● | ○ | ○ | ● | ● | ● |
| Costs | ● | ○ | ● (signed) | ● | ● | ● |
| Scenarios | ● | ○ | ● (packs) | ○ | ○ | ● |
| Timeline | ● | ○ | ○ | ○ | ○ | ● |
| Reports | ● | ○ | ● | ○ | ● | ● |
| AI | ● | ○ | ● (emb) | ○ | ● | ● |
| Chat | ● | ○ | ○ (archive) | ○ | ○ | ● |
| Marketplace | ● | ○ | ○ | ○ | ● | ● |
| Billing | ● | ○ | ○ | ● | ○ | ● |
| Notifications | ● | ○ | ○ | ○ | ○ | ● |
| Settings | ● | ● | ○ | ● | ○ | ● |
| Audit | ● | ○ | ● (exports) | ○ | ○ | ○ |
| Plugins | ● | ● (manifest) | ○ | ○ | ● | ● |

Leyenda: ● primario, ○ opcional/secundario.

---

## Apéndice D — Matriz evento × consumidores

| Evento | Consumidores principales |
|--------|--------------------------|
| PlanoSubido | Perception, Notifications, Billing meters |
| MediaAssetListo | Perception, media_deriv |
| PlanoProcesado | Geometry, Search, Notifications, WS |
| CalibracionActualizada | Geometry |
| ModeloActualizado | Materials, Search, AI Indexer, Notifications, Projections |
| MaterialCalculado | Costs, Search, AI Indexer, Notifications |
| CostoActualizado | Reports(sched), Notifications, AI Indexer, Marketplace suggestions |
| EscenarioCreado | WS, Audit |
| ChangeSetConfirmado | Projections, Materials/Costs if needed |
| EscenarioMerged | Projections, Materials, Costs, Notifications |
| EscenarioPromovido | Reports, Notifications, Audit |
| PresupuestoFirmado | Audit, Notifications, Reports |
| CertificacionEmitida | Audit, Timeline, Notifications, lock service |
| ProveedorSeleccionado | Costs (optional), Notifications |
| CompraRealizada | Notifications, Audit, Billing? (if marketplace fee) |
| PluginInstalado | TypologyRegistry, Settings, Notifications |
| EmbeddingsActualizados | (meta ops) |
| SuscripcionCambiada | Entitlements cache, Notifications |
| QuotaUmbralAlcanzado | Notifications, Gateway limits |
| ChatRespuestaUsadaEnDoc | Audit |
| AIProposalResuelta | Scenarios/Construction (if accept path), Audit |
| ProyectoArchivado | cancel jobs, retention, Notifications |

---

## Apéndice E — Checklist onboarding de nuevo ingeniero

1. Leer este documento completo (ARQ-IA 3.0 Arquitectura Definitiva).  
2. Interiorizar: MDO truth; IA no reemplaza motores.  
3. Dibujar de memoria flujo `PlanoSubido→CostoActualizado`.  
4. Listar bounded contexts y qué no pueden conocer.  
5. Entender ChangeSet/Scenario vs baseline.  
6. Revisar catálogo de eventos y envelope.  
7. Practicar: dónde se guarda un mask vs TakeoffLine vs SignedBudget.  
8. Repasar AuthZ: tenant → entitlement → RBAC → ABAC.  
9. Entender Jobs API + WS progress.  
10. Leer ADRs existentes (cuando existan) listados en Apéndice F.  
11. Montar entorno local de un solo dominio (sin re-auditar producto legacy).  
12. Escribir un consumer idempotente de juguete contra envelope.  
13. Correr checklist “Qué NO hacer” sobre un diseño propio.  
14. Conocer planes Free/Pro/Enterprise como gates.  
15. Entender plugin capability mínima (`takeoff.lines`).  
16. Saber cómo citar una TakeoffLine en Chat.  
17. Revisar retención: qué nunca hard-delete.  
18. Observabilidad: métricas de cola + correlation ids.  
19. Pedir mentoría en FormulaEngine antes de tocar costos.  
20. Primera contribución: test de contrato o proyección, no feature UI aislada.

---

## Apéndice F — ADRs recomendados

Lista de títulos (solo títulos) a redactar formalmente:

1. ADR-001: MDO como única fuente de verdad de la obra  
2. ADR-002: Separación Percepción / Twin / Inteligencia  
3. ADR-003: Prohibición de geometría autoritativa generada por LLM  
4. ADR-004: Outbox para domain/integration events  
5. ADR-005: Identificadores y particionado multi-tenant por `org_id`  
6. ADR-006: Strategy de almacenamiento híbrido OLTP + Document + Object  
7. ADR-007: Versionado Git-like con Scenario/ChangeSet  
8. ADR-008: Modelo de idempotencia en API y consumers  
9. ADR-009: Jobs async obligatorios para pipelines de percepción  
10. ADR-010: Citation Guard como gate de respuestas cuantitativas  
11. ADR-011: Entitlements Free/Pro/Enterprise en Gateway y Workers  
12. ADR-012: Soft-delete y retención de artefactos comerciales  
13. ADR-013: Plugin capability contracts y sandbox  
14. ADR-014: Inmutabilidad de SignedBudget y Certification  
15. ADR-015: Read-only tools para IA sobre el MDO  
16. ADR-016: Ordenamiento de eventos por partición de proyecto  
17. ADR-017: Public API surface y versionado `/api/v1`  
18. ADR-018: Estrategia de merge y clasificación de conflictos  
19. ADR-019: Fair scheduling multi-tenant en colas  
20. ADR-020: Data residency options Enterprise  
21. ADR-021: SSO OIDC/SAML adoption boundaries  
22. ADR-022: Embeddings event-driven y rebuildability  
23. ADR-023: Marketplace desacoplado del core twin  
24. ADR-024: Accounting light integration scope  
25. ADR-025: Observabilidad mínima correlation/causation  
26. ADR-026: Error model estable cross-domain  
27. ADR-027: Rate limits y abuse prevention AI/upload  
28. ADR-028: Projection invalidation rules  
29. ADR-029: Formula engine version pinning  
30. ADR-030: DR/Backup objectives por clase de dato  

---

## Apéndice G — Criterios de aceptación arquitectónicos

Un diseño/implementación se acepta arquitectónicamente solo si cumple:

1. **Truth**: cantidades comerciales trazables a MDO versionado (o manual explícito auditado).  
2. **Layering**: L1 no escribe costos; L3 no escribe geometría raw.  
3. **Async**: pipelines pesados vía jobs/eventos, con progreso WS.  
4. **Tenant safety**: toda query/job/evento lleva y aplica `org_id`.  
5. **Idempotencia**: consumers y mutaciones críticas son safe bajo retry.  
6. **Outbox**: no hay publish pre-commit en caminos de dominio.  
7. **Citations**: chat cuantitativo exige citations o refuse.  
8. **Confidence**: se preserva y se muestra; no se maquilla.  
9. **Versionado**: cambios al twin pasan por ChangeSet/Scenario.  
10. **Immutables**: certs/signed budgets/audit no se hard-deleten ni mutate-in-place.  
11. **Plugins**: extensiones nuevas de disciplina no requieren fork del core.  
12. **Entitlements**: features premium no bypasseables desde workers.  
13. **Observability**: correlation_id presente end-to-end en el camino feliz.  
14. **Contracts**: eventos nuevos documentados en catálogo con schema_version.  
15. **Compare/Promote**: baseline protegida; merges con conflictos clasificados.  
16. **Storage isolation**: paths/URLs no permiten browse cross-tenant.  
17. **Degradation**: fallo de IA no rompe takeoff determinista.  
18. **LATAM defaults**: moneda/unidades coherentes al proyecto.  
19. **Security**: AuthZ evaluada en Gateway y revalidada en servicio.  
20. **Scale path**: decisiones no impiden particionar por `org_id` después.  
21. **Reports purity**: reportes no alteran twin.  
22. **Marketplace periphery**: compras no corrompen geometría.  
23. **Eval readiness** (desde Etapa 3): cambios de orquestación con señal de eval.  
24. **DLQ ownership**: colas nuevas definen reintentos, DLQ y alerta.  
25. **Doc sync**: cambios estructurales actualizan ADRs + este mapa cuando aplique.

---

### Fin del documento

**ARQ-IA 3.0 — Arquitectura Definitiva**  
Estado: Arquitectura objetivo aprobada para diseño — 2026-08-02  
Naturaleza: diseño técnico denso para guiar años de evolución — sin código de implementación en este artefacto.

