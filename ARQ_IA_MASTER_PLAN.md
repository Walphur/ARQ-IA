# ARQ-IA 2.0 — PLAN MAESTRO DE EVOLUCIÓN

| Campo | Valor |
|-------|-------|
| **Documento** | Plan Maestro Estratégico ARQ-IA 2.0 |
| **Fecha** | 2026-08-02 |
| **Horizonte** | 5 años (2026–2031) |
| **Naturaleza** | Estratégico — no es especificación de implementación |
| **Audiencia** | Fundadores, producto, ingeniería, go-to-market, inversores |
| **Clasificación** | Uso interno — visión de producto y categoría |
| **Línea base** | SaaS arq-ia.pro (cómputo desde planos coloreados + estimaciones ARS) |
| **Idioma** | Español (LATAM) |
| **Versión del plan** | 1.0 — Master Plan |

> Este documento define **qué debe convertirse ARQ-IA**, no cómo se implementa línea a línea. Toda referencia al producto actual sirve únicamente como punto de partida. El foco es el futuro: el sistema operativo de la cuantificación constructiva.

---

## Índice

1. [0. Preámbulo ejecutivo](#0-preámbulo-ejecutivo)
   - [0.1 La pregunta central](#01-la-pregunta-central)
   - [0.2 Tesis estratégica en una página](#02-tesis-estratégica-en-una-página)
   - [0.3 Principios no negociables](#03-principios-no-negociables)
   - [0.4 Lectura recomendada por rol](#04-lectura-recomendada-por-rol)
   - [0.5 Definición de éxito a 5 años](#05-definición-de-éxito-a-5-años)
2. [1. Visión del producto (5 años)](#1-visión-del-producto-5-años)
   - [1.1 Identidad de producto](#11-identidad-de-producto)
   - [1.2 Creación de categoría](#12-creación-de-categoría)
   - [1.3 Job-to-be-done emocional y funcional](#13-job-to-be-done-emocional-y-funcional)
   - [1.4 North Star y métricas satélite](#14-north-star-y-métricas-satélite)
   - [1.5 Promesa de marca](#15-promesa-de-marca)
   - [1.6 Lo que el usuario debe sentir](#16-lo-que-el-usuario-debe-sentir)
3. [2. Modelo digital de la obra](#2-modelo-digital-de-la-obra)
   - [2.1 Argumento central](#21-argumento-central)
   - [2.2 Jerarquía conceptual](#22-jerarquía-conceptual)
   - [2.3 Pros y contras vs Process JSON plano](#23-pros-y-contras-vs-process-json-plano)
   - [2.4 Ciclo de vida del modelo](#24-ciclo-de-vida-del-modelo)
   - [2.5 Versionado y confianza](#25-versionado-y-confianza)
   - [2.6 Observabilidad del modelo](#26-observabilidad-del-modelo)
4. [3. Modelo de datos (arquitectura conceptual)](#3-modelo-de-datos-arquitectura-conceptual)
   - [3.1 Vista de alto nivel](#31-vista-de-alto-nivel)
   - [3.2 Entidades núcleo](#32-entidades-núcleo)
   - [3.3 Entidades MEP y sistemas](#33-entidades-mep-y-sistemas)
   - [3.4 Costos, proveedores y compras](#34-costos-proveedores-y-compras)
   - [3.5 Obra, progreso y certificación](#35-obra-progreso-y-certificación)
   - [3.6 Documentos, IA y auditoría](#36-documentos-ia-y-auditoría)
   - [3.7 Cardinalidades y reglas](#37-cardinalidades-y-reglas)
5. [4. Funcionalidades (catálogo exhaustivo)](#4-funcionalidades-catálogo-exhaustivo)
6. [5. IA (sobre el motor, nunca reemplazándolo)](#5-ia-sobre-el-motor-nunca-reemplazándolo)
7. [6. Chat inteligente](#6-chat-inteligente)
8. [7. BIM simplificado propio](#7-bim-simplificado-propio)
9. [8. Escalabilidad](#8-escalabilidad)
10. [9. Nuevos módulos](#9-nuevos-módulos)
11. [10. Experiencia de usuario](#10-experiencia-de-usuario)
12. [11. Competencia](#11-competencia)
13. [12. Diferenciadores](#12-diferenciadores)
14. [13. Roadmap 5 fases](#13-roadmap-5-fases)
15. [14. MVP vs Enterprise packaging](#14-mvp-vs-enterprise-packaging)
16. [15. Riesgos](#15-riesgos)
17. [16. Conclusión](#16-conclusión)
18. [Apéndices](#apéndices)
    - [A. Glosario](#apéndice-a--glosario)
    - [B. Principios de producto](#apéndice-b--principios-de-producto)
    - [C. KPIs norte](#apéndice-c--kpis-norte)
    - [D. Anti-objetivos](#apéndice-d--anti-objetivos)
    - [E. Escenarios de fracaso](#apéndice-e--escenarios-de-fracaso)
    - [F. Matriz visión × capacidad actual](#apéndice-f--matriz-visión--capacidad-actual)

---

## 0. Preámbulo ejecutivo

### 0.1 La pregunta central

> **¿Puede ARQ-IA dejar de ser “la app que pinta planos y tira un presupuesto” para convertirse en el sistema operativo de la cuantificación constructiva en LATAM — y desde ahí, en un estándar global de estimación confiable, operable y explicable?**

Esta pregunta no se responde con más botones. Se responde con un cambio de naturaleza del producto:

| Dimensión | Producto actual (baseline) | ARQ-IA 2.0 (destino) |
|-----------|----------------------------|----------------------|
| Unidad de valor | Cómputo + estimado rápido | Modelo digital vivo de la obra |
| Persistencia | Resultado de proceso | Grafo de elementos con historial |
| Inteligencia | CV clásico + reglas | CV + twin digital + agentes LLM |
| Rol del usuario | Operador de pipeline | Director de decisión |
| Horizonte temporal | Antes de obra | Anteproyecto → obra → certificación → archivo |
| Moat | Velocidad de estimado | Corpus + fórmulas + precios + workflow + confianza |

La pregunta central implica tres subpreguntas que este plan responde:

1. **¿Qué artefacto digital debe poseer ARQ-IA?** → Un modelo digital de obra propio (no un PDF ni un JSON opaco).
2. **¿Dónde vive la IA?** → Encima del modelo y del motor de cómputo, nunca sustituyéndolos.
3. **¿Cómo se gana el mercado?** → Primero LATAM con precisión comunicada y precio local; luego expansión por workflows, no por feature parity con Revit.

### 0.2 Tesis estratégica en una página

**Tesis:** El mercado de arquitectura y construcción no necesita otro CAD ni otro BIM pesado. Necesita un **sistema de cuantificación operativa** que convierta planos (y luego modelos) en decisiones económicas confiables en minutos, no en semanas.

ARQ-IA ya demostró un wedge único: **de plano coloreado a cantidades y precio en ARS con fricción baja**. Ese wedge no debe abandonarse; debe convertirse en la puerta de entrada a un **Operating System of Construction Quantification**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TESIS EN UNA IMAGEN                              │
│                                                                         │
│   PLANO / DOCUMENTO                                                     │
│        │                                                                │
│        ▼                                                                │
│   ┌─────────────┐     ┌──────────────────┐     ┌────────────────────┐ │
│   │ PERCEPCIÓN  │────▶│ MODELO DIGITAL   │────▶│ INTELIGENCIA       │ │
│   │ CV / OCR /  │     │ DE LA OBRA       │     │ Chat + Agentes +   │ │
│   │ ML assist   │     │ (twin cuantitativo)│   │ Escenarios         │ │
│   └─────────────┘     └────────┬─────────┘     └─────────┬──────────┘ │
│                                │                         │            │
│                                ▼                         ▼            │
│                     PRESUPUESTO · PLANIFICACIÓN · OBRA · COMPRAS      │
│                     CERTIFICACIÓN · REPORTES · MARKETPLACE            │
└─────────────────────────────────────────────────────────────────────────┘
```

**Por qué ahora:**
- La IA generativa abarata la capa de explicación y asistencia, pero **no puede inventar metros cuadrados confiables**. Quien combine percepción geométrica + modelo estructurado + LLM gana.
- LATAM sigue sub-digitalizado en cómputos: Excel, ojo, y software europeo caro/desalineado.
- Constructoras y estudios necesitan velocidad + trazabilidad ante inflación, proveedores volátiles y certificaciones.
- El “BIM completo” fracasa por costo de adopción; un **BIM Lite cuantitativo** puede ganar por pragmatismo.

**Qué NO es la tesis:**
- No es “reemplazar OpenCV con GPT”.
- No es “clonar Revit en el browser”.
- No es “ser un ERP de construcción genérico”.
- No es “marketplace primero, producto después”.

**Qué SÍ es:**
- Poseer el modelo digital de cada obra.
- Medir confianza por entidad.
- Explicar cada número.
- Conectar cómputo → dinero → tiempo → compras → avance.
- Convertir velocidad en hábito, y hábito en datos propietarios.

### 0.3 Principios no negociables

Estos principios gobiernan cada decisión de producto, diseño e inversión. Si un feature los viola, no entra al roadmap aunque sea “sexy”.

#### Principio P1 — La visión NO reemplaza el motor CV

| Aspecto | Regla |
|---------|-------|
| Motor de cómputo | Sigue siendo geométrico, determinista, auditable |
| IA / LLM | Asiste, explica, sugiere, simula; no inventa cantidades base |
| Evolución CV | Puede sumar ML assist (segmentación, OCR robusto), sin borrar el pipeline clásico |
| Criterio de merge | Si un modelo ML discrepa del motor, se marca conflicto; no se silencia |

**Observación:** El brand “IA” debe evolucionar de marketing aspiracional a arquitectura real de tres capas. Mentir al mercado destruye el moat de confianza.

#### Principio P2 — IA sobre datos estructurados

La inteligencia opera sobre el **modelo digital**, libros de precios, fórmulas y trazas — no sobre pantallazos sueltos. Sin twin cuantitativo, el chat es teatro.

#### Principio P3 — Precisión comunicada

Todo número material lleva:
- valor,
- unidad,
- fuente (percepción / regla / usuario / proveedor),
- score de confianza,
- rango o disclaimer cuando aplique.

**Nunca** presentar un estimado como certificación. **Nunca** ocultar incertidumbre detrás de decimales falsos.

#### Principio P4 — LATAM first, then global

| Fase | Geografía | Implicancia |
|------|-----------|-------------|
| 0–24 meses | Argentina + países vecinos | ARS/USD, unidades locales, hábitos de obra, proveedores, normativas parciales |
| 24–48 meses | LATAM ampliado (UY, CL, PY, PE, CO, MX) | Multi-moneda, price books regionales, idiomas ES/PT |
| 48–60 meses | Selectivo global | Workflows exportables; no feature-parity con incumbentes anglosajones |

#### Principio P5 — Velocidad con trazabilidad

El wow inicial (minutos) debe convivir con auditoría (quién cambió qué, por qué cambió el cómputo).

#### Principio P6 — Multi-tenant por diseño

Estudios, constructoras y redes de colaboradores son ciudadanos de primera clase. El particular es onboarding; el estudio es retención; la constructora es ACV.

#### Principio P7 — Human-in-the-loop en decisiones de dinero

Autorizar compras, certificar avances y firmar presupuestos requiere humano. La IA prepara; el profesional decide.

### 0.4 Lectura recomendada por rol

| Rol | Secciones prioritarias | Tiempo estimado |
|-----|------------------------|-----------------|
| Founder / CEO | 0, 1, 12, 13, 16 | 45–60 min |
| Producto | 1, 2, 4, 5, 6, 10, 14 | 2–3 h |
| Ingeniería | 2, 3, 5, 7, 8, 15 | 2–3 h |
| Comercial / GTM | 1, 11, 12, 14, Ap. C–E | 1–1.5 h |
| Inversor | 0, 1, 12, 13, 16, Ap. E | 40–50 min |

### 0.5 Definición de éxito a 5 años

Éxito no es “tener muchas features”. Éxito es ocupar una categoría mental:

> “Cuando hay que cuantificar y presupuestar una obra en LATAM con confianza y velocidad, se usa ARQ-IA.”

| Indicador de categoría | Señal cualitativa | Señal cuantitativa (orientativa) |
|------------------------|-------------------|----------------------------------|
| Habito | Profesionales abren ARQ-IA antes que Excel | ≥3 proyectos activos / usuario Pro / mes |
| Confianza | Presupuestos se envían al cliente desde la plataforma | ≥60% de proyectos Pro con export/share |
| Modelo | Usuarios exploran elementos, no solo totales | ≥40% sesiones con interacción al explorer |
| Chat | Preguntas de obra se resuelven in-product | ≥5 queries chat / proyecto / semana (fase 2+) |
| Red | Price books y proveedores locales alimentan el sistema | Cobertura de canasta básica materiales en AMBA + 3 provincias |
| Empresa | Cuentas Enterprise con obra viva (avance/certificación) | ≥15% revenue de Enterprise en año 5 |

---

## 1. Visión del producto (5 años)

### 1.1 Identidad de producto

ARQ-IA 2.0 no es un “módulo de cómputo”. Es la **capa de verdad cuantitativa** entre el diseño y el dinero.

**Identidad corta:**
> El sistema operativo de la cuantificación constructiva.

**Identidad extendida:**
> ARQ-IA convierte documentos de arquitectura y obra en un modelo digital cuantitativo, explicable y operable — para estimar, planificar, comprar, certificar y aprender — con IA que asiste sobre datos reales, no sobre alucinaciones.

**Metáfora útil:**
- CAD/BIM pesado = el taller de diseño.
- Excel/Presto clásico = la planilla de costos.
- ARQ-IA = el **tablero de mando cuantitativo** que habla ambos idiomas y agrega tiempo, compras y confianza.

```
        DISEÑO                    ARQ-IA                         GESTIÓN
   (CAD / croquis /          (OS de cuantificación)         (ERP / obra / finanzas)
    planos PDF)
         │                           │                              │
         └─────────▶ percepción ─────┤                              │
                     twin digital ───┼──── presupuesto ────────────▶│
                     chat / escenarios┤                              │
                     avance/certif. ─┘                              │
```

### 1.2 Creación de categoría

#### Nombre de categoría propuesto

**Operating System of Construction Quantification (OSCQ)**  
En español de go-to-market: **Sistema Operativo de Cuantificación Constructiva**.

#### Por qué crear categoría (y no pelear en la del competidor)

| Si competimos en… | Perdemos contra… | Si creamos OSCQ… |
|-------------------|------------------|------------------|
| BIM completo | Revit, Archicad | Ganamos por pragmatismo y velocidad |
| CAD | AutoCAD | No es nuestro juego |
| ERP construcción | Buildertrend, locales | Entramos tarde y pesados |
| Takeoff puro | PlanSwift, Bluebeam | Commodity de clicks |
| OSCQ | Nadie dominante en LATAM | Definimos reglas, UX y datos |

#### Atributos de categoría (lo que el mercado debe asociar a ARQ-IA)

1. **De plano a modelo cuantitativo en minutos**
2. **Confianza visible por elemento**
3. **Chat que cita el cómputo**
4. **Precios LATAM vivos**
5. **De estimado a obra sin cambiar de sistema**
6. **Comparación de sistemas constructivos como decisión, no como Excel heroico**

### 1.3 Job-to-be-done emocional y funcional

#### Jobs funcionales

| Job | Momento | Resultado deseado |
|-----|---------|-------------------|
| Cuantificar rápido | Anteproyecto / cliente esperando | Cantidades creíbles en minutos |
| Presupuestar con respaldo | Presentación a cliente | Precio + desglose + supuestos |
| Comparar alternativas | Definición de sistema | “Ladrillo vs Steel Frame vs Wood” con impacto $ y plazo |
| Planificar compras | Pre-obra | Lista de materiales y proveedores |
| Controlar avance | Obra | Snapshot vs cómputo base |
| Certificar | Hitos contractuales | Documento trazable |
| Explicar un número | Reunión / duda | “Por qué este muro sale X” |

#### Jobs emocionales

| Emoción actual (dolor) | Emoción deseada (ARQ-IA) |
|------------------------|---------------------------|
| Ansiedad por error de cómputo | Control y calma |
| Vergüenza al justificar precios | Orgullo profesional con evidencia |
| Caos de planillas | Claridad narrativa |
| Miedo a inflación / desactualización | Sensación de estar “al día” |
| Soledad del arquitecto solo | Copiloto experto disponible 24/7 |

#### Jobs sociales

- Parecer moderno y serio frente al cliente.
- Coordinar estudio sin WhatsApp-archivos-v3-final-FINAL.
- Hablar el idioma del constructor y del comitente.

### 1.4 North Star y métricas satélite

#### North Star Metric (propuesta)

> **Proyectos con Modelo Digital Confianza≥Umbral que generan al menos una decisión económica exportada por semana**  
> (presupuesto compartido, OC, certificación o escenario elegido)

Nombre corto: **Weekly Quantified Decisions (WQD)**.

#### Por qué esta métrica

| Alternativa débil | Por qué no alcanza |
|-------------------|--------------------|
| Usuarios registrados | Vanidad |
| Planos subidos | Actividad ≠ valor |
| Minutos de procesamiento | Eficiencia interna |
| Tokens de chat | Teatro de IA |
| WQD | Une uso + confianza + dinero |

#### Métricas satélite

| Capa | Métrica | Intención |
|------|---------|-----------|
| Adquisición | Activaciones Free→primer cómputo | Fricción onboarding |
| Activación | % proyectos con review de confianza completado | Calidad de adopción |
| Retención | Proyectos activos / cuenta / mes | Habito |
| Confianza | Distribución de confidence scores | Salud del motor |
| Monetización | Free→Pro→Enterprise | Packaging |
| Expansión | Módulos usados por proyecto | Superficie de valor |
| Datos | Entidades etiquetadas / corregidas | Moat ML futuro |
| IA útil | % respuestas chat con citation válida | Anti-alucinación |

### 1.5 Promesa de marca

**Promesa externa (cliente):**
> Cuantificá con velocidad, defendé cada número, operá la obra desde el mismo modelo.

**Promesa interna (equipo):**
> Cada feature debe aumentar la fidelidad, la operabilidad o la explicabilidad del modelo digital — o no se construye.

### 1.6 Lo que el usuario debe sentir

En los primeros 10 minutos:

1. “Entendieron mi oficio.”
2. “Esto fue más rápido que mi Excel.”
3. “Sé qué tanto puedo confiar.”
4. “Puedo preguntarle a la obra.”
5. “Puedo mostrar esto al cliente sin miedo.”

En los primeros 90 días:

1. “Mis proyectos viven acá.”
2. “Comparar sistemas me cambió una decisión.”
3. “El chat me ahorró una tarde.”
4. “Mis precios locales están mejor que la última lista del corralón.”
5. “No vuelvo al flujo anterior.”

---

## 2. Modelo digital de la obra

### 2.1 Argumento central

Hoy el valor se materializa como **salida de un proceso** (cantidades + costos derivados de un pipeline). Mañana el valor debe materializarse como **estado persistente de una obra digital**.

Sin modelo digital:
- el chat no tiene suelo,
- los escenarios son copias frágiles,
- el avance de obra no tiene baseline,
- la certificación no tiene ancla,
- la IA explica PDFs en lugar de entidades.

Con modelo digital:
- cada muro, ambiente y tramo MEP es un objeto con identidad,
- cada cambio es un evento,
- cada estimación es una proyección sobre el mismo grafo,
- cada pregunta del chat resuelve contra entidades.

**Definición:**
> El Modelo Digital de la Obra (MDO) es un grafo versionado de entidades constructivas, espaciales, de sistemas, materiales, costos y tiempo, con scores de confianza y linaje de origen.

### 2.2 Jerarquía conceptual

```
Organization / Studio
└── Project
    ├── Lot / Terrain
    ├── Building(s)
    │   ├── Level(s)
    │   │   ├── Space / Ambiente
    │   │   ├── Wall
    │   │   ├── Opening (door/window)
    │   │   ├── FloorFinish
    │   │   ├── Ceiling / Roof (por nivel o edificio)
    │   │   └── StructureElement (futuro)
    │   └── Systems (MEP + especiales)
    │       ├── ColdWater / HotWater
    │       ├── Sewage
    │       ├── Electrical
    │       ├── Gas
    │       ├── HVAC
    │       └── FireProtection
    ├── MaterialTakeoff (vistas agregadas)
    ├── CostModel / CostItems
    ├── ScheduleActivities
    ├── PurchaseOrders
    ├── ProgressSnapshots
    ├── Certifications
    ├── Documents
    ├── Scenarios / Variants
    └── AIConversations + AuditTrail
```

#### Diagrama de relaciones lógicas

```
[Project] 1──* [Building] 1──* [Level] 1──* [Space]
                      │           │
                      │           ├──* [Wall] *──* [Opening]
                      │           ├──* [FloorFinish]
                      │           └──* [CeilingPart]
                      │
                      └──* [System] 1──* [SystemRun/Segment]
                                        │
                     [Material] *──* [TakeoffLine] *──┘
                            │
                            └──* [CostItem] *── [PriceBookEntry] ── [Supplier]

[ScheduleActivity] *──* [TakeoffLine|CostItem|System]
[ProgressSnapshot] ── captura estado de [Project] @ t
[Certification] ── agrega avances aprobados
```

### 2.3 Pros y contras vs Process JSON plano

| Criterio | Process JSON plano (hoy) | Modelo Digital (destino) |
|----------|--------------------------|---------------------------|
| Velocidad inicial | Alta | Media al inicio; alta después |
| Consultas parciales | Difíciles | Naturales |
| Chat / RAG | Débil | Fuerte |
| Versionado fino | Costoso | Nativo |
| Escenarios | Copiar blob | Branch del grafo |
| Avance de obra | Desalineado | Snapshot diferencial |
| Colaboración | Choques | Locks / PRs de modelo |
| Auditoría | Gruesa | Por entidad |
| Migración | N/A | Requiere ETL desde procesos |
| Complejidad engineering | Baja | Alta (justificada) |

**Observación estratégica:** Mantener el Process JSON como **artefacto de importación/compatibilidad** durante la transición, pero dejar de ser la fuente de verdad.

### 2.4 Ciclo de vida del modelo

```
  BORRADOR          REVISIÓN           BASELINE           OBRA VIVA          ARCHIVO
     │                 │                  │                   │                 │
     ▼                 ▼                  ▼                   ▼                 ▼
  Ingesta         Corrección         Congela            Progress          Read-only
  percepción      humana HITL        cómputo            snapshots         + lecciones
  + auto-map      confidence         comercial          + certs           aprendidas
```

| Estado | Quién escribe | Qué se permite | Salidas típicas |
|--------|---------------|----------------|-----------------|
| Borrador | Sistema + usuario | Todo editable | Preview cómputo |
| Revisión | Usuario / revisor | Edits + aceptar/rechazar sugerencias | Lista de dudas |
| Baseline | Owner del proyecto | Cambios vía change-set | Presupuesto v1 |
| Obra viva | Jefe de obra / estudio | Avances, OC, extras | Certificaciones |
| Archivo | Sistema | Metadatos / tags | Benchmarks anónimos |

### 2.5 Versionado y confianza

#### Versionado

- **ProjectVersion**: snapshot inmutable etiquetado (v1.0 presupuesto cliente).
- **ChangeSet**: conjunto de edits atómicos (como commit).
- **Scenario**: rama paralela para simulación (no contamina baseline).
- **Diff**: muros añadidos/eliminados, m² delta, $ delta, plazo delta.

#### Confidence scores por entidad

| Score | Significado | UX sugerida |
|------:|-------------|-------------|
| 0.90–1.00 | Alta confianza geométrica/regla | Verde — listo |
| 0.70–0.89 | Aceptable con revisión ligera | Amarillo — revisar |
| 0.40–0.69 | Dudoso (OCR, color límite, oclusión) | Naranja — atención |
| <0.40 | No usable sin intervención | Rojo — bloquear uso en presupuesto firmado |

**Regla de oro:** Un presupuesto “para cliente” no puede incluir entidades rojas sin override explícito firmado (usuario + timestamp + motivo).

### 2.6 Observabilidad del modelo

El MDO debe exponer:

| Señal | Para qué |
|-------|----------|
| Cobertura espacial | % de m² asignados a ambientes |
| Cobertura sistemas | Sistemas presentes vs checklist tipología |
| Drift de precios | Antigüedad media de PriceBook usados |
| Deuda de revisión | Entidades amarillas/rojas abiertas |
| Consistencia topológica | Muros sin ambiente, aberturas huérfanas |
| Completitud comercial | Takeoff sin CostItem |

---

## 3. Modelo de datos (arquitectura conceptual)

> Nota: esto es arquitectura de información, **no** esquema SQL ni código. Los nombres son conceptuales.

### 3.1 Vista de alto nivel

```
┌──────────────┐     ┌──────────────┐     ┌────────────────┐
│ Organization │────▶│    User      │────▶│ Membership/Role│
└──────┬───────┘     └──────────────┘     └────────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐     ┌────────────────┐
│   Project    │────▶│  Document    │────▶│ PerceptionJob  │
└──────┬───────┘     └──────────────┘     └────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│                 DIGITAL MODEL GRAPH                       │
│  Building · Level · Space · Elements · Systems · Materials│
└──────────────────────────────────────────────────────────┘
       │
       ├──── Cost · PriceBook · Supplier · PO
       ├──── Schedule · Progress · Certification
       ├──── Scenario · AIConversation · AuditTrail
       └──── Reports / Exports
```

### 3.2 Entidades núcleo

#### Organization / Studio

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Contenedor multi-tenant de personas, proyectos, price books y billing |
| **Atributos clave** | nombre, tipo (estudio/constructora/particular), país, moneda base, plan, límites |
| **Relaciones** | 1—* UserMembership; 1—* Project; 1—* PriceBook; 1—* Supplier |
| **Cardinalidad** | Raíz tenant |

**Observación:** El “studio” actual se eleva a Organization con subtipos y políticas.

#### User

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Identidad humana o servicio |
| **Atributos clave** | email, nombre, locale, timezone, credenciales, preferencias UX |
| **Relaciones** | *—* Organization vía Membership; 1—* AIConversation; 1—* Audit events |
| **Cardinalidad** | N:M con orgs |

#### Membership / Role

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Autorización y alcance |
| **Atributos clave** | role (Owner, Admin, Estimator, SiteManager, Viewer, ClientGuest), scopes |
| **Relaciones** | User N—1 Org; opcional scope por Project |
| **Cardinalidad** | N:M con metadatos |

#### Project

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Unidad de trabajo = una obra / encargo |
| **Atributos clave** | nombre, tipología, ubicación, cliente, estado lifecycle, moneda, unidad sistema |
| **Relaciones** | N—1 Org; 1—* Building; 1—* Document; 1—* Scenario; 1—0..1 Lot |
| **Cardinalidad** | Centro gravitacional del producto |

#### Building

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Edificio o cuerpo edilicio dentro del predio |
| **Atributos clave** | nombre, huella, tipología estructural, cantidad de niveles |
| **Relaciones** | N—1 Project; 1—* Level; 1—* System |
| **Cardinalidad** | 1..* por project típico (casas pueden ser 1) |

#### Level

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Planta / nivel altimétrico |
| **Atributos clave** | índice, nombre, cota, altura libre, plano fuente |
| **Relaciones** | N—1 Building; 1—* Space; 1—* Wall; 1—* FloorFinish |
| **Cardinalidad** | 1..* |

#### Space / Ambiente

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Local usable (living, baño, cocina, local comercial) |
| **Atributos clave** | nombre, uso, área, perímetro, criticidad húmeda, ocupación |
| **Relaciones** | N—1 Level; *—* Wall (bound); 1—* FloorFinish; links a MEP terminals |
| **Cardinalidad** | 0..* (puede haber zonas no ambientadas al inicio) |

#### Wall

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Muro / tabique con geometría y sistema constructivo |
| **Atributos clave** | longitud, altura, espesor, tipo (exterior/interior), sistema, confianza |
| **Relaciones** | N—1 Level; *—* Space; 1—* Opening; → MaterialTakeoff lines |
| **Cardinalidad** | núcleo del cómputo de albañilería |

#### Opening

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Puerta, ventana, paso, vano |
| **Atributos clave** | tipo, ancho, alto, antepecho, carpintería ref, confianza |
| **Relaciones** | N—1 Wall (o Space); → carpintería / cost items |
| **Cardinalidad** | 0..* por muro |

#### FloorFinish

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Solado / terminación de piso |
| **Atributos clave** | área, material, junta, zócalo, sustrato |
| **Relaciones** | N—1 Space o Level; → takeoff |
| **Cardinalidad** | 0..* |

#### Ceiling / Roof

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Cielorraso y/o cubierta |
| **Atributos clave** | área, pendiente, sistema, aislación, cielorraso bajo cubierta |
| **Relaciones** | N—1 Building/Level; → takeoff + estructura ligera |
| **Cardinalidad** | 0..* |

#### Lot / Terrain

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Predio, topografía simplificada, movimientos de suelo |
| **Atributos clave** | superficie, perímetro, pendientes, rellenos/cortes estimados |
| **Relaciones** | 1—0..1 Project; → landscaping / riego / cercos |
| **Cardinalidad** | opcional pero valioso en residencial |

#### Structure (StructureElement)

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Elementos estructurales simplificados (bases, columnas, vigas, losas) |
| **Atributos clave** | tipo, dimensiones, hormigón, acero estimado, confianza |
| **Relaciones** | N—1 Building/Level; → módulo hormigón armado |
| **Cardinalidad** | fase 3+ para madurez alta |

### 3.3 Entidades MEP y sistemas

#### System (genérico)

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Contenedor de un sistema técnico |
| **Atributos clave** | disciplina, norma ref, estado diseño, completeness |
| **Relaciones** | N—1 Building/Project; 1—* SystemSegment; 1—* Terminal/Fixture |

#### ColdWater / HotWater

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Redes de agua fría/caliente |
| **Atributos clave** | longitud por diámetro, artefactos, bomba/termotanque, pérdidas |
| **Relaciones** | terminals en Spaces; materiales caños/fittings |

#### Sewage

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Desagües cloacales / pluviales |
| **Atributos clave** | tramos, pendientes mínimas, cámaras, ventilaciones |
| **Relaciones** | Spaces húmedos; Lot connection |

#### Electrical

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Potencia, circuitos, iluminación, tomas |
| **Atributos clave** | puntos, metros de cable, tableros, potencia estimada |
| **Relaciones** | Spaces; Lighting; Domótica futura |

#### Gas

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Distribución de gas |
| **Atributos clave** | tramos, artefactos, reguladores, ventilaciones |
| **Relaciones** | Spaces; compliance flags |

#### HVAC

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Climatización |
| **Atributos clave** | carga térmica simplificada, equipos, conductos/cañerías refrigerante |
| **Relaciones** | Spaces; Electrical load |

#### FireProtection

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Detección / extinción simplificada |
| **Atributos clave** | detectores, matafuegos, hidrantes, señalética |
| **Relaciones** | Building use; normative checklist |

### 3.4 Costos, proveedores y compras

#### MaterialTakeoff

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Líneas de cómputo agregables |
| **Atributos clave** | material, cantidad, unidad, merma, origen entidad, confianza |
| **Relaciones** | *—* Elements/Systems; 1—* CostItem mapping |

#### CostItem

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Ítem presupuestario (material, mano de obra, equipo, subcontrato) |
| **Atributos clave** | código, descripción, cantidad, PU, moneda, fórmula, fecha precio |
| **Relaciones** | N—1 Project/Budget; → PriceBookEntry; → ScheduleActivity |

#### Supplier

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Proveedor / corralón / instalador |
| **Atributos clave** | nombre, región, contacto, lead time, confiabilidad |
| **Relaciones** | Org/Project; PriceBook entries; POs |

#### PriceBook

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Lista de precios versionada |
| **Atributos clave** | región, moneda, vigencia, fuente (manual/scrape/partner), índice inflación |
| **Relaciones** | Org o Platform; 1—* PriceBookEntry |

#### PurchaseOrder

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Orden de compra |
| **Atributos clave** | estado, supplier, líneas, total, entrega, vínculo a takeoff |
| **Relaciones** | Project; CostItems; Progress (recibido) |

#### ScheduleActivity

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Actividad de planificación |
| **Atributos clave** | WBS, duración, predecesoras, recurso, % complete |
| **Relaciones** | CostItems / Systems; Certification milestones |

### 3.5 Obra, progreso y certificación

#### ProgressSnapshot

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Foto del avance en un momento |
| **Atributos clave** | fecha, % por capítulo/entidad, evidencia documental, autor |
| **Relaciones** | ProjectVersion baseline; fotos/Documents |

#### Certification

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Certificación de avance / pago |
| **Atributos clave** | período, montos, retenciones, estado aprobación, PDF export |
| **Relaciones** | ProgressSnapshots; Contract terms (futuro) |

### 3.6 Documentos, IA y auditoría

#### Document

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Plano, foto, PDF, planilla, contrato |
| **Atributos clave** | tipo, storage URI, hash, linked level, perception status |
| **Relaciones** | Project; PerceptionJob; Evidence de Progress |

#### AuditTrail

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Bitácora inmutable de acciones |
| **Atributos clave** | actor, acción, entity ref, before/after, timestamp, ip/device |
| **Relaciones** | Todo lo sensible |

#### AIConversation

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Hilos de chat con contexto de proyecto |
| **Atributos clave** | messages, tools used, citations, feedback user |
| **Relaciones** | Project; User; retrieved entities |

#### Scenario / Variant

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Alternativa de diseño/sistema/costo |
| **Atributos clave** | nombre, branch del MDO, delta $, delta plazo, elegida? |
| **Relaciones** | Project; baselines comparables |

### 3.7 Cardinalidades y reglas

| Relación | Cardinalidad | Regla de integridad conceptual |
|----------|--------------|--------------------------------|
| Org → Project | 1..* | Todo project pertenece a un tenant |
| Project → Building | 1..* | Al menos un building lógico |
| Level → Wall | 0..* | Walls sin space permitido en borrador |
| Wall → Opening | 0..* | Opening no puede exceder geometría muro sin flag |
| Space ↔ Wall | N..M | Topología debe cerrar para baseline comercial |
| Takeoff → CostItem | 1..* | Puede haber MO + materiales |
| CostItem → PriceBookEntry | 0..1 | Si falta, marcar precio estimado |
| Scenario → Project | N..1 | Scenarios no borran baseline |
| Certification → Progress | 1..* | Certifica subconjunto aprobado |
| AIConversation → Project | N..1 | Contexto siempre anclado |

#### Tabla resumen de entidades (checklist de diseño)

| # | Entidad | Capa | Fase mínima |
|---|---------|------|-------------|
| 1 | Organization/Studio | Tenant | 1 |
| 2 | User | Tenant | 1 |
| 3 | Membership/Role | Tenant | 1 |
| 4 | Project | Core | 1 |
| 5 | Building | MDO | 2 |
| 6 | Level | MDO | 2 |
| 7 | Space/Ambiente | MDO | 2 |
| 8 | Wall | MDO | 1→2 |
| 9 | Opening | MDO | 1→2 |
| 10 | FloorFinish | MDO | 1→2 |
| 11 | Ceiling/Roof | MDO | 1→2 |
| 12 | Lot/Terrain | MDO | 2 |
| 13 | StructureElement | MDO | 3 |
| 14 | System (+ MEP) | MDO | 1→3 |
| 15 | MaterialTakeoff | Cost | 1 |
| 16 | CostItem | Cost | 1 |
| 17 | Supplier | Procurement | 3→4 |
| 18 | PriceBook | Cost | 1→2 |
| 19 | ScheduleActivity | Time | 3→4 |
| 20 | PurchaseOrder | Procurement | 4 |
| 21 | ProgressSnapshot | Site | 4 |
| 22 | Certification | Site | 4 |
| 23 | Document | Cross | 1 |
| 24 | AuditTrail | Cross | 1→2 |
| 25 | AIConversation | Intelligence | 2 |
| 26 | Scenario/Variant | Intelligence | 2→3 |

---

## 4. Funcionalidades (catálogo exhaustivo)

> Ideación amplia. No todo se construye; todo informa priorización. Cada ítem: 1–2 líneas de intención de producto.

### 4.1 Cuantificación

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| Q01 | Takeoff desde plano coloreado | Mantener y endurecer el wedge actual: HSV + reglas → cantidades por disciplina. |
| Q02 | Revisión geométrica asistida | Overlay de polígonos detectados con edición de vértices y recompute. |
| Q03 | Confidence heatmap | Mapa visual de confianza sobre el plano para priorizar revisión humana. |
| Q04 | Ambientación automática | Propuesta de espacios a partir de cerramientos y textos OCR. |
| Q05 | Biblioteca de tipologías de muro | Plantillas (ladrillo, block, drywall, steel) con fórmulas de consumo. |
| Q06 | Mermas configurables | Políticas de merma por material, región y práctica de obra. |
| Q07 | Cómputo diferencial | Diff de cantidades entre versiones de plano o escenarios. |
| Q08 | Medición manual override | Herramientas de polyline/área cuando la percepción falla. |
| Q09 | OCR de cotas robustecido | Pipeline de cotas con validación cruzada contra escala. |
| Q10 | Escala asistida | Detección/confirmación de escala con reglas anti-absurdo (puerta 2 km). |
| Q11 | Capas por disciplina | Separar muros, pisos, MEP visualmente en el explorer. |
| Q12 | Validación topológica | Detectar muros abiertos, ambientes no cerrados, solapes imposibles. |
| Q13 | Importación multi-plano | Varias plantas/cubierta/instalaciones en un mismo Project. |
| Q14 | Plantillas tipológicas | Casa PH, duplex, local comercial: checklists de cómputo mínimo. |
| Q15 | Quantities API interna | Cualquier módulo consulta cantidades canónicas del MDO. |

### 4.2 Estimación / presupuestos

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| E01 | Presupuesto por capítulos | Estructura tipo computo-presupuesto con subtotales. |
| E02 | Dual moneda ARS/USD | Visualización y congelamiento de tipo de cambio por versión. |
| E03 | Indexación inflacionaria | Actualizar precios por índice o canasta propia. |
| E04 | Mano de obra regional | Tablas de jornales / rendimientos por zona. |
| E05 | Costos indirectos y utilidad | Porcentajes configurables, gastos generales, IVA. |
| E06 | Escenarios what-if | Cambiar sistema constructivo y ver delta $ / plazo. |
| E07 | Presupuesto cliente vs interno | Dos vistas: comercial limpia y analítica interna. |
| E08 | Supuestos explícitos | Lista de assumptions exportable junto al presupuesto. |
| E09 | Rangos P50/P80 | Presentar incertidumbre cuando confidence global es media. |
| E10 | Comparador de ofertas | Side-by-side de 2–3 escenarios para el comitente. |
| E11 | Histórico de precios usados | Linaje de cada PU: fecha, fuente, supplier. |
| E12 | Plantillas de presupuesto | Packs por tipología y calidad de terminación. |
| E13 | Export Excel/PDF profesional | Salidas presentables y editables controladamente. |
| E14 | Firma de presupuesto | Freeze + hash + link de aceptación del cliente. |
| E15 | Alertas de precio viejo | Flags si un ítem supera N días sin actualización. |

### 4.3 Planificación / scheduling

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| S01 | WBS desde capítulos | Generar actividades sugeridas a partir del presupuesto. |
| S02 | Duraciones por rendimiento | Estimar días según cantidades y cuadrillas. |
| S03 | Dependencias simples | Finish-to-start para camino crítico ligero. |
| S04 | Gantt operable | Vista temporal con hitos de certificación. |
| S05 | Calendario de obra | Feriados locales, lluvia (proxy), restricciones. |
| S06 | Recursos y cuadrillas | Asignación básica de equipos internos/subcontratos. |
| S07 | Look-ahead 2–3 semanas | Plan corto para jefes de obra. |
| S08 | Baseline de plazo | Congelar schedule v1 y medir desvíos. |
| S09 | Impacto de extras | Insertar adicional y recalcular plazo/costo. |
| S10 | Export a MS Project/CSV | Interop sin pretender ser Primavera. |

### 4.4 Certificaciones y progreso

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| C01 | Snapshot de avance | Cargar % por capítulo/entidad con fecha. |
| C02 | Evidencia fotográfica | Adjuntar fotos geolocalizadas/etiquetadas al avance. |
| C03 | Certificación periódica | Generar certificado de avance con retenciones. |
| C04 | Comparativo contractual | Avance vs curva planificada vs cobrado. |
| C05 | Adicionales y deducciones | Flujo de change orders ligado al MDO. |
| C06 | Aprobaciones multi-rol | Workflow estimador → director → cliente. |
| C07 | Historial de certificaciones | Serie temporal auditable. |
| C08 | Anticipos y descuentos | Manejo financiero básico de certificados. |
| C09 | Export legalmente usable | PDF estructurado para Argentina/LATAM. |
| C10 | Alertas de sobre-certificación | Detectar % inconsistentes con evidencias. |

### 4.5 Procurement / compras

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| P01 | Lista de materiales viva | BOM desde takeoff con mermas. |
| P02 | Agrupar por proveedor | Sugerir splitting de OC. |
| P03 | RFQ simple | Pedir cotización a suppliers del directorio. |
| P04 | Purchase Orders | Emitir OC con estados (borrador→enviada→recibida). |
| P05 | Recepción parcial | Actualizar stock/avance de compra. |
| P06 | Lead time planning | Conectar fechas de compra al schedule. |
| P07 | Alternativas equivalentes | Sugerir material sustituto ante falta de stock. |
| P08 | Umbrales de aprobación | OC grandes requieren rol superior. |
| P09 | Historial de compras por obra | Aprendizaje de precios reales pagados. |
| P10 | Integración marketplace | Ver sección 4.14; bridge a partners. |

### 4.6 Control financiero

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| F01 | Cashflow de obra | Curva de egresos planificados vs reales. |
| F02 | Presupuesto comprometido | Committed vs spent vs forecast. |
| F03 | Alertas de desvío | Umbrales % por capítulo. |
| F04 | Multi-moneda consolidada | Vista gerencial ARS/USD. |
| F05 | Costos no contemplados | Registro de imprevistos con causa. |
| F06 | Rentabilidad por proyecto | Margen estimado vs real. |
| F07 | Dashboard estudio | Portafolio de obras y salud financiera. |
| F08 | Export contable ligero | CSV para sistemas externos (no ERP completo). |
| F09 | Escenarios de inflación | Stress test de presupuesto a 3/6/12 meses. |
| F10 | Retenciones y garantías | Tracking básico de fondos retenidos. |

### 4.7 Comparación de sistemas constructivos

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| X01 | Ladrillo vs Steel Frame | Comparar costo, plazo, mano de obra, prestaciones. |
| X02 | Wood Frame pack | Tipología madera con supuestos climáticos. |
| X03 | Hormigón vs mampostería | Trade-offs estructurales simplificados. |
| X04 | Cubiertas alternativas | Chapa, teja, membrana, losa. |
| X05 | Score multicriterio | Costo, plazo, sustentabilidad, mantenimiento, confort. |
| X06 | Narrativa para cliente | Texto auto-generado con citations al modelo. |
| X07 | Sensibilidad de precio | Qué material mueve más el total. |
| X08 | Biblioteca de sistemas ARQ-IA | Packs curados LATAM. |
| X09 | Bloqueo de supuestos | Congelar hipótesis al presentar comparación. |
| X10 | Recomendación asistida | Agente sugiere, humano elige. |

### 4.8 Stock e inventario de obra

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| K01 | Depósito de obra | Stock mínimo por material crítico. |
| K02 | Entradas desde OC | Integración recepción→stock. |
| K03 | Consumo teórico vs real | Desvíos de merma. |
| K04 | Transferencias entre obras | Para constructoras multi-proyecto. |
| K05 | Alertas de quiebre | Material que frena camino crítico. |
| K06 | Inventario móvil | Carga desde celular en obrador. |
| K07 | Materiales sobrantes | Reutilización y valuación. |
| K08 | Mermas excepcionales | Registro de robo/lluvia/rotura. |

### 4.9 Seguimiento de obra (site tracking)

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| T01 | Bitácora digital | Notas diarias ligadas a espacios/sistemas. |
| T02 | Punch list / pendientes | Defectos y terminaciones. |
| T03 | Checklist de calidad | Por etapa y disciplina. |
| T04 | Clima y novedades | Registro simple que explica desvíos. |
| T05 | Asistencia de cuadrillas | Presentismo básico (no HRIS). |
| T06 | Seguridad e incidentes | Log mínimo de eventos. |
| T07 | Visitas de dirección | Formulario + fotos + acciones. |
| T08 | Mapa de avance visual | Colorear ambientes por % complete. |

### 4.10 Residuos y sustentabilidad

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| W01 | Estimación de residuos | m³/ton por tipología y fase. |
| W02 | Plan de gestión RCD | Clasificación básica. |
| W03 | Huella simplificada | CO2e proxy por materiales dominantes. |
| W04 | Comparar sistemas por impacto | Extensión de X05. |
| W05 | Proveedores con reciclado | Tags en PriceBook. |
| W06 | Reportes municipales | Plantillas según jurisdicción (fase larga). |

### 4.11 Planificación de anteproyecto

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| A01 | Estimación temprana por m² | Antes de plano detallado, con rangos anchos. |
| A02 | Brief del cliente | Captura de programa arquitectónico. |
| A03 | Chequeo de factibilidad $ | “¿Entra en el presupuesto objetivo?” |
| A04 | Generación de premisa de cómputo | Defaults tipológicos editables. |
| A05 | Roadmap de definición | Qué falta medir para bajar incertidumbre. |

### 4.12 Reportes y BI

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| R01 | Dashboard de proyecto | Salud cómputo/costo/plazo/confianza. |
| R02 | Portfolio estudio | Comparar obras. |
| R03 | Benchmark anónimo | m² de muro / m² cubierto vs red ARQ-IA. |
| R04 | Reporte ejecutivo PDF | Una página para comitente. |
| R05 | BI de precios | Evolución de canasta de materiales. |
| R06 | Funnel de revisión | Tiempo a baseline comercial. |
| R07 | Uso de módulos | Product analytics internos. |
| R08 | Export datalake (Enterprise) | Para BI del cliente. |

### 4.13 Colaboración

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| L01 | Roles y permisos granulares | Ver matriz Enterprise. |
| L02 | Comentarios en entidades | Thread sobre muro #12. |
| L03 | Mentions y tareas | Asignar revisión de OCR dudoso. |
| L04 | Guest client view | Vista limitada al presupuesto/scenarios. |
| L05 | Activity feed | Qué cambió ayer. |
| L06 | Conflict resolution | Dos editores en mismo level. |
| L07 | Plantillas de estudio | Standards internos reutilizables. |
| L08 | Multi-proyecto carpetas | Organización por cliente/año. |

### 4.14 Compliance Argentina / LATAM

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| N01 | Unidades y nomenclatura local | m², ml, global, ítems tipo Cype/AR. |
| N02 | IVA y cargas | Config tributaria básica de presupuesto. |
| N03 | Etiquetas de instalación gas/elec | Flags de documentación requerida. |
| N04 | Accesibilidad (checklist) | No simulación normativa completa. |
| N05 | Incendio checklist tipológico | Según uso/superficie aproximada. |
| N06 | Localización de feriados/obra | Calendarios AR + expansión. |
| N07 | Contratos tipo (plantillas) | Texto asistido, no asesoría legal. |
| N08 | Multi-país tax packs | Extensión gradual. |

### 4.15 Marketplace

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| M01 | Directorio de proveedores | Por región y categoría. |
| M02 | Price feeds partners | Actualización de listas. |
| M03 | Servicios de cómputo humano | Overflow cuando confidence baja. |
| M04 | Instaladores verificados | Match por disciplina y zona. |
| M05 | Plantillas premium | Sistemas constructivos de terceros. |
| M06 | Lead-gen controlado | Opt-in; no spamear al usuario. |
| M07 | Ratings post-obra | Calidad de proveedor observada. |
| M08 | API comercial | Para corralones Enterprise. |

### 4.16 Mobile

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| U01 | App de visita de obra | Fotos + avance + bitácora. |
| U02 | Aprobaciones push | Certificados y OC. |
| U03 | Consulta de cantidades offline | Cache del MDO esencial. |
| U04 | Captura de plano en campo | Foto + cola de procesamiento. |
| U05 | Voice notes → bitácora | Dictado estructurado. |
| U06 | QR de ambientes | Etiquetar espacios físicos. |

### 4.17 Integraciones

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| I01 | Object storage planos | Salir de blobs en DB. |
| I02 | Mercado Pago billing | Mantener y sofisticar. |
| I03 | Resend / email workflows | Notificaciones de obra. |
| I04 | Google Drive/Dropbox import | Traer planos. |
| I05 | Webhooks Enterprise | Eventos de presupuesto/certificación. |
| I06 | Contabilidad CSV/API | Xero/local según país. |
| I07 | CAD export light | DXF/IFC light opcional fase tardía. |
| I08 | Slack/Teams alerts | Para estudios medianos. |
| I09 | SSO / SAML | Enterprise. |
| I10 | API pública versionada | Ecosistema fase 5. |

### 4.18 Ideas adicionales (ampliación a 80+)

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| Z01 | Detector de inconsistencias de leyenda de color | Valida que el protocolo de pintado se cumplió. |
| Z02 | Simulador de cambio de altura de entrepiso | Recalcula muros/instalaciones verticales. |
| Z03 | Pack baños húmedos | Cómputo intensivo de locales húmedos. |
| Z04 | Pack cocinas | Mesadas, revestimientos, MEP asociados. |
| Z05 | Estimador de andamios/apuntalamiento | Proxi de costos de seguridad e instalaciones temporarias. |
| Z06 | Generador de pliegos de especificaciones | Texto técnico desde sistemas elegidos. |
| Z07 | Control de versiones de planos con OCR de sello | Identificar “Rev C”. |
| Z08 | Asistente de reunión | Resumen de cambios del modelo desde la última visita. |
| Z09 | Modo enseñanza | Para universidades / talleres de cómputo. |
| Z10 | Sandbox de fórmulas | Autores de estudio crean reglas sin code deploy. |
| Z11 | Gemelo de costos regionales | Comparar AMBA vs interior automáticamente. |
| Z12 | Priorizador de compras críticas | Qué comprar primero según lead time + camino crítico. |
| Z13 | Detector de scope creep | Diff cualitativo + cuantitativo para cliente. |
| Z14 | Biblioteca de detalles constructivos | No CAD: parámetros que afectan cómputo. |
| Z15 | Modo “particular informado” | UX simplificada para dueño de obra. |
| Z16 | Firma digital de certificación | Integración con proveedores de firma. |
| Z17 | Conciliación de factura vs OC | Control 3-way light. |
| Z18 | Panel de riesgos de obra | Lista viva de riesgos $ / plazo. |
| Z19 | Traducción ES↔PT de reportes | Expansión Brasil/PT. |
| Z20 | Copiloto de presentación | Genera slides del presupuesto con citations. |
| Z21 | Auditoría de calidad de cómputo | Scorecard pre-envío a cliente. |
| Z22 | Simulación de lluvia de ideas de extras | Impacto de pedidos del comitente en vivo. |
| Z23 | Catálogo de carpintería paramétrica | Ventanas/puertas con PUs. |
| Z24 | Módulo acústica básico | Superficies y recomendaciones, no simulación FEM. |
| Z25 | Módulo demolición | Ítems de retiro y disposición. |

**Conteo del catálogo:** 15+15+10+10+10+10+10+8+8+6+5+8+8+8+8+6+10+25 = **180** ideas de funcionalidad (el plan exige ≥80; se supera a propósito para alimentar priorización).

### 4.19 Criterios de priorización de funcionalidades

| Criterio | Peso relativo | Pregunta |
|----------|---------------|----------|
| Alinea a MDO | Alto | ¿Enriquece el modelo digital? |
| Aumenta confianza | Alto | ¿Baja incertidumbre o la hace visible? |
| Monetizable | Medio-Alto | ¿Mueve upgrade Pro/Enterprise? |
| Diferenciador LATAM | Alto | ¿Incumbente global no lo hace bien aquí? |
| Complejidad | Inverso | ¿Es un pozo de años? |
| Dependencias | Alto | ¿Desbloquea chat/obra/compras? |

```
PRIORIDAD ESTRATÉGICA (mapa)
                     Alto impacto
                          │
   Chat+MDO+Confidence ───┼─── Price intelligence LATAM
   Escenarios sistemas ───┼─── Certificación/Avance
                          │
 Bajo effort ─────────────┼─────────────── Alto effort
                          │
   Export PDF polish ─────┼─── IFC/BIM completo
   Templates tipológicos ─┼─── ERP financiero total
                          │
                     Bajo impacto
```

---

## 5. IA (sobre el motor, nunca reemplazándolo)

### 5.1 Arquitectura de tres capas

```
┌────────────────────────────────────────────────────────────────────────────┐
│ L3  INTELLIGENCE LAYER                                                     │
│     LLM agents · chat · redacción · escenarios narrativos · price intel    │
│     (tool calling + RAG; sin inventar geometría)                           │
└───────────────────────────────▲────────────────────────────────────────────┘
                                │ lee / sugiere / explica
┌───────────────────────────────┴────────────────────────────────────────────┐
│ L2  DIGITAL TWIN LAYER                                                     │
│     MDO versionado · takeoff · costos · schedule · confidence · audit      │
└───────────────────────────────▲────────────────────────────────────────────┘
                                │ entidades + scores
┌───────────────────────────────┴────────────────────────────────────────────┐
│ L1  PERCEPTION LAYER                                                       │
│     OpenCV HSV · OCR · (futuro) ML assist segmentación/detección           │
│     salida determinista + incertidumbre                                    │
└────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Capa de percepción (L1)

| Componente | Rol hoy | Evolución |
|------------|---------|-----------|
| HSV color protocol | Core | Mantener + validadores de protocolo |
| Tesseract OCR | Frágil | Mejorar + ML OCR assist + HITL |
| Reglas geométricas | Core | Expandir topología |
| ML segmentation (futuro) | N/A | Asistente, nunca dictador silencioso |
| Human corrections | Parcial | Feedback loop → dataset propietario |

**Observación:** Cada corrección humana es entrenamiento futuro. El producto debe capturar labels sin fricción.

### 5.3 Capa twin (L2)

Es la **única fuente de verdad** para L3. Si L3 no puede citar una entidad L2, no afirma cantidades.

### 5.4 Capa intelligence (L3) — casos de uso

| Caso | Input | Output | Guardrail |
|------|-------|--------|-----------|
| Detección de anomalías | MDO + reglas | Lista de inconsistencias | No auto-fix |
| Sugerencia de sistema | Tipología + presupuesto objetivo | Top 3 escenarios | Humano elige |
| Explicación de ítem | CostItem / Wall | Narrativa con citations | Citar o callar |
| Simulación de escenario | Parámetros | Delta $ / plazo | Usa motor, no inventa |
| Price intelligence | PriceBooks + mercado | Alertas y sustitutos | Fuentes fechadas |
| Redacción documental | Modelo + plantilla | Pliego/presupuesto notes | Disclaimer legal |
| Asistente de revisión | Heatmap confidence | Plan de revisión óptimo | No ocultar rojos |
| Resumen ejecutivo | Proyecto | 1-pager | Marcar estimaciones |

### 5.5 Agentes conceptuales (no implementación)

| Agente | Mandato | Tools conceptuales |
|--------|---------|--------------------|
| Quant Auditor | Encontrar huecos e inconsistencias | query_entities, topology_check |
| Cost Copilot | Explicar y stress-testear costos | pricebook_lookup, recompute_cost |
| Scenario Planner | Armar variantes | clone_scenario, apply_system_pack |
| Site Assistant | Interpretar avance vs baseline | progress_diff, photo_caption |
| Docs Scribe | Redactar con plantillas | render_template, cite |
| Procurement Scout | Armar listas y OC sugeridas | bom_export, supplier_rank |

### 5.6 Guardrails

1. **No geometry from LLM:** el LLM no dibuja muros ni inventa ml.
2. **Citation required** para afirmaciones numéricas.
3. **Uncertainty passthrough:** si L1/L2 tienen score bajo, L3 lo declara.
4. **Role-aware answers:** un ClientGuest no ve margen interno.
5. **Action permissions:** tools que mutan requieren confirmación.
6. **Prompt injection defense** sobre documentos subidos.
7. **PII minimization** en logs de conversación.
8. **Eval harness continuo** con golden questions por tipología.

### 5.7 Human-in-the-loop

| Decisión | ¿IA puede proponer? | ¿IA puede ejecutar sola? |
|----------|---------------------|--------------------------|
| Corregir geometría menor | Sí | No (salvo política experimental interna) |
| Cambiar sistema constructivo | Sí | No |
| Publicar presupuesto a cliente | Sí (draft) | No |
| Emitir OC | Sí | No |
| Certificar avance | Sí | No |
| Reordenar schedule | Sí | Condicional (sandbox) |
| Responder chat informativo | Sí | Sí, con citations |

### 5.8 Qué NO automatizar

- Dictamen estructural/legal/normativo vinculante.
- Firma de certificación.
- Sustitución silenciosa de materiales críticos de seguridad.
- “Precio final cerrado” cuando confidence global < umbral.
- Selección de proveedor con conflicto de interés oculto del marketplace.
- Borrado de audit trail.
- Entrenar modelos del cliente sin consentimiento (Enterprise data).

### 5.9 Estrategia de datos para IA

| Dataset | Origen | Uso |
|---------|--------|-----|
| Planos coloreados + labels | Uso producto + correcciones | Mejorar percepción |
| Entidades MDO anónimas | Proyectos opt-in | Benchmarks |
| Fórmulas AR | Expertos + estudios partner | Motor determinista |
| Series de precios | Partners + usuarios | Price intel |
| Conversaciones feedback | Thumbs + correcciones | Eval de chat |

### 5.10 Posicionamiento honesto de “IA”

Mensaje externo recomendado:
> “Usamos visión por computadora y un modelo digital de tu obra. La IA te explica, audita y simula sobre esos datos — no inventa metros.”

---

## 6. Chat inteligente

### 6.1 Diseño general

```
Usuario ──▶ Chat UI ──▶ Orchestrator
                           │
                           ├─▶ Retriever (RAG): MDO · PriceBook · Fórmulas · Docs
                           ├─▶ Tool Router: get_quantity · get_cost · diff_scenario · ...
                           ├─▶ Policy Guard: rol · disclaimer · citation check
                           └─▶ Response Composer: texto + citations + widgets
```

### 6.2 RAG — corpus

| Corpus | Contenido | Freshness |
|--------|-----------|-----------|
| MDO entities | Muros, espacios, sistemas, takeoff | Tiempo real |
| Price books | PUs y vigencia | Horas/días |
| Formula library | Rendimientos y reglas AR | Versionada |
| Project docs | Memorias, notas, PDFs | Al indexar |
| Playbooks ARQ-IA | Cómo interpretar módulos | Release notes |

### 6.3 Tool calling conceptual

| Tool | Propósito |
|------|-----------|
| `list_spaces` | Ambientes del nivel |
| `get_wall_quantities` | ml/m²/consumos muro |
| `get_system_takeoff` | MEP por disciplina |
| `get_cost_breakdown` | Capítulos $ |
| `compare_scenarios` | Deltas |
| `get_confidence_issues` | Rojas/amarillas |
| `explain_cost_item` | Linaje de un ítem |
| `simulate_param_change` | What-if controlado |
| `draft_client_summary` | Texto comercial |
| `create_task` | Pedir revisión humana |

### 6.4 Tipos de pregunta y diálogos ejemplo

#### Tipo A — Cantidades directas

**Usuario:** ¿Cuántos m² de muro interior tengo en planta baja?  
**ARQ-IA:** Según el modelo, planta baja suma **142,3 m²** de muro interior (entidades muro #12–#48), confianza media-alta **0,86**. Excluye tabiques propuestos en escenario “Steel”.  
**Citation:** `Wall[level=PB, type=interior]`.

#### Tipo B — Costos

**Usuario:** ¿Qué capítulo más me encarece si sube 20% el hierro?  
**ARQ-IA:** El capítulo Estructura/Herrería asociada representa **18%** del total baseline. Un +20% en hierro impacta **+3,6%** del presupuesto (simulación scenario tmp). Fuentes de PU: PriceBook AMBA 2026-07-15.

#### Tipo C — Explicación

**Usuario:** ¿Por qué el baño suite sale tan caro?  
**ARQ-IA:** Tres drivers: (1) revestimientos húmedos 28 m², (2) kit sanitario premium, (3) densidad MEP. Detalle con links a Space #baño-suite.

#### Tipo D — Anomalías

**Usuario:** ¿Hay algo raro en el cómputo?  
**ARQ-IA:** Sí: 2 ambientes sin solado; 1 ventana con OCR de cota inconsistente (±35%); gas sin ventilación asociada. ¿Creo tareas de revisión?

#### Tipo E — Escenarios

**Usuario:** Pasá la casa a Steel Frame y contame diferencia.  
**ARQ-IA:** Creé escenario “SF-A”. Delta costo **-6% a +4%** según pack de aislación; plazo estructura **-12 días** estimados. ¿Querés ver score multicriterio?

#### Tipo F — Obra

**Usuario:** ¿Cuánto certificamos este mes vs lo planificado?  
**ARQ-IA:** Certificación agosto = **22%** acumulado vs **25%** planificado (−3 pp). Capítulos atrasados: Revoques y Carpintería. Evidencias: 14 fotos.

#### Tipo G — Compras

**Usuario:** Armame la lista de compras críticas para las próximas 3 semanas.  
**ARQ-IA:** Prioridad: cemento, hierros Ø8/12, caños agua Ø20/25, aberturas YA pedidas (lead 21 días). OC sugeridas: 2 proveedores.

#### Tipo H — Cliente / narrativa

**Usuario:** Redactá un párrafo para el cliente explicando el aumento.  
**ARQ-IA:** Draft + disclaimer: estimado no certificado; basado en PriceBook fecha X; pendientes de revisión amarillos listados.

### 6.5 Memoria

| Tipo | Alcance | Notas |
|------|---------|-------|
| Turno | Mensaje | Contexto inmediato |
| Hilo | Conversación | Objetivos del usuario |
| Proyecto | MDO sticky notes | Preferencias (“siempre separar MO”) |
| Org | Glosario estudio | Nombres de capítulos propios |
| No memoria cruzada | Entre tenants | Aislamiento estricto |

### 6.6 Citations y disclaimers

Formato canónico:
> “Según cómputo **muro #12** (PB, living-comedor), longitud 4,20 m · confianza 0,91 · origen percepción 2026-08-01.”

Disclaimer estándar:
> “Valores de estimación. No constituyen certificación de avance ni oferta vinculante salvo que el usuario congele y firme una versión.”

### 6.7 Multi-idioma y voz

| Fase | Capacidad |
|------|-----------|
| 2 | ES completo |
| 3 | PT-BR lectura/respuesta |
| 4 | Voice input obra (mobile) |
| 5 | Voice walkthrough de visita |

### 6.8 UX del chat

- Respuestas cortas + “ver detalle”.
- Widgets: tablas, diffs, botones “crear escenario”.
- Siempre panel lateral de citations clickables.
- Modo escéptico: muestra dudas primero.
- Empty state educativo con preguntas sugeridas por tipología.

### 6.9 Métricas de calidad del chat

| Métrica | Objetivo cualitativo |
|---------|----------------------|
| Citation coverage | Casi todo número citado |
| Hallucination rate (eval) | Cercano a 0 en cantidades |
| Time-to-useful-answer | Segundos, no minutos |
| Escalation rate | % en que pide HITL |
| Thumbs-up profesional | Feedback de estimadores |

### 6.10 Anti-patrones del chat

- Responder con prosa larga sin números.
- Prometer precisión de certificación.
- Mezclar datos de otro proyecto.
- Ejecutar cambios sin confirmación.
- Usar tono “mágico” que oculte incertidumbre.

---

## 7. BIM simplificado propio

### 7.1 Qué es ARQ-BIM Lite

No es un clon de Revit. Es un **modelo topológico-cuantitativo** nativo SaaS:

- espacios y cerramientos,
- aberturas,
- sistemas como grafos,
- materiales y costos,
- tiempo y avance,
- confianza y linaje.

```
         Revit/Archicad                      ARQ-BIM Lite
    ┌─────────────────────┐            ┌─────────────────────┐
    │ Geometría 3D rica   │            │ Topología + qty     │
    │ Familias complejas  │            │ Sistemas grafo      │
    │ Documentación planos│            │ Cost/time nativos   │
    │ Curva aprendizaje   │            │ Minutos a valor     │
    │ Desktop-centric     │            │ SaaS + chat         │
    └─────────────────────┘            └─────────────────────┘
```

### 7.2 Ventajas estratégicas

| Ventaja | Por qué importa |
|---------|-----------------|
| Ownership del modelo | Moat de datos y UX |
| Velocidad | Wedge comercial intacto |
| SaaS-native | Colaboración y versionado web |
| LATAM workflows | Certificaciones, inflación, proveedores |
| Costo de adopción | El usuario no necesita BIM Manager |
| IA actionable | Entidades simples = mejor tool calling |

### 7.3 Incluir / excluir por año

| Año | Incluir | Excluir conscientemente |
|-----|---------|-------------------------|
| 1 | Entidades 2D cuantitativas, confidence, exports | Editor 3D completo |
| 2 | Explorer MDO, scenarios, chat, price books vivos | Familias paramétricas tipo Revit |
| 3 | Sistemas MEP grafo, packs constructivos, schedule light | Cálculo estructural firmable |
| 4 | Avance/certificación, POs, mobile site | Coordinación clash detection total |
| 5 | IFC light export, API ecosistema, marketplace | Ser “el CAD” |

### 7.4 IFC light (opcional tardío)

Objetivo: interoperar, no competir. Exportar espacios, muros simplificados, cantidades como property sets. Import parcial solo si hay ROI claro.

### 7.5 Principios de modelado Lite

1. **Preferir entidades útiles a fidelidad estética.**
2. **Toda geometría sirve a una cantidad o a una validación.**
3. **3D solo si reduce incertidumbre o vende claridad** — no por FOMO.
4. **El grafo de sistemas vale más que el render.**
5. **El usuario corrige significado (esto es baño), no solo polígonos.**

### 7.6 Experiencia del explorer BIM Lite

```
┌──────── Project ──────────────────────────────┐
│ Tree          │ Canvas / Plan     │ Inspector │
│ ▸ PB          │  [floor plan]     │ Wall #12  │
│   ▸ Living    │   spaces colored  │ L=4.20m   │
│   ▸ Cocina    │   confidence hue  │ conf 0.91 │
│ ▸ Sistemas    │                   │ takeoff…  │
│   ▸ Agua      │                   │ [chat]    │
└───────────────────────────────────────────────┘
```

---

## 8. Escalabilidad

### 8.1 Principio

Escalar **el cómputo de percepción** y **el grafo MDO** por separado. No todas las cuentas necesitan GPU. Todas necesitan isolation y costos predecibles.

### 8.2 Tiers de usuarios

| Tier | Usuarios concurrentes orientativos | Arquitectura dominante |
|------|------------------------------------|------------------------|
| T100 | ~100 | Monolito modular + cola simple |
| T1K | ~1.000 | Workers horizontales + object storage |
| T10K | ~10.000 | Multi-servicio · read replicas · CDN · cache |
| T100K | ~100.000 | Multi-región · tenancy duro · autoscaling · finops |

### 8.3 Tabla por capacidad

| Capacidad | T100 | T1K | T10K | T100K |
|-----------|------|-----|------|-------|
| API app | Single region | HA pair | Autoscale | Multi-region active-passive/active |
| Cola de percepción | Redis/RQ/basic | Managed queue | Particionada por tenant | Colas regionales |
| Storage planos | DB→Object storage migrado | S3-compatible | Lifecycle tiers | Cross-region replication selectiva |
| Postgres | Vertical | Primary+replica | Sharding lógico por tenant grandes | Partitioning + celulas |
| CDN/assets | Básico | Sí | Sí + image transforms | Global |
| Rate limits | Por IP/user | Por plan | Por org + fair use compute | Token buckets + créditos cómputo |
| Observability | Logs + métricas | Tracing | SLO burn rates | Platform ops 24/7 |
| ML assist GPU | No | Spot opcional | Pool compartido | Pools regionales |
| Tenancy | schema/row | row + quotas | noisy-neighbor controls | cell-based isolation Enterprise |
| Backup/DR | Diario | PITR | Multi-AZ | DR runbooks + RPO/RTO contractual |

### 8.4 Costo por compute (principios)

| Idea | Detalle |
|------|---------|
| Créditos de procesamiento | Cada plano/página consume créditos según MP |
| Cache de percepción | Reproceso solo si hash/params cambian |
| Async first | Nunca bloquear UX en jobs largos |
| Early rejection | Escala inválida / protocolo roto → fail barato |
| Spot GPU | Solo para colas batch no interactivas |
| FinOps dashboards | Costo/proyecto y costo/usuario Pro |

### 8.5 Multi-región LATAM → global

| Fase | Regiones | Motivo |
|------|----------|--------|
| 1 | 1 región (p.ej. us-east o latam sur) | Simplicidad |
| 2–3 | Residencia de datos Brasil/MX si vende Enterprise | Compliance + latency |
| 4–5 | Active-passive global | Expansión |

### 8.6 Límites de rate y abuso

- Free: cola low-priority + watermark.
- Pro: fair share.
- Enterprise: reserved concurrency.
- Detección de bots de scraping de price books.
- Quotas de chat tokens por plan.

### 8.7 Diagrama evolutivo

```
[T100]  App + API + DB + Worker
           │
           ▼
[T1K]   App ── Queue ── Workers N
         │ \               │
         │  \─ Object Store│
         └── DB + replica  │
           │
           ▼
[T10K]  Edge/CDN ── API gateway ── services
                      │     │
                   Queue   MDO service
                      │
                   GPU pool (opt)
           │
           ▼
[T100K] Cells per segment + multi-region control plane
```

### 8.8 Escalabilidad del producto (no solo infra)

| Riesgo de escala producto | Mitigación |
|---------------------------|------------|
| Soporte ahogado por dudas de cómputo | Chat + playbooks + confidence UX |
| Price books desactualizados | Partners + crowdsource + alertas |
| Enterprise custom forever | Packs configurables, no forks |
| Deuda de módulos mediocres | Madurez por fase (sección 9) |

---

## 9. Nuevos módulos

### 9.1 Filosofía de módulos

Un módulo ARQ-IA no es un micrositio aislado: es un **pack de entidades + fórmulas + UX de review + salidas de costo/tiempo** que escribe en el MDO.

Criterios para crear un módulo:
1. ¿Existe dolor de cómputo recurrente en LATAM?
2. ¿Podemos modelarlo con inputs disponibles (plano/parametría)?
3. ¿Mejora WQD o retención?
4. ¿Tiene precio/book y fórmulas defendibles?
5. ¿Podemos lanzarlo en madurez “útil” sin fingir ingeniería firmada?

### 9.2 Catálogo de módulos (tabla maestra)

| Módulo | Inputs principales | Outputs principales | Fase madurez |
|--------|--------------------|---------------------|--------------|
| Muros / albañilería (core) | Planos coloreados, alturas, tipología | ml, m², ladrillos/block, mezcla | Ya → Fase 1 endurecer |
| Pisos y aberturas (core) | Ambientes, vanos, tipologías | m² solados, unidades carpintería | Ya → Fase 1 |
| Agua fría/caliente (core) | Locales húmedos, artefactos | ml cañerías, fittings, equipos | Ya → Fase 2 grafo |
| Cloacas / desagües (core) | Locales, recorridos | ml, cámaras, ventilaciones | Ya → Fase 2 |
| Eléctrico (core) | Ambientes, puntos | cables, circuitos, tablero | Ya → Fase 2 |
| Cubiertas (core) | Huella, pendiente, sistema | m², aislación, zinguería | Ya → Fase 2 |
| Terreno (core) | Lote, cotas simples | movimiento suelos proxy, cercos | Ya → Fase 2 |
| Hormigón armado | Esquema estructural, luces, cargas tipológicas | m³ H°, kg acero, encofrado | Fase 3 |
| Steel Frame | Layout, paneles, entrepisos | perfiles, placas, anclajes, aislación | Fase 3 |
| Wood Frame | Layout, clima, especies | madera, fijaciones, barreras | Fase 3 |
| Pintura | Áreas netas muros/cielos | litros, manos, andamios proxy | Fase 2–3 |
| Paisajismo | Lote, zonas | tierra, especies, senderos | Fase 3–4 |
| Sanitarios / artefactos | Locales húmedos, calidad | unidades, grifería, accesorios | Fase 2 |
| Carpintería | Aberturas + placards | unidades, m² paños, herrajes | Fase 2–3 |
| Muebles / amoblamientos | Ambientes, brief | ml mesadas, módulos | Fase 3 |
| Iluminación | Ambientes, lux target tipológico | luminarias, circuitos | Fase 3 |
| Domótica | Escenarios, puntos eléctricos | nodos, cableado especial | Fase 4 |
| Energía solar | Cubierta útil, consumo proxy | paneles, inversores, estructura | Fase 3–4 |
| Piscinas | Geometría, tipo | excavación, revestimiento, equipo | Fase 4 |
| Riego | Paisaje, zonas | ml, aspersores, bomba | Fase 4 |
| Ascensores | Niveles, tipología edilicia | pozo, equipo, instalaciones | Fase 4–5 |
| Incendio | Uso, superficie | detectores, matafuegos, señalética | Fase 3–4 |
| Gas | Artefactos, recorridos | ml, reguladores, ventilación | Fase 3 |
| Climatización / HVAC | Ambientes, orientación proxy | equipos, cañerías/conductos | Fase 3–4 |
| Acústica | Usos sensibles | tratamientos superf., checklist | Fase 4 |
| Accesibilidad | Circulaciones, baños | checklist + ítems de adecuación | Fase 3–4 |
| Demoliciones | Estado existente, alcance | m³ retiro, disposición, ruido | Fase 3 |
| Movimiento de suelos | Topografía light, plataforma | corte/relleno, transporte | Fase 3 |
| Impermeabilización | Azoteas, locales húmedos | m² sistemas, detalles | Fase 2–3 |
| Aislación térmica | Envolvente, clima zona | m² aislantes, puentes térmicos proxy | Fase 3 |
| Fachadas | Elevaciones, sistema | m² revestimiento, subestructura | Fase 3–4 |
| Revoques / yesos | Muros netos | m², espesores, mallas | Fase 2 |
| Contrapisos / carpetas | Áreas | m³/m², niveles | Fase 2 |
| Zinguería | Cubierta | ml canaletas, bajadas | Fase 2 |
| Herrería | Barandas, rejas, estructuras light | kg/ml, pintura | Fase 3 |
| Vidrios especiales | Paños | m² DVH, film, herrajes | Fase 3 |
| Limpieza final de obra | m² tipología | global / por ambiente | Fase 4 |
| Obrador y temporarios | Plazo, tamaño obra | costos indirectos de sitio | Fase 4 |
| Seguridad e higiene | Plazo, personal proxy | ítems SH | Fase 4 |
| Señalética y exteriores | Accesos | unidades | Fase 4 |
| Rehabilitación / retrofit | Existente + intervencion | demolición selectiva + nuevos sistemas | Fase 4–5 |
| Modular / prefabricado | Grid, módulos | unidades, logística | Fase 5 |
| Smart metering | Eléctrico/agua | dispositivos, integración | Fase 5 |

### 9.3 Detalle expandido de módulos clave futuros

#### 9.3.1 Hormigón armado

| Tema | Contenido |
|------|-----------|
| Ambición | Estimación paramétrica útil para anteproyecto/presupuesto, **no** reemplazo de cálculo estructural firmado |
| Inputs | Tipología (losas macizas/nervuradas), luces típicas, nº pisos, suelo proxy, sobrecargas de uso |
| Motor | Tablas de ratio m³/m² y kg acero/m³ por tipología + ajustes |
| Outputs | Hormigón por resistencia, acero por diámetros agrupados, encofrado, aislaciones de fundación |
| Riesgos | Que el usuario lo tome como ingeniería → disclaimer fuerte + HITL |
| Madurez | Alpha fase 3; beta con partners estructurales |

#### 9.3.2 Steel Frame / Wood Frame

| Tema | Steel | Wood |
|------|-------|------|
| Valor | Velocidad + comparación vs mampostería | Nicho y exportación de método |
| Inputs | Panelización light, entrepisos, cargas viento tipológicas | Especie, tratamiento, zona húmeda |
| Outputs | Perfiles, OSB/placas, anclajes, barreras | Montantes, rigidizadores, fijaciones |
| UX | Packs “económico / estándar / premium” | Idem + clima |
| Chat | “¿Cuánto ahorro vs ladrillo?” con rango | Idem |

#### 9.3.3 Pintura

Frecuentemente subestimado. Módulo de alta rotación: áreas netas (descontando aberturas), manos, tipo de pintura, preparación de superficie, andamios/sillas.

#### 9.3.4 Energía solar

Puente a conversación de opex vs capex. Inputs desde cubierta + consumo eléctrico proxy del módulo eléctrico. Output: kit sugerido + estructura + protección eléctrica. No diseño eléctrico firmado.

#### 9.3.5 Incendio + accesibilidad

Módulos “checklist cuantificado”: generan ítems y pendientes documentales más que física compleja. Muy valiosos para Enterprise y usos comerciales.

### 9.4 Matriz de dependencia entre módulos

```
Terreno ──▶ Mov. suelos ──▶ Fundaciones/HA ──▶ Muros ──▶ Revoque ──▶ Pintura
                              │                  │
                              ▼                  ▼
                           Cubierta          Aberturas ──▶ Carpintería
                              │                  │
                              ▼                  ▼
                           Solar            Impermeabilización
                                                 │
                     Agua/Cloacas/Gas/Eléctrico/HVAC/Incendio
                              │
                              ▼
                     Schedule ▶ Compras ▶ Avance ▶ Certificación
```

### 9.5 Criterios de “done” de un módulo

| Checkpoint | Definición de done |
|------------|--------------------|
| Fórmulas v1 | Documentadas y testeadas con casos dorados |
| PriceBook mapping | ≥80% ítems con fuente de precio |
| Confidence model | Cada entidad/línea con score |
| UX review | Flujo de corrección humana |
| Chat tools | Preguntas frecuentes respondibles con citations |
| Export | Capítulos en presupuesto |
| Disclaimer | Visible y correcto |
| Analytics | Tracking de uso y error reports |

### 9.6 Observaciones de portfolio

- Evitar lanzar 10 módulos flojos el mismo trimestre.
- Preferir **profundidad en 3** antes que **superficialidad en 15**.
- Cada módulo nuevo debe mejorar el grafo, no solo sumar un tab.

---

## 10. Experiencia de usuario

### 10.1 Journey ideal end-to-end

```
Signup → Onboarding paleta/protocolo → Upload planos → Procesamiento async
    → Review confidence → Ambientar/corregir → Explorer MDO
    → Chat de auditoría → Escenarios de sistema → Presupuesto freeze
    → Schedule light → Lista de compras → Obra (mobile)
    → Progress snapshots → Certificación → Archivo + benchmarks
```

### 10.2 Stages detallados

#### Stage 0 — Signup / activación

| Momento | Experiencia ideal | Anti-experiencia |
|---------|-------------------|------------------|
| Landing | Marca clara, promesa de velocidad+confianza | Feature salad |
| Signup | Email + estudio + tipología dominante | Formulario eterno |
| Primer éxito | “Tu primer cómputo en <10 minutos” | Tutorial de 45 minutos |

#### Stage 1 — Onboarding de paleta

El protocolo de color es un moat y una fricción. UX debe:
- enseñar con ejemplo interactivo,
- validar una muestra antes del lote,
- ofrecer plantillas de leyenda descargables,
- detectar incumplimientos temprano.

#### Stage 2 — Upload y procesamiento

- Multi-file, estados visibles, notificaciones.
- Estimación de tiempo honesta.
- Reproceso parcial.

#### Stage 3 — Review de confianza

Pantalla más importante del producto post-wedge:

| Zona UI | Función |
|---------|---------|
| Heatmap | Dónde mirar |
| Lista priorizada | Top N riesgos |
| Inspector | Corregir entidad |
| CTA | “Listo para baseline” solo si umbral |

#### Stage 4 — Explorer del modelo digital

Árbol + plano + inspector + chat contextual. El usuario “pasea” la obra digital.

#### Stage 5 — Chat

Preguntas sugeridas al entrar: anomalías, top costos, incompletos.

#### Stage 6 — Escenarios

Comparador visual, no tabla infinita. Elegir ganador con razones.

#### Stage 7 — Presupuesto

Freeze, share link, dual view cliente/interno.

#### Stage 8 — Schedule + compras

Generadas desde el mismo modelo; edición ligera.

#### Stage 9 — Obra y certificación

Mobile-first. Evidencia. Aprobaciones.

#### Stage 10 — Archivo

Proyecto read-only + lecciones + contribución opt-in a benchmarks.

### 10.3 Personas

#### Persona A — Arquitecto solo

| Atributo | Detalle |
|----------|---------|
| Contexto | 1–8 obras/año, hace todo |
| Dolor | Tiempo, Excel, miedo a errar precios |
| Valor ARQ-IA | Velocidad + chat + presupuesto presentable |
| Riesgo UX | Sobrecarga Enterprise |
| Packaging | Pro |

#### Persona B — Estudio (5–30 personas)

| Atributo | Detalle |
|----------|---------|
| Contexto | Roles, estándares, varios proyectos |
| Dolor | Consistencia entre proyectistas |
| Valor | Templates, roles, price books del estudio |
| Riesgo | Permisos y onboarding |
| Packaging | Pro team / early Enterprise |

#### Persona C — Constructora

| Atributo | Detalle |
|----------|---------|
| Contexto | Compras, avance, subcontratos |
| Dolor | Desvíos, certificaciones, stock |
| Valor | MDO → OC → cert |
| Riesgo | Pedir ERP completo |
| Packaging | Enterprise |

#### Persona D — MMO / municipal / institucional

| Atributo | Detalle |
|----------|---------|
| Contexto | Control, transparencia, pliegos |
| Dolor | Auditoría y comparabilidad |
| Valor | Trazabilidad, exports, roles |
| Riesgo | Ciclos de venta largos |
| Packaging | Enterprise + compliance packs |

#### Persona E — Particular (dueño de obra)

| Atributo | Detalle |
|----------|---------|
| Contexto | Una obra en la vida |
| Dolor | No entiende presupuestos |
| Valor | Escenarios claros, lenguaje simple |
| Riesgo | Soporte emocional alto / bajo LTV |
| Packaging | Free limitado + upsell a su arquitecto |

### 10.4 Principios de UX para confianza en estimaciones

1. **Incertidumbre visible > precisión fingida.**
2. **Cada número es clickable hasta su origen.**
3. **Rojo no se puede “maquillar” en export cliente sin override.**
4. **Comparar siempre con supuestos listados.**
5. **El vacío (falta de dato) es un estado de primera clase.**
6. **Microcopy anti-ansiedad:** explicar qué hacer, no solo qué falló.
7. **Velocidad percibida:** skeletons, jobs async, resultados parciales.
8. **Modo presentación:** ocultar ruido interno sin ocultar disclaimers.
9. **Responsive real:** obra pasa en el teléfono.
10. **Accesibilidad básica:** contraste, teclado, labels — confianza también es inclusión.

### 10.5 Motions e interacción (presencia, no ruido)

Sin caer en UI genérica: transiciones de heatmap→entidad, morph de escenarios (antes/después), y progreso de certificación como curva viva. 2–3 motions intencionales en superficies clave.

### 10.6 Onboarding métrico

| Funnel | Meta cualitativa |
|--------|------------------|
| Signup → first upload | Muy alto |
| Upload → first review | Alto |
| Review → first share budget | Medio-alto (valor) |
| Share → second project | Retención verdadera |

### 10.7 Contenido educativo in-product

- Lexicón de cómputo.
- “Por qué tu OCR falló”.
- Guías por tipología.
- Videos de 60–90s, no cursos de 2h.

### 10.8 Estados emocionales a diseñar

| Estado | Diseño |
|--------|--------|
| Ansiedad pre-envío a cliente | Auditoría preflight |
| Confusión técnica | Chat + ejemplos |
| Desconfianza al número | Citations y rangos |
| Orgullo | Share aesthetics profesionales |
| Urgencia de obra | Mobile shortcuts |

---

## 11. Competencia

> Comparación conceptual. Sin guerra de precios. Objetivo: encontrar **wedges** defendibles.

### 11.1 Mapa de categorías competitivas

```
                 DISEÑO                          GESTIÓN DE OBRA
    AutoCAD ── Archicad ── Revit          Buildertrend ── ERPs locales
                 │                                 │
                 └──── takeoff/estimating ─────────┘
                        PlanSwift · Bluebeam · Presto · Cype · Buildxact
                                       │
                                       ▼
                         ARQ-IA (OSCQ) — puente cuantitativo
```

### 11.2 Tabla competitiva

| Producto | Qué hace bien | Qué no resuelve para nuestro ICP LATAM | ARQ-IA hoy / mañana | Wedge de oportunidad |
|----------|---------------|----------------------------------------|---------------------|----------------------|
| **Revit** | BIM profundo, documentación, familias | Adopción cara; no es OS de precio LATAM | No compite en CAD; interop futura light | Velocidad a presupuesto sin BIM Manager |
| **AutoCAD** | Dibujo universal | Cero inteligencia de cómputo nativa | Importar planos, no reemplazar CAD | De DWG/PDF a cantidades rápidas |
| **Archicad** | BIM arquitectónico amable | Costo/ecosistema; estimating limitado local | Similar a Revit: no clonar | Puente a decisión $ |
| **Presto** | Presupuesto/certificaciones ES | UX legacy; poca percepción automática | Certificaciones fase 4; UX moderna | Automatizar takeoff previo |
| **Cype** | Cálculo + mediciones ecosistema ES | Curva y foco no siempre AR obra chica | Módulos paramétricos selectivos | Simplicidad + chat + precios AR |
| **Buildxact** | Estimating constructores (ANZ/US) | No nace para planos coloreados ni AR | Estimación + compras | Localización LATAM profunda |
| **Buildertrend** | Gestión de obra / cliente | Débil en percepción de planos | Site+client fase 4 | Entrar por cómputo, expandir a obra |
| **PlanSwift** | Takeoff digital click-heavy | Laborioso; poco modelo vivo | Takeoff asistido CV | Menos clicks, más modelo |
| **Bluebeam** | Markup PDF colaboración | No es estimating OS | Markup no es foco | De markup a entidades |
| **MagicPlan** | Captura as-built mobile | No presupuesto obra nueva completa | Mobile fase 4 para as-built parcial | Obra nueva + estimación AR |

### 11.3 Competencia informal (a menudo la real)

| Alternativa | Por qué gana hoy | Cómo se desplaza |
|-------------|------------------|------------------|
| Excel + experiencia | Flexible, ubicuo | Templates vivos + menos error + velocidad |
| Cadista + medidor externo | Delegar | In-house en minutos + costo menor |
| “Ojo de buen cubero” | Rápido | Rangos honestos + defensa ante cliente |
| Software pirata europeo | Precio 0 ilegal | SaaS legal, updates, precios locales |
| WhatsApp + fotos | Coordinación | Bitácora y modelo con memoria |

### 11.4 Matriz “quién gana la job”

| Job | Favorito tradicional | Favorito ARQ-IA 2.0 |
|-----|----------------------|---------------------|
| Dibujar plano | CAD/BIM | No pelear |
| Medir rápido desde PDF coloreado/pintado | ARQ-IA | ARQ-IA |
| Presupuesto presentable LATAM | Excel/Presto | ARQ-IA |
| Comparar sistemas constructivos | Consultoría | ARQ-IA escenarios |
| Certificar | Presto/ERP | ARQ-IA Enterprise |
| Clash 3D | Revit/Navisworks | No pelear |
| Chat sobre cantidades | Nadie | ARQ-IA |

### 11.5 Estrategia competitiva

1. **No atacar el núcleo BIM 3D.** Rodearlo.
2. **Atacar el tiempo-a-presupuesto.**
3. **Ser el sistema donde el número se explica.**
4. **Ganar datos LATAM que los globales no tienen.**
5. **Expandir hacia obra solo después de ownership del cómputo.**

### 11.6 Señales de que un competidor nos “ve”

- Copian protocolo de color (bajo moat solo).
- Lanzan chat sin modelo (teatro).
- Localizan precios AR sin comunidad (frágil).
- Compran un takeoff tool y lo traducen.

**Respuesta:** profundizar MDO + corpus etiquetado + fórmulas + workflow certificación + marca de confianza.

---

## 12. Diferenciadores

### 12.1 Por qué elegir ARQ-IA

| # | Diferenciador | Manifestación tangible |
|---|---------------|------------------------|
| 1 | De plano pintado a decisión $ en minutos | Pipeline percepción + presupuesto |
| 2 | Modelo digital cuantitativo propio | Explorer + versionado |
| 3 | Confianza por entidad | Heatmap + gates de export |
| 4 | Chat con citations al cómputo | “según muro #12” |
| 5 | Precio LATAM vivo | Price graphs / books regionales |
| 6 | Comparación de sistemas como producto | Scenarios packs |
| 7 | Continuidad a obra | Avance/cert/OC sin reingresar datos |
| 8 | Honestidad de IA | IA sobre motor, no en lugar del motor |

### 12.2 Moats (activos difíciles de copiar)

| Moat | Por qué es duro de copiar | Cómo se acumula |
|------|---------------------------|-----------------|
| Corpus de planos coloreados + labels | Datos propietarios de correcciones | Cada review HITL |
| Librería de fórmulas AR/LATAM | Conocimiento tácito codificado | Expertos + estudios partner |
| Grafo de precios regionales | Series temporales reales | Compras + partners + índices |
| Workflow speed habit | Switching cost cognitivo | UX + templates estudio |
| Marca de confianza profesional | Reputación | Precisión comunicada consistente |
| Eval harness de chat cuantitativo | Golden sets | Uso real + feedback |
| Red de proveedores | Efectos de red locales | Marketplace fase 5 |

### 12.3 Anti-moats (no confundir)

- “Tenemos IA en el nombre.”
- Un color picker bonito.
- Un PDF export lindo sin modelo.
- Features clonadas de Revit a medias.

### 12.4 Flywheel

```
Más proyectos ──▶ más correcciones ──▶ mejor percepción/confianza
       ▲                                         │
       │                                         ▼
       │                              mejor MDO / fórmulas
       │                                         │
       │                                         ▼
más retención ◀── mejor chat/precios ◀───────────┘
```
### 12.5 Narrativa de ventas (interna)

> No vendemos “un software de arquitectura”. Vendemos **tiempo recuperado + números defendibles + continuidad a obra**.

### 12.6 Pruebas de diferenciación (tests)

| Test | Pregunta |
|------|----------|
| Test del plano | ¿Un competidor llega al mismo presupuesto en el mismo tiempo con menos fricción? |
| Test del cliente | ¿El comitente entiende y confía más? |
| Test del chat | ¿La respuesta cita entidades reales? |
| Test del desvío | ¿La constructora puede explicar extras con diff de modelo? |
| Test del dato | ¿Nuestro price book regional supera a la lista estática del rival? |

---

## 13. Roadmap 5 fases

### 13.1 Vista panorámica

```
2026        2027         2028         2029         2030-31
Fase 1      Fase 2       Fase 3       Fase 4       Fase 5
Foundation  Digital      Systems &    Site Ops &   Platform &
& Trust     Model+Chat   Methods      Enterprise   Ecosystem
```

### 13.2 Fase 1 — Foundation & Trust

| Campo | Contenido |
|-------|-----------|
| **Objetivos** | Confiabilidad del wedge actual; salir de deudas que impiden escala (blobs, sync, OCR frágil); comunicar incertidumbre |
| **Impacto** | Alto en retención y reputación |
| **Complejidad** | Media-alta técnica; baja en alcance de categoría |
| **Prioridad** | Máxima (sin esto, el castillo se cae) |
| **Key deliverables (no código)** | Object storage strategy; jobs async; confidence scores v1; review UX; audit básico; hardening protocolo color; price freshness alerts; packaging Free/Pro claro; telemetría WQD preliminar |
| **Éxito** | Menos tickets “número loco”; más presupuestos compartidos |

**Observaciones Fase 1:**
- Resistir la tentación del chat flashy antes de confidence.
- Resistir BIM theatre.
- Documentar fórmulas existentes como activo.

### 13.3 Fase 2 — Digital Model & Chat

| Campo | Contenido |
|-------|-----------|
| **Objetivos** | El Process deja de ser la verdad; nace MDO; chat RAG+tools; escenarios básicos |
| **Impacto** | Categoría: de tool a OS embrionario |
| **Complejidad** | Alta (datos + UX + IA guardrailed) |
| **Prioridad** | Máxima tras estabilidad F1 |
| **Key deliverables** | Jerarquía Project→Level→Space→Elements; explorer; versionado/changeset; AIConversation con citations; compare 2 escenarios; PriceBook versionado; disclaimers UX; eval set de 100 preguntas doradas |
| **Éxito** | % sesiones en explorer; citation coverage; WQD sube |

### 13.4 Fase 3 — Systems & Construction Methods

| Campo | Contenido |
|-------|-----------|
| **Objetivos** | Profundizar MEP como grafos; packs Steel/Wood/HA paramétrico; pintura/impermeabilización; comparación multicriterio |
| **Impacto** | Diferenciación fuerte vs takeoff tools |
| **Complejidad** | Alta de dominio |
| **Prioridad** | Alta selectiva (pocos módulos profundos) |
| **Key deliverables** | 3–5 módulos nuevos maduros; system packs; scenario scores; formula sandbox estudio; PT-BR básico; partnerships precio |
| **Éxito** | Multiplicidad de módulos/proyecto; wins competitivos documentados |

### 13.5 Fase 4 — Site Operations & Enterprise

| Campo | Contenido |
|-------|-----------|
| **Objetivos** | Llevar el MDO a obra: avance, certificación, OC, mobile, SSO, roles finos |
| **Impacto** | ACV alto; expansión revenue Enterprise |
| **Complejidad** | Alta organizacional + producto |
| **Prioridad** | Alta cuando F2 sólida en SMB |
| **Key deliverables** | ProgressSnapshot; Certifications; PO workflow; app visita; dashboard portfolio; SLA; residencias de datos selectivas; integraciones contables light |
| **Éxito** | % revenue Enterprise; obras vivas mensuales |

### 13.6 Fase 5 — Platform & Ecosystem

| Campo | Contenido |
|-------|-----------|
| **Objetivos** | API pública, marketplace proveedores/plantillas, IFC light, células a escala, marca categoría OSCQ |
| **Impacto** | Efectos de red |
| **Complejidad** | Muy alta (negocio + tech + legal) |
| **Prioridad** | Solo con foundation y marca |
| **Key deliverables** | API versionada; partner program; directory; export IFC light; benchmarks anonymized; expansión países; governance de datos |
| **Éxito** | Partners activos; developers terceros; categoría reconocida |

### 13.7 Dependencias entre fases

| Debe existir… | Antes de… |
|---------------|-----------|
| Confidence + async | Chat numérico |
| MDO | Escenarios serios |
| Escenarios | Comparación de sistemas creíble |
| Presupuesto freeze | Certificación |
| Takeoff estable | POs |
| Roles Enterprise | Guest client / MMO |
| Eval chat | Marketing agresivo de “IA” |

### 13.8 Temas transversales en las 5 fases

| Tema | F1 | F2 | F3 | F4 | F5 |
|------|----|----|----|----|----|
| Confianza/precisión | ★★★ | ★★★ | ★★ | ★★ | ★★ |
| IA | ★ | ★★★ | ★★ | ★★ | ★★ |
| LATAM prices | ★★ | ★★★ | ★★★ | ★★ | ★★★ |
| Escala infra | ★★ | ★★ | ★★ | ★★★ | ★★★ |
| Enterprise | ★ | ★ | ★★ | ★★★ | ★★★ |

### 13.9 Qué no entra aunque duela

Ver Apéndice D. Ejemplos: motor render 3D fotorealista; red social de arquitectos; ERP nómina; marketplace antes de retención.

---

## 14. MVP vs Enterprise packaging

### 14.1 Principios de packaging

1. Free enseña el wedge y captura corpus (con límites éticos/técnicos).
2. Pro es el hogar del profesional y estudio chico.
3. Enterprise es obra viva + control + integraciones + seguridad.
4. No esconder la confianza detrás de un paywall engañoso: el Free puede ser limitado en volumen, no en honestidad.

### 14.2 Matriz de features (detalle)

| Capacidad | Free | Pro | Enterprise |
|-----------|------|-----|------------|
| Proyectos activos | 1–2 | Ilimitados razonables | Ilimitados + portafolio |
| Procesamientos/mes | Low | Alto | Reserved + fair use |
| Módulos core | Sí básicos | Sí completos core | Sí + packs |
| Confidence heatmap | Sí | Sí | Sí + políticas export |
| Export PDF | Watermark | Sí | Sí white-label opcional |
| Export Excel | No/limitado | Sí | Sí + API |
| MDO Explorer | Read light | Full | Full + custom fields |
| Chat inteligente | Trial limitado | Sí con quotas | Quotas altas + retention policies |
| Escenarios | 1 | N | N + approvals |
| PriceBooks | Público básico | + estudio | + feeds partners + privados |
| Roles | Owner only | Admin/Estimator/Viewer | Granular + SSO |
| Guest client | No | Sí limitado | Sí + NDA spaces |
| Schedule | No | Light | Full light + look-ahead |
| Compras / OC | No | Listas | OC + approvals |
| Progress + Certificación | No | No/beta | Sí |
| Mobile obra | No | Bitácora light | Completo |
| Audit trail | Mínimo | Sí | Sí + retención configurable |
| SSO/SAML | No | No | Sí |
| SLA / support | Community | Email prioritario | CSM + SLA |
| Residencia datos | Default | Default | Opciones contractuales |
| API / webhooks | No | Limitada | Full |
| Marketplace leads | No | Opt-in | Opt-in + private suppliers |
| Benchmarks red | Opt-in anónimo | Sí | Sí + privados sectoriales |

### 14.3 Empaquetado por persona

| Persona | Plan recomendado | Trigger de upgrade |
|---------|------------------|--------------------|
| Particular | Free | Necesita compartir sin watermark / más escenarios |
| Arquitecto solo | Pro | Segundo proyecto serio + chat |
| Estudio | Pro Team / Ent. | Roles + pricebooks + varios usuarios |
| Constructora | Enterprise | Certificaciones + OC |
| MMO | Enterprise | Auditoría + SSO |

### 14.4 Add-ons posibles

| Add-on | Descripción |
|--------|-------------|
| Pack Steel/Wood | Sistemas constructivos avanzados |
| Pack Solar | Energía |
| Créditos compute extra | Picos de procesamiento |
| Partner price feed | Región premium |
| Onboarding concierge | Carga asistida primeros proyectos |
| Formación estudio | Workshops |

### 14.5 Política de límites honestos

- Nunca degradar silenciosamente la precisión.
- Si Free tiene OCR peor adrede → **prohibido**.
- Sí limitar concurrencia, historial, seats, exports.

---

## 15. Riesgos

### 15.1 Riesgos técnicos

| Riesgo | Severidad | Mitigación de principio |
|--------|-----------|-------------------------|
| OCR/percepción crónicamente frágil | Alta | Confidence gates + HITL + dataset + no overclaim |
| Migración Process→MDO falla | Alta | Dual-write temporal; imports; flags |
| Costos de compute explotan | Media-Alta | Créditos; async; cache; early reject |
| Alucinaciones del chat | Alta | Tools+citations+evals; kill switch |
| Deuda monolitica impide escala | Media | Modularización gradual por dominios |
| Pérdida de planos / blobs | Alta | Object storage + backups + hash |
| GPU/ML como distracción | Media | ROI claro; opcional |
| Multi-tenant leak | Crítica | Tests de aislamiento; reviews seguridad |

### 15.2 Riesgos comerciales

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| No pagarían por chat | Media | Vender decisiones/WQD, no tokens |
| Enterprise ciclo eterno | Media-Alta | Land Pro en estudio, expandir a obra |
| Commoditización takeoff | Alta | Subir a MDO+obra+precios |
| Dependencia Mercado Pago / un PSP | Baja-Media | Abstracción billing |
| CAC alto en paid ads | Media | PLG + universidades + estudios ancla |

### 15.3 Riesgos de mercado

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Incumbente global localiza LATAM | Media | Profundidad workflow + datos |
| Crisis macro / construcción frena | Alta | Planes low-cost; valor anti-error; sectores mix |
| Estudios no quieren cambiar Excel | Alta | Import/export; time-to-first-win |
| Protocolo color rechazado | Media | Alternativas de input graduales (ML assist, medición manual) |

### 15.4 Riesgos legales / compliance

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Usuario trata estimado como cálculo firmado | Alta | Disclaimers; UX; términos; educación |
| Responsabilidad por precio erróneo | Alta | Precisión comunicada; no garantía de mercado |
| Datos de planos confidenciales | Alta | Tenancy; cifrado; políticas Enterprise |
| Marketplace y reputación proveedores | Media | Términos; ratings; moderación |
| Normativa AI / consumer | Media | Transparencia modelo; logs; human oversight |
| Laboral/impuestos en presupuestos | Baja-Media | No asesorar; configuraciones user-owned |

### 15.5 Riesgos de precisión (corazón del negocio)

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Errores sistemáticos de escala | Crítica | Validadores anti-absurdo; checks tipológicos |
| Mermas irreales | Alta | Defaults regionales editables + aprendizaje |
| Precios stale en inflación | Alta | Freshness score; dual currency; alerts |
| Falsa confianza (UI verde indebida) | Crítica | Calibración de scores con realidad |
| Scope incompleto silencioso | Alta | Checklists tipológicos de completitud |

### 15.6 Mapa severidad × velocidad de contagio

```
Contagio rápido
      │
      │  Alucinación chat pública
      │  Leak multi-tenant
      │
      │           Error escala masivo
      │
      └──────────────────────────────── Precisión
                                  Contagio lento
                     (Excel inercia, CAC, etc.)
```

### 15.7 Principios de gestión de riesgo

1. Medir precisión en producción con muestreo.
2. Separar incidentes de percepción vs precios vs UX copy.
3. Feature flags para inteligencia.
4. War room playbook para “número viralmente absurdo”.
5. Cultura: celebrar quien encuentra un bug de cómputo.

---

## 16. Conclusión

### 16.1 ¿Puede ARQ-IA convertirse en una empresa importante?

**Sí — condicionalmente.**  
La condición no es “agregar IA”. Es **apropiarse de la capa de verdad cuantitativa de la obra** en un mercado enorme, fragmentado y sub-digitalizado, partiendo de un wedge real ya probado.

ARQ-IA puede ser importante si logra las tres transformaciones:

1. **De resultado de proceso → modelo digital vivo.**
2. **De CV disfrazado → arquitectura L1/L2/L3 honesta.**
3. **De presupuesto rápido → sistema operativo de cuantificación con continuidad a obra.**

### 16.2 Por qué es creíble

| Señal a favor | Interpretación |
|---------------|----------------|
| Wedge de velocidad existente | Hay product-market seed |
| Dolor universal (cómputo/presupuesto) | Mercado amplio |
| Incumbentes pesados o ajenos a LATAM | Espacio de categoría |
| Inflación y volatilidad de precios | Valor de price intelligence |
| LLM baratos para explicación | Apalancan twin, no lo sustituyen |

### 16.3 Qué debe hacerse (imperativos)

1. **Endurecer confianza** del motor y comunicarla.
2. **Construir el MDO** como apuesta estructural.
3. **Lanzar chat solo con citations y evals.**
4. **Codificar fórmulas y precios LATAM como moat.**
5. **Profundizar pocos módulos nuevos**, no una feria.
6. **Empaquetar Enterprise cuando la obra viva esté lista**, no antes.
7. **Mantener LATAM first** hasta tener playbooks exportables.
8. **Rechazar anti-objetivos** con disciplina de fundador.

### 16.4 Veredicto estratégico final

> ARQ-IA 2.0 debe dejar de pensarse como “la app que lee planos de colores” y pasar a pensarse como **el sistema operativo de la cuantificación constructiva**.  
> Si preserva el motor determinista, construye el modelo digital, pone la IA encima con guardrails, y convierte velocidad en hábito y datos, puede convertirse en una compañía relevante de infraestructura de software para la construcción en LATAM — con opción real de expansión global selectiva.  
> Si persigue el espejismo de “Revit + GPT”, diluye el wedge y quiebra la confianza, será una feature más en un mercado cruel.  
> **La batalla no es de renders. Es de números defendibles.**

---

## Apéndices

### Apéndice A — Glosario

| Término | Definición |
|---------|------------|
| **OSCQ** | Operating System of Construction Quantification / Sistema Operativo de Cuantificación Constructiva |
| **MDO** | Modelo Digital de la Obra — grafo cuantitativo versionado |
| **ARQ-BIM Lite** | BIM simplificado propio enfocado en topología, cantidades y sistemas |
| **Percepción (L1)** | CV/OCR/ML assist que extrae señales de documentos |
| **Twin (L2)** | Capa del MDO y costos/tiempo |
| **Intelligence (L3)** | Agentes LLM y experiencias generativas guardrailed |
| **Confidence score** | Estimación de confiabilidad de una entidad o ítem |
| **Baseline** | Versión congelada usada como referencia comercial/contractual |
| **Scenario / Variant** | Rama de simulación del MDO |
| **Takeoff** | Cómputo de materiales/cantidades |
| **PriceBook** | Lista de precios versionada |
| **WQD** | Weekly Quantified Decisions — north star propuesta |
| **HITL** | Human-in-the-loop |
| **ChangeSet** | Paquete de cambios atómicos al modelo |
| **Certification** | Documento de avance/pago |
| **Protocolo de color** | Convención de pintado de planos para percepción |
| **Citation** | Referencia navegable a entidad/fuente de un número |
| **Fair use compute** | Política de uso razonable de procesamiento |
| **Cell-based tenancy** | Aislamiento por células de infra en escala alta |
| **Golden questions** | Set de evaluación del chat |
| **Scope creep** | Crecimiento no controlado del alcance |
| **RCD** | Residuos de construcción y demolición |
| **P50/P80** | Percentiles de estimación probabilística |
| **Look-ahead** | Planificación corta de obra |
| **Dual-write** | Escribir en sistema viejo y nuevo durante migración |

### Apéndice B — Principios de producto

| # | Principio | Implicancia práctica |
|---|-----------|----------------------|
| B1 | Motor primero | Ninguna feature IA bypasea cantidades canónicas |
| B2 | Confianza visible | UI de incertidumbre obligatoria |
| B3 | Un modelo, muchas vistas | Presupuesto/schedule/OC leen el mismo MDO |
| B4 | Minutos a valor | Time-to-first-compute sagrado |
| B5 | Explicabilidad | Citations o silencio |
| B6 | LATAM realism | Inflación, proveedores, certificaciones |
| B7 | Profundidad > feria | Módulos maduros |
| B8 | Multi-tenant ethics | Aislamiento y privacidad |
| B9 | Human decides money | Confirmaciones en dinero/plazo contractual |
| B10 | Medir WQD | Vanity metrics no dirigen roadmap |
| B11 | Defaults opinados | Tipologías con buenos starting points |
| B12 | Export is a promise | Lo exportado respeta gates de confianza |
| B13 | Educar in-product | Reducir soporte por diseño |
| B14 | Composable packs | Sistemas constructivos como plugins de dominio |
| B15 | Honest branding | No vender magia |

### Apéndice C — KPIs norte

| KPI | Definición | Frecuencia |
|-----|------------|------------|
| WQD | Decisiones económicas semanales ancladas a MDO confiable | Semanal |
| Time-to-first-compute | Mediana signup→primer resultado | Semanal |
| Time-to-baseline | Mediana upload→baseline comercial | Mensual |
| Confidence yield | % entidades ≥0.85 en proyectos Pro | Semanal |
| Review completion rate | % proyectos con review cerrada | Semanal |
| Chat citation coverage | % respuestas numéricas con citation válida | Semanal |
| Hallucination eval score | Fallos en golden set | Por release |
| Share rate | % proyectos con presupuesto compartido | Mensual |
| Pro conversion | Free→Pro | Mensual |
| Enterprise NRR | Net revenue retention | Trimestral |
| Modules per project | Diversidad de uso | Mensual |
| Price freshness | Edad media PUs usados | Semanal |
| Compute cost / Pro user | FinOps | Mensual |
| Support tickets / 100 projects | Calidad percibida | Mensual |
| Logo retention 12m | Estudios que siguen | Anual |

### Apéndice D — Anti-objetivos (qué NO ser)

| Anti-objetivo | Por qué se rechaza |
|---------------|-------------------|
| Clon de Revit browser | Pozo infinito; mata el wedge |
| ERP de nómina/contabilidad completa | Fuera de DNA; distracción |
| Red social de arquitectos | Engagement vanity ≠ WQD |
| Marketplace antes que retención | Quemar confianza y foco |
| “GPT que mira el plano y listo” | Alucinación + responsabilidad |
| Precisión fingida con muchos decimales | Suicidio reputacional |
| Dark patterns de upgrade que ocultan errores | Ética + churn |
| Custom forever por cliente | Quiebra el producto |
| Soportar todo país day-one | Diluye LATAM first |
| App de renders / moodboards | Categoría ajena |
| Hardware IoT primero | Prematuro |
| Tokenomics / crypto pagos | Ruido |
| Ser Bluebeam | Markup no es el centro |
| Ser solo PlanSwift | Commodity de clicks |

### Apéndice E — Escenarios de fracaso

| Escenario | Síntomas tempranos | Cómo se evita |
|-----------|--------------------|---------------|
| **Teatro de IA** | Demo wow, usuarios no confían en números | Evals + citations + motor |
| **Pozo BIM** | 18 meses sin mejorar presupuesto | Capas Lite; decir no |
| **Excel gana igual** | Uso esporádico solo para “probar” | Habito WQD; templates estudio |
| **Inflación de features** | 40 módulos a 30% | Portfolio discipline |
| **Fuga de datos** | Un incidente de tenancy | Seguridad como feature |
| **Precio stale** | Quejas de presupuestos irreales | Freshness + dual currency |
| **Enterprise trap** | Roadmap dictado por 2 logos | Packaging + principle B7 |
| **Fundador se enamora del 3D** | Hiring de graphics sin ROI | Volver a OSCQ |
| **Soporte colapsa** | Escala de usuarios Free ruidosos | UX confidence + limits |
| **Competidor compra el mercado** | Descuentos agresivos | Moat de datos + workflow obra |

### Apéndice F — Matriz visión × capacidad actual

| Dimensión de visión | Capacidad actual (baseline alto nivel) | Gap | Fase que cierra |
|---------------------|----------------------------------------|-----|-----------------|
| Percepción CV color | Existe | Robustez/OCR/async | F1 |
| Confianza por entidad | Débil/ausente | Alto | F1 |
| MDO jerárquico | Process JSON plano | Muy alto | F2 |
| Chat cuantitativo | No | Muy alto | F2 |
| Escenarios sistemas | No | Alto | F2–3 |
| Price intelligence LATAM | Estimaciones ARS básicas | Alto | F1–3 |
| Schedule | No | Medio | F3–4 |
| Compras/OC | No | Alto | F4 |
| Certificación/avance | No | Alto | F4 |
| Mobile obra | No | Medio | F4 |
| BIM Lite explorer | No | Alto | F2 |
| IFC/interop | No | Bajo prioridad | F5 |
| Marketplace | No | Medio | F5 |
| Multi-región / 100k | Monolito inicial | Alto gradual | F1→5 |
| ML assist percepción | No (CV clásico) | Medio | F2–3 |
| Hormigón/Steel/Wood packs | No | Alto dominio | F3 |
| SSO/Enterprise security | Limitado | Medio | F4 |
| API ecosistema | No | Medio | F5 |
| Benchmarks de red | No | Medio | F3–5 |
| PT-BR | No | Medio | F3 |

#### Lectura del gap

El producto actual ya demuestra **demanda del wedge**. El gap dominante no es “falta un botón”, es **falta el sistema de verdad (MDO) + la capa de confianza + la continuidad operativa**. Ese es el puente entre startup con tracción temprana y compañía importante.

---

### Apéndice G — Preguntas estratégicas abiertas (para el board)

| # | Pregunta | Por qué importa |
|---|----------|-----------------|
| G1 | ¿Cuál es el umbral mínimo de confidence para permitir share a cliente? | Define reputación |
| G2 | ¿Qué % del corpus se puede usar para entrenar modelos? | Legal + moat |
| G3 | ¿Enterprise se vende en año 2 o se espera a certificaciones reales? | Foco GTM |
| G4 | ¿Protocolo color se mantiene como entrada primaria 5 años? | Roadmap percepción |
| G5 | ¿Qué país #2 después de Argentina? | Expansión |
| G6 | ¿Marketplace es revenue o utility? | Conflicto de interés percibido |
| G7 | ¿Cuál es el “logo ancla” que queremos como caso? | Posicionamiento |
| G8 | ¿Hasta dónde llega la promesa solar/HA sin partners licenciados? | Riesgo legal |

### Apéndice H — Checklist de alineación de una iniciativa nueva

Antes de aprobar cualquier iniciativa, marcar:

| Check | Sí/No |
|-------|-------|
| ¿Aumenta fidelidad, operabilidad o explicabilidad del MDO? | |
| ¿Respeta L1/L2/L3 (no reemplaza motor)? | |
| ¿Declara incertidumbre? | |
| ¿Tiene dueño de dominio y casos dorados? | |
| ¿Tiene camino a Pro/Enterprise value? | |
| ¿Es LATAM-relevante en los próximos 24 meses? | |
| ¿Evita un anti-objetivo del Ap. D? | |
| ¿Define métrica de éxito ligada a WQD u satélite? | |
| ¿Tiene plan de soporte/educación in-product? | |
| ¿Puede lanzarse en madurez útil (no teatro)? | |

Si hay ≥2 “No” críticos → no entra al trimestre.

### Apéndice I — Narrativa de cultura interna

| Hábito | Descripción |
|--------|-------------|
| **Culto al caso dorado** | Cada módulo tiene obras de referencia |
| **Bug de cómputo = P0 cultural** | Aunque el CSS esté roto |
| **Demo con disclaimer** | Orgullo profesional |
| **Hablar con jefes de obra** | No solo con arquitectos de Instagram |
| **Escribir la fórmula** | Si no está documentada, no existe |
| **Decir no con elegancia** | Roadmap es estrategia, no wishlist |

### Apéndice J — Mapa de stakeholders y mensajes

| Stakeholder | Mensaje núcleo |
|-------------|----------------|
| Arquitecto | “Defendé tu presupuesto con evidencia.” |
| Estudio | “Estandarizá el cómputo sin matar la velocidad.” |
| Constructora | “Del cómputo a la certificación sin rehacer Excel.” |
| Proveedor | “Conectá tu lista a demanda real de obra.” |
| Inversor | “Categoría OSCQ · wedge · datos · expansión obra.” |
| Equipo | “Números defendibles > magia.” |

### Apéndice K — Diagrama resumen del plan maestro

```
                    ┌─────────────────────────┐
                    │   CATEGORÍA OSCQ        │
                    │   (identidad 5 años)    │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
   CONFIANZA                 MDO VIVO                 IA GUARDRAILED
   (Fase 1)                  (Fase 2)                 (Fase 2+)
        │                       │                       │
        └───────────┬───────────┴───────────┬───────────┘
                    ▼                       ▼
            SISTEMAS/PACKS              OBRA+ENTERPRISE
               (Fase 3)                    (Fase 4)
                    │                       │
                    └───────────┬───────────┘
                                ▼
                     PLATAFORMA & ECOSISTEMA
                            (Fase 5)
                                │
                                ▼
                     COMPAÑÍA IMPORTANTE
              (números defendibles · hábito · red)
```

### Apéndice L — Tabla de decisiones fundacionales ya tomadas por este plan

| Decisión | Estado |
|----------|--------|
| No reemplazar motor CV por LLM | Tomada |
| Construir MDO propio | Tomada |
| LATAM first | Tomada |
| Chat con citations obligatorias | Tomada |
| No clonar Revit | Tomada |
| Enterprise después de obra viva real | Tomada |
| Precisión comunicada como marca | Tomada |
| Free no miente en precisión | Tomada |
| Marketplace tarde (F5) | Tomada |
| WQD como north star candidata | Tomada |

### Apéndice M — Observaciones finales de uso del documento

1. Este plan es una **brújula**, no un contrato de sprint.
2. Debe revisarse cada trimestre: lo que no cambia son los principios; lo que cambia son apuestas de módulos.
3. Cualquier pitch externo debe poder reducirse a la tesis de la sección 0.2.
4. Si una slide de inversores contradice el Ap. D, gana el Ap. D.
5. La medida del plan no es su longitud: es si el equipo dice “no” mejor.

---

## Cierre

**Documento:** ARQ-IA 2.0 — Plan Maestro de Evolución  
**Fecha:** 2026-08-02  
**Horizonte:** 2026–2031  
**Naturaleza:** Estratégico  

> *La visión es convertirse en el sistema operativo de la cuantificación constructiva.  
> El método es modelo digital + confianza + IA sobre el motor.  
> El mercado es LATAM primero.  
> La disciplina es no traicionar el wedge ni la verdad de los números.*

**— Fin del Plan Maestro —**


---

## Ampliaciones estratégicas (detalle operativo de visión)

> Las siguientes subsecciones profundizan el Plan Maestro sin convertirlo en especificación de implementación. Sirven como material de trabajo para producto, dominio e inversores.

### Ampl. 1 — Escenarios narrativos de usuario (day-in-the-life)

#### Escenario N1 — Arquitecta sola, anteproyecto de PH

| Hora | Acción | Valor ARQ-IA |
|------|--------|--------------|
| 09:10 | Cliente pide “números tentativos para mañana” | Urgencia real |
| 09:25 | Sube planta coloreada con paleta del onboarding | Wedge velocidad |
| 09:40 | Review: 6 entidades amarillas, 1 roja (cota OCR) | Confianza visible |
| 09:55 | Corrige cota; confidence global sube a 0.88 | HITL |
| 10:10 | Chat: “¿me alcanza con 120k USD?” | Decisión económica |
| 10:25 | Crea escenario Steel Frame | Comparación |
| 10:40 | Comparte link cliente (vista guest) | Profesionalidad |
| 11:00 | Congela baseline v1 | Habito WQD |

**Observación:** El “win” no es el procesamiento; es enviar un link defendible antes del mediodía.

#### Escenario N2 — Estudio de 12 personas, estandarización

| Momento | Dolor previo | Experiencia 2.0 |
|---------|--------------|-----------------|
| Onboarding de junior | Cada uno computa distinto | Template de tipología PH del estudio |
| Price books | Excel del contador desactualizado | PriceBook del tenant con vigencia |
| Revisión del socio | “¿De dónde salió este número?” | Click a muro #27 + fórmula |
| Entrega a cliente | PowerPoint desconectado | Export + narrativa con citations |
| Postventa | Nadie recuerda supuestos | Assumptions freeze en baseline |

#### Escenario N3 — Constructora, obra en curso

| Momento | Uso |
|---------|-----|
| Pre-obra | BOM + OC a corralón partner |
| Semana 4 | Progress snapshot con fotos |
| Semana 4 | Certificación parcial |
| Extra del comitente | Scenario “ampliación deck” → change order |
| Cierre | Archivo + mermas reales alimentan defaults futuros |

#### Escenario N4 — Particular informado

| Momento | Uso |
|---------|-----|
| Recibe 3 presupuestos dispares | Pide a su arquitecto correr escenarios en ARQ-IA |
| No entiende capítulos | Chat en lenguaje simple (rol guest) |
| Decide calidad de terminación | Pack “estándar vs premium” |
| No opera la herramienta a fondo | LTV vía profesional, no self-serve eterno |

### Ampl. 2 — Taxonomía de incertidumbre

| Tipo de incertidumbre | Ejemplo | Tratamiento UX | ¿Chat puede afirmar? |
|-----------------------|---------|----------------|----------------------|
| Geométrica | Escala dudosa | Bloqueo rojo | No cantidad absoluta |
| Semántica | “¿Es muro o placard?” | Pregunta HITL | Solo con caveat |
| De completitud | Falta cubierta | Checklist | Declara hueco |
| De precio | PU de hace 120 días | Freshness badge | Rango / alerta |
| De alcance | Cliente no definió calidad | Assumptions | Escenarios |
| De ejecución | Merma real desconocida | Default + aprendizaje | Proxy declarado |
| Normativa | Incendio según uso | Checklist no dictamen | No asesoría legal |

### Ampl. 3 — Estados de calidad del proyecto (scorecard)

| Dimensión | Peso | 0–1 significa |
|-----------|------|---------------|
| Cobertura espacial | 0.20 | Ambientes/muros coherentes |
| Calidad percepción | 0.25 | Confidence media ponderada |
| Completitud tipológica | 0.15 | Checklist módulos mínimos |
| Frescura de precios | 0.15 | Edad PUs |
| Consistencia topológica | 0.10 | Validaciones |
| Listitud comercial | 0.15 | Gates para share |

**Índice de Listitud Comercial (ILC)** = suma ponderada.  
Regla propuesta: share “cliente formal” requiere ILC ≥ 0.80 y cero rojos sin override.

### Ampl. 4 — Biblioteca de fórmulas (visión de activo)

| Familia de fórmula | Ejemplos conceptuales | Owner de dominio |
|--------------------|-----------------------|------------------|
| Albañilería | ladrillos/m² según formato + rotura | Core qty |
| Mezclas | cemento/arena/cal por m³ | Core qty |
| Revoques | m² netos × espesor × desperdicio | Terminaciones |
| Instalaciones agua | ml equivalentes por artefacto + desarrollo | MEP |
| Eléctrico | puntos × metros promedio tipológicos | MEP |
| Cubiertas | m² pendientes × solapes | Envelope |
| Steel Frame | kg perfil / m² panel | Systems packs |
| HA ratios | m³/m² · kg/m³ por tipología | Estructura light |
| Pintura | m² × manos × rendimiento L/m² | Terminaciones |
| Indirectos | % sobre directo por escala de obra | Cost model |

**Observación:** La librería debe ser versionada, testeable y forkeable por Organization (sin romper defaults ARQ-IA).

### Ampl. 5 — Política de datos y aprendizaje

| Pregunta | Postura estratégica |
|----------|---------------------|
| ¿Entrenamos con planos de clientes? | Solo con consentimiento / ToS claro; Enterprise opt-out |
| ¿Benchmarks anónimos? | Agregados mínimos k-anonymity |
| ¿Venden datos crudos? | No — anti-objetivo ético y comercial |
| ¿Labels de corrección? | Sí, como fuel del moat de percepción |
| ¿Conversaciones chat? | Retención limitada; redacción de PII |
| ¿Precios aportados por usuarios? | Contribución voluntaria a Price graph |

### Ampl. 6 — Modelo de go-to-market alineado al plan

```
PLG (Free → Pro)
  │  contenido educativo + wedge velocidad
  │
  ├─▶ Estudios ancla (diseño partnership)
  │     templates + pricebooks regionales
  │
  ├─▶ Universidades / colegios profesionales
  │     modo enseñanza
  │
  └─▶ Enterprise motion (Fase 4)
        constructoras + MMO
        land: cómputo estandarizado
        expand: cert + OC + SSO
```

| Canal | Fase | Nota |
|-------|------|------|
| Product-led | 1–2 | Principal |
| Community/Education | 1–3 | Semilla de hábito |
| Partners corralones | 3–5 | Price feeds |
| Sales Enterprise | 4–5 | Cuando obra viva existe |
| Marketplace | 5 | Después de retención |

### Ampl. 7 — Matriz de priorización ICE (ejemplos)

| Idea | Impacto (1–10) | Confianza (1–10) | Esfuerzo (1–10 inverso) | ICE orientativo |
|------|----------------|------------------|-------------------------|-----------------|
| Confidence UX + gates | 10 | 9 | 6 | Alto |
| Object storage + async | 9 | 9 | 5 | Alto |
| MDO explorer v1 | 10 | 7 | 3 | Alto |
| Chat citations | 9 | 6 | 3 | Alto |
| Pack Steel Frame | 8 | 6 | 4 | Medio-Alto |
| Certificaciones | 8 | 7 | 2 | Medio (después) |
| IFC export | 4 | 5 | 3 | Bajo |
| Red social | 2 | 3 | 2 | Descartar |
| Render 3D | 3 | 4 | 1 | Descartar |
| Mobile bitácora | 7 | 7 | 4 | Medio (F4) |

### Ampl. 8 — Detailed entity attribute catalogs (conceptual)

#### Project — atributos extendidos

| Atributo conceptual | Uso |
|---------------------|-----|
| typology_code | Casa / PH / Local / Mixto |
| quality_target | Económico / estándar / premium |
| target_budget | Para factibilidad |
| fx_rate_freeze | Tipo de cambio de baseline |
| climate_zone | Aislación / wood / HVAC defaults |
| regulatory_profile | Checklist packs |
| ilc_score | Listitud comercial |
| lifecycle_state | Borrador…archivo |

#### Wall — atributos extendidos

| Atributo | Uso |
|----------|-----|
| length · height · thickness | Geometría |
| boundary_role | exterior/interior/medianera |
| system_pack_id | Ladrillo/SF/WF/… |
| finish_inner · finish_outer | Revoque/pintura/fachada |
| openings_area_sum | Neto |
| perception_source | HSV / manual / ML assist |
| confidence · confidence_reasons | Trust |
| takeoff_line_ids | Trazabilidad |

#### CostItem — atributos extendidos

| Atributo | Uso |
|----------|-----|
| chapter_code | Estructura presupuesto |
| resource_type | MAT / MO / EQ / SUB |
| qty · unit · unit_price | Números |
| price_as_of · source | Freshness |
| formula_ref | Explicabilidad |
| contingency_pct | Riesgo |
| taxable flags | Localización |
| locked_in_baseline | Inmutabilidad |

### Ampl. 9 — Patrones de colaboración en el MDO

| Patrón | Descripción | Fase |
|--------|-------------|------|
| Live edit con presencia | Ver quién mira un level | 2–3 |
| Proposed change | Junior propone, senior acepta | 2 |
| Review checklist asignable | Tasks sobre rojos | 2 |
| Client comment on scenario | Guest comenta alternativa | 3 |
| Site note linked to Space | Obra | 4 |
| Change order branch | Extra contractual | 4 |

### Ampl. 10 — Ejemplo de diff de escenario (ilustrativo)

```
Baseline: Mampostería estándar
Scenario: Steel Frame + aislación lana 100mm

DELTA CANTIDADES (extracto)
  Ladrillos huecos 12x18x33     -18.400 u
  Mezcla cemento                 -12.2 m³
  Perfiles SF galvanizados      +3.120 kg
  Placa OSB 11.1mm              +412 m²
  Lana mineral 100mm            +390 m²

DELTA COSTO
  Directos materiales           -2.1% a +3.4% (rango precios)
  Mano de obra estructura       -8.0% (rendimiento pack)
  Indirectos plazo              -6.5% (12 días menos)

DELTA PLAZO
  Estructura/envolvente         -12 días
  Instalaciones                 0 a -3 días (mejor trazado)

DELTA PRESTACIONES (cualitativo score 1–5)
  Velocidad obra                4 → 5
  Inercia térmica               4 → 3
  Acústica impact               3 → 3 (depende pack)
  Mantenimiento percibido       3 → 3
```

**Observación:** El producto gana cuando el diff es legible por el comitente, no solo por el medidor.

### Ampl. 11 — Guardrails de marketplace (anticipación F5)

| Riesgo | Guardrail |
|--------|-----------|
| Sesgo a supplier que paga más | Ranking dual: orgánico vs sponsored etiquetado |
| Usuario siente spam | Opt-in granular por categoría |
| Precio partner vs precio real obra | Feedback loop de OC pagadas |
| Controversia ética | Separar “recomendación técnica” de “anuncio” |

### Ampl. 12 — Programa de partners de conocimiento

| Partner type | Aporta | Recibe |
|--------------|--------|--------|
| Estudio ancla | Templates + feedback dominio | Descuento / influence roadmap |
| Corralón | Price feed | Demanda cualificada |
| Ingeniero estructural | Ratios HA/SF | Leads de anteproyecto (opt-in) |
| Universidad | Casos + talento | Licencias education |
| Software contable | Integración | Ecosystem |

### Ampl. 13 — Matriz de contenido de marca (no genérica)

| Pieza | Mensaje | Evitar |
|-------|---------|--------|
| Landing | Velocidad + números defendibles | “AI magic for buildings” vacío |
| Case study | Antes/después de horas de Excel | Renders de fantasía |
| Docs | Protocolo color + confidence | Jerga BIM intimidante |
| Sales Enterprise | Continuidad a certificación | Prometer ERP |
| Changelog | Mejoras de precisión | Feature dump semanal |

### Ampl. 14 — Operación de precisión (Precision Ops)

| Práctica | Descripción |
|----------|-------------|
| Sampling semanal | Re-cómputo manual de N planos al azar |
| Error budget | % máximo de desvío tolerable por clase |
| Calibration curves | Confidence vs error real |
| Incident postmortems | Sin blame; con caso dorado nuevo |
| Panel externo | 2–3 profesionales revisan releases sensibles |

### Ampl. 15 — Tabla de “completeness” por tipología (ejemplo casa)

| Ítem checklist | Obligatorio para baseline cliente |
|----------------|-----------------------------------|
| Escala validada | Sí |
| Muros PB/PA | Sí |
| Aberturas | Sí |
| Pisos | Sí |
| Cubierta | Sí |
| Agua + cloacas | Sí si tipología residencial |
| Eléctrico | Sí (aunque sea proxy) |
| Gas | Si hay artefactos a gas |
| Pintura | Recomendado |
| Indirectos | Sí |
| Supuestos calidad | Sí |
| HA detallado | No (salvo pack) |
| Solar | No |
| Paisajismo | No |

### Ampl. 16 — Evolución del protocolo de entrada (sin abandonar el wedge)

```
Año 1: Protocolo color dominante + validadores
Año 2: Color + corrección geométrica rica + OCR assist
Año 3: Color + ML segmentation assist (sugerencias)
Año 4: Captura mobile as-built parcial
Año 5: Import IFC light / DXF selectivo como secundario

REGLA: nuevas entradas alimentan el MISMO MDO.
```

### Ampl. 17 — Roles y permisos (visión)

| Permiso | Owner | Admin | Estimator | SiteManager | Viewer | ClientGuest |
|---------|-------|-------|-----------|-------------|--------|-------------|
| Gestionar billing | ✓ | ✓ | | | | |
| Editar MDO | ✓ | ✓ | ✓ | limitado | | |
| Aprobar baseline | ✓ | ✓ | opcional | | | |
| Ver márgenes internos | ✓ | ✓ | ✓ | | | |
| Chat completo | ✓ | ✓ | ✓ | ✓ | ✓ | limitado |
| Cargar avance | ✓ | ✓ | | ✓ | | |
| Emitir certificación | ✓ | ✓ | | proponer | | |
| Emitir OC | ✓ | ✓ | proponer | proponer | | |
| Ver escenarios | ✓ | ✓ | ✓ | ✓ | ✓ | invitados |
| Export sin watermark | ✓ | ✓ | ✓ | ✓ | ✓ | según link |

### Ampl. 18 — SLOs conceptuales de experiencia

| Superficie | SLO de producto (visión) |
|------------|--------------------------|
| Upload → job queued | Segundos |
| Job percepción plano típico | Minutos, no decenas |
| Explorer search entidad | Sub-segundo percibido |
| Chat tool answer | Pocos segundos |
| Share link open | Rápido global via CDN |
| Mobile snapshot sync | Tolerante offline |

### Ampl. 19 — Finanzas de unidad (principios, no forecast)

| Palanca | Dirección saludable |
|---------|---------------------|
| Gross margin SaaS | Proteger vs compute abusivo |
| Compute credits | Alinean costo variable al plan |
| Expansion revenue | Módulos + Enterprise + seats |
| Support cost | Baja con confidence UX + docs |
| Data moat spend | Etiquetado y partners > ads solo |

### Ampl. 20 — Tablero de salud de categoría OSCQ

| Señal de categoría | Estado deseado año 5 |
|--------------------|----------------------|
| Búsqueda mental “cómputo rápido LATAM” | ARQ-IA top-of-mind en nicho |
| Programas de estudio | Cursos lo mencionan |
| Job posts | “experiencia ARQ-IA” aparece |
| Partners | Corralones preguntan por integración |
| Prensa | Habla de “sistema de cuantificación”, no de “app IA” |

### Ampl. 21 — Ejemplos de mensajes de error / confianza (microcopy estratégico)

| Situación | Microcopy ideal (sentido) |
|-----------|---------------------------|
| Escala absurda | “Esto daría puertas de 3 m de ancho. Revisá la escala antes de presupuestar.” |
| Precio viejo | “Este PU tiene 140 días. ¿Actualizamos canasta AMBA?” |
| Rojo en export | “Hay 3 entidades críticas. Podés exportar borrador o resolverlas.” |
| Chat sin dato | “No tengo ese tramo en el modelo. ¿Lo agregamos o estimamos por tipología?” |
| Scenario aplicado | “Cambié el pack de muros. Cantidades regeneradas; precios recalculados con PriceBook v27.” |

### Ampl. 22 — Roadmap de datos maestros de precios

| Etapa | Contenido |
|-------|-----------|
| v1 | Canasta básica AMBA (cemento, hierros, ladrillos, arenas, aberturas genéricas) |
| v2 | Mano de obra por zona + mermas |
| v3 | Interior Argentina + Uruguay |
| v4 | Chile/Paraguay/Perú packs |
| v5 | Brasil PT + MX selectivo |
| Siempre | Freshness, fuente, moneda, fecha |

### Ampl. 23 — Criterios de “empresa importante” (score interno)

| Criterio | Umbral cualitativo año 5 |
|----------|--------------------------|
| Categoría | OSCQ asociada a la marca |
| Retención | Estudios no vuelven a Excel como home |
| Datos | Price graph y corpus relevantes |
| Revenue mix | Pro sólido + Enterprise material |
| Talento | Dominio construcción + software top |
| Confianza pública | Incidentes de precisión manejados con transparencia |
| Opción global | Playbooks listos para 2–3 países nuevos |

### Ampl. 24 — Tabla de conflictos estratégicos y resolución

| Conflicto | Resolución del plan |
|-----------|---------------------|
| Velocidad vs precisión | Velocidad con uncertainty visible |
| PLG vs Enterprise | PLG primero; Enterprise cuando obra viva |
| IA hype vs honestidad | Honestidad (marca durable) |
| BIM profundo vs Lite | Lite cuantitativo |
| Horizontal ERP vs vertical OSCQ | Vertical OSCQ |
| Multi-país vs profundidad AR | Profundidad primero |

### Ampl. 25 — Agenda trimestral tipo (plantilla)

| Semana | Foco |
|--------|------|
| 1 | Precision Ops + incident review |
| 2–4 | Entregables de fase activa |
| 5 | User advisory board (estudios) |
| 6–8 | Entregables |
| 9 | Eval chat + golden cases |
| 10–11 | Packaging/GTM sync |
| 12 | Revisión de principios y anti-objetivos |

### Ampl. 26 — Señales para acelerar o frenar una fase

| Señal | Acción |
|-------|--------|
| ILC mediano Pro > 0.85 y share rate alto | Acelerar F2 chat |
| Hallucination eval > umbral | Frenar marketing IA |
| Compute cost / user explota | Frenar Free abuse; optimizar |
| 3 constructoras piden cert | Traer F4 parcial anticipado |
| Pedidos de IFC > pedidos de confidence | Decir no; reeducar mercado |
| Retention D30 floja | Volver a journey onboarding |

### Ampl. 27 — Inventario de “objetos de experiencia” del producto futuro

| Objeto UX | Rol |
|-----------|-----|
| Legend Coach | Enseña protocolo color |
| Confidence Heatmap | Prioriza revisión |
| Entity Inspector | Edita significado + geometría |
| Model Tree | Navega MDO |
| Scenario Compare Board | Decide packs |
| Citation Chips | Confianza en chat |
| Budget Stage Gate | Control de export |
| Site Pulse | Avance mobile |
| Certification Binder | Paquete auditable |
| Archive Capsule | Proyecto cerrado con lecciones |

### Ampl. 28 — Mapa de métricas por fase

| Fase | Métrica primaria | Secundarias |
|------|------------------|-------------|
| 1 | Confidence yield + ticket rate | Time-to-first-compute |
| 2 | Explorer engagement + citation coverage | WQD |
| 3 | Modules/project + scenario adoption | Win rates vs Excel |
| 4 | Live sites + certs/month | Enterprise NRR |
| 5 | API calls partners + marketplace GMV utility | Category mentions |

### Ampl. 29 — Principios de diseño de reportes

1. Una página ejecutiva antes que veinte.
2. Supuestos siempre anexos.
3. Deltas > absolutos cuando hay baseline.
4. Colores de confidence no se pierden en PDF blanco-negro (usar patrones/textos).
5. Idempotencia: mismo ProjectVersion → mismo reporte hash.

### Ampl. 30 — Cierre de ampliaciones

Estas ampliaciones no agregan features “porque sí”: **operacionalizan la tesis**. Si el equipo solo recuerda cinco cosas de todo el documento, que sean:

1. OSCQ como categoría.  
2. MDO como verdad.  
3. IA sobre el motor.  
4. Precisión comunicada.  
5. LATAM first → obra viva → ecosistema.

---

### Apéndice N — Catálogo extendido de preguntas doradas del chat (eval)

| ID | Pregunta dorada | Debe citar | No debe |
|----|-----------------|------------|---------|
| GQ01 | ¿Cuántos m² cubiertos hay? | Level/Space areas | Inventar |
| GQ02 | ¿Ml de muro exterior PB? | Walls filtrados | Mezclar interior |
| GQ03 | ¿Cuántas ventanas hay? | Openings | Contar puertas |
| GQ04 | ¿Qué ambiente es el más caro? | Cost rollup Space | Opinión estética |
| GQ05 | ¿Falta algo para un PH típico? | Completeness checklist | Norma legal firme |
| GQ06 | ¿Impacto +15% cemento? | Simulación cost | Afirmar stock mercado |
| GQ07 | ¿Diferencia vs escenario SF? | compare_scenarios | Ignorar rangos |
| GQ08 | ¿Qué entidades están rojas? | confidence query | Minimizar riesgo |
| GQ09 | ¿Cuánto certificamos vs plan? | Progress/Cert | Hablar sin datos obra |
| GQ10 | Armá resumen para cliente | Draft + disclaimer | Prometer fijo sin freeze |
| GQ11 | ¿Qué comprar esta semana? | BOM + schedule | OC sin confirmación |
| GQ12 | ¿Hay inconsistencia de escala? | Validators | Callar anomalía |
| GQ13 | ¿m² de pintura interior? | Takeoff pintura | Incluir exterior sin pedir |
| GQ14 | ¿Potencia eléctrica estimada? | Electrical proxies | Dictamen de instalador |
| GQ15 | ¿Merma usada en pisos? | Policy mermas | Ocultar default |

### Apéndice O — Matriz RACI estratégica (roles de compañía)

| Decisión | Founder/CEO | Product | Eng | Domain Expert | GTM |
|----------|-------------|--------|-----|---------------|-----|
| Principios no negociables | A | C | C | C | I |
| Prioridad de fase | A | R | C | C | C |
| Umbrales confidence | A | R | C | R | I |
| Lanzamiento chat público | A | R | R | C | C |
| Entrada a un país nuevo | A | C | C | C | R |
| Partner marketplace | A | C | I | C | R |
| Declaraciones de precisión externas | A | C | I | R | R |

R = Responsible, A = Accountable, C = Consulted, I = Informed

### Apéndice P — Glosario extendido LATAM obra-cómputo

| Término local | Equivalencia en ARQ-IA |
|---------------|------------------------|
| Cómputo y presupuesto | Takeoff + CostModel |
| Computista / medidor | Rol Estimator |
| Global | CostItem tipo paquete |
| Certificado de avance | Certification |
| Adicional | Change order / scenario aprobado |
| Obrador | Site context / temporarios |
| Corralón | Supplier category |
| Expediente municipal | Document pack (no automatizado total) |
| Dirección de obra | SiteManager workflows |
| Memoria descriptiva | Docs Scribe output |
| Pliego | Docs pack |
| Ítem | CostItem |
| Análisis de precios | Formula + PU breakdown |
| Curva de inversión | Cashflow view |

### Apéndice Q — Plantilla de one-pager para inversores (contenido)

1. Problema: cómputo lento, opaco, frágil ante inflación.  
2. Wedge: plano→cantidades→ARS en minutos.  
3. Visión: OSCQ con MDO.  
4. Por qué ahora: LLM para explicación + subdigitalización LATAM.  
5. Producto: L1 percepción · L2 twin · L3 inteligencia.  
6. Moat: corpus · fórmulas · precios · hábito.  
7. Roadmap: Trust → MDO/Chat → Systems → Site/Ent → Platform.  
8. Packaging: Free/Pro/Enterprise.  
9. Riesgo principal: precisión; mitigación: confidence+HITL.  
10. Ask: construir la capa de verdad cuantitativa de la construcción.

### Apéndice R — Declaración de alineación final

Este Plan Maestro se alinea explícitamente con la realidad baseline de arq-ia.pro (percepción clásica, monolitos, módulos core, planes Free/Pro) **solo como trampolín**. El destino no es un CV mejorado: es una compañía que posee el modelo digital de millones de decisiones de obra.

---

**Control de longitud y densidad:** secciones 0–16 + apéndices A–R + ampliaciones 1–30 constituyen el cuerpo estratégico completo destinado a lectura interna profunda y extracción de one-pagers por rol.

**— Fin de ampliaciones y apéndices extendidos —**
