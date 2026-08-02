# ARQ-IA — DOMAIN HANDBOOK

**Manual oficial del dominio de negocio**

| Campo | Valor |
| --- | --- |
| Título | ARQ-IA — DOMAIN HANDBOOK |
| Subtítulo | Manual oficial del dominio de negocio |
| Fecha | 2026-08-02 |
| Estado | Official business reference |
| Audiencia | Todos los builders de ARQ-IA (desarrolladores, arquitectos de software, ingenieros, product, AIs) |
| Naturaleza | Lenguaje de negocio — sin implementación |
| Mercado de referencia | LATAM primero, Argentina primero |
| Autoridad conceptual | MDO como fuente de verdad de hechos de obra |
| Empaque comercial | Free / Pro / Enterprise (no es ontología de dominio) |

> Este handbook define **qué significa** el negocio de ARQ-IA. No describe APIs, tablas, clases ni código. Si un término de presupuesto, cómputo, muro o certificación aparece en producto o conversación de equipo, su significado se busca aquí primero.

---

## Índice

- 0. Cómo usar este handbook
- 1. Principios de dominio (negocio)
- 2. Catálogo de conceptos
- 3. Reglas de negocio globales
- 4. Unidades y convenciones LATAM
- 5. Matriz de impactos (resumen)
- 6. Anti-definiciones (qué ARQ-IA NO es en dominio)
- 7. Errores de dominio frecuentes (catálogo)
- 8. Glosario rápido A–Z
- 9. Criterios de conformidad
- Apéndice A — Tipologías de obra de referencia
- Apéndice B — Checklist jefe de obra al revisar un cómputo
- Apéndice C — Checklist arquitecto al pintar/interpretar plano
- Apéndice D — Escenarios constructivos canónicos
- Apéndice E — Approval / change control de este handbook

---

## 0. Cómo usar este handbook

### 0.1 Propósito

ARQ-IA cuantifica obra. El producto convierte interpretación de planos y hechos de obra en cantidades, materiales, costos y decisiones. Este handbook es la biblia del lenguaje de negocio: qué es un muro, qué es un presupuesto sellado, qué puede proponer la IA y qué decide un humano.

Se escribe para que un desarrollador, un arquitecto de software, un ingeniero civil, un jefe de obra argentino y un agente de IA usen las mismas palabras con el mismo significado.

### 0.2 Jerarquía de autoridad (significado vs construcción)

| Orden | Documento | Autoridad sobre… |
| --- | --- | --- |
| 1 | **Domain Handbook (este documento)** | Significado de términos de negocio, reglas de dominio, impactos, anti-definiciones |
| 2 | RFCs de dominio (p. ej. RFC-E02-MDO, RFC-E01) | Contratos de diseño alineados al significado; si hay conflicto de *significado*, gana este handbook |
| 3 | Architecture / Engineering Roadmap / Master Plan | Cómo construir, secuenciar y empaquetar producto |
| 4 | Código, UI, prompts, scripts | Implementación; nunca redefine el dominio en silencio |

**Regla de lectura:** si un RFC nombra una entidad y este handbook define el concepto de negocio, el RFC operacionaliza; el handbook semántiza. Si el código inventa un término sin ancla aquí, es deuda de dominio.

### 0.3 Reglas de lectura del glosario y del catálogo

1. Leer primero **Qué es** y **Qué no representa** antes de inventar pantallas o mensajes.
2. Las **Reglas de negocio** son obligatorias en producto; no son tips opcionales.
3. Los **Casos especiales** son situaciones reales de obra LATAM que el dominio debe soportar conceptualmente.
4. **Relaciones** describen dependencia de significado, no esquemas de datos.
5. **Ejemplos reales** priorizan vivienda unifamiliar, PH, local comercial y obra chica/mediana argentina.
6. **Errores frecuentes** son anti-patrones de pensamiento de negocio.
7. Las secciones de **Impacto** siempre se leen en cuatro ejes: presupuestos, materiales, costos, cronograma.

### 0.4 Qué significa «impacto» en cada sección

| Eje de impacto | Pregunta de negocio | Ejemplo mental |
| --- | --- | --- |
| **Presupuestos** | ¿Cambia el documento comercial, el sello, la comparación entre versiones o la certificación? | Sellado, baseline, extras |
| **Materiales** | ¿Cambia qué se compra, en qué unidad, con qué desperdicio o sistema constructivo? | Ladrillo vs retak, cerámicos de baño |
| **Costos** | ¿Cambia el dinero (ARS u otra moneda local), unitarios, mano de obra o rubros? | Precio unitario, inflación, OC |
| **Cronograma** | ¿Cambia secuencia, duración, avance o hitos de obra? | Contrapiso antes de piso, certificaciones parciales |

| Nivel | Significado operativo |
| --- | --- |
| **Alto** | Si se malinterpreta el concepto, el estimado o la obra se corrompe de forma material |
| **Medio** | Distorsiona cantidades o dinero de forma relevante pero acotada |
| **Bajo** | Afecta claridad, trazabilidad o calidad de decisión sin romper el núcleo |
| **Nulo** | No mueve ese eje por definición de dominio |

### 0.5 Roles mentales al leer

| Rol | Pregunta que debe hacerse |
| --- | --- |
| Desarrollador / AI coding | ¿Estoy modelando un hecho de obra, una proyección, una propuesta o un empaque comercial? |
| Arquitecto de software | ¿Quién es autoridad: MDO, percepción, humano, libro de precios? |
| Ingeniero / arquitecto de obra | ¿Esta definición sobrevive en una vivienda de 90 m² en Gran Buenos Aires? |
| Jefe de obra | ¿Puedo certificar o pedir compra con este significado sin pelearme con el cómputo? |
| Producto | ¿Free/Pro/Enterprise limita *capacidad*, no redefine *qué es un muro*? |

### 0.6 Distinciones fundacionales

| Distinción | Definición corta |
| --- | --- |
| Hecho vs proyección | El hecho vive en el Modelo Digital de la Obra; la proyección (cómputo, costo) se deriva y se puede regenerar |
| Propuesta vs decisión | Percepción e IA proponen; humano (o política humana explícita) decide, sobre todo si hay dinero |
| Versión abierta vs sellada | Abierta admite cambio de hechos; sellada congela el estado para dinero/certificación |
| Escenario vs tipología de obra | Escenario = alternativa constructiva/comercial; tipología = clase de edificio/uso |
| Empaque vs ontología | Free/Pro/Enterprise limita capacidades; no inventa entidades distintas |
| Cantidad neta vs comprable | Neta sale del cómputo; comprable suma desperdicio, redondeo de compra y criterio de obra |

### 0.7 Cómo NO usar este handbook

- No copiar fragmentos como especificación de API.
- No usarlo para justificar inventar metros cuadrados desde un LLM.
- No usarlo para mezclar dominio de obra con pricing de plan SaaS.
- No usarlo como reglamento municipal ni como cálculo estructural firmable.
- No usarlo para pelear «BIM vs no BIM»: ARQ-IA es cuantificación operativa.

### 0.8 Protocolo de desacuerdo

1. Detectar ambigüedad de término en PR, diseño o prompt.
2. Buscar el concepto en la sección 2 y la regla global en la sección 3.
3. Si falta el concepto, proponer enmienda al handbook (Apéndice E) antes de inventar semántica en código.
4. Si el conflicto es de *cómo construir*, ir a Architecture/Roadmap; si es de *qué significa*, queda aquí.

---

## 1. Principios de dominio (negocio)

Estos principios son de **negocio**. No son patrones de software. Violarios corrompe presupuestos, compras y confianza del cliente aunque la feature «funcione».

### D01 — El MDO es la fuente de verdad conceptual de la obra

Los hechos de obra (espacios, muros, aberturas, sistemas, bindings de material por escenario, sellos) viven en el Modelo Digital de la Obra. Listas de precios, renders, chats y PDFs no son autoridad de hechos.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D02 — La percepción propone; no declara verdad final

Un motor de visión, OCR o asistente puede detectar un muro o una medida. Eso es evidencia o propuesta. Hasta aceptación humana (o política humana acotada y explícita), no es cantidad presupuestable confiable.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D03 — La IA nunca inventa cantidades

Un modelo de lenguaje puede explicar, clasificar, sugerir rubros o redactar. No puede fabricar metros, kilos ni unidades sin ancla en hechos medidos o confirmados. Sin cita a hecho o proyección, no hay número comercial.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D04 — El humano decide el dinero

Firmas, sellos de presupuesto, certificaciones y órdenes de compra que mueven dinero requieren aceptación humana. La automatización puede preparar; no cerrar en silencio.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D05 — Inmutabilidad de presupuestos sellados

Una versión sellada o firmada no se «arregla» editando el pasado. Todo cambio material produce nueva versión, cambio documentado o adicional/extra.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D06 — Confianza obligatoria en hechos cuantitativos

Toda cantidad material lleva (explícita o heredada) una noción de confianza y origen. Un número sin confianza no debe presentarse al cliente como cerrado.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D07 — Provenance: todo número tiene pedigrí

Debe poder responderse: ¿vino de plano calibrado, de regla de obra, de carga manual, de proveedor o de propuesta de IA? Sin pedigrí no hay auditoría.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D08 — Prohibido el doble conteo

Un muro compartido entre living y dormitorio no se compra dos veces. Una abertura no se descuenta dos veces del mismo revoque. El dominio privilegia identidad única del elemento.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D09 — Unidades SI con hábitos LATAM

Metros, m², m³, ml, kg, unidades. Espesores en cm cuando el oficio habla en cm. Dinero en moneda local del proyecto (ARS en wedge Argentina).

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D10 — Separar cantidad, unitario y dinero

Cantidad ≠ precio. Precio unitario ≠ presupuesto. Presupuesto ≠ certificación. Certificación ≠ orden de compra.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D11 — Escenarios comparan alternativas; no clonan la obra entera

Ladrillo vs steel frame vs retak son escenarios sobre geometría compartida cuando la geometría no cambia.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D12 — Free/Pro/Enterprise es empaque, no ontología

Que un plan permita tres escenarios o uno no cambia qué es un escenario. Los límites comerciales no redefinen muros, ambientes ni certificaciones.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D13 — Baseline es el ancla de comparación y avance

Sin baseline claro no hay certificación coherente ni extras medibles. El avance se mide contra lo aprobado.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D14 — Los extras/adicionales son cambios con dinero y trazabilidad

Un adicional no es un ajuste silencioso. Es un cambio de alcance respecto del baseline, con impacto en cantidad, costo y a menudo cronograma.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D15 — Ambientes húmedos imponen terminaciones y sistemas distintos

Baño, cocina, lavadero y similares cambian impermeabilización, desagües, revestimientos y supuestos de terminación.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D16 — Altura es supuesto de negocio explícito

Si el plano no declara altura, el dominio usa supuestos documentados (global o por ambiente). Nunca altura mágica distinta por pantalla.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D17 — Desperdicio es criterio de obra, no adorno

El desperdicio transforma cantidad neta en cantidad comprable. Debe ser visible, tipificado y revisable por humano de obra.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D18 — Rubro organiza el lenguaje comercial del presupuesto

El cliente y el contratista piensan en albañilería, sanitarios, electricidad. El cómputo alimenta rubros; los rubros no reescriben la geometría.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D19 — Evidencia no es presupuesto

Una foto, un recorte de plano o una detección es soporte. No reemplaza el sello ni la línea de cómputo aceptada.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D20 — Cronograma sigue a la lógica constructiva

Contrapiso antes de piso; instalaciones embutidas antes de revoque fino cuando corresponde. El dominio respeta dependencias de oficio.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D21 — Un solo significado por término

Ambiente, zona y local no se usan como sinónimos flojos. Si el producto habla español de obra, usa las definiciones de este handbook.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D22 — Escala/calibración es condición de medida

Sin escala confiable no hay cantidad confiable. Un cómputo hermoso con escala dudosa es un riesgo comercial.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D23 — El cómputo métrico es el puente entre modelo y dinero

Takeoff/cómputo traduce elementos a líneas cuantificadas. Sin ese puente, el presupuesto flota.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D24 — Proveedor y precio no definen geometría

Una oferta puede bindearse a una especificación o línea de cómputo; no puede crear muros fantasma.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### D25 — Transparencia ante inflación y volatilidad LATAM

El dominio distingue cantidad estable (hechos) de precio actualizable (libros/ofertas), y documenta la fecha de referencia del dinero.

**Implicancia diaria:** cualquier feature, prompt o regla que contradiga este principio debe detenerse y escalarse a Domain Owner / CTO antes de adoptarse como verdad de producto.

### 1.1 Tabla resumen de principios

| ID | Principio (corto) | Violación típica |
| --- | --- | --- |
| D01 | El MDO es la fuente de verdad conceptual de la obra | Ignorar el principio «por velocidad» o «solo en el chat» |
| D02 | La percepción propone; no declara verdad final | Ignorar el principio «por velocidad» o «solo en el chat» |
| D03 | La IA nunca inventa cantidades | Ignorar el principio «por velocidad» o «solo en el chat» |
| D04 | El humano decide el dinero | Ignorar el principio «por velocidad» o «solo en el chat» |
| D05 | Inmutabilidad de presupuestos sellados | Ignorar el principio «por velocidad» o «solo en el chat» |
| D06 | Confianza obligatoria en hechos cuantitativos | Ignorar el principio «por velocidad» o «solo en el chat» |
| D07 | Provenance: todo número tiene pedigrí | Ignorar el principio «por velocidad» o «solo en el chat» |
| D08 | Prohibido el doble conteo | Ignorar el principio «por velocidad» o «solo en el chat» |
| D09 | Unidades SI con hábitos LATAM | Ignorar el principio «por velocidad» o «solo en el chat» |
| D10 | Separar cantidad, unitario y dinero | Ignorar el principio «por velocidad» o «solo en el chat» |
| D11 | Escenarios comparan alternativas; no clonan la obra entera | Ignorar el principio «por velocidad» o «solo en el chat» |
| D12 | Free/Pro/Enterprise es empaque, no ontología | Ignorar el principio «por velocidad» o «solo en el chat» |
| D13 | Baseline es el ancla de comparación y avance | Ignorar el principio «por velocidad» o «solo en el chat» |
| D14 | Los extras/adicionales son cambios con dinero y trazabilidad | Ignorar el principio «por velocidad» o «solo en el chat» |
| D15 | Ambientes húmedos imponen terminaciones y sistemas distintos | Ignorar el principio «por velocidad» o «solo en el chat» |
| D16 | Altura es supuesto de negocio explícito | Ignorar el principio «por velocidad» o «solo en el chat» |
| D17 | Desperdicio es criterio de obra, no adorno | Ignorar el principio «por velocidad» o «solo en el chat» |
| D18 | Rubro organiza el lenguaje comercial del presupuesto | Ignorar el principio «por velocidad» o «solo en el chat» |
| D19 | Evidencia no es presupuesto | Ignorar el principio «por velocidad» o «solo en el chat» |
| D20 | Cronograma sigue a la lógica constructiva | Ignorar el principio «por velocidad» o «solo en el chat» |
| D21 | Un solo significado por término | Ignorar el principio «por velocidad» o «solo en el chat» |
| D22 | Escala/calibración es condición de medida | Ignorar el principio «por velocidad» o «solo en el chat» |
| D23 | El cómputo métrico es el puente entre modelo y dinero | Ignorar el principio «por velocidad» o «solo en el chat» |
| D24 | Proveedor y precio no definen geometría | Ignorar el principio «por velocidad» o «solo en el chat» |
| D25 | Transparencia ante inflación y volatilidad LATAM | Ignorar el principio «por velocidad» o «solo en el chat» |

---

## 2. Catálogo de conceptos

Cada concepto usa la misma plantilla. Los grupos son de navegación; la ontología de negocio es el conjunto completo.

### 2.1 Núcleo de proyecto y espacialidad

Este grupo responde: ¿dónde está la obra, qué versión de la verdad usamos, y cómo partimos el espacio?

#### Proyecto

- **Qué es**
  - Unidad de negocio que agrupa una obra (o conjunto coherente) bajo un tenant, con actores, planos, versiones, escenarios y documentos comerciales asociados.
- **Qué representa**
  - La obra digital como expediente vivo: desde anteproyecto hasta archivo.
  - El contenedor de decisiones: cliente, moneda, baseline, escenarios activos.
  - El ancla de colaboración entre estudio, contratista y proveedores.
- **Qué no representa**
  - Un archivo PDF suelto.
  - Una suscripción Free/Pro/Enterprise (empaque de cuenta).
  - Un presupuesto único e inmutable por sí solo.
  - Un modelo BIM completo de coordinación multidisciplinaria.
- **Reglas de negocio**
  - Todo hecho de obra pertenece a un proyecto (directa o vía versión).
  - El proyecto declara moneda local de trabajo y hábitos de unidades.
  - Archivar un proyecto no borra historia sellada.
  - Duplicar un proyecto crea nuevas identidades; no comparte hechos mudables con el original.
  - Los actores del proyecto son roles de negocio, no equivalen automáticamente a usuarios de login.
- **Casos especiales**
  - PH con unidades por etapa: un proyecto puede tener varios edificios o niveles con baselines parciales.
  - Obra en dos lotes contiguos del mismo cliente: un proyecto con dos sitios o dos proyectos; la decisión es de expediente comercial.
  - Remodelación sobre existente: admite baseline de estado actual vs estado proyectado vía versiones/escenarios.
- **Relaciones con otras entidades**
  - Contiene Sitio/Edificio/Nivel/Ambiente a través de sus versiones.
  - Posee Versiones, Escenarios, Planos, Timeline, Presupuestos y Certificaciones.
  - Se relaciona con Cliente, Contratista, Subcontratista y Proveedor vía roles.
- **Ejemplos reales**
  - Vivienda unifamiliar 120 m² en Moreno (GBA): un sitio, un edificio, PB + terraza.
  - Local comercial en PB de edificio existente en Palermo: proyecto de adecuación con baseline de demolición/obra nueva.
  - PH de 6 unidades en Córdoba: un proyecto, un edificio, múltiples ambientes por unidad.
- **Errores frecuentes**
  - Tratar el último Excel exportado como el proyecto.
  - Crear un proyecto por cada escenario (ladrillo/steel) en lugar de escenarios dentro del proyecto.
  - Confundir proyecto con tenant u organización.
- **Impacto sobre presupuestos**
  - Alto: define el expediente sobre el que se sellan presupuestos.
  - Sin proyecto claro no hay baseline ni certificación atribuible.
- **Impacto sobre materiales**
  - Medio: organiza catálogos y bindings, pero no es un material.
  - Determina contexto de sistemas constructivos admitidos.
- **Impacto sobre costos**
  - Alto: moneda, locale y actores del dinero viven aquí.
  - Los costos sin proyecto son listas huérfanas.
- **Impacto sobre cronograma**
  - Medio-Alto: el timeline de obra es del proyecto.
  - Hitos de certificación y avance se anclan al proyecto/baseline.

#### Plano

- **Qué es**
  - Documento gráfico de referencia (planta, corte, detalle) que alimenta la percepción y la calibración de medida; es evidencia documental, no el modelo de obra.
- **Qué representa**
  - La hoja de dibujo que el oficio usa para entender geometría y usos.
  - Un activo de proyecto con escala, nombre de hoja y supersesión.
  - La fuente típica del wedge color→cantidad en LATAM.
- **Qué no representa**
  - El Modelo Digital de la Obra.
  - El presupuesto.
  - La verdad final de cantidades sin calibración ni aceptación.
  - Un CAD editable autoritativo dentro de ARQ-IA.
- **Reglas de negocio**
  - Un plano puede ser supersedido; el plano viejo permanece como evidencia histórica.
  - Sin escala/calibración confiable, las cantidades derivadas se marcan de baja confianza.
  - Pintar o interpretar colores es protocolo de percepción; no cambia la ontología de muro.
  - Varios planos pueden describir el mismo edificio; el modelo unifica.
  - El plano no se vende como certificación.
- **Casos especiales**
  - Plano sin cota ni escala gráfica legible: se exige calibración manual antes de cómputo cliente.
  - Plano de instalaciones superpuesto a arquitectura: aporta sistemas, no redefine ambientes salvo criterio explícito.
  - Replanteo en obra que contradice el plano: se documenta Cambio + Evidencia.
- **Relaciones con otras entidades**
  - Se asocia al Proyecto; produce Evidencia; informa Escala/calibración.
  - Las Versiones citan qué planos/evidencias respaldan elementos.
  - No posee cantidades por sí mismo; las cantidades viven en el Cómputo vía elementos.
- **Ejemplos reales**
  - Planta de vivienda en A0 escaneada desde estudio en Rosario.
  - Plano municipal de local gastronómico con cocina y salón.
  - Planta de PH con medianeras y patios de aire/luz.
- **Errores frecuentes**
  - Creer que subir el plano ya es tener modelo.
  - Mezclar hojas de distintas escalas sin recalibrar.
  - Usar un detalle 1:20 como si fuera planta 1:50 para medir muros.
- **Impacto sobre presupuestos**
  - Alto indirecto: mala interpretación del plano corrompe todo presupuesto derivado.
  - El plano en sí no es línea de presupuesto.
- **Impacto sobre materiales**
  - Alto indirecto: tipologías interpretadas disparan sistemas y materiales.
- **Impacto sobre costos**
  - Alto indirecto vía cómputo; nulo como precio unitario.
- **Impacto sobre cronograma**
  - Bajo-Medio: define hitos de documentación; no programa cuadrillas por sí solo.

#### Versión

- **Qué es**
  - Instantánea versionada de los hechos de obra del proyecto (estado del MDO) que puede abrirse, sellarse o firmarse; es el commit de negocio de la verdad cuantitativa.
- **Qué representa**
  - Un estado recuperable del modelo: geometría, espacios, bindings relevantes al head.
  - El ancla de un presupuesto o certificación (presupuestado sobre versión V12).
  - La unidad de comparación entre antes y después de un Cambio.
- **Qué no representa**
  - Un escenario (el escenario apunta a heads de versión).
  - Un archivo de plano.
  - Un export PDF del presupuesto.
  - Un autosave cosmético sin hechos.
- **Reglas de negocio**
  1. Crear versión implica partir de un padre o baseline coherente.
  2. Al sellar o firmar, los hechos de esa versión no se editan in-place.
  3. Todo cambio material posterior produce nueva versión (o tip de escenario) vía cambio documentado.
  - Una versión puede ser baseline del proyecto o de un escenario.
  - Comparar versiones es operación de negocio legítima para extras y auditorías.
  - La confianza agregada de una versión condiciona si puede mostrarse al cliente como cerrada.
- **Casos especiales**
  - Versión de anteproyecto vs versión de obra: mismo proyecto, distinto grado de detalle y confianza.
  - Versión firmada para cliente y versión de trabajo interna: no confundir sellos.
  - Cambio de nombre de ambiente sigue siendo cambio versionado si toca hechos.
- **Relaciones con otras entidades**
  - Pertenece a un Proyecto; puede ser head de un Escenario.
  - Congela el contexto de Cómputo, Presupuesto y Certificación.
  - Se relaciona con Timeline y con Evidencia aceptada hasta ese punto.
- **Ejemplos reales**
  - V0 tras carga inicial de planta de chalet en Nordelta.
  - V7 sellada enviada al cliente del local; V8 abre adicionales de aire acondicionado.
  - Baseline de PH antes de enchapes; versión posterior con cambio de cerámico.
- **Errores frecuentes**
  - Editar la versión firmada porque el cliente pidió un ajuste chico.
  - Crear versiones sin resumen de cambio: se pierde memoria de obra.
  - Confundir número de versión de app con versión de obra.
- **Impacto sobre presupuestos**
  - Alto: el presupuesto serio cita versión.
  - Sin sello de versión, el dinero es borrador.
- **Impacto sobre materiales**
  - Alto: los bindings de material efectivos se leen en la versión/escenario head.
- **Impacto sobre costos**
  - Alto: unitarios aplicados sobre cómputo de esa versión.
  - Reapreciar sin nueva versión rompe trazabilidad.
- **Impacto sobre cronograma**
  - Medio: el avance y las certificaciones se anclan a versiones/baseline.

#### Escenario

- **Qué es**
  - Rama de negocio que representa una alternativa constructiva o de especificación (p. ej. ladrillo vs steel frame vs retak) sobre una base compartida de hechos, permitiendo comparar cantidades y costos sin redefinir la obra entera.
- **Qué representa**
  - Una hipótesis operable: misma vivienda, distinto sistema de muros.
  - Un head que apunta a una Versión efectiva para lectura de bindings y proyecciones.
  - La unidad de comparación A/B/C en decisiones de cliente y dirección de obra.
- **Qué no representa**
  - Un plan comercial Free/Pro/Enterprise.
  - Una tipología de edificio (vivienda/PH/local).
  - Una copia completa e independiente de toda la geometría por default.
  - Un presupuesto sin relación con el baseline.
- **Reglas de negocio**
  - La geometría base se comparte cuando no cambia; divergen materiales, parámetros de sistema y a veces espesores.
  - Firmar un escenario no sella automáticamente los demás.
  - Comparar escenarios exige misma base geométrica o declarar divergencia geométrica explícita.
  - El número de escenarios visibles puede estar limitado por empaque comercial; el concepto no cambia.
  - Un pack ladrillo→steel es un cambio de escenario, no un nuevo proyecto.
- **Casos especiales**
  - Escenario de terminaciones premium vs standard con misma albañilería.
  - Escenario con HVAC split vs sin climatización.
  - Escenario de ampliación futura no construida: marcar fuera de baseline de certificación actual.
- **Relaciones con otras entidades**
  - Apunta a Versión (head).
  - Reinterpreta Material / Sistema constructivo / bindings.
  - Alimenta Cómputo y Presupuesto comparativos.
  - Convive con Baseline del proyecto (promote elige un head).
- **Ejemplos reales**
  - Casa 3 dormitorios: Escenario A ladrillo común, B steel frame, C retak.
  - Local: frente vidriado pesado vs carpintería standard.
  - PH: azotea transitable vs no transitable.
- **Errores frecuentes**
  - Clonar el proyecto tres veces y perder comparabilidad.
  - Mezclar en un mismo head dos sistemas incompatibles sin declarar pack.
  - Certificar el promedio de tres escenarios.
- **Impacto sobre presupuestos**
  - Alto: cambia el presupuesto comparable y a veces el sellable.
  - Es la herramienta de decisión económica pre-contrato.
- **Impacto sobre materiales**
  - Alto: redefine especificaciones y consumos.
- **Impacto sobre costos**
  - Alto: es el corazón del diff de costos A/B/C.
- **Impacto sobre cronograma**
  - Medio-Alto: distintos sistemas implican distintas cuadrillas y plazos.

#### Sitio

- **Qué es**
  - El predio o lote donde se inserta la obra: límites, ubicación de negocio y contexto de implantación.
- **Qué representa**
  - El dónde predial de la obra.
  - La referencia de implantación de uno o más edificios.
  - El marco de restricciones de entorno (medianeras, frente, fondo) cuando importan al cómputo.
- **Qué no representa**
  - La dirección de facturación del cliente.
  - Un pin de mapa como única verdad geométrica de muros.
  - El municipio como entidad legal certificadora.
- **Reglas de negocio**
  - Un proyecto típico wedge tiene un sitio; puede tener más si el expediente lo justifica.
  - Área de lote no reemplaza área cubierta ni área de ambientes.
  - Medianeras y retiros afectan muros y aberturas de borde.
  - Sin sitio explícito, el edificio puede existir, pero se pierde contexto de implantación.
- **Casos especiales**
  - Dos casas en un mismo lote: un sitio, dos edificios.
  - Local en shopping: el sitio puede ser la unidad funcional arrendada.
  - Obra en PH: sitio del conjunto + clarificación de unidad.
- **Relaciones con otras entidades**
  - Contiene Edificio(s).
  - Pertenece al Proyecto vía Versión.
  - Condiciona Fundación y accesos, y a veces acometidas.
- **Ejemplos reales**
  - Lote 8,50 × 30 m en Isidro Casanova con vivienda al frente.
  - Terreno en esquina en Mendoza: dos frentes afectan aberturas y revoques exteriores.
  - Predio industrial chico con nave y oficina: un sitio, tipologías mixtas.
- **Errores frecuentes**
  - Usar área de lote como m² a revestir.
  - Ignorar medianera y distorsionar muros de frontera.
- **Impacto sobre presupuestos**
  - Medio: impacta ítems de implantación, cercos, movimientos de suelo cuando están en alcance.
- **Impacto sobre materiales**
  - Medio: acometidas, rellenos, bases.
- **Impacto sobre costos**
  - Medio: costos de obrador, transporte, dificultad de acceso.
- **Impacto sobre cronograma**
  - Medio-Alto: logística de obra y secuencia de replanteo.

#### Edificio

- **Qué es**
  - Volumen construible principal (o secundario) dentro del sitio, con tipología de uso y organización en niveles.
- **Qué representa**
  - La casa, el bloque de PH, el local, la nave.
  - El contenedor de Niveles y de la lógica estructural/envolvente.
  - La unidad tipológica de referencia (vivienda, PH, comercial).
- **Qué no representa**
  - Un ambiente.
  - Un rubro del presupuesto.
  - Un archivo RVT/IFC completo.
- **Reglas de negocio**
  - Todo ambiente y nivel pertenece a un edificio en el modelo canónico.
  - La tipología del edificio condiciona supuestos (alturas, instalaciones mínimas, terminaciones).
  - Ampliaciones pueden modelarse como parte del mismo edificio o como volumen vinculado; debe declararse.
  - Demoliciones parciales son Cambios sobre el edificio, no un edificio negativo silencioso.
- **Casos especiales**
  - Edificio existente + ampliación: distinguir elementos existentes vs nuevos.
  - Local en PB de edificio de viviendas: edificio/unidad funcional según expediente.
  - Quincho separado: segundo edificio en el mismo sitio.
- **Relaciones con otras entidades**
  - Pertenece a Sitio; contiene Niveles.
  - Agrupa Muros, Losas, Cubierta, Fundación a escala de obra.
  - Determina Escenarios aplicables de envolvente.
- **Ejemplos reales**
  - Chalet PB+1 en Tigre.
  - Bloque de PH con PB comercial + dos plantas de unidades.
  - Local esquina con entrepiso liviano.
- **Errores frecuentes**
  - Presupuestar el edificio como una sola línea cuando el cliente necesita rubros.
  - Duplicar el edificio al crear escenario de material.
- **Impacto sobre presupuestos**
  - Alto: concentra el alcance sellable.
- **Impacto sobre materiales**
  - Alto: define paquetes de sistema constructivo.
- **Impacto sobre costos**
  - Alto: estructura el presupuesto por obra.
- **Impacto sobre cronograma**
  - Alto: unidad de programación macro.

#### Nivel

- **Qué es**
  - Planta o piso del edificio con elevación de negocio (PB, 1º, azotea, sótano) que organiza ambientes y elementos horizontales.
- **Qué representa**
  - La planta de trabajo donde se contabilizan ambientes.
  - La referencia de altura entre pisos y de circulación vertical.
  - El contenedor habitual de plantas de arquitectura.
- **Qué no representa**
  - Un layer de dibujo sin significado de obra.
  - Un ambiente.
  - Una etapa de certificación por sí sola.
- **Reglas de negocio**
  - Cada ambiente pertenece a un nivel.
  - La altura libre por nivel es supuesto crítico para muros, pintura e instalaciones.
  - Azotea/terraza es nivel con reglas de cubierta/impermeabilización distintas.
  - Entreplantas y altillos se declaran; no se dibujan de contrabando en PB.
- **Casos especiales**
  - PB comercial + planta alta vivienda: dos niveles con tipologías distintas.
  - Sótano de servicios: nivel con MEP especiales.
  - No confundir depósito de obra con nivel arquitectónico.
- **Relaciones con otras entidades**
  - Pertenece a Edificio; contiene Ambientes y Zonas.
  - Hospeda Losas, Pisos, parte de Columnas/Escaleras.
  - Corta verticalmente Instalaciones.
- **Ejemplos reales**
  - PB de vivienda con living-comedor y cocina.
  - 1º piso con dormitorios y baño en suite.
  - Azotea con lavadero exterior y tanque.
- **Errores frecuentes**
  - Aplicar altura de PB a todos los niveles sin revisar.
  - Olvidar antepechos y barandas de terraza en azotea.
- **Impacto sobre presupuestos**
  - Alto: reparte cantidades por planta en el presupuesto.
- **Impacto sobre materiales**
  - Alto: pisos, carpetas, cielorrasos por nivel.
- **Impacto sobre costos**
  - Alto: mano de obra y andamios pueden cambiar por nivel.
- **Impacto sobre cronograma**
  - Alto: secuencia vertical de obra.

#### Ambiente

- **Qué es**
  - Espacio ocupable o funcional con uso tipificado (dormitorio, baño, cocina, local de venta, depósito) y área, que concentra terminaciones e instalaciones de uso.
- **Qué representa**
  - La habitación o local que el cliente reconoce por nombre.
  - La unidad de cómputo de solados, pintura interior, zócalos y muchas instalaciones terminales.
  - El portador de reglas de ambiente húmedo cuando aplica.
- **Qué no representa**
  - Una zona lógica de incendio/HVAC.
  - Un muro.
  - Un renglón genérico ambientes varios sin tipificar.
- **Reglas de negocio**
  - Todo ambiente tiene tipo de uso; el tipo dispara reglas (húmedo, carga eléctrica, desagües).
  - El área de ambiente no incluye muros por arte de magia; el criterio de medición debe ser explícito.
  - Ambientes abiertos (living-comedor) pueden modelarse unidos o separados; el criterio debe ser estable.
  - Patios y terrazas se tipifican; no son dormitorios.
  - La altura del ambiente, si difiere del nivel, se declara.
- **Casos especiales**
  - Toilette vs baño completo: distinto cómputo sanitario y revestimientos.
  - Cocina integrada: frontera con living afecta terminaciones.
  - Local comercial diáfano: un ambiente grande con zonas internas.
- **Relaciones con otras entidades**
  - Pertenece a Nivel; hospeda Piso, parte de Aberturas, terminales MEP.
  - Se relaciona con Zona.
  - Dispara Impermeabilización/Aislación/Terminación según uso.
- **Ejemplos reales**
  - Dormitorio 3,20 × 3,50 en vivienda de La Plata.
  - Baño de PH con ducha y ventilación a patio.
  - Salón de ventas 60 m² + depósito trasero 15 m².
- **Errores frecuentes**
  - Usar el nombre del ambiente como única tipificación.
  - Computar pintura de cielorraso con área de piso sin validar cielorraso real.
  - Olvidar umbrales y desniveles en ambientes húmedos.
- **Impacto sobre presupuestos**
  - Alto: gran parte del presupuesto de terminaciones se arma por ambiente.
- **Impacto sobre materiales**
  - Alto: cerámicos, pinturas, grifería, artefactos.
- **Impacto sobre costos**
  - Alto: unitarios de terminación y sanitarios.
- **Impacto sobre cronograma**
  - Medio-Alto: habilita trabajo por frente de ambientes.

#### Zona

- **Qué es**
  - Agrupación lógica dentro de un nivel (o cruzando ambientes) para criterios operativos: HVAC, etapa de obra, sector comercial; no necesariamente un ambiente arquitectónico.
- **Qué representa**
  - Un recorte de gestión: sector noche, área húmeda, zona A/C.
  - Una etiqueta de cómputo/planificación cuando el ambiente solo no alcanza.
  - Un mecanismo para reglas transversales sin romper tipología de ambiente.
- **Qué no representa**
  - Un ambiente con otro nombre.
  - Un rubro contable.
  - Un escenario constructivo.
- **Reglas de negocio**
  - Las zonas no duplican área automáticamente: debe definirse si particionan o solo etiquetan.
  - Una zona HVAC puede agrupar varios ambientes.
  - Las zonas de etapa ayudan certificaciones parciales.
  - No reemplazan la geometría de muros.
- **Casos especiales**
  - Local: zona pública vs zona empleados.
  - Vivienda: zona húmeda (baño+cocina+lavadero) para control de impermeabilización.
  - PH: circulación común vs unidad privada.
- **Relaciones con otras entidades**
  - Pertenece a Nivel típicamente; etiqueta Ambientes y a veces Sistemas.
  - Influye Timeline/Avance cuando se usa como frente de obra.
- **Ejemplos reales**
  - Zona de cocina abierta + barra en local gastronómico.
  - Zona de servicios en vivienda.
  - Zona de cocheras descubiertas vs cubiertas.
- **Errores frecuentes**
  - Crear zonas que parten un ambiente y luego sumar áreas dos veces.
  - Usar zona como reemplazo de tipificación de ambiente húmedo.
- **Impacto sobre presupuestos**
  - Medio: útil para presupuestos por etapa/sector.
- **Impacto sobre materiales**
  - Medio: agrupa especificaciones.
- **Impacto sobre costos**
  - Medio: facilita packs de precio por sector.
- **Impacto sobre cronograma**
  - Alto cuando se usa como frente de avance.
### 2.2 Elementos constructivos

Este grupo es el corazón del cómputo de obra gruesa y envolvente. Pensar como jefe de obra: cada elemento tiene identidad única y no se compra dos veces.

#### Muro

- **Qué es**
  - Elemento vertical de cerramiento o división, portante o no portante, con longitud, altura y espesor, que puede hospedar aberturas y recibir terminaciones.
- **Qué representa**
  - La pared que se levanta en obra: medianera, fachada, tabique interior, muro de carga.
  - La entidad que concentra m² de revoque/pintura, ml de longitud y tipología de sistema.
  - El anfitrión de puertas y ventanas.
- **Qué no representa**
  - Una línea de dibujo sin espesor de negocio.
  - Solo pintura (la pintura es terminación sobre el muro).
  - Un escenario completo.
  - Una columna (la columna es elemento estructural distinto aunque esté embebida).
- **Reglas de negocio**
  - Un muro tiene identidad única aunque limite dos ambientes; no se duplica por ambiente.
  - Debe declararse si es portante, tabique, medianero, exterior o interior.
  - Longitud × altura = área bruta de paramento; las aberturas descuentan según reglas de terminación.
  - El espesor condiciona sistema (ladrillo 18, retak 15, steel, etc.) y a veces aislación.
  - Altura por defecto = altura del nivel/ambiente salvo override explícito.
  - Muros compartidos entre unidades de PH requieren criterio de propiedad/cómputo explícito.
- **Casos especiales**
  - Tabique vs muro portante: ver clarificación específica más abajo en este catálogo.
  - Muro curva o en diagonal: se mide por desarrollo real, no por bounding box perezoso.
  - Muro existente a conservar en remodelación: cantidad de obra nueva = 0 en ese elemento; pueden existir ítems de refuerzo/reparación.
  - Doble muro con cámara de aire: modelar como sistema/parámetros, no como dos compras ciegas sin criterio.
- **Relaciones con otras entidades**
  - Pertenece a Nivel y/o delimita Ambientes.
  - Hospeda Abertura/Puerta/Ventana.
  - Se bindea a Sistema constructivo y Material según Escenario.
  - Alimenta Cómputo de albañilería, revoque, pintura, aislación.
- **Ejemplos reales**
  - Medianera de 12 m de fondo en vivienda de barrio.
  - Tabique de dormitorio en PH liviano.
  - Muro de local comercial con gran frente vidriado (el muro macizo restante + aberturas).
- **Errores frecuentes**
  - Contar el muro dos veces, una por cada ambiente que limita.
  - Olvidar descontar aberturas en revoque fino.
  - Tratar un tabique de drywall como muro de ladrillo portante en el mismo escenario sin pack.
  - Usar espesor de dibujo decorativo como espesor de compra.
- **Impacto sobre presupuestos**
  - Alto: suele ser el renglón dominante de obra gruesa en vivienda LATAM.
  - Define buena parte del presupuesto de envolvente.
- **Impacto sobre materiales**
  - Alto: ladrillos, bloques, perfiles, placas, morteros, mallas.
- **Impacto sobre costos**
  - Alto: mano de obra de albañilería/steel y unitarios por m² o ml.
- **Impacto sobre cronograma**
  - Alto: camino crítico de levantamiento antes de instalaciones y terminaciones.

#### Tabique vs muro portante (clarificación)

- **Qué es**
  - Distinción de negocio entre un cerramiento no estructural (tabique) y un muro que participa de la estabilidad (portante/estructural).
- **Qué representa**
  - Dos roles constructivos distintos bajo el concepto Muro.
  - Un criterio que cambia sistema, espesor, costo, secuencia y responsabilidad.
  - Una bandera de interpretación obligatoria en cómputos serios.
- **Qué no representa**
  - Dos entidades geométricas necesariamente distintas en el plano.
  - Una diferencia solo estética de terminación.
  - Una excusa para duplicar el elemento.
- **Reglas de negocio**
  - Todo muro debe poder clasificarse al menos como portante, tabique o indeterminado (con baja confianza).
  - Indeterminado no puede sellarse en presupuesto cliente sin revisión humana.
  - Cambiar de tabique a portante (o viceversa) es Cambio material: impacta escenario y a veces estructura.
  - En steel frame/retak la nomenclatura popular varía; el dominio usa el rol (carga vs división), no el marketing del fabricante.
- **Casos especiales**
  - Muro de fachada autoportante no estructural: tabique/envolvente según criterio del proyecto.
  - Muro de carga de ladrillo común de 30 cm en vivienda tradicional.
  - Tabique de 10 cm entre baño y pasillo.
- **Relaciones con otras entidades**
  - Especialización de Muro; condiciona Sistema constructivo, Fundación/Viga/Columna cuando hay carga.
  - Impacta Desperdicio y Mano de obra distintos.
- **Ejemplos reales**
  - Casa antigua a refaccionar: muro interior que parece tabique pero es portante.
  - PH nuevo en drywall: casi todos los interiores son tabique.
  - Local: muro de depósito que sostiene entrepiso — portante.
- **Errores frecuentes**
  - Presupuestar todos los muros como el mismo unitario.
  - Dejar la clasificación solo en el color del plano sin rol explícito.
- **Impacto sobre presupuestos**
  - Alto: cambia unitarios y alcance estructural.
- **Impacto sobre materiales**
  - Alto: cambia tipología de compra.
- **Impacto sobre costos**
  - Alto: portante suele ser más caro y más lento.
- **Impacto sobre cronograma**
  - Alto: altera secuencia y controles de obra.

#### Abertura

- **Qué es**
  - Vano en un muro u otro elemento hospedante destinado a puerta, ventana u otro paso; es el hueco con geometría (ancho, alto, peana) antes de especializarse.
- **Qué representa**
  - El agujero que descuenta muro y recibe carpintería.
  - La entidad padre conceptual de Puerta y Ventana.
  - Un modulador de iluminación, ventilación y costo de carpintería.
- **Qué no representa**
  - La hoja de la puerta o el vidrio por sí solos.
  - Un ambiente.
  - Un simple descuento abstracto sin hospedante.
- **Reglas de negocio**
  - Toda abertura tiene muro (u hospedante) y dimensiones.
  - El área de abertura descuenta del área de terminación del muro según reglas (revoque, pintura, revestimiento).
  - No se compra albañilería del hueco como muro macizo.
  - Peana/antepecho importa para ventanas y para preframes.
  - Aberturas en medianera tienen reglas legales/consorciales; el dominio exige tipificar.
- **Casos especiales**
  - Arco o vano irregular: medir por geometría real.
  - Paño vidriado continuo: puede ser una abertura grande o varias; criterio debe ser estable.
  - Tapada de vano existente: ítem de cierre, no solo «borrar abertura» sin rastro.
- **Relaciones con otras entidades**
  - Hospedada por Muro.
  - Se especializa en Puerta o Ventana.
  - Afecta Cómputo de muro, revoque, pintura, carpintería, a veces dintel.
- **Ejemplos reales**
  - Ventanal de living a patio 2,00 × 1,50.
  - Paso de 0,90 m a cocina.
  - Vano de balcón en PH con baranda.
- **Errores frecuentes**
  - Descontar la abertura del muro y además no cargar carpintería (o viceversa, cargar ambas mal).
  - Duplicar la misma abertura en dos muros por error de interpretación.
  - Olvidar dintel/premarco en sistemas que lo requieren.
- **Impacto sobre presupuestos**
  - Alto: mueve carpintería y descuentos de terminación.
- **Impacto sobre materiales**
  - Alto: marcos, hojas, vidrios, preframes, dinteles.
- **Impacto sobre costos**
  - Alto: unitarios de carpintería suelen ser sensibles.
- **Impacto sobre cronograma**
  - Medio-Alto: fabricación/lead time de aberturas afecta habilitación.

#### Puerta

- **Qué es**
  - Abertura de paso con hoja(s), marco y herrajes, tipificada por uso (interior, exterior, placa, madera, metálica, corta fuego).
- **Qué representa**
  - La carpintería de paso entre ambientes o al exterior.
  - Un ítem de cómputo en unidades (u) con tipología y medidas.
  - Un elemento de seguridad, privacidad y terminación.
- **Qué no representa**
  - Una ventana operable.
  - Solo la cerradura.
  - Un muro con nombre «puerta».
- **Reglas de negocio**
  - Se mide por unidad tipificada + ancho/alto; el vano asociado descuenta muro.
  - Puerta exterior ≠ interior en precio, herrajes y aislación.
  - Puertas de baño/cocina pueden exigir tipologías resistentes a humedad.
  - Sentido de apertura importa a obra y a veces a cómputo de espacio libre, no siempre a precio.
- **Casos especiales**
  - Puerta de entrada metálica de seguridad en vivienda.
  - Puerta vaivén de local comercial.
  - Puerta corrediza de placard: puede ser carpintería de mueble, no abertura de muro; tipificar bien.
- **Relaciones con otras entidades**
  - Es una Abertura hospedada en Muro.
  - Consume Material/herrajes; impacta Terminación del vano.
  - Aparece en Rubro carpintería/herrería según criterio.
- **Ejemplos reales**
  - Puerta placa 0,70 m en baño de PH.
  - Doble hoja 1,40 m en acceso de living.
  - Puerta de depósito de local con cerradura reforzada.
- **Errores frecuentes**
  - Presupuestar todas las puertas al mismo unitario.
  - Olvidar marcos y tapajuntas.
  - Contar puerta y vano como dos aberturas distintas.
- **Impacto sobre presupuestos**
  - Alto en rubro carpintería.
- **Impacto sobre materiales**
  - Alto: hojas, marcos, herrajes, selladores.
- **Impacto sobre costos**
  - Alto: gran variación de precio por tipología.
- **Impacto sobre cronograma**
  - Medio: instalación tras revoque/antes de pintura fina según oficio.

#### Ventana

- **Qué es**
  - Abertura de iluminación/ventilación con marco, hoja y vidrio (u otro cerramiento transparente/translúcido), tipificada por material y tipo de apertura.
- **Qué representa**
  - La carpintería de fachada o patio.
  - Un ítem usualmente en unidades con tipología (DVH, aluminio, PVC, madera).
  - Un factor de confort térmico/acústico vía especificación.
- **Qué no representa**
  - Un paño de muros vidriados estructurales sin tipificar (sigue siendo abertura/sistema).
  - Solo el vidrio suelto sin marco cuando el sistema es carpintería completa.
  - Una puerta-ventana sin tipificar (debe tipificarse: puerta-ventana).
- **Reglas de negocio**
  - Ancho, alto y peana son obligatorios para cómputo serio.
  - DVH vs simple cambia costo y a veces espesor de marco.
  - Descuenta terminaciones de muro como toda abertura.
  - Barandas y antepechos asociados no son la ventana; se vinculan.
- **Casos especiales**
  - Ventana en baño con vidrio opaco.
  - Paño fijo + hoja practicable combinados.
  - Remplazo de ventana en remodelación: demoliciones + nueva unidad.
- **Relaciones con otras entidades**
  - Es Abertura en Muro.
  - Relacionada con Aislación (térmica/acústica) y a veces con HVAC (cargas).
  - Rubro carpintería/vidrio.
- **Ejemplos reales**
  - Ventana corrediza de aluminio 1,20 × 1,10 en dormitorio.
  - Frente de local con paños fijos.
  - Ventiluz alto en cocina de PH.
- **Errores frecuentes**
  - Olvidar peana y mandar a fabricar mal.
  - Aplicar desperdicio de muro al vidrio.
  - No distinguir exterior e interior (cuando hay ventanas interiores raras, tipificar).
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto: perfiles, vidrios, burletes, herrajes.
- **Impacto sobre costos**
  - Alto y volátil según tipo de vidrio.
- **Impacto sobre cronograma**
  - Medio-Alto: lead time de fabricación.

#### Piso

- **Qué es**
  - Terminación horizontal de tránsito del ambiente (solado): cerámico, porcelanato, madera, microcemento, etc., aplicada sobre base preparada.
- **Qué representa**
  - El solado visible y usable.
  - La cantidad típica en m² por ambiente.
  - La capa de terminación, no la estructura.
- **Qué no representa**
  - La losa estructural.
  - El contrapiso o la carpeta (son bases).
  - La pintura de zócalo sola.
- **Reglas de negocio**
  - Se computa por área de ambiente según criterio (descontar núcleos? platos de ducha? — declarar).
  - Requiere base (carpeta/contrapiso) compatible.
  - Ambientes húmedos imponen tipologías antideslizantes/aptas.
  - Desperdicio de solado es crítico (cortes, despunte).
  - Zócalos son ítem relacionado, no el piso mismo.
- **Casos especiales**
  - Piso existente a conservar: cantidad nueva 0; posibles ítems de reparación/protección.
  - Cambio de solado en local: incluye demoliciones y nivelación.
  - Transiciones entre ambientes: burletes/perfiles.
- **Relaciones con otras entidades**
  - Pertenece a Ambiente/Nivel.
  - Depende de Carpeta/Contrapiso.
  - Usa Material (Cerámicos u otros) + Mano de obra.
  - En húmedos se relaciona con Impermeabilización.
- **Ejemplos reales**
  - Porcelanato 60×60 en living.
  - Cerámico 30×30 en baño.
  - Piso vinílico en depósito de local.
- **Errores frecuentes**
  - Usar área de muro como área de piso.
  - Olvidar desperdicio y quedarse corto en compra.
  - Presupuestar piso sin base.
- **Impacto sobre presupuestos**
  - Alto en terminaciones.
- **Impacto sobre materiales**
  - Alto: piezas, adhesivos, juntas, zócalos.
- **Impacto sobre costos**
  - Alto: mano de obra de colocación.
- **Impacto sobre cronograma**
  - Alto: habilita avance de obra fina y limpieza final.

#### Carpeta

- **Qué es**
  - Capa de nivelación/terminación de base (usualmente cementicia) sobre la que se coloca el solado; corrige planitud y pendientes suaves.
- **Qué representa**
  - La base fina de piso.
  - Cantidad en m² (y a veces espesor en cm).
  - Un ítem de preparación, no el solado.
- **Qué no representa**
  - El contrapiso grueso.
  - La losa.
  - El cerámico.
- **Reglas de negocio**
  - Se distingue de contrapiso: carpeta es más fina/niveladora; contrapiso aporta espesor/formación.
  - Espesor declarado; no asumir 0.
  - Pendientes en baños/balcones se tipifican.
  - Puede incluir malla o aditivos según especificación.
- **Casos especiales**
  - Carpeta autonivelante vs tradicional.
  - Reparación de carpeta existente.
  - Carpeta en terraza con pendiente a desagües.
- **Relaciones con otras entidades**
  - Sobre Contrapiso o Losa; bajo Piso.
  - Relacionada con Ambientes húmedos e Impermeabilización.
- **Ejemplos reales**
  - Carpeta 2–3 cm en dormitorios.
  - Carpeta con pendiente en lavadero.
  - Nivelación localizada en remodelación de local.
- **Errores frecuentes**
  - Fusionar carpeta y contrapiso en un solo renglón opaco.
  - Olvidar pendientes y generar embalse.
- **Impacto sobre presupuestos**
  - Medio-Alto.
- **Impacto sobre materiales**
  - Medio: cementos, arenas, aditivos, mallas.
- **Impacto sobre costos**
  - Medio: mano de obra especializada de nivelación.
- **Impacto sobre cronograma**
  - Alto en secuencia: bloquea colocación de piso.

#### Contrapiso

- **Qué es**
  - Capa gruesa de formación de solado que aporta espesor, relleno y a veces paso de instalaciones antes de la carpeta/piso.
- **Qué representa**
  - El cuerpo de formación sobre losa o terreno preparado.
  - Cantidad en m² y espesor; a veces m³.
  - Base de instalaciones embebidas horizontales cuando aplica.
- **Qué no representa**
  - La carpeta fina.
  - La platea/fundación.
  - El piso terminado.
- **Reglas de negocio**
  - Espesor y tipo (liviano, tradicional, con aislación) deben declararse.
  - En PB sobre terreno, no confundir con platea estructural.
  - Puede convivir con pasos de sanitarios/eléctricos.
  - Desperdicio/merma de mezcla es criterio de obra.
- **Casos especiales**
  - Contrapiso liviano en entrepisos.
  - Relleno de nivel en locales con desniveles.
  - Contrapiso radiante (si hay HVAC de piso): tipificar sistema.
- **Relaciones con otras entidades**
  - Sobre Losa/terreno; bajo Carpeta/Piso.
  - Coordina con Instalaciones (pasos).
  - Afecta cargas y a veces Aislación.
- **Ejemplos reales**
  - Contrapiso 8–10 cm en PB de vivienda.
  - Contrapiso en azotea no transitable (formación de pendiente).
  - Regularización en PH sobre losa existente.
- **Errores frecuentes**
  - Llamar contrapiso a la platea.
  - Omitir espesor y subestimar material.
  - Ejecutar piso sin contrapiso cuando el detalle lo exige.
- **Impacto sobre presupuestos**
  - Alto en obra gruesa de solados.
- **Impacto sobre materiales**
  - Alto: hormigón/mezclas, aislaciones, agregados.
- **Impacto sobre costos**
  - Alto: volumen y mano de obra.
- **Impacto sobre cronograma**
  - Alto: hito previo a terminaciones de piso.

#### Losa

- **Qué es**
  - Elemento estructural horizontal que conforma entrepiso o cubierta estructural, con espesor y rol estructural.
- **Qué representa**
  - La estructura que pisás (no el solado).
  - Cantidades en m² y espesor; a veces m³ de hormigón y kg de acero.
  - El soporte de contrapiso/carpeta/cubierta.
- **Qué no representa**
  - El piso cerámico.
  - Una viga (aunque la losa apoye en vigas).
  - Un cielorraso.
- **Reglas de negocio**
  - Rol estructural distinto de terminación.
  - En cómputo wedge puede estimarse por área/espesor; no reemplaza cálculo estructural firmado.
  - Losas existentes vs nuevas en remodelación se tipifican.
  - Aberturas verticales (escalera, patio) descuentan área de losa.
- **Casos especiales**
  - Losa maciza vs nervurada vs pretensada: tipología cambia materiales.
  - Losa de entrepiso liviano en steel: otro sistema.
  - Losa sanitaria con pendientes.
- **Relaciones con otras entidades**
  - Relacionada con Viga, Columna, Fundación, Nivel.
  - Soporta Contrapiso/Cubierta.
  - Escenario de Hormigón armado vs otros sistemas.
- **Ejemplos reales**
  - Losa de entrepiso 12 cm en vivienda PB+1.
  - Losa de PH con pasos de instalaciones.
  - Entrepiso de local para depósito alto.
- **Errores frecuentes**
  - Presupuestar losa como «piso».
  - Olvidar huecos de escalera.
  - Tratar estimación como cálculo estructural legal.
- **Impacto sobre presupuestos**
  - Alto cuando hay obra estructural.
  - Nulo/bajo en remodelaciones solo de terminación.
- **Impacto sobre materiales**
  - Alto: hormigón, acero, encofrados, o sistema alternativo.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: camino crítico de estructura.

#### Viga

- **Qué es**
  - Elemento estructural lineal que salva luces y traslada cargas a columnas/muros portantes.
- **Qué representa**
  - La viga de H°A°, metálica o del sistema adoptado.
  - Cantidad en ml y sección; a veces kg.
  - Parte del esqueleto portante.
- **Qué no representa**
  - Un dintel menor de vano (puede modelarse aparte o como viga corta; tipificar).
  - Una columna.
  - Una instalación.
- **Reglas de negocio**
  - No se inventan vigas desde un LLM sin evidencia de plano/estructura.
  - En wedge, pueden existir como elementos tipificados cuando el plano las declara.
  - Cambio de sistema (ladrillo portante → steel) redefine paquete de vigas.
- **Casos especiales**
  - Viga inversa / lintell de abertura grande.
  - Viga metálica vista en local.
  - Encadenado perimetral tipificado como viga/encadenado.
- **Relaciones con otras entidades**
  - Conecta Columnas; soporta Losa; relacionada con Muro portante.
  - Escenario estructural.
- **Ejemplos reales**
  - Viga central de living de 5 m.
  - Encadenados en vivienda de mampostería.
  - Viga de entrepiso de local.
- **Errores frecuentes**
  - Duplicar viga y losa nervurada sin criterio.
  - Olvidar encofrado/apuntalamiento en costo indirecto cuando corresponde.
- **Impacto sobre presupuestos**
  - Medio-Alto según tipología.
- **Impacto sobre materiales**
  - Alto en acero/hormigón/perfiles.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto en estructura.

#### Columna

- **Qué es**
  - Elemento estructural vertical que transmite cargas a la fundación.
- **Qué representa**
  - Pilar de H°A°, metálico o del sistema.
  - Cantidad en u o ml + sección.
  - Puntos duros del replanteo.
- **Qué no representa**
  - Un tabique.
  - Una bajada de instalación.
  - Un mueble columna.
- **Reglas de negocio**
  - Identidad única; no confundir con encuentros de muro.
  - En mampostería portante puede haber menos columnas explícitas; no forzar columnas fantasma.
  - Remates y capitales no son la columna completa.
- **Casos especiales**
  - Columna metálica en local con entrepiso.
  - Pilares de galería.
  - Columnas embebidas en muros.
- **Relaciones con otras entidades**
  - Apoya en Fundación; recibe Viga/Losa; puede estar en Nivel múltiple.
  - Escenario estructural.
- **Ejemplos reales**
  - Cuatro columnas de esquina en ampliación.
  - Retícula de depósito.
  - Pórtico de acceso.
- **Errores frecuentes**
  - Contar encuentros de ladrillo como columnas de H°A°.
  - Omitir columnas en cómputo porque «están en el muro».
- **Impacto sobre presupuestos**
  - Medio-Alto.
- **Impacto sobre materiales**
  - Alto: hormigón/acero/perfiles.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: habilita niveles superiores.

#### Fundación

- **Qué es**
  - Conjunto de elementos de apoyo al suelo (platea, zapatas, plateas corridas, pilotines según tipología) que transfieren cargas del edificio al terreno.
- **Qué representa**
  - La base de la obra sobre el terreno.
  - Ítems en m³, m² o ml según tipología.
  - Condición de arranque de muros/columnas.
- **Qué no representa**
  - El contrapiso de PB.
  - El movimiento de suelos completo de urbanización.
  - Un cálculo geotécnico firmado (ARQ-IA no lo reemplaza).
- **Reglas de negocio**
  - Tipología de fundación debe declararse; no asumir platea siempre.
  - Estimaciones de dominio no sustituyen estudio de suelos ni cálculo legal.
  - Remodelaciones pueden tener fundaciones existentes: tipificar alcance de refuerzo.
  - Desagües bajo platea se coordinan con sanitarios.
- **Casos especiales**
  - Platea de vivienda chica.
  - Zapatas corridas en ampliación.
  - Fundaciones de quincho liviano distintas a la casa.
- **Relaciones con otras entidades**
  - Relaciona Sitio, Edificio, Columna, Muro portante.
  - Coordina con Cloacas/desagües de PB.
- **Ejemplos reales**
  - Platea 12×8 m en casa de GBA.
  - Zapata de columna de esquina.
  - Sobre-fundación en terreno rellenado (señalar riesgo/confianza).
- **Errores frecuentes**
  - Llamar fundación al contrapiso.
  - Presupuestar fundación sin tipología.
  - Ignorar terreno y aplicar unitario genérico como certeza.
- **Impacto sobre presupuestos**
  - Alto en obra nueva.
  - Variable en remodelación.
- **Impacto sobre materiales**
  - Alto: hormigón, acero, rellenos, aislaciones bajo platea.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: hito cero de obra.

#### Cubierta

- **Qué es**
  - Sistema de cierre superior del edificio (techo): estructura de cubierta + aislación + impermeabilización + terminación (chapa, teja, losa transitabile, etc.).
- **Qué representa**
  - El techo como sistema, no solo la chapa vista.
  - Cantidades en m² de desarrollo (considerar pendiente).
  - Paquete de impermeabilización + aislación + terminación.
- **Qué no representa**
  - Solo la losa de último nivel sin sistema de techado.
  - Un cielorraso interior.
  - Una terraza sin tipificar (terraza es nivel + sistema de cubierta/piso).
- **Reglas de negocio**
  - Se mide por desarrollo real cuando hay pendiente; planta no alcanza si hay faldones.
  - Cubierta transitable ≠ no transitable.
  - Canaletas, cumbreras, babetas son parte del sistema o ítems vinculados.
  - PH y azoteas: impermeabilización es crítica.
- **Casos especiales**
  - Techo de chapa a dos aguas en vivienda.
  - Azotea transitable con piso sobre impermeabilización.
  - Cubierta de local con equipos de HVAC encima: sobrecargas y bases.
- **Relaciones con otras entidades**
  - Sobre último Nivel/Losa; incluye Impermeabilización y Aislación frecuentemente.
  - Relacionada con Desagües pluviales.
  - Escenarios de material de cubierta.
- **Ejemplos reales**
  - Chapa sinusoidal sobre cabriadas.
  - Teja colonial en refacción.
  - Membrana + piso en azotea de PH.
- **Errores frecuentes**
  - Medir solo en planta y comprar corto.
  - Olvidar zinguería.
  - Tratar membrana como pintura.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto: chapas, tejas, membranas, aislantes, fijaciones.
- **Impacto sobre costos**
  - Alto y sensible a tipología.
- **Impacto sobre cronograma**
  - Alto: cierre de obra gruesa al agua.
### 2.3 Instalaciones (MEP)

Las instalaciones son sistemas, no «líneas decorativas» del plano. En obra LATAM se presupuestan por tipología de servicio y por ambiente terminal, con coordinación con muros y solados.

#### Instalación sanitaria

- **Qué es**
  - Sistema (o conjunto de sistemas) de agua y desagües de la obra: alimentación, distribución y evacuación vinculadas a artefactos y locales húmedos.
- **Qué representa**
  - El paquete sanitario de negocio que agrupa agua fría, agua caliente y cloacas/desagües cuando se habla en rubro.
  - La red que conecta acometida, distribución y artefactos.
  - Un sistema con terminales en ambientes húmedos.
- **Qué no representa**
  - Solo el artefacto (inodoro) sin red.
  - Gas o electricidad.
  - Un cálculo hidráulico municipal firmado.
- **Reglas de negocio**
  - Se modela como sistema con elementos y terminales; no como texto libre único.
  - Ambientes húmedos disparan densidad sanitaria mínima tipológica.
  - Obra nueva vs refacción cambian demolición y reutilización de tramos.
  - La estimación de dominio no reemplaza proyecto sanitario ejecutable cuando la obra lo exige.
- **Casos especiales**
  - Local gastronómico: densidad y grasas (cámaras) especiales.
  - PH: bajadas comunes vs instalaciones de unidad.
  - Vivienda con tanque/cisterna y bomba.
- **Relaciones con otras entidades**
  - Agrupa Agua fría, Agua caliente, Cloacas.
  - Atraviesa Muros/Losas/Contrapiso.
  - Alimenta Rubro sanitarios y Órdenes de compra de caños/artefactos.
- **Ejemplos reales**
  - Casa 3 dormitorios con 2 baños y cocina.
  - Local con 1 toilette público + cocina.
  - PH con baño en suite + toilette social.
- **Errores frecuentes**
  - Presupuestar «sanitarios globales» sin tipificar baños.
  - Olvidar ventilaciones y accesos de limpieza.
  - Mezclar pluvial con cloacal sin distinguir.
- **Impacto sobre presupuestos**
  - Alto en rubro instalaciones.
- **Impacto sobre materiales**
  - Alto: caños, fittings, artefactos, válvulas.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: requiere coordinación antes de cerrar muros/solados.

#### Agua fría

- **Qué es**
  - Subistema de alimentación y distribución de agua fría potable (o de servicio) hasta los puntos de consumo.
- **Qué representa**
  - La red de agua fría: acometida, montantes, ramales, llaves de paso, puntos.
  - Cantidades en ml de cañería + u de accesorios/puntos.
  - Un servicio crítico de habilitación.
- **Qué no representa**
  - Agua caliente.
  - Cloacas.
  - El tanque como único ítem sin red.
- **Reglas de negocio**
  - Cada punto de consumo tipificado (cocina, lavatorio, ducha, lavarropas, exterior).
  - Material de cañería (termofusión, etc.) es especificación de escenario/material, no geometría de muro.
  - Presiones/tanque/bomba se tipifican cuando el expediente lo requiere.
  - No inventar puntos sin ambiente o sin criterio tipológico.
- **Casos especiales**
  - Riego de jardín como ramal separado.
  - Local con hidrante de cocina.
  - Refacción: reutilizar montante y cambiar solo ramales.
- **Relaciones con otras entidades**
  - Parte de Instalación sanitaria.
  - Terminales en Ambientes; cruza Niveles.
  - Compra vía Proveedor de materiales sanitarios.
- **Ejemplos reales**
  - Montante a tanque en azotea de PH.
  - Punto de lavarropas en lavadero.
  - Canilla de patio en vivienda.
- **Errores frecuentes**
  - Contar artefactos y olvidar ml de distribución.
  - Usar longitudes de sueño del chat sin plano.
- **Impacto sobre presupuestos**
  - Alto dentro de sanitarios.
- **Impacto sobre materiales**
  - Alto: caños y fittings.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Medio-Alto: pruebas de presión antes de cerrar.

#### Agua caliente

- **Qué es**
  - Subistema de generación y distribución de agua caliente sanitaria hasta los puntos que la requieren.
- **Qué representa**
  - Termotanque/caldera/calefón + red de ACS.
  - Puntos de ducha, lavatorio, cocina, etc.
  - Decisión de sistema (central, por punto, gas/eléctrico).
- **Qué no representa**
  - Calefacción por radiadores (puede compartir generación, pero es otro servicio si es HVAC térmico).
  - Agua fría.
  - Solo el artefacto sin ramal.
- **Reglas de negocio**
  - Declarar tipo de generación: cambia gas/electricidad y espacio técnico.
  - Recirculación en obras mayores se tipifica; en vivienda chica suele no asumir se.
  - Aislación de cañería de ACS es material vinculado.
  - En escenarios, cambiar gas↔eléctrico es Cambio material.
- **Casos especiales**
  - Calefón de paso a gas en vivienda.
  - Termotanque eléctrico en PH sin gas.
  - Sistema central en edificio (fuera del wedge chico, pero conceptualmente sistema).
- **Relaciones con otras entidades**
  - Depende de Gas y/o Electricidad.
  - Parte de Instalación sanitaria.
  - Impacta Ambiente de lavadero/cocina/baño.
- **Ejemplos reales**
  - ACS a cocina y 2 baños.
  - Solo cocina en local (sin duchas).
  - Ducha exterior de quincho como adicional.
- **Errores frecuentes**
  - Presupuestar termotanque y olvidar cañería.
  - Asumir gas cuando el edificio es solo eléctrico.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto: generador + caños + aislación.
- **Impacto sobre costos**
  - Alto y sensible a tipo de energía.
- **Impacto sobre cronograma**
  - Medio-Alto: habilitación y pruebas.

#### Cloacas

- **Qué es**
  - Subistema de desagües cloacales/servidos (y su distinción de pluviales) desde artefactos hasta salida/conexión.
- **Qué representa**
  - La red de evacuación: ramales, bajadas, ventilaciones, cámara/inspección cuando aplica.
  - Cantidades en ml + u de piezas especiales.
  - Condición de salubridad del edificio.
- **Qué no representa**
  - Desagüe pluvial de cubierta (se tipifica aparte aunque se coordine).
  - Agua fría.
  - El pozo/absorción como detalle oculto sin tipificar cuando es el sistema.
- **Reglas de negocio**
  - Separar cloacal de pluvial en el lenguaje de negocio.
  - Pendientes y diámetros son de proyecto; el cómputo estima tramos tipológicos con confianza.
  - Artefactos sin desagüe tipificado = cómputo incompleto.
  - En PH, bajadas comunes vs privadas deben declararse en alcance.
- **Casos especiales**
  - Cámara de inspección en PB.
  - Bomba de achique en sótano.
  - Local gastronómico: grasas/pretratamiento.
- **Relaciones con otras entidades**
  - Parte de Instalación sanitaria.
  - Coordina con Contrapiso/Fundación/Cubierta (pluvial).
  - Ambientes húmedos.
- **Ejemplos reales**
  - Bajada de inodoro + lavatorio + ducha en baño.
  - Desagüe de cocina con sifón/acceso.
  - Conexión a red cloacal municipal vs sistema autónomo tipificado.
- **Errores frecuentes**
  - Mezclar pluvial y cloacal en un solo ml mágico.
  - Olvidar ventilación cloacal.
  - Asumir que «baño» incluye automáticamente cámara exterior.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto: caños, codos, cámaras, selladores.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: debe ejecutarse antes de cerrar contrapiso en muchos tramos.

#### Gas

- **Qué es**
  - Sistema de suministro de gas (típicamente natural o envasado) para cocina, agua caliente y/o calefacción, con artefactos y seguridad asociados.
- **Qué representa**
  - La red de gas y sus puntos.
  - Decisión de servicio energizado del edificio.
  - Ítems en ml + u de válvulas/artefactos.
- **Qué no representa**
  - Electricidad.
  - Solo la cocina sin acometida/regulación.
  - Habilitación del distribuidor (ARQ-IA no es el ente habilitador).
- **Reglas de negocio**
  - Si el escenario es «sin gas», no se inventan puntos.
  - Artefactos a gas exigen tipificación y ventilaciones según oficio/norma; el dominio marca necesidad, no certifica.
  - Cambio a eléctrico elimina o reduce este sistema y crea adicionales eléctricos.
  - Garrafas/envasado vs red: tipología distinta.
- **Casos especiales**
  - Cocina + calefón a gas en casa.
  - Solo anafe en local, resto eléctrico.
  - PH sin gas: escenario eléctrico completo.
- **Relaciones con otras entidades**
  - Relacionado con Agua caliente y a veces HVAC térmico.
  - Atraviesa Muros; requiere pasadas.
  - Proveedor/instalador matriculado en la realidad operativa.
- **Ejemplos reales**
  - Punto de cocina 1/2" tipificado.
  - Calefacción por tiro balanceado (si está en alcance).
  - Eliminación de gas en refacción: tapadas + adicionales eléctricos.
- **Errores frecuentes**
  - Dejar gas dibujado cuando el cliente eligió inducción.
  - Presupuestar artefactos sin ml de red.
- **Impacto sobre presupuestos**
  - Alto cuando el escenario lo incluye; nulo si escenario sin gas.
- **Impacto sobre materiales**
  - Alto: caños, válvulas, flexibles, artefactos.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Medio-Alto: inspecciones y habilitación externa.

#### Electricidad

- **Qué es**
  - Sistema de suministro y distribución eléctrica: acometida/tablero, circuitos, puntos de luz/tomacorrientes y especiales.
- **Qué representa**
  - La red eléctrica de la obra.
  - Cantidades en u de puntos + ml de cableado tipológico + tableros.
  - Servicio crítico de habilitación y seguridad.
- **Qué no representa**
  - Automatización completa BMS.
  - Solo la lámpara del cliente.
  - El cálculo de potencia firmado del electricista matriculado (ARQ-IA estima/organiza, no lo reemplaza).
- **Reglas de negocio**
  - Todo ambiente tiene densidad tipológica mínima de puntos salvo override.
  - Circuitos especiales (aire, cocina eléctrica, lavarropas, termotanque) se tipifican.
  - Tablero principal y seccionales aparecen como elementos/sistema.
  - Escenario sin gas aumenta carga eléctrica típica.
- **Casos especiales**
  - Local: vidriera, cartelería, fuerza motriz chica.
  - Vivienda con tomas USB/datos: datos puede ser sistema aparte.
  - PH: medidores y columnas montantes comunes vs unidad.
- **Relaciones con otras entidades**
  - Sistema propio; interactúa con HVAC, Agua caliente eléctrica, Iluminación como terminación.
  - Pasa por Muros/Losas/Cielorrasos.
  - Rubro electricidad.
- **Ejemplos reales**
  - Tablero + 40 puntos en casa de 100 m² (orden de magnitud tipológico, no dogma).
  - Toma para split en living.
  - Fuerza para cámara fría en local (adicional).
- **Errores frecuentes**
  - Presupuestar «electricidad global» sin puntos.
  - Olvidar especiales de aires.
  - Inventar cantidad de cables sin tipología.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto: cables, caños, cajas, termomagnéticas, artefactos.
- **Impacto sobre costos**
  - Alto y sensible a tipología de calidad.
- **Impacto sobre cronograma**
  - Alto: embutidos antes de revoque fino; pruebas al final.

#### HVAC

- **Qué es**
  - Sistema de climatización y/o ventilación mecánica (calor/frío/ventilación) que no se reduce a «poner un aire».
- **Qué representa**
  - Equipos + distribución (split, multi, conductos, ventilación).
  - Cargas asociadas a ambientes y orientaciones cuando se estiman.
  - Un escenario frecuente de adicional en LATAM.
- **Qué no representa**
  - Una ventana (ventilación natural).
  - Calefacción a gas sin tipificar como sistema.
  - Confort subjetivo del cliente.
- **Reglas de negocio**
  - Cada equipo tipificado exige punto eléctrico y desagüe de condensado cuando aplica.
  - No inventar toneladas de refrigeración sin criterio; si no hay dato, confianza baja.
  - Cubiertas y balcones reciben bases de equipos: ítems vinculados.
  - Ventilación de baños sin ventana es regla de ambiente húmedo.
- **Casos especiales**
  - Un split por dormitorio + living.
  - Cortina de aire en acceso de local.
  - Extracción de cocina gastronómica (sistema pesado).
- **Relaciones con otras entidades**
  - Depende de Electricidad; a veces de Agua/desagües.
  - Se ancla a Ambientes/Zonas.
  - Impacta Cubierta/fachada por unidades exteriores.
- **Ejemplos reales**
  - Split 3000W en dormitorio.
  - Multi-split en PH chico.
  - Solo ventilación mecánica en baño interior.
- **Errores frecuentes**
  - Cargar equipos y olvidar instalación eléctrica/desagüe.
  - Usar el chat para inventar carga térmica como certeza.
- **Impacto sobre presupuestos**
  - Alto cuando está en alcance; a menudo Extra.
  - Medio en vivienda básica sin climatización.
- **Impacto sobre materiales**
  - Alto: equipos, caños, isolación, soportes.
- **Impacto sobre costos**
  - Alto y volátil.
- **Impacto sobre cronograma**
  - Medio-Alto: suele instalarse en obra fina / pre-entrega.

### 2.4 Materiales y sistemas constructivos

Material y sistema no son lo mismo: el sistema es la lógica de construcción; el material es lo que se compra y se coloca dentro de esa lógica. Los escenarios canónicos LATAM pivotan aquí.

#### Material

- **Qué es**
  - Especificación comprable y colocable (producto o familia) que se bindea a elementos o líneas de cómputo para transformar cantidad neta en compra y costo.
- **Qué representa**
  - Ladrillo, cemento, perfil, placa, cerámico, cable, caño, pintura tipificada.
  - La unidad de compra (u, m², kg, bolsa, ml).
  - El ancla de desperdicio y de oferta de proveedor.
- **Qué no representa**
  - El elemento geométrico (el muro no es el ladrillo).
  - El precio solo (el precio es unitario/oferta).
  - Una marca obligatoria si el dominio admite equivalente.
- **Reglas de negocio**
  - Todo binding material vive en un escenario/versión head.
  - Cambiar material sin cambiar geometría es overlay de escenario legítimo.
  - Material sin unidad clara no es presupuestable.
  - Equivalencias (marca A↔B) no cambian cantidad neta; pueden cambiar desperdicio/costo.
- **Casos especiales**
  - Material «a definir» con confianza baja: no sellar al cliente.
  - Material existente reutilizado: cantidad comprable 0, posible ítem de manipulación.
  - Material importado con lead time: impacta cronograma más que geometría.
- **Relaciones con otras entidades**
  - Se bindea a Elementos y a Líneas de Cómputo.
  - Tiene Desperdicio tipológico.
  - Se precios vía Unitario/Proveedor.
  - Pertenece a Sistema constructivo cuando aplica.
- **Ejemplos reales**
  - Ladrillo hueco 18×18×33.
  - Porcelanato 60×60 rectificado.
  - Perfil steel frame 89 mm.
- **Errores frecuentes**
  - Poner precio sin material tipificado.
  - Cambiar material en versión sellada sin adicional.
  - Usar el nombre comercial como única especificación sin unidad.
- **Impacto sobre presupuestos**
  - Alto: redefine renglones del presupuesto.
- **Impacto sobre materiales**
  - Alto: es el objeto mismo.
- **Impacto sobre costos**
  - Alto: determina unitarios.
- **Impacto sobre cronograma**
  - Medio-Alto: lead times y cuadrillas según material.

#### Sistema constructivo

- **Qué es**
  - Lógica organizada de construir un conjunto de elementos (envolvente, estructura, tabiquería) con reglas, espesores típicos, secuencia y paquetes de materiales compatibles.
- **Qué representa**
  - Mampostería de ladrillo, steel frame, retak/bloques, hormigón armado, drywall, etc.
  - El «cómo se construye» comparable entre escenarios.
  - Un pack que redefine bindings y a veces parámetros (espesor, aislación).
- **Qué no representa**
  - Un solo material suelto.
  - Un estilo arquitectónico.
  - Un plan SaaS.
- **Reglas de negocio**
  - Un edificio puede combinar sistemas (estructura HA + tabiques drywall); debe declararse por elemento/rol.
  - Cambiar sistema de muros portantes es Cambio mayor; no es un repaint.
  - Cada sistema trae supuestos de mano de obra y desperdicio distintos.
  - Comparar sistemas exige geometría base comparable.
- **Casos especiales**
  - Híbridos: fachada ladrillo visto + interiores drywall.
  - Sistema de cubierta independiente del sistema de muros.
  - Upgrade de aislación dentro del mismo sistema.
- **Relaciones con otras entidades**
  - Gobierna Materiales bindeados a Muros/Losas/etc.
  - Define Escenarios canónicos.
  - Condiciona Cronograma y Rubros.
- **Ejemplos reales**
  - Vivienda de ladrillo común con losa HA.
  - Ampliación steel frame sobre existente.
  - PH retak con losa tradicional.
- **Errores frecuentes**
  - Mezclar consumos de ladrillo con unitarios de steel en el mismo renglón.
  - Declarar sistema en el brochure y otro en el cómputo.
- **Impacto sobre presupuestos**
  - Alto: cambia estructura del presupuesto comparable.
- **Impacto sobre materiales**
  - Alto: cambia casi todo el paquete comprable de envolvente/estructura.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: redefine cuadrillas y plazos.

#### Ladrillo

- **Qué es**
  - Sistema/material de mampostería tradicional (ladrillo común, hueco, bloque cerámico) usado como escenario canónico A de envolvente/muros en LATAM.
- **Qué representa**
  - El modo más legible para jefes de obra y clientes en Argentina.
  - Consumos por m² de muro según espesor y tipo.
  - Morteros, hierros de encadenado y revoques asociados.
- **Qué no representa**
  - Steel frame.
  - Solo el revoque.
  - Un ladrillo decorativo suelto sin muro.
- **Reglas de negocio**
  - Declarar tipo (común, hueco, bloque) y espesor.
  - Muros portantes vs tabiques de ladrillo tienen consumos distintos.
  - Aberturas descuentan m² de mampostería.
  - Desperdicio de ladrillo es tipológico y revisable.
- **Casos especiales**
  - Ladrillo visto vs revocado.
  - Doble muro con cámara.
  - Recupero de ladrillo en demolición (crédito/manejo).
- **Relaciones con otras entidades**
  - Es Material y a la vez bandera de Sistema constructivo.
  - Escenario A canónico.
  - Alimenta Revoque/Pintura/Encadenados.
- **Ejemplos reales**
  - Muro de 18 cm hueco en interiores.
  - Muro de 30 cm en fachada portante.
  - Medianera de ladrillo común.
- **Errores frecuentes**
  - Aplicar consumo de ladrillo a un muro tipificado steel.
  - Olvidar mortero y hierros.
  - Contar m² de ambos lados como doble mampostería.
- **Impacto sobre presupuestos**
  - Alto en escenario A.
- **Impacto sobre materiales**
  - Alto: ladrillos + mortero + hierros.
- **Impacto sobre costos**
  - Alto; referencia cultural de precio.
- **Impacto sobre cronograma**
  - Alto: ritmo de cuadrilla de albañilería.

#### Steel Frame

- **Qué es**
  - Sistema constructivo de estructura liviana de perfiles de acero galvanizado con placas y aislaciones, escenario canónico B de comparación frente a mampostería.
- **Qué representa**
  - Envolvente/tabiquería liviana industrializada.
  - Perfiles, placas, aislación, barreras, fijaciones.
  - Otra secuencia de obra (más seca, otra cuadrilla).
- **Qué no representa**
  - Una ventana de aluminio.
  - Hormigón armado.
  - Solo «chapa» de cubierta.
- **Reglas de negocio**
  - Geometría de muros puede compartirse con escenario ladrillo; cambian espesores efectivos, capas y consumos.
  - No se cuantifica en «ladrillos equivalentes».
  - Aislación y barreras son parte del sistema, no opcionales silenciosas.
  - Anclajes a platea/fundación tipificados.
- **Casos especiales**
  - Steel en ampliación sobre losa existente.
  - Híbrido: steel interior + fachada tradicional.
  - Requerimientos acústicos entre unidades de PH.
- **Relaciones con otras entidades**
  - Sistema constructivo del Escenario B.
  - Materiales: perfiles, OSB/placas, lanas, membranas.
  - Impacta Electricidad/sanitarios por cavidades.
- **Ejemplos reales**
  - Casa steel completa en periurbano.
  - Entreplantas livianas de local.
  - Tabiques steel en remodelación rápida.
- **Errores frecuentes**
  - Convertir m² de ladrillo a steel multiplicando por un factor mágico sin pack.
  - Olvidar aislación y vender solo perfiles.
  - Asumir misma duración de obra que mampostería.
- **Impacto sobre presupuestos**
  - Alto en escenario B.
- **Impacto sobre materiales**
  - Alto: paquete industrializado.
- **Impacto sobre costos**
  - Alto; comparar contra A/C es el valor.
- **Impacto sobre cronograma**
  - Alto: distinta ruta crítica.

#### Retak

- **Qué es**
  - Sistema/material de bloques de hormigón celular/curado (marca-categoría de uso común en Argentina) como escenario canónico C de muros, con lógica de mampostería liviana y juntas específicas.
- **Qué representa**
  - Alternativa de muros frente a ladrillo y steel.
  - Bloques + adhesivo/mortero específico + terminaciones compatibles.
  - Percepción de velocidad y aislación distinta.
- **Qué no representa**
  - Ladrillo hueco tradicional.
  - Un revoque proyectado solo.
  - Cualquier bloque de hormigón pesado sin tipificar.
- **Reglas de negocio**
  - Tipificar espesor de bloque y junta.
  - No usar consumos de ladrillo común.
  - Compatibilidad de fijaciones de aberturas y de instalaciones embutidas debe considerarse.
  - Terminaciones (revoque fino, placas) según detalle.
- **Casos especiales**
  - Retak en muros interiores + ladrillo en medianera (híbrido declarado).
  - Retak con revestimiento exterior específico.
  - Recortes por instalaciones: desperdicio propio.
- **Relaciones con otras entidades**
  - Escenario C canónico.
  - Material bloque + Sistema de mampostería liviana.
  - Relaciona Aberturas/Instalaciones por rozas.
- **Ejemplos reales**
  - Vivienda retak en Cordón urbano.
  - Tabiques retak en ampliación.
  - Comparativa comercial A/B/C para cliente.
- **Errores frecuentes**
  - Presupuestar retak con unitario de ladrillo «porque es pared».
  - Olvidar esquineros/mallas de terminación.
  - Ignorar diferencias de anclaje de puertas.
- **Impacto sobre presupuestos**
  - Alto en escenario C.
- **Impacto sobre materiales**
  - Alto: bloques + adhesivos + refuerzos.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: ritmo distinto de cuadrilla.

#### Hormigón

- **Qué es**
  - Material/sistema de hormigón (simple o armado) presente en fundaciones, losas, vigas, columnas y a veces muros; núcleo del escenario estructural tradicional.
- **Qué representa**
  - H° y H°A° como paquete de negocio: hormigón + acero + encofrado + mano de obra.
  - Cantidades en m³ y kg.
  - Base de muchos edificios LATAM.
- **Qué no representa**
  - El contrapiso no estructural tipificado aparte (aunque use material cementicio).
  - El cálculo estructural firmado.
  - Solo el cemento en bolsa sin tipificar uso.
- **Reglas de negocio**
  - Separar hormigón estructural de carpetas/contrapisos en el lenguaje comercial cuando el oficio lo separa.
  - Acero de refuerzo es parte del paquete HA, no un extra sorpresa.
  - Encofrado y apuntalamiento impactan costo/cronograma aunque a veces se metan en unitario.
- **Casos especiales**
  - Hormigón elaborado vs hecho en obra.
  - Losas postensadas (tipología especial).
  - Reparaciones estructurales: no son «un balde más».
- **Relaciones con otras entidades**
  - Fundación, Losa, Viga, Columna.
  - Escenario estructural.
  - Proveedores de elaborado / acero.
- **Ejemplos reales**
  - Platea + columnas + losa de vivienda PB+1.
  - Dintel HA sobre ventanal.
  - Ampliación de local con nuevas bases.
- **Errores frecuentes**
  - Meter todo el cementicio en un solo m³ opaco.
  - Olvidar acero.
  - Tratar estimación como certificación de cálculo.
- **Impacto sobre presupuestos**
  - Alto en obra nueva estructural.
- **Impacto sobre materiales**
  - Alto: m³, kg, encofrados, desmoldantes.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: hitos de fraguado y desencofrado.

#### Revoque

- **Qué es**
  - Terminación cementicia (o proyectada) de paramentos: grueso/fino/exterior/interior, que prepara o constituye la superficie del muro.
- **Qué representa**
  - m² de paramento a revestir con revoque.
  - Capas (azotado, grueso, fino, impermeable) según detalle.
  - Base típica antes de pintura o revestimiento.
- **Qué no representa**
  - Pintura.
  - El ladrillo mismo.
  - Un revestimiento placa completo (otro sistema).
- **Reglas de negocio**
  - Se computa sobre área de muro descontando aberturas según regla.
  - Exterior ≠ interior.
  - Ambientes húmedos pueden exigir revoques impermeables o bases especiales.
  - En steel/retak el «revoque» puede reemplazarse por placas; no forzar revoque fantasma.
- **Casos especiales**
  - Revoque proyectado.
  - Salpicrete/revestimiento plástico exterior.
  - Reparches en refacción.
- **Relaciones con otras entidades**
  - Sobre Muro; bajo Pintura/Cerámicos de pared.
  - Relacionado con Impermeabilización en bases.
- **Ejemplos reales**
  - Revoque fino interior en todos los ambientes secos.
  - Azotado hidrófugo en baños.
  - Fachada con revoque exterior texturable.
- **Errores frecuentes**
  - No descontar ventanas.
  - Aplicar revoque a ambos lados y además contar un muro doble de material base mal.
  - Presupuestar revoque en muro drywall sin detalle.
- **Impacto sobre presupuestos**
  - Alto en obra tradicional.
- **Impacto sobre materiales**
  - Alto: cementos, arenas, hidrófugos, mallas.
- **Impacto sobre costos**
  - Alto: mano de obra intensiva.
- **Impacto sobre cronograma**
  - Alto: precede a pintura y a muchas terminaciones.

#### Pintura

- **Qué es**
  - Terminación superficial de paramentos y cielorrasos por sistema de pintura (látex, epoxi, etc.), computada en m² con manos y preparación.
- **Qué representa**
  - m² pintables × sistema (manos, imprimación).
  - Ítem de terminación visible al cliente.
  - Criterio estético y de mantenimiento.
- **Qué no representa**
  - El color del plano de percepción (el color de cómputo no es la pintura de obra).
  - Revoque.
  - Papel mural u otros revestimientos sin tipificar.
- **Reglas de negocio**
  - Descontar aberturas; definir si cielorraso se pinta con área de piso u otra regla.
  - Ambientes húmedos: sistemas lavables/aptos.
  - Manos y rendimiento son parte del unitario/desperdicio de pintura.
  - Muros nuevos vs repintes de existentes.
- **Casos especiales**
  - Pintura epoxi en depósito de local.
  - Cielorrasos distintos de muros.
  - Cambio de color post-sello = adicional si ya estaba definido.
- **Relaciones con otras entidades**
  - Sobre Revoque/placas; en Ambiente.
  - Material pintura + Mano de obra.
  - Rubro pintura/terminaciones.
- **Ejemplos reales**
  - Látex interior 2 manos en vivienda.
  - Esmalte en puertas (a veces carpintería).
  - Fachada con impermeabilizante coloreado.
- **Errores frecuentes**
  - Usar m² de piso como m² de muros.
  - Olvidar cielorrasos.
  - No descontar aberturas.
- **Impacto sobre presupuestos**
  - Alto en terminaciones.
- **Impacto sobre materiales**
  - Medio-Alto: litros/baldes + cintas + lijas.
- **Impacto sobre costos**
  - Medio-Alto.
- **Impacto sobre cronograma**
  - Alto al final de obra fina; sensible a limpieza y entrega.

#### Cerámicos

- **Qué es**
  - Familia de revestimientos rígidos de piezas (cerámico, porcelanato, azulejo) para pisos y paredes, con juntas y piezas especiales.
- **Qué representa**
  - m² de revestimiento + u de especiales (sanitarios, cenefas, listelos) cuando aplican.
  - Estrella de terminación en húmedos y muchos locales.
  - Desperdicio alto por cortes.
- **Qué no representa**
  - Microcemento continuo (otro material).
  - Pintura.
  - La carpeta.
- **Reglas de negocio**
  - Separar piso y pared.
  - Formato de pieza cambia desperdicio.
  - Ambientes húmedos: altura de revestimiento tipificada (no asumir 1,80 m siempre sin criterio).
  - Impermeabilización bajo cerámico en duchas/balcones según detalle.
- **Casos especiales**
  - Porcelanato rectificado con junta mínima.
  - Cerámico económico 30×30 en toilette de servicio.
  - Simil-madera en local retail.
- **Relaciones con otras entidades**
  - Material sobre Piso/Muro; en Ambientes húmedos casi mandatorio.
  - Depende de Carpeta; relaciona Impermeabilización.
- **Ejemplos reales**
  - Baño revestido total.
  - Cocina con solado cerámico y pared bajo aéreos.
  - Acceso de local con porcelanato alto tránsito.
- **Errores frecuentes**
  - Aplicar desperdicio de pintura a cerámicos.
  - Olvidar piezas especiales de rincones/maquinas.
  - Medir pared húmeda con altura de nivel completo sin criterio.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto: piezas, adhesivo, pastina, crucetas, perfiles.
- **Impacto sobre costos**
  - Alto y muy sensible a elección de cliente.
- **Impacto sobre cronograma**
  - Alto: frente típico de obra fina.
### 2.5 Cantidades, dinero y compras

Aquí se separa con cirugía lo que es cantidad, lo que es precio, lo que es documento comercial y lo que es pago/certificación de avance.

#### Cantidad

- **Qué es**
  - Magnitud medida o tipificada de un hecho o línea (m, m², m³, ml, kg, u) antes de multiplicar por precio; puede ser neta o comprable.
- **Qué representa**
  - El número que responde «cuánto hay / cuánto se necesita».
  - La base del cómputo métrico.
  - El insumo del presupuesto y de la OC.
- **Qué no representa**
  - El precio.
  - La confianza sola.
  - Un porcentaje de avance.
- **Reglas de negocio**
  - Toda cantidad material tiene unidad explícita.
  - Cantidad neta ≠ cantidad con desperdicio.
  - Cantidades de versión sellada no se editan in-place.
  - Una cantidad sin provenance/confianza es borrador.
  - La IA no inventa cantidades; solo puede proponer revisiones ancladas.
- **Casos especiales**
  - Cantidad cero de elemento existente conservado.
  - Cantidad negativa no es un adicional; los retiros se modelan como cambio/alcance.
  - Redondeo de compra (bolsas enteras) ocurre al pasar a comprable/OC, no al medir geometría.
- **Relaciones con otras entidades**
  - Sale de Elementos vía Cómputo/Takeoff.
  - Entra a Presupuesto × Unitario.
  - Se ajusta por Desperdicio y Avance.
- **Ejemplos reales**
  - 45,2 m² de muro interior neto.
  - 12 u de puertas placa.
  - 3,4 m³ de hormigón de platea.
- **Errores frecuentes**
  - Mezclar unidades en una suma.
  - Presentar cantidad comprable como si fuera medición pura.
  - Cambiar cantidad sellada sin adicional.
- **Impacto sobre presupuestos**
  - Alto: es el esqueleto numérico del presupuesto.
- **Impacto sobre materiales**
  - Alto: determina compras.
- **Impacto sobre costos**
  - Alto: base del dinero.
- **Impacto sobre cronograma**
  - Medio: cantidades grandes tipifican duración.

#### Cómputo

- **Qué es**
  - Proyección ordenada de cantidades a partir del modelo de obra (takeoff) agrupable por rubro, ambiente, sistema o elemento; puente entre hechos y dinero.
- **Qué representa**
  - El cómputo métrico de la obra en un head de versión/escenario.
  - Líneas cuantificadas trazables a elementos/hechos.
  - La base auditable del presupuesto.
- **Qué no representa**
  - El plano pintado.
  - El presupuesto con precios.
  - La certificación de avance.
  - Un Excel sin ancla a hechos (eso es sombra, no cómputo de dominio).
- **Reglas de negocio**
  - Toda línea relevante cita origen (elemento, regla, ajuste manual).
  - Regenerable cuando cambian hechos; no es segunda fuente de verdad geométrica.
  - Debe respetar no doble conteo.
  - Ajustes manuales quedan marcados como override con autor.
  - Cómputo cliente-facing exige umbral de confianza.
- **Casos especiales**
  - Cómputo de demolición + obra nueva en refacción.
  - Cómputo comparativo A/B/C por escenario.
  - Cómputo parcial por etapa/zona para certificación.
- **Relaciones con otras entidades**
  - Sinónimo de negocio de Takeoff/Cómputo métrico.
  - Alimenta Presupuesto, OC, Certificación.
  - Depende de Versión/Escenario y Escala.
- **Ejemplos reales**
  - Cómputo de albañilería + sanitarios de casa 90 m².
  - Cómputo solo de terminaciones de local.
  - Cómputo de adicionales post-baseline.
- **Errores frecuentes**
  - Usar el cómputo como si fuera geometría editable directa.
  - Duplicar líneas a mano «por las dudas».
  - Perder trazabilidad al pegar en Excel y volver sin marca.
- **Impacto sobre presupuestos**
  - Alto: sin cómputo no hay presupuesto serio.
- **Impacto sobre materiales**
  - Alto: lista de compras nace aquí.
- **Impacto sobre costos**
  - Alto: multiplica unitarios.
- **Impacto sobre cronograma**
  - Medio: organiza frentes de trabajo.

#### Takeoff / Cómputo métrico

- **Qué es**
  - Acto y resultado de extraer cantidades medibles desde el modelo/plano interpretado hacia líneas de cómputo; nombre técnico-operativo del puente de cuantificación.
- **Qué representa**
  - La disciplina de medición de obra digitalizada.
  - El proceso color/geometría/hechos → cantidades.
  - La garantía de que el número «viene de algo».
- **Qué no representa**
  - Una apreciación a ojo sin ancla.
  - Una cotización de proveedor.
  - Un prompt de IA sin citas.
- **Reglas de negocio**
  - No hay takeoff confiable sin escala/calibración aceptable.
  - Takeoff propone líneas; el humano valida overrides y sellos.
  - Debe distinguir medición neta, tipológica y comprable.
  - Comparar takeoffs entre escenarios es comparación de proyecciones, no de planos distintos necesariamente.
- **Casos especiales**
  - Takeoff solo de muros (wedge mínimo).
  - Takeoff MEP tipológico (menos geométrico, más por puntos).
  - Re-takeoff tras cambio de aberturas.
- **Relaciones con otras entidades**
  - Produce Cómputo; lee Muro/Ambiente/etc.
  - Condicionado por Confidence/Provenance.
  - Entrada de Presupuesto.
- **Ejemplos reales**
  - Medición de 38 muros + 11 aberturas en planta PB.
  - Takeoff de solados por ambiente.
  - Takeoff de revoques descontando vanos.
- **Errores frecuentes**
  - Llamar takeoff a un precio cerrado de contratista sin cantidades.
  - Reutilizar takeoff de otra escala.
  - Sumar takeoffs de dos escenarios como si fueran aditivos.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Medio.

#### Presupuesto

- **Qué es**
  - Documento/estado comercial que aplica unitarios y reglas de armado de rubros sobre un cómputo anclado a versión/escenario, destinado a decisión de cliente o contrato.
- **Qué representa**
  - La oferta económica estructurada.
  - La suma de renglones (cantidad × unitario + lógicas de cargos) con moneda y fecha de referencia.
  - Un artefacto sellable.
- **Qué no representa**
  - El cómputo sin precios.
  - La certificación de avance.
  - La factura.
  - El plan Free/Pro/Enterprise.
- **Reglas de negocio**
  1. Un presupuesto serio declara versión/escenario y moneda.
  2. Sellar/firmar congela el paquete; cambios posteriores son nueva versión o extras.
  3. No se presenta al cliente como cerrado si la confianza agregada no supera el umbral.
  - Separar borrador interno de presupuesto emitido.
  - Inflación/volatilidad: fecha de precios visible.
  - Comparar presupuestos A/B/C solo con bases comparables.
- **Casos especiales**
  - Presupuesto de anteproyecto (baja confianza, rangos).
  - Presupuesto contractual.
  - Presupuesto de adicionales.
- **Relaciones con otras entidades**
  - Lee Cómputo + Unitarios + Rubros.
  - Se sella sobre Versión/Escenario.
  - Deriva Certificación y compara contra Baseline.
- **Ejemplos reales**
  - Presupuesto de vivienda 120 m² escenario ladrillo.
  - Comparativa steel vs retak para el mismo cliente.
  - Presupuesto de adecuación de local 60 m².
- **Errores frecuentes**
  - Editar precios en un PDF sellado y fingir que es el mismo presupuesto.
  - Mezclar unitarios de meses distintos sin declarar.
  - Incluir ítems de IA sin cita.
- **Impacto sobre presupuestos**
  - Alto: es el impacto mismo.
  - Centro del dinero pre-obra.
- **Impacto sobre materiales**
  - Alto indirecto: congela especificaciones comprables.
- **Impacto sobre costos**
  - Alto: expresa costos.
- **Impacto sobre cronograma**
  - Medio: define hitos de decisión; no es el Gantt.

#### Certificación

- **Qué es**
  - Documento/estado de avance económico que declara qué parte del alcance aprobado (baseline/presupuesto) se reconoce en un período, sin exceder lo aprobado salvo adicional formal.
- **Qué representa**
  - La certificación de avance de obra (mensual o por hito).
  - Porcentajes o cantidades ejecutadas × precios contractuales.
  - El puente entre avance físico y dinero a pagar.
- **Qué no representa**
  - El presupuesto original.
  - Una selfie de obra sin medición.
  - Una OC.
  - Una habilitación municipal.
- **Reglas de negocio**
  - No puede exceder el baseline aprobado sin change order / adicional.
  - Se ancla a versión/baseline y a reglas de medición de avance.
  - Requiere evidencia de avance cuando el expediente lo pide.
  - Ítems no presupuestados no «se cuelan» en certificación silenciosa.
  - Humano certifica; la IA puede proponer % con cita a evidencia.
- **Casos especiales**
  - Certificación parcial por zona/nivel.
  - Certificación de adicionales en documento separado o sección clara.
  - Retenciones/fondos de reparo como lógica comercial asociada (no redefinen cantidad).
- **Relaciones con otras entidades**
  - Contra Baseline/Presupuesto.
  - Lee Avance de obra + Evidencia.
  - Aparece en Timeline.
- **Ejemplos reales**
  - Certificación 1: excavación + platea 100%, muros 30%.
  - Certificación de terminaciones de baños cerrados.
  - Certificación final con pendientes de detalles.
- **Errores frecuentes**
  - Certificar 110% de un renglón porque «casi».
  - Usar avance de otro escenario.
  - Certificar sin baseline.
- **Impacto sobre presupuestos**
  - Alto: mueve dinero de contrato.
- **Impacto sobre materiales**
  - Medio: dispara compras de siguiente frente.
- **Impacto sobre costos**
  - Alto: monto certificado.
- **Impacto sobre cronograma**
  - Alto: ritmo de caja y secuencia de frentes.

#### Orden de compra

- **Qué es**
  - Documento de adquisición que solicita a un proveedor cantidades comprables tipificadas, referenciando líneas de cómputo/especificaciones; no crea geometría.
- **Qué representa**
  - La OC de materiales/servicios.
  - Cantidad comprable + material + proveedor + fecha.
  - Ejecución del presupuesto hacia la obra.
- **Qué no representa**
  - El presupuesto completo.
  - Un muro nuevo.
  - Una certificación.
- **Reglas de negocio**
  - Debe referenciar líneas de takeoff/cómputo o specs equivalentes.
  - No inventa cantidades: toma comprables del cómputo + criterio de compra.
  - Cambios de OC por precio no reescriben el modelo; pueden crear evento de costo.
  - Aprobación humana cuando impacta dinero/alcance.
- **Casos especiales**
  - OC parcial por etapa.
  - OC de largos lead time (aberturas) anticipada.
  - OC de servicio de hormigón elaborado por descarga.
- **Relaciones con otras entidades**
  - Lee Cómputo/Material/Proveedor.
  - Se alinea a Presupuesto/Baseline.
  - Puede vincularse a Avance (no comprar todo day-0).
- **Ejemplos reales**
  - OC de ladrillos + cemento para PB.
  - OC de aberturas de aluminio a fábrica.
  - OC de cerámicos una vez elegido el modelo.
- **Errores frecuentes**
  - Crear OC desde un chat sin líneas.
  - Comprar el doble «por las dudas» sin registrar desperdicio/criterio.
  - Usar OC para esconder un adicional.
- **Impacto sobre presupuestos**
  - Medio-Alto: ejecuta el presupuesto.
  - No reemplaza el sello.
- **Impacto sobre materiales**
  - Alto: es la compra.
- **Impacto sobre costos**
  - Alto: precio acordado con proveedor.
  - Impacta cashflow.
- **Impacto sobre cronograma**
  - Alto: desabastecimiento frena cronograma.

#### Unitario

- **Qué es**
  - Precio por unidad de medida de un renglón (ARS/m², ARS/u, etc.) en una fecha y contexto de compra/mano de obra.
- **Qué representa**
  - El multiplicador monetario de la cantidad.
  - Puede incluir o separar mano de obra según criterio del rubro.
  - Un dato volátil en LATAM.
- **Qué no representa**
  - La cantidad.
  - El presupuesto total.
  - La inflación misma (la inflación lo mueve).
- **Reglas de negocio**
  - Todo unitario serio tiene fecha y moneda.
  - Unitario de material ≠ unitario de mano de obra si se separan.
  - No se aplica un unitario de un escenario a cantidades de otro sin revisión.
  - Overrides de unitario son cambios con autor.
- **Casos especiales**
  - Unitario llave en mano vs desglosado.
  - Unitario regional (CABA vs interior).
  - Unitario de oferta de proveedor vs libro interno.
- **Relaciones con otras entidades**
  - Multiplica Cantidad en Presupuesto.
  - Viene de libro/Proveedor/estimación tipológica.
  - Se congela al sellar según política.
- **Ejemplos reales**
  - ARS/m² de revoque fino interior.
  - ARS/u puerta placa 0,70.
  - ARS/m³ hormigón H21 elaborado.
- **Errores frecuentes**
  - Mezclar unitarios con/sin IVA sin declarar.
  - Actualizar unitarios en documento sellado.
  - Usar unitario de steel en renglón ladrillo.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Medio: no cambia piezas, cambia valuación.
- **Impacto sobre costos**
  - Alto: es el costo unitario.
- **Impacto sobre cronograma**
  - Bajo-Medio: puede cambiar make-or-buy y plazos de compra.

#### Rubro

- **Qué es**
  - Agrupación comercial del presupuesto (albañilería, sanitarios, electricidad, pintura, etc.) que organiza la comunicación con cliente y contratista.
- **Qué representa**
  - El capítulo del presupuesto.
  - Una vista del cómputo valuado.
  - Un lenguaje compartido de oficio.
- **Qué no representa**
  - Un ambiente.
  - Un sistema MEP completo por sí solo (aunque suelen alinearse).
  - Una entidad geométrica.
- **Reglas de negocio**
  - Los rubros no duplican cantidades: son agrupación.
  - Un elemento puede contribuir a un rubro primario; evitar doble asignación de dinero.
  - La estructura de rubros debe ser estable dentro del proyecto para comparar versiones.
  - Subrubros permitidos; no infinita fragmentación cosmética.
- **Casos especiales**
  - Rubro de demoliciones en refacción.
  - Rubro de seguridad e higiene / obrador (indirectos).
  - Rubro de adicionales.
- **Relaciones con otras entidades**
  - Organiza líneas de Presupuesto derivadas del Cómputo.
  - Comunica a Cliente/Contratista.
  - Puede alinear Certificaciones por capítulo.
- **Ejemplos reales**
  - Rubro Albañilería 45% del total en casa ladrillo.
  - Rubro Instalaciones en local gastronómico dominante.
  - Rubro Pintura al cierre.
- **Errores frecuentes**
  - Crear un rubro por cada ambiente (explota comparabilidad).
  - Meter el mismo m² en dos rubros y sumar.
  - Cambiar taxonomía de rubros entre versiones sin mapa.
- **Impacto sobre presupuestos**
  - Alto en presentación y control.
  - Medio en geometría (nulo directo).
- **Impacto sobre materiales**
  - Medio: organiza compras por familia.
- **Impacto sobre costos**
  - Alto: estructura del dinero.
- **Impacto sobre cronograma**
  - Medio: certificaciones por rubro.

#### Desperdicio

- **Qué es**
  - Margen de material que transforma cantidad neta de cómputo en cantidad comprable, según tipología de material/sistema y criterio de obra.
- **Qué representa**
  - Porcentajes o factores por familia (ladrillo, cerámico, cable, etc.).
  - La diferencia entre medir y comprar.
  - Un criterio editable por humanos de obra.
- **Qué no representa**
  - Un error de medición (eso es otra cosa).
  - Inflación.
  - Doble conteo.
- **Reglas de negocio**
  - Debe ser visible; no esconderse dentro del unitario sin poder explicarlo.
  - Distinto por material; no un % global ciego salvo decisión explícita.
  - Cambio de desperdicio post-sello es cambio de dinero: versionar/adicional.
  - Cerámicos y vidrios suelen exigir desperdicio mayor que pintura.
- **Casos especiales**
  - Desperdicio de corte en porcelanato rectificado.
  - Merma de hormigón en descarga.
  - Desperdicio casi nulo en artefactos contados por u.
- **Relaciones con otras entidades**
  - Ajusta Cantidad neta → comprable.
  - Depende de Material/Sistema.
  - Afecta OC y Presupuesto.
- **Ejemplos reales**
  - +8% ladrillo hueco.
  - +12% cerámico de baño con muchos cortes.
  - +5% cables tipológicos.
- **Errores frecuentes**
  - Meter desperdicio dos veces (en cantidad y en unitario) sin saberlo.
  - Usar desperdicio para esconder incertidumbre de escala.
  - Aplicar desperdicio a mano de obra como si fuera material.
- **Impacto sobre presupuestos**
  - Alto: hincha el presupuesto si se abusa; lo deja corto si se omite.
- **Impacto sobre materiales**
  - Alto: define compra real.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Bajo-Medio: faltantes frenan obra.

#### Mano de obra

- **Qué es**
  - Componente de trabajo humano (y cuadrilla) necesario para ejecutar un renglón, medido en dinero por unidad, jornales o porcentaje según criterio.
- **Qué representa**
  - El costo de hacer, no solo de comprar.
  - Especialidades: albañil, sanitarista, electricista, pintor, colocador.
  - Un driver de cronograma.
- **Qué no representa**
  - El material.
  - El contratista como empresa (el contratista provee mano de obra).
  - Un usuario de software.
- **Reglas de negocio**
  - Declarar si el unitario es material+mo o separado.
  - Distinta productividad por sistema (ladrillo vs steel).
  - No se certifica mano de obra fantasma sin avance.
  - Adicionales de mo por trabajo en altura/fin de semana se tipifican.
- **Casos especiales**
  - Cuadrilla propia vs subcontratista.
  - Mano de obra especializada de impermeabilización.
  - Instalación de aberturas por fabricante.
- **Relaciones con otras entidades**
  - Parte de Unitario/Presupuesto.
  - Ejecutada por Contratista/Subcontratista.
  - Ligado a Cronograma/Avance.
- **Ejemplos reales**
  - Jornales de revoque fino.
  - Colocación de porcelanato por m².
  - Tendido eléctrico por punto.
- **Errores frecuentes**
  - Olvidar mo y cotizar solo materiales al cliente final.
  - Usar productividades de otro país sin ajuste.
  - Duplicar mo en rubro y en gasto general.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Nulo directo sobre piezas; alto sobre capacidad de colocarlas.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: es el tiempo.

#### Baseline

- **Qué es**
  - Versión/alcance aprobado que sirve de referencia oficial para comparar cambios, extras y certificaciones.
- **Qué representa**
  - El «contrato cuantitativo» de referencia.
  - El ancla del avance y de los adicionales.
  - Un head promovido/sellado con rol de baseline.
- **Qué no representa**
  - Cualquier borrador reciente.
  - El promedio de escenarios.
  - El wish-list del cliente.
- **Reglas de negocio**
  - Solo puede haber un baseline vigente por alcance declarado (proyecto o fase).
  - Certificación no excede baseline sin adicional.
  - Cambiar baseline es acto formal (promote) con Timeline.
  - Escenarios alternativos no son baseline hasta promoverse.
- **Casos especiales**
  - Baseline de anteproyecto vs baseline de contrato.
  - Baseline por etapa (fase 1 habilitada).
  - Baseline de unidad de PH dentro de un proyecto mayor.
- **Relaciones con otras entidades**
  - Es un rol de Versión/Presupuesto aprobado.
  - Referencia de Extras/adicionales, Certificación, Avance.
- **Ejemplos reales**
  - V12 escenario ladrillo firmada como baseline de obra.
  - Baseline de demoliciones aprobada antes de obra nueva.
  - Baseline de terminaciones tras elección de cerámicos.
- **Errores frecuentes**
  - Certificar contra el último whatsapp.
  - Tener dos baselines silenciosas.
  - Mover baseline para ocultar extras.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto indirecto: congela specs de compra.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: define el plan de avance.

#### Avance de obra

- **Qué es**
  - Medición del progreso físico/contractual respecto del baseline, por renglón, rubro, zona o hito.
- **Qué representa**
  - % o cantidades ejecutadas.
  - Input de certificación.
  - Foto de estado de la obra en el tiempo.
- **Qué no representa**
  - El deseo de cobro.
  - La OC ya emitida.
  - Un escenario futuro.
- **Reglas de negocio**
  - Avance ≤ alcance aprobado (+ adicionales formales).
  - Debe ser consistente con evidencia cuando se exige.
  - Avance por ambiente/zona ayuda frentes.
  - No confundir avance de compra (material en obrador) con avance colocado.
- **Casos especiales**
  - Avance de estructura 100% con terminaciones 0%.
  - Material en obra no colocado: avance de logística, no de renglón colocado.
  - Retrabajo: puede reducir avance certificado según contrato.
- **Relaciones con otras entidades**
  - Alimenta Certificación.
  - Se registra en Timeline.
  - Se apoya en Evidencia.
- **Ejemplos reales**
  - Muros PB 80% levantados.
  - Sanitarios embutidos 100%, artefactos 0%.
  - Pintura 50% en planta alta.
- **Errores frecuentes**
  - Declarar 100% porque el material está comprado.
  - Avanzar renglones no existentes en baseline.
  - Usar avance de otro escenario.
- **Impacto sobre presupuestos**
  - Alto vía certificación.
- **Impacto sobre materiales**
  - Medio: ordena siguientes compras.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: es el cronograma real.

#### Extras / adicionales

- **Qué es**
  - Cambios de alcance o especificación respecto del baseline que generan cantidades y/o dinero fuera de lo aprobado, con trazabilidad.
- **Qué representa**
  - El adicional de obra.
  - El change order de negocio.
  - La memoria de «esto no estaba».
- **Qué no representa**
  - Un ajuste silencioso de Excel.
  - Un redondeo de desperdicio oculto.
  - Un escenario completo no promovido (hasta que se incorpore).
- **Reglas de negocio**
  1. Todo adicional cita baseline y describe el cambio.
  2. Tiene cómputo y precio propios o delta explícito.
  3. Requiere aceptación humana para impacto de dinero.
  - No se certifica dentro del baseline como si siempre hubiera estado.
  - Puede afectar cronograma (plazos) además de dinero.
- **Casos especiales**
  - Adicional de HVAC no contemplado.
  - Upgrade de aberturas a DVH.
  - Demolición no prevista al abrir un muro.
- **Relaciones con otras entidades**
  - Nace de Cambio; altera Presupuesto/Certificación; se registra en Timeline.
  - Puede originarse en Evidencia de obra real vs plano.
- **Ejemplos reales**
  - +1 baño en PB.
  - Cambio de cerámico a porcelanato premium.
  - Refuerzo estructural hallado en remodelación.
- **Errores frecuentes**
  - Esconder adicionales como «ajuste de desperdicio».
  - Emitir adicional sin cantidades.
  - Aprobar por chat y no versionar.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto: nuevas compras.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: alarga o reordena obra.
### 2.6 Actores de negocio

Los actores son roles de obra/comercio. No se confunden con planes SaaS ni con permisos técnicos de login, aunque en producto puedan mapearse.

#### Proveedor

- **Qué es**
  - Parte que ofrece materiales u servicios de suministro/instalación parcial, con precios y plazos, sin ser necesariamente el contratista general.
- **Qué representa**
  - Corralón, fábrica de aberturas, hormigonera, marketplace seller.
  - Fuente de unitarios y lead times.
  - Emisor potencial de ofertas bindeables a specs/líneas.
- **Qué no representa**
  - El cliente.
  - El modelo de obra.
  - Un precio sin entidad.
- **Reglas de negocio**
  - Sus ofertas se bindean a materiales/líneas; no crean muros.
  - Cambio de proveedor no debe silent-edit cantidades geométricas.
  - Varios proveedores pueden cotizar la misma línea.
  - La OC referencia proveedor + líneas.
- **Casos especiales**
  - Proveedor exclusivo de aberturas con medición en obra.
  - Proveedor de hormigón con ventana horaria.
  - Marketplace vs proveedor histórico del contratista.
- **Relaciones con otras entidades**
  - Emite ofertas/unitarios; recibe OC.
  - Se relaciona con Material y Contratista.
  - Aparece en Timeline de compras.
- **Ejemplos reales**
  - Corralón local para ladrillo/cemento.
  - Fábrica de aluminio en Parque Industrial.
  - Distribuidor de retak.
- **Errores frecuentes**
  - Dejar que el proveedor «ajuste» el cómputo sin traza.
  - Duplicar compras al mismo y a otro sin cancelar.
  - Confundir oferta con presupuesto sellado al cliente.
- **Impacto sobre presupuestos**
  - Medio: cambia opciones de renglón.
  - No redefine alcance por sí solo.
- **Impacto sobre materiales**
  - Alto: quién entrega qué.
- **Impacto sobre costos**
  - Alto: precio y condiciones.
- **Impacto sobre cronograma**
  - Alto: lead time.

#### Cliente

- **Qué es**
  - Parte demandante del proyecto que recibe presupuestos, aprueba baselines/adicionales y es destinatario del valor de la cuantificación.
- **Qué representa**
  - Comitente, dueño, desarrollador, locatario que construye/adecúa.
  - Quien decide escenarios y sellos comerciales.
  - El receptor de explicaciones de confianza.
- **Qué no representa**
  - El usuario operador del estudio (puede coincidir, no siempre).
  - El contratista.
  - El plan Enterprise.
- **Reglas de negocio**
  - El cliente no edita hechos en silencio vía chat de IA sin rol.
  - Documentos cliente-facing exigen umbrales de confianza.
  - Aprobación de baseline/adicionales es acto de cliente (o su representante).
  - Comparativas A/B/C se presentan en su lenguaje (rubros), no en jerga interna.
- **Casos especiales**
  - Cliente final vivienda vs desarrollador de PH.
  - Cliente de local franquicia con specs rígidas.
  - Comitente público (más controles; fuera del wedge típico pero conceptualmente cliente).
- **Relaciones con otras entidades**
  - Rol en Proyecto; aprueba Presupuesto/Baseline/Extras.
  - Recibe Certificaciones para pago.
  - Interactúa con Contratista.
- **Ejemplos reales**
  - Familia que construye casa en GBA.
  - Dueño de PH en pozo.
  - Comerciante que adecúa local en peatonal.
- **Errores frecuentes**
  - Mostrar borradores de baja confianza como cierre.
  - Mezclar tres escenarios en un único total «promedio».
  - Ocultar exclusiones.
- **Impacto sobre presupuestos**
  - Alto: es el destinatario del presupuesto.
- **Impacto sobre materiales**
  - Medio: elige terminaciones/materiales.
- **Impacto sobre costos**
  - Alto: aprueba dinero.
- **Impacto sobre cronograma**
  - Medio-Alto: aprueba plazos y etapas.

#### Contratista

- **Qué es**
  - Parte que ejecuta la obra (o el paquete principal), usa el cómputo/presupuesto para comprar y certificar, y coordina subcontratistas.
- **Qué representa**
  - Constructora, empresa de reformas, constructor de vivienda.
  - Operador principal del avance y de las certificaciones.
  - Usuario típico jefe de obra / dirección técnica de ejecución.
- **Qué no representa**
  - Un subcontratista especializado único.
  - El proveedor de ladrillos.
  - El software.
- **Reglas de negocio**
  - Certifica contra baseline; no inventa alcance.
  - Puede proponer adicionales con cómputo delta.
  - Responsable de integrar mediciones de campo (evidencia) al expediente.
  - Sus productividades no reescriben geometría.
- **Casos especiales**
  - Contratista llave en mano vs por rubros.
  - Constructor amigo del cliente vs empresa formal.
  - Contratista distinto por fase.
- **Relaciones con otras entidades**
  - Ejecuta; propone Cambios; coordina Subcontratista; compra a Proveedor.
  - Usa Cómputo/Presupuesto/Certificación.
  - Carga Avance/Evidencia.
- **Ejemplos reales**
  - PyME constructora de viviendas en Córdoba.
  - Empresa de adecuaciones comerciales en CABA.
  - Constructor de PH de escala media.
- **Errores frecuentes**
  - Certificar de más para financiar la obra.
  - Usar otro escenario más barato sin aprobación.
  - Comprar fuera de cómputo y reclamar adicional después.
- **Impacto sobre presupuestos**
  - Alto: opera el presupuesto en obra.
- **Impacto sobre materiales**
  - Alto: ejecuta compras.
- **Impacto sobre costos**
  - Alto: cobra certificaciones.
- **Impacto sobre cronograma**
  - Alto: dueño del cronograma de ejecución.

#### Subcontratista

- **Qué es**
  - Parte especializada contratada por el contratista (o a veces por el cliente) para un rubro o sistema (sanitarios, electricidad, herrería, pintura).
- **Qué representa**
  - Cuadrilla/empresa de oficio.
  - Ejecutor de un paquete con su propio unitario interno.
  - Fuente de evidencia de avance de su frente.
- **Qué no representa**
  - El contratista general.
  - El proveedor de materiales (puede solaparse en instaladores-proveedores; tipificar rol).
  - Un rubro sin persona.
- **Reglas de negocio**
  - Su alcance debe mapear a rubros/líneas; no a obra entera ambigua.
  - Mediciones del subcontratista se validan contra cómputo baseline.
  - Conflictos entre gremios (roza vs embutido) son coordinación de obra, documentada como cambio si hay costo.
- **Casos especiales**
  - Sanitarista matriculado.
  - Electricista.
  - Colocador de porcelanato.
  - Impermeabilizador de azotea.
- **Relaciones con otras entidades**
  - Contrato con Contratista/Cliente.
  - Ejecuta Mano de obra especializada; consume Materiales.
  - Reporta Avance de su frente.
- **Ejemplos reales**
  - Subcontrato de aberturas con instalación.
  - Subcontrato de HVAC.
  - Subcontrato de pintura final.
- **Errores frecuentes**
  - Dejar que el subcontratista redefine cantidades sin pasar por cómputo.
  - Duplicar su mo en gasto general y en rubro.
  - Certificar su avance sin ver el frente.
- **Impacto sobre presupuestos**
  - Medio-Alto vía rubros.
- **Impacto sobre materiales**
  - Medio: pide materiales según su consumo.
- **Impacto sobre costos**
  - Alto en su paquete.
- **Impacto sobre cronograma**
  - Alto en su camino crítico local.

### 2.7 Proceso, calidad, evidencia e IA

Este grupo fija quién propone, quién decide, cómo se recuerda la obra y cómo se comunica incertidumbre. Es el antídoto contra el «número mágico».

#### Timeline

- **Qué es**
  - Línea de tiempo de negocio del proyecto: hitos y eventos relevantes (carga de plano, cambios confirmados, escenarios, sellos, certificaciones, compras significativas).
- **Qué representa**
  - La memoria narrativa de la obra digital.
  - El orden de decisiones.
  - El contexto de auditoría para humanos.
- **Qué no representa**
  - Un log técnico de servidores.
  - El Gantt completo de cuadrillas (puede vinculares, no es lo mismo).
  - El chat completo de IA.
- **Reglas de negocio**
  - Eventos de sello/certificación/adicionales son de primera clase.
  - El timeline no reescribe hechos; los señala.
  - Debe distinguir propuesta vs confirmación.
  - Útil para explicar por qué el presupuesto cambió.
- **Casos especiales**
  - Timeline de anteproyecto denso en cambios de diseño.
  - Timeline de obra denso en certificaciones.
  - Timeline de disputa (extras).
- **Relaciones con otras entidades**
  - Registra Cambios, Sellos, Certificaciones, Avances, Evidencias aceptadas.
  - Se ancla al Proyecto.
- **Ejemplos reales**
  - «V7 sellada enviada a cliente» → «V8 adicional HVAC».
  - «Cerámicos elegidos» → «OC emitida».
  - «Filtración en azotea» → evidencia → adicional de impermeabilización.
- **Errores frecuentes**
  - Usar el timeline como prueba de cantidades sin cómputo.
  - Registrar solo automáticamente ruido sin hitos de negocio.
  - Borrar historia de sellos.
- **Impacto sobre presupuestos**
  - Medio-Alto: explica evolución del presupuesto.
- **Impacto sobre materiales**
  - Bajo directo.
- **Impacto sobre costos**
  - Medio: contextualiza cambios de costo.
  - Alto en disputas.
- **Impacto sobre cronograma**
  - Alto: es la historia del cronograma de decisiones.

#### Cambio

- **Qué es**
  - Modificación documentada de hechos o de alcance/spec que produce un nuevo estado versionado; unidad de evolución del modelo y del dinero.
- **Qué representa**
  - El change set de negocio: qué se tocó y por qué.
  - El origen de deltas de cómputo/presupuesto.
  - La diferencia entre memoria y amnesia de obra.
- **Qué no representa**
  - Un undo cosmético de UI.
  - Una alucinación de chat aplicada.
  - Una actualización de precio de libro sin tocar hechos (eso es evento de costo, no de geometría).
- **Reglas de negocio**
  1. Todo cambio material deja traza (quién/cuándo/porqué).
  2. No se aplica sobre versión sellada in-place.
  3. Si impacta dinero, requiere aceptación humana.
  - Cambios de percepción llegan como propuestas hasta confirmarse.
  - Cambios de escenario material se distinguen de cambios geométricos.
- **Casos especiales**
  - Cambio por error de interpretación de plano.
  - Cambio por pedido de cliente.
  - Cambio por hallazgo en obra (existente distinto).
- **Relaciones con otras entidades**
  - Produce nueva Versión/tip; genera Extras si hay baseline; aparece en Timeline.
  - Puede originarse en Evidencia/IA/humano de obra.
- **Ejemplos reales**
  - Sumar una ventana al living.
  - Pasar de ladrillo a steel en escenario B.
  - Eliminar un tabique (y su impacto en ambientes).
- **Errores frecuentes**
  - «Ajustar» sin cambio formal.
  - Agrupar 50 cambios no relacionados en uno opaco.
  - Aplicar cambio de IA sin revisión.
- **Impacto sobre presupuestos**
  - Alto.
- **Impacto sobre materiales**
  - Alto si toca bindings/geometría.
- **Impacto sobre costos**
  - Alto si hay delta.
- **Impacto sobre cronograma**
  - Alto si reordena frentes.

#### Evidencia

- **Qué es**
  - Soporte perceptivo o documental anclado (recorte de plano, detección, foto de obra, medición de campo) que respalda o cuestiona un hecho; no es el hecho final por sí sola.
- **Qué representa**
  - Prueba de origen de una cantidad o de un avance.
  - Salida de percepción o de relevamiento.
  - Objeto con estado propuesto/aceptado/rechazado.
- **Qué no representa**
  - El presupuesto.
  - La cantidad sellada.
  - Un rumor de cuadrilla.
- **Reglas de negocio**
  - Evidencia propuesta no mueve dinero.
  - Aceptar evidencia vincula hechos/elementos con provenance.
  - Rechazar evidencia se retiene para auditoría; no se hard-borra si fue citada.
  - Confianza de evidencia propaga a hechos derivados.
- **Casos especiales**
  - Foto de muro ya levantado para certificar.
  - Detección de vano por visión en plano.
  - Medición láser de diagonal que corrige escala dudosa.
- **Relaciones con otras entidades**
  - Soporta Elementos/Cantidades/Avance.
  - Alimenta Confidence/Provenance.
  - Puede disparar Cambio.
- **Ejemplos reales**
  - Screenshot de planta con muro marcado.
  - Foto de filtración.
  - Planilla de replanteo firmada por jefe de obra (como evidencia de negocio).
- **Errores frecuentes**
  - Certificar solo con evidencia sin renglón.
  - Aceptar evidencia de baja calidad sin marcar confianza.
  - Dejar evidencia propuesta como si fuera baseline.
- **Impacto sobre presupuestos**
  - Medio-Alto: habilita o bloquea sellos.
  - Indirecto.
- **Impacto sobre materiales**
  - Medio: valida qué se compra/colocó.
- **Impacto sobre costos**
  - Medio-Alto vía aceptación.
- **Impacto sobre cronograma**
  - Alto para validar avance.

#### Confidence

- **Qué es**
  - Expresión de negocio del grado de certeza de un hecho cuantitativo o de un documento agregado (0..1 o escala equivalente), comunicable al usuario.
- **Qué representa**
  - La incertidumbre manejada con honestidad.
  - Un gate para documentos cliente-facing.
  - Una agregación de calidades de escala, detección, tipificación y overrides.
- **Qué no representa**
  - Un score de marketing.
  - Una garantía legal.
  - Un porcentaje de avance.
- **Reglas de negocio**
  - Hechos cuantitativos llevan confidence.
  - Umbrales bloquean sello/emisión cliente si no se cumplen.
  - Overrides manuales pueden subir o bajar confidence según política, pero quedan marcados.
  - Baja confidence exige disclaimer o rango, no decimales falsos.
  - La IA no «pone 0.99» para embellecer.
- **Casos especiales**
  - Escala dudosa → confidence baja global de medidas.
  - Ambiente tipificado a mano por arquitecto → alta en uso, media en geometría si no midió.
  - Presupuesto de anteproyecto: confidence agregada baja por diseño.
- **Relaciones con otras entidades**
  - Se deriva de Evidencia/Provenance/Escala.
  - Gates de Presupuesto/Certificación.
  - Visible en explicaciones al Cliente.
- **Ejemplos reales**
  - 0.95 en muros bien calibrados.
  - 0.55 en MEP tipológico sin plano de instalaciones.
  - 0.40 en remodelación con existentes desconocidos.
- **Errores frecuentes**
  - Ocultar confidence al cliente.
  - Promediar confidence de escenarios para «mejorar» el número.
  - Usar confidence como precio.
- **Impacto sobre presupuestos**
  - Alto: decide si el presupuesto es emitible.
- **Impacto sobre materiales**
  - Medio: señala specs dudosas.
- **Impacto sobre costos**
  - Alto: riesgo de desvío de costo.
  - Indirecto.
- **Impacto sobre cronograma**
  - Medio: obras con baja certainty requieren buffers de plazo.

#### Provenance

- **Qué es**
  - Pedigrí de un hecho o número: de dónde salió, quién lo confirmó, con qué evidencia y en qué versión.
- **Qué representa**
  - La respuesta a «¿quién dice que son 45 m²?».
  - La cadena percepción → propuesta → confirmación → sello.
  - La base de auditoría y de explicación al cliente.
- **Qué no representa**
  - Un attachment suelto sin vínculo.
  - El nombre del archivo del plano solo.
  - Un disclaimer genérico de pie de PDF.
- **Reglas de negocio**
  - Cantidades materiales deben poder citar provenance.
  - Cambios manuales declaran autor y motivo.
  - Propuestas de IA declaran author_type IA y no se auto-confirman en dinero.
  - Al sellar, el provenance relevante queda congelado con la versión.
- **Casos especiales**
  - Provenance mixto: muro detectado + espesor tipificado a mano.
  - Provenance de precio (libro 2026-08-01) distinto del de cantidad.
  - Provenance de avance fotográfico.
- **Relaciones con otras entidades**
  - Acompaña Cantidad/Elemento/Cambio.
  - Se apoya en Evidencia.
  - Soporta Confidence.
- **Ejemplos reales**
  - «Longitud desde eje calibrado en planta PB hoja 1».
  - «Puntos eléctricos tipológicos por norma de proyecto, no plano MEP».
  - «Override jefe de obra: +1 ventana patio».
- **Errores frecuentes**
  - Perder provenance al exportar/importar.
  - Atribuir a «sistema» un override humano.
  - Citar IA como fuente de metros.
- **Impacto sobre presupuestos**
  - Alto en defensa del presupuesto.
  - Medio en armado.
- **Impacto sobre materiales**
  - Medio.
- **Impacto sobre costos**
  - Alto en disputas de costo.
  - Medio en valuación.
- **Impacto sobre cronograma**
  - Medio.

#### IA

- **Qué es**
  - Capa de asistencia inteligente que lee hechos/proyecciones, explica, clasifica y propone borradores; nunca es autoridad de cantidades ni de dinero.
- **Qué representa**
  - Copiloto de interpretación y redacción.
  - Generador de propuestas de cambio con citas.
  - Asistente de comparación de escenarios y de checklist de obra.
- **Qué no representa**
  - Fuente de verdad del MDO.
  - Motor de cómputo geométrico.
  - Firmante de presupuestos.
  - Entidad legal.
- **Reglas de negocio**
  - Toda afirmación cuantitativa comercial cita hechos/proyecciones.
  - Propuestas = borradores; confirmación humana si hay dinero o hechos materiales.
  - No inventa cantidades sin ancla.
  - No mutea versiones selladas.
  - Free/Pro/Enterprise puede limitar features de IA; no cambia estas reglas de dominio.
- **Casos especiales**
  - IA explica por qué bajó el total al pasar a steel.
  - IA propone tipificación de ambiente húmedo a partir del nombre «baño».
  - IA arma checklist de faltantes de cómputo; no los completa con números fantasma.
- **Relaciones con otras entidades**
  - Lee Versión/Cómputo/Timeline; propone Cambio; usa Provenance/Confidence.
  - No reemplaza Percepción ni Takeoff determinista.
- **Ejemplos reales**
  - «¿Cuánto sale cambiar a DVH?» → responde con delta anclado a aberturas existentes.
  - «Armá un resumen para el cliente del escenario B».
  - «¿Qué líneas tienen confidence < 0.7?».
- **Errores frecuentes**
  - Pedirle a la IA metros cuadrados «aproximados» y sellarlos.
  - Dejar que confirme adicionales sola.
  - Usarla como ERP de proveedores.
- **Impacto sobre presupuestos**
  - Alto riesgo si se malusa; Bajo si se usa bien (explica).
  - Nunca autoridad.
- **Impacto sobre materiales**
  - Puede sugerir equivalencias; no impone compra.
- **Impacto sobre costos**
  - Puede simular; no firmar.
- **Impacto sobre cronograma**
  - Puede alertar secuencias; no certificar avance.

### 2.8 Conceptos transversales de medición y terminación

Cierran coherencia del oficio: medir bien, tratar húmedos, terminar e impermeabilizar/aislar sin mezclar capas.

#### Escala / calibración

- **Qué es**
  - Condición de negocio que convierte dibujo en medida real; sin ella no hay cantidad confiable.
- **Qué representa**
  - La relación entre papel/píxel y metros.
  - Un acto de calibración (cota conocida, escala gráfica, medición de campo).
  - Un gate de calidad del twin cuantitativo.
- **Qué no representa**
  - El zoom de la pantalla.
  - El tamaño del PDF en disco.
  - Una estimación a ojo del arquitecto pasada como calibración.
- **Reglas de negocio**
  - Sin calibración aceptable, el cómputo queda en confianza baja / no emitible.
  - Cambiar calibración invalida cantidades derivadas y exige re-takeoff.
  - Hojas distintas pueden tener escalas distintas; no reutilizar ciegamente.
  - Calibración de campo (láser) puede corregir plano escaneado; queda como evidencia.
- **Casos especiales**
  - Plano escaneado torcido: calibración con dos segmentos.
  - Detalle 1:20 vs planta 1:50 en el mismo expediente.
  - Plano sin escala: bloqueo de sello cliente.
- **Relaciones con otras entidades**
  - Condiciona Plano → Cantidades.
  - Propaga a Confidence de elementos medidos.
  - Precondición de Takeoff.
- **Ejemplos reales**
  - Calibrar con muro de frente cotado 8,50 m.
  - Usar escala gráfica del margen.
  - Contraste con medida real de medianera en obra.
- **Errores frecuentes**
  - Asumir 1:100 porque «se ve como 1:100».
  - Calibrar con un mueble dibujado a escala dudosa.
  - No recalibrar tras reemplazar el plano.
- **Impacto sobre presupuestos**
  - Alto: corrompe todo dinero derivado.
- **Impacto sobre materiales**
  - Alto: compras incorrectas.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Medio: errores graves frenan obra al descubrirse tarde.

#### Ambientes húmedos

- **Qué es**
  - Clase de uso de ambientes (baño, cocina, lavadero, toilette, ducheros, zonas de pileta/quinchos húmedos) que dispara reglas de impermeabilización, desagües y revestimientos.
- **Qué representa**
  - Un conjunto de reglas tipológicas, no solo un nombre.
  - Densidad sanitaria y eléctrica particular.
  - Alturas de revestimiento y pendientes típicas.
- **Qué no representa**
  - Cualquier ambiente con humedad ambiente alta por clima.
  - Una zona HVAC.
  - Un rubro.
- **Reglas de negocio**
  - Tipificar explícitamente; no inferir solo por color del plano sin confirmación cuando hay duda.
  - Impermeabilización bajo duchas/platos y en paredes críticas según detalle.
  - Solados antideslizantes/aptos.
  - Ventilación natural o mecánica.
- **Casos especiales**
  - Cocina de local gastronómico: húmedo + grasas + extracción.
  - Lavadero en azotea.
  - Baño sin ventana en PH.
- **Relaciones con otras entidades**
  - Especialización de Ambiente; dispara Impermeabilización, Cloacas, Agua, Cerámicos, a veces HVAC de extracción.
- **Ejemplos reales**
  - Baño completo 4 m².
  - Toilette de recepción de local.
  - Cocina integrada con zona húmeda de mesada.
- **Errores frecuentes**
  - Tratar baño como dormitorio chico.
  - Olvidar desagüe de piso cuando el detalle lo pide.
  - Presupuestar cerámico de pared a altura incorrecta sin criterio.
- **Impacto sobre presupuestos**
  - Alto en terminaciones e instalaciones.
- **Impacto sobre materiales**
  - Alto.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: frentes sensibles a filtraciones/retrabajo.

#### Terminación

- **Qué es**
  - Capa o estado de acabado visible/usable (solado, pintura, revestimiento, zócalo, cielorraso visto) que el cliente percibe como «obra terminada».
- **Qué representa**
  - El finish del ambiente.
  - Ítems de obra fina.
  - El cierre cualitativo del presupuesto de habitabilidad.
- **Qué no representa**
  - La estructura.
  - El contrapiso solo.
  - El color de percepción del plano.
- **Reglas de negocio**
  - Se especifica por ambiente/zona.
  - Depende de bases (revoque/carpeta) listas.
  - Cambios de terminación post-baseline son adicionales típicos.
  - Niveles de calidad (standard/premium) son escenarios o packs de binding, no geometría nueva.
- **Casos especiales**
  - Terminación provisorio de entrega vs final.
  - Local: terminación a cargo de marca/franquicia.
  - Obra gris / semi-gris / llave en mano: declarar alcance de terminación.
- **Relaciones con otras entidades**
  - Incluye Piso, Pintura, Cerámicos, parte de Aberturas vistas.
  - Relaciona Cliente (elección) y Mano de obra fina.
- **Ejemplos reales**
  - Pintura + piso + zócalos en dormitorios.
  - Revestimientos totales en baños.
  - Fachada pintada + frente comercial.
- **Errores frecuentes**
  - Vender terminación premium con cómputo standard.
  - Certificar terminación con base incompleta.
  - Olvidar cielorrasos.
- **Impacto sobre presupuestos**
  - Alto en percepción de valor del presupuesto.
- **Impacto sobre materiales**
  - Alto: materiales visibles.
  - Elección de cliente.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto al cierre; retrabajo caro.

#### Impermeabilización

- **Qué es**
  - Sistema de barreras contra agua (membranas, emulsiones, cementicios hidrófugos, detalles de babetas) en cubiertas, húmedos, muros enterrados y balcones.
- **Qué representa**
  - La protección al agua.
  - m² + detalles críticos (encuentros, desagües, juntas).
  - Ítem cuya falla sale carísima.
- **Qué no representa**
  - Pintura látex común.
  - Una pendiente sola sin membrana cuando el detalle la exige.
  - Zinguería completa (vinculada, no idéntica).
- **Reglas de negocio**
  - Tipificar sustrato (losa, carpeta, muro).
  - Húmedos y cubiertas son prioritarios.
  - Garantías de fabricante son comerciales; el dominio registra espec, no garantiza legalmente.
  - Inspección/evidencia de capas es buena práctica antes de cubrir.
- **Casos especiales**
  - Membrana asfáltica en azotea.
  - Hidrófugo en ducha.
  - Muro contra terreno con barrera.
- **Relaciones con otras entidades**
  - Relacionada con Cubierta, Ambientes húmedos, Carpeta, Desagües.
  - Material + Mano de obra especializada.
- **Ejemplos reales**
  - Azotea de PH.
  - Balcón de dormitorio.
  - Baño con platea de ducha a desagüe.
- **Errores frecuentes**
  - Pintar «impermeabilizante» de góndola como sistema de azotea.
  - Tapar la membrana sin documentar.
  - Olvidar encuentros con barandas/pasantes.
- **Impacto sobre presupuestos**
  - Alto (riesgo y costo de falla).
  - Medio-Alto en m².
- **Impacto sobre materiales**
  - Alto: membranas, imprimaciones, geotextiles.
- **Impacto sobre costos**
  - Alto.
- **Impacto sobre cronograma**
  - Alto: debe respetar tiempos de curado/clima; bloquea pisos superiores.

#### Aislación

- **Qué es**
  - Sistema de control térmico, acústico o ambos, por materiales y capas (lanas, EPS, barreras, cámaras) asociados a muros, cubiertas, entrepisos o instalaciones.
- **Qué representa**
  - Confort y eficiencia como especificación.
  - m² de aislante + espesores.
  - Parte inseparable de steel frame y de cubiertas bien resueltas.
- **Qué no representa**
  - Solo el revoque grueso «porque abriga».
  - Una ventana DVH sola (es componente; la aislación de opacos es otra).
  - Un claim de marketing sin espesor.
- **Reglas de negocio**
  - Declarar si es térmica, acústica o mixta.
  - En escenarios, steel/retak vs ladrillo cambian paquetes de aislación.
  - PH exige atención acústica entre unidades.
  - Aislación de cañerías de ACS se tipifica en instalaciones.
- **Casos especiales**
  - Lana de vidrio en steel.
  - EPS bajo contrapiso radiante.
  - Barrera acústica en tabique de dormitorio a living de PH.
- **Relaciones con otras entidades**
  - Capa de Muro/Cubierta/Contrapiso; Material específico; Escenario.
- **Ejemplos reales**
  - Fachada con aislación exterior (EIFS) tipificada.
  - Cubierta con aislante bajo chapa.
  - Shaft de instalaciones con aislación.
- **Errores frecuentes**
  - Vender steel sin aislación.
  - Usar espesor decorativo de plano como aislación real.
  - Olvidar acústica en PH.
- **Impacto sobre presupuestos**
  - Medio-Alto (valor percibido y cumplimiento tipológico).
- **Impacto sobre materiales**
  - Alto: placas, mantas, espumas, barreras.
- **Impacto sobre costos**
  - Medio-Alto.
- **Impacto sobre cronograma**
  - Medio: se instala en la secuencia de capas del sistema.

---
## 3. Reglas de negocio globales

Reglas transversales. Numeradas. Aplican aunque un concepto particular no las repita. Si una feature las viola, no es detalle de UX: es defecto de dominio.

Hay 81 reglas globales numeradas:

1. La autoridad de hechos de obra es el Modelo Digital de la Obra (MDO), no el PDF, no el chat, no el Excel exportado.
2. Percepción y visión proponen evidencias y operaciones; no declaran cantidades presupuestables finales sin aceptación.
3. La IA nunca inventa metros, kilos ni unidades; toda cifra comercial cita hecho o proyección.
4. Todo impacto de dinero (sello, certificación, OC relevante, adicional) requiere aceptación humana explícita.
5. Una versión sellada/firmada es inmutable en sus hechos; todo arreglo crea nueva versión o adicional.
6. Free/Pro/Enterprise limita capacidades de producto; no redefine ontología (muro sigue siendo muro).
7. Unidades canónicas: m, m², m³, ml, kg, u. Espesores de oficio en cm cuando el gremio habla en cm.
8. Moneda del proyecto es local (ARS en wedge Argentina). Toda cifra lleva moneda y, si es precio, fecha de referencia.
9. No mezclar sistemas de unidades en un mismo renglón sin conversión explícita documentada.
10. Redondeo de medición se declara por política de proyecto; redondeo de compra ocurre al pasar a cantidad comprable/OC.
11. Prohibido doble conteo de muros compartidos entre ambientes: identidad única del muro.
12. Un muro compartido entre dos ambientes puede recibir terminaciones distintas por cara; la mampostería base no se duplica.
13. Las aberturas descuentan del área de terminación del muro hospedante según regla del proyecto.
14. Las aberturas no descuentan dos veces el mismo paramento.
15. Si una abertura se tapa, el cierre es ítem/cambio; no reescritura amnésica del pasado sellado.
16. Altura de muros: usar altura del nivel/ambiente; override solo si está declarado.
17. Si no hay altura en plano, aplicar supuesto global documentado del proyecto (no un valor distinto por pantalla).
18. Se puede usar altura por ambiente cuando hay dobles alturas, entrepisos o cielorrasos especiales; debe tipificarse.
19. Ambientes húmedos disparan reglas de impermeabilización, desagües y revestimientos; no son dormitorios con otro nombre.
20. Separar cloacal de pluvial en lenguaje y cómputo.
21. Cantidad neta y cantidad comprable son distintas; el desperdicio es visible.
22. No esconder incertidumbre de escala dentro del porcentaje de desperdicio.
23. Sin calibración/escala aceptable no hay presupuesto cliente-facing cerrado.
24. Takeoff/cómputo es regenerable desde hechos; no es segunda geometría autoritativa.
25. Overrides manuales de cantidad marcan autor, motivo y afectan confidence según política.
26. Comparar escenarios solo con base geométrica comparable o declarando divergencias geométricas.
27. Firmar/sellar un escenario no sella los demás.
28. Baseline vigente es único por alcance declarado; certificaciones se miden contra él.
29. La certificación no puede exceder el alcance aprobado (baseline + adicionales formales).
30. Material en obrador no equivale a avance colocado.
31. Toda OC referenciable debe apuntar a líneas de cómputo/specs; no a prosa libre como única ancla.
32. Proveedor no crea elementos geométricos.
33. Precios pueden actualizarse; hechos geométricos no se actualizan por inflación.
34. Rubros agrupan; no duplican dinero del mismo m² en dos capítulos sumables.
35. Tabique vs portante debe clasificarse; indeterminado bloquea sello si el impacto es material.
36. Existente a conservar: cantidad de obra nueva 0 en ese elemento; demoliciones/reparaciones tipificadas aparte.
37. Demoliciones no son cantidades negativas silenciosas de obra nueva.
38. Todo adicional cita baseline y delta de cómputo/precio.
39. Evidencia propuesta no paga ni sella.
40. Evidencia aceptada aporta provenance; evidencia rechazada citada se retiene.
41. Confidence agregada bajo umbral implica documento cliente con disclaimer o bloqueo de sello.
42. No presentar estimado como certificación ni certificación como habilitación municipal.
43. Cielorrasos: declarar regla de medición (área de piso, desarrollo real, exclusiones).
44. Pintura de muros usa área de paramento descontando aberturas, no área de piso.
45. Solados usan área de ambiente según criterio explícito (nichos, placards, platos de ducha).
46. Cubiertas inclinadas se miden por desarrollo, no solo por planta.
47. Contrapiso, carpeta, piso y losa no se fusionan en un renglón opaco si el oficio los separa.
48. Hormigón estructural y carpetas cementicias no se comunican como el mismo concepto al cliente.
49. En steel frame, aislaciones y barreras forman parte del sistema; no son opcionales ocultas.
50. En retak/ladrillo, consumos son tipológicos propios; no hay conversión mágica entre sistemas sin pack.
51. Instalaciones tipológicas (puntos) deben declarar que son tipológicas cuando no hay plano MEP.
52. Cambiar gas por eléctrico es cambio de sistemas y de presupuesto, no un toggle cosmético.
53. HVAC incluye eléctricos y desagües de condensado asociados cuando aplica.
54. Pasantes de instalaciones que rompen impermeabilización exigen detalle/ítem; no ignorarlos.
55. Zonas no duplican áreas de ambientes salvo partición explícita.
56. Living-comedor abierto: criterio de un ambiente o dos estable en todo el proyecto.
57. Medianeras: tipificar ownership/cómputo; no asumir doble muro de ambos vecinos en el mismo presupuesto.
58. PH: distinguir unidad privada vs comunes en alcance.
59. Local comercial: zona pública vs servicio puede gobernar terminaciones y certificaciones parciales.
60. Timeline registra sellos, adicionales y certificaciones como hitos de negocio.
61. Prohibido hard-borrar historia de hechos sellados o evidencias citadas (salvo política legal explícita fuera de este handbook).
62. Toda comparación A/B de dinero muestra fecha de precios y escenario/versión.
63. Si un número no tiene provenance, no entra a documento sellado.
64. El jefe de obra puede corregir con evidencia de campo; eso crea cambio versionado, no verdad paralela.
65. El arquitecto tipifica usos y criterios; no inventa medidas sin calibración.
66. El desarrollador no introduce sinónimos nuevos de conceptos sin enmienda a este handbook.
67. Los prompts de IA deben alinear a estas reglas; un prompt no las deroga.
68. Cuando haya conflicto entre velocidad comercial y trazabilidad, gana trazabilidad en cualquier cifra que toque dinero.
69. Los supuestos (altura, desperdicio, densidades eléctricas) viven listados y versionados conceptualmente con el proyecto.
70. Un supuesto cambiado invalida proyecciones que dependen de él y exige regeneración/revisión.
71. No se certifica trabajo fuera de lista; se adicionaliza o se rechaza.
72. Retenciones, anticipos e IVA son capas comerciales: deben declararse aparte de cantidades físicas.
73. Cotizaciones de proveedor son inputs de unitario/oferta; no reemplazan cómputo.
74. El marketplace (si existe) bindea ofertas; no forkea geometría.
75. Un pack de sistema (ladrillo a steel) se aplica como cambio de escenario coherente, no pieza por pieza sin criterio.
76. La documentación cliente debe listar exclusiones frecuentes cuando están fuera de alcance.
77. Obra en etapas: cada etapa puede tener baseline propio; no mezclar certificaciones cruzadas.
78. La confianza no se maquilla promediando con ítems altos para tapar ítems bajos críticos.
79. Cualquier automatización auto-confirm solo aplica a allowlist de bajo riesgo definida por negocio; nunca dinero.
80. Si el plano y la obra difieren, manda el expediente de cambio con evidencia.
81. Este handbook prevalece sobre comentarios de PR al definir significado de términos de dominio.

### 3.1 Matriz rápida regla → eje impactado

| Regla (rango) | Presupuestos | Materiales | Costos | Cronograma |
| --- | --- | --- | --- | --- |
| 1–6 Autoridad / IA / empaque | Alto | Medio | Alto | Medio |
| 7–10 Unidades / redondeo | Alto | Alto | Alto | Bajo |
| 11–15 Muros / aberturas | Alto | Alto | Alto | Medio |
| 16–19 Alturas / húmedos | Alto | Alto | Alto | Medio |
| 20–27 Cómputo / escenarios / baseline | Alto | Alto | Alto | Alto |
| 28–35 Certificación / OC / precios | Alto | Alto | Alto | Alto |
| 36–50 Oficio constructivo | Alto | Alto | Alto | Alto |
| 51–80 Actores / calidad / gobierno | Alto | Medio | Alto | Alto |

---
## 4. Unidades y convenciones LATAM

### 4.1 Unidades físicas

| Unidad | Uso típico de negocio | Notas LATAM / Argentina |
| --- | --- | --- |
| m | Longitudes de muro, tramos, peanas | Preferir metros decimales (3,20 m), no pies |
| m² | Áreas de paramento, solado, cubierta | Descontar vanos cuando corresponde a terminaciones |
| m³ | Hormigón, rellenos, algunos aislantes | No usar m³ para pintura |
| ml | Cañerías, zócalos, encadenados, perfiles lineales | Metro lineal, no mililitro |
| kg | Acero, algunos revestimientos, insumos | Puede convertirse a barras/u al comprar |
| u | Puertas, ventanas, artefactos, puntos tipológicos | Tipología obligatoria junto a la unidad |
| cm | Espesores de muro, carpetas, bloques | Hablar 18 cm aunque se derive a m |
| % | Desperdicio, avance | No es unidad de elemento |

### 4.2 Dinero

| Concepto | Convención |
| --- | --- |
| Moneda wedge | ARS |
| Fecha de precio | Obligatoria en presupuestos emitidos |
| IVA / impuestos | Declarar si unitarios son netos o finales; no mezclar |
| Multimoneda futura | Conversión explícita; no silenciar |
| Redondeo monetario | Política de proyecto; no confundir con redondeo de obra |

### 4.3 Alturas — cuándo global vs por ambiente

| Situación | Criterio |
| --- | --- |
| Vivienda estándar / niveles regulares | Altura global por nivel (ej. 2,60 m libre) |
| Doble altura / entrepiso / altillo | Altura por ambiente o por tramo de muro |
| Local con cielo suspendido distinto | Paramento hasta cielorraso o hasta losa: declarar |
| Azotea / pretiles | Alturas específicas de pretil/baranda |
| Remodelación con cielorrasos irregulares | Override por ambiente + evidencia |

### 4.4 Espesores y tipologías frecuentes (referencia de oficio, no norma)

| Elemento | Espesores habituales de conversación | Impacto |
| --- | --- | --- |
| Tabique interior ladrillo hueco | 8–12–15–18 cm | Consumo y aislación |
| Muro exterior / portante | 18–27–30 cm (según sistema) | Estructura y costo |
| Retak | 10–15–20 cm tipológicos | Pack C |
| Steel frame | Ancho de perfil + capas | No comparar 1:1 con ladrillo |
| Carpeta | 2–4 cm | Nivelación |
| Contrapiso | 5–12 cm (variable) | Volumen |
| Losa | 8–15 cm tipológico conversacional | No es cálculo firmado |

### 4.5 Desperdicios de referencia (punto de partida, revisables)

| Familia | Orden de magnitud inicial | Comentario de jefe de obra |
| --- | --- | --- |
| Ladrillo / bloque | 5–10% | Rotura y cortes |
| Cerámicos / porcelanatos | 8–15% | Más cortes en baños chicos |
| Pintura | Según rendimiento + 5–10% | Manos en unitario o separadas |
| Cables | 5–10% | Tipológico |
| Perfiles steel | 5–8% | Recortes |
| Artefactos por u | 0% típico | Salvo stock de seguridad declarado |

Estas tablas no autorizan a la IA a inventar; autorizan a humanos a partir de un default visible.

### 4.6 Convenciones de nombre de ambientes (español AR)

| Nombre frecuente | Tipificación de dominio |
| --- | --- |
| Living / estar | Ambiente seco social |
| Comedor | Seco social (o unido a living) |
| Cocina | Húmedo / servicio |
| Lavadero | Húmedo / servicio |
| Baño / baño completo | Húmedo sanitario |
| Toilette | Húmedo sanitario reducido |
| Dormitorio / suite | Seco privado |
| Pasillo / circulación | Seco circulación |
| Balcón / terraza | Exterior o semi; tipificar cubierta |
| Local de ventas | Comercial público |
| Depósito | Servicio / carga |
| Cochera | Tipificar cubierta/descubierta |

### 4.7 Qué no se mezcla

- No sumar m² de muro con m² de piso en un total único sin etiqueta.
- No convertir steel a equivalente ladrillo para embellecer una comparativa.
- No usar global como unidad.
- No usar abreviaciones ambiguas (mt, mts²) en documentos sellados; preferir m y m².

---

## 5. Matriz de impactos (resumen)

Niveles: Alto / Medio / Bajo / Nulo. Lectura: impacto de malinterpretar o cambiar el concepto sobre cada eje.

| Concepto | Presupuestos | Materiales | Costos | Cronograma |
| --- | --- | --- | --- | --- |
| Proyecto | Alto | Medio | Alto | Alto |
| Plano | Alto | Alto | Alto | Medio |
| Versión | Alto | Alto | Alto | Medio |
| Escenario | Alto | Alto | Alto | Alto |
| Sitio | Medio | Medio | Medio | Alto |
| Edificio | Alto | Alto | Alto | Alto |
| Nivel | Alto | Alto | Alto | Alto |
| Ambiente | Alto | Alto | Alto | Alto |
| Zona | Medio | Medio | Medio | Alto |
| Muro | Alto | Alto | Alto | Alto |
| Tabique vs portante | Alto | Alto | Alto | Alto |
| Abertura | Alto | Alto | Alto | Alto |
| Puerta | Alto | Alto | Alto | Medio |
| Ventana | Alto | Alto | Alto | Alto |
| Piso | Alto | Alto | Alto | Alto |
| Carpeta | Medio | Medio | Medio | Alto |
| Contrapiso | Alto | Alto | Alto | Alto |
| Losa | Alto | Alto | Alto | Alto |
| Viga | Medio | Alto | Alto | Alto |
| Columna | Medio | Alto | Alto | Alto |
| Fundación | Alto | Alto | Alto | Alto |
| Cubierta | Alto | Alto | Alto | Alto |
| Instalación sanitaria | Alto | Alto | Alto | Alto |
| Agua fría | Alto | Alto | Alto | Alto |
| Agua caliente | Alto | Alto | Alto | Alto |
| Cloacas | Alto | Alto | Alto | Alto |
| Gas | Alto | Alto | Alto | Medio |
| Electricidad | Alto | Alto | Alto | Alto |
| HVAC | Alto | Alto | Alto | Alto |
| Material | Alto | Alto | Alto | Alto |
| Sistema constructivo | Alto | Alto | Alto | Alto |
| Ladrillo | Alto | Alto | Alto | Alto |
| Steel Frame | Alto | Alto | Alto | Alto |
| Retak | Alto | Alto | Alto | Alto |
| Hormigón | Alto | Alto | Alto | Alto |
| Revoque | Alto | Alto | Alto | Alto |
| Pintura | Alto | Medio | Medio | Alto |
| Cerámicos | Alto | Alto | Alto | Alto |
| Cantidad | Alto | Alto | Alto | Medio |
| Cómputo | Alto | Alto | Alto | Medio |
| Takeoff / Cómputo métrico | Alto | Alto | Alto | Medio |
| Presupuesto | Alto | Alto | Alto | Medio |
| Certificación | Alto | Medio | Alto | Alto |
| Orden de compra | Medio | Alto | Alto | Alto |
| Unitario | Alto | Medio | Alto | Bajo |
| Rubro | Alto | Medio | Alto | Medio |
| Desperdicio | Alto | Alto | Alto | Medio |
| Mano de obra | Alto | Nulo | Alto | Alto |
| Baseline | Alto | Alto | Alto | Alto |
| Avance de obra | Alto | Medio | Alto | Alto |
| Extras / adicionales | Alto | Alto | Alto | Alto |
| Proveedor | Medio | Alto | Alto | Alto |
| Cliente | Alto | Medio | Alto | Medio |
| Contratista | Alto | Alto | Alto | Alto |
| Subcontratista | Medio | Medio | Alto | Alto |
| Timeline | Medio | Bajo | Medio | Alto |
| Cambio | Alto | Alto | Alto | Alto |
| Evidencia | Medio | Medio | Medio | Alto |
| Confidence | Alto | Medio | Alto | Medio |
| Provenance | Alto | Medio | Alto | Bajo |
| IA | Alto | Medio | Alto | Medio |
| Escala / calibración | Alto | Alto | Alto | Medio |
| Ambientes húmedos | Alto | Alto | Alto | Alto |
| Terminación | Alto | Alto | Alto | Alto |
| Impermeabilización | Alto | Alto | Alto | Alto |
| Aislación | Medio | Alto | Medio | Medio |

### 5.1 Lectura para priorización de producto

- Si un concepto es **Alto** en Presupuestos y Costos, no se experimenta en silencio en producción.
- Si es **Alto** en Cronograma, el timeline y el avance deben mencionarlo.
- Si es **Nulo** en Materiales (mano de obra), no se forcejea un SKU.

---

## 6. Anti-definiciones (qué ARQ-IA NO es en dominio)

Estas anti-definiciones protegen el lenguaje. Si alguien dice «somos un Revit», está fuera de dominio.

| ARQ-IA NO es… | Por qué importa en dominio | Qué sí es en cambio |
| --- | --- | --- |
| Un CAD de autoría | No es el lugar donde se dibuja la arquitectura completa como herramienta primaria | Un sistema de cuantificación que parte de planos/hechos |
| Un BIM authoring completo | No coordina disciplinas IFC/Revit como promesa central | Un BIM-lite cuantitativo / twin de cómputo |
| Un ERP de construcción genérico | No reemplaza contabilidad, RRHH, stock multi-depósito completo | Conecta cómputo→dinero→compras→certificación en su lane |
| Un software de cálculo estructural firmable | No emite cálculo de H°A° legal | Estima/organiza cantidades estructurales tipificadas con disclaimers |
| Un ente de habilitación municipal / gasista / electricista matriculado | No firma habilitación | Señala necesidades y documenta evidencias |
| Un marketplace que define la obra | El precio no crea muros | Puede ofertar sobre líneas/specs |
| Un chat que inventa metros | Viola el principio D03 | Un copiloto con citas |
| Un sustituto del jefe de obra | El juicio de campo manda en hallazgos | Amplifica cómputo y memoria |
| Un sustituto del arquitecto proyectista | No produce documentación ejecutiva completa | Ayuda a tipificar y cuantificar |
| Una planilla Excel con logo | Excel no versiona hechos ni citas | Modelo versionado + proyecciones |
| Un motor de render / marketing inmobiliario | La imagen no es cantidad | Puede explicar cantidades |
| Un sistema de facility management IoT | No es twin físico sensorizado en el alcance conceptual actual | Twin cuantitativo de obra/estimación |
| Un clasificador de planes Free/Pro como ontología | Empaque ≠ dominio | Empaque limita capacidades |
| Un diccionario de marcas obligatorias | Equivalencias existen | Specs tipológicas + bindings |
| Una fuente notarial de verdad legal | No es escribano ni perito único | Expediente auditable de cuantificación |

### 6.1 Frases prohibidas en dominio (semántica)

| Frase peligrosa | Reformulación correcta |
| --- | --- |
| «La IA calculó 87,3 m² así que está» | «La proyección mide 87,3 m² con confidence X, evidencia Y, pendiente de aceptación» |
| «Revit de ARQ-IA» | «Modelo digital de obra para cuantificación» |
| «Certificación municipal automática» | «Certificación de avance contractual del expediente» |
| «ERP completo» | «Cadena cómputo–presupuesto–compra–certificación» |
| «Escenario Free» | «Escenario constructivo; el plan Free limita cuántos podés usar» |

---

## 7. Errores de dominio frecuentes (catálogo)

Errores cruzados que corrompen estimados.

| Error | Síntoma | Causa | Corrección |
| --- | --- | --- | --- |
| E01 Doble muro entre ambientes | Living y dormitorio traen cada uno el mismo tabique. | Pensar el muro como propiedad del ambiente. | Identidad única de muro; terminaciones por cara si hace falta. |
| E02 Escala asumida | Totales redondos sospechosos; aberturas raras. | Asumir 1:50/1:100 por costumbre. | Calibrar; bajar confidence; bloquear sello. |
| E03 Abertura no descontada | Revoque/pintura inflados. | Medir paramento bruto y olvidar vanos. | Aplicar regla de descuento de aberturas. |
| E04 Abertura descontada dos veces | Terminaciones cortas. | Descontar en muro y otra vez en ambiente. | Una sola regla de descuento por paramento. |
| E05 Piso = muro | m² de pintura tomados de solado. | Confundir áreas. | Unidad y superficie tipificadas por elemento. |
| E06 Contrapiso = platea | Fundación mal comunicada. | Todo lo cementicio es lo mismo. | Separar fundación / losa / contrapiso / carpeta / piso. |
| E07 Baño como dormitorio | Faltan impermeabilización y densidades sanitarias. | Solo cambia el nombre. | Tipificar ambiente húmedo. |
| E08 Escenario clon-proyecto | Imposible comparar A/B/C. | Crear un proyecto por sistema. | Usar escenarios sobre base compartida. |
| E09 Promedio de escenarios | Número único mentiroso. | Querer una sola cifra equilibrada. | Presentar tabla comparativa; promover uno a baseline. |
| E10 Sello editado | Pérdida de confianza contractual. | Era un ajuste chico. | Nueva versión o adicional. |
| E11 Certificar > baseline | Pago de trabajo no aprobado. | Presión de caja. | Adicional formal o rechazo. |
| E12 OC sin líneas | Compras fantasma. | WhatsApp al corralón. | OC ancla a cómputo. |
| E13 IA inventa MEP | Puntos eléctricos inventados como certeza. | Completar vacíos con LLM. | Tipológico declarado + baja confidence o plano MEP. |
| E14 Desperdicio escondido | No se puede auditar margen. | Meter merma en unitario opaco. | Desperdicio visible. |
| E15 Unitarios de otro mes | Presupuesto no ejecutable. | Reusar PDF viejo. | Fecha de precios + actualización versionada. |
| E16 Steel con consumo ladrillo | Comparativa falsa. | Factor mágico de conversión. | Pack de sistema / takeoff propio. |
| E17 Proveedor redefine geometría | Muros según fábrica. | Delegar medición sin expediente. | Medición vuelve como evidencia/cambio. |
| E18 Avance = compra | Certificación inflada. | Material en obrador como porcentaje. | Separar logística de colocado. |
| E19 Zona duplica área | m² de piso duplicados. | Partir ambiente en zonas sumables. | Etiquetar o particionar con regla clara. |
| E20 Cubierta en planta | Falta chapa/teja. | Medir solo proyección horizontal. | Desarrollo por pendiente. |
| E21 Tabique portante indeterminado | Unitario incorrecto y riesgo. | No clasificar rol. | Clasificar o bloquear sello. |
| E22 Extras como desperdicio | Corrupción ética/comercial. | Esconder cambios de alcance. | Adicional con delta. |
| E23 Empaque como ontología | Muro Enterprise. | Mezclar billing con dominio. | Separar límites de plan de conceptos. |
| E24 Sin provenance | No se puede defender el número. | Export/import lavan origen. | Citar elemento/evidencia/versión. |
| E25 Confundir certificación contractual con habilitación | Expectativa legal imposible. | Palabra certificación ambigua. | Calificar siempre: avance de obra / no municipal. |

### 7.1 Patrones de corrupción (resumen)

1. **Amnesia:** editar el pasado sellado.
2. **Doble conteo:** identidades duplicadas.
3. **Categoría cruzada:** mezclar capas (losa/piso, cloacal/pluvial).
4. **Autoridad invertida:** IA/proveedor/PDF mandan sobre MDO.
5. **Cosmética de incertidumbre:** decimales, promedios, desperdicios tapahuecos.

---

## 8. Glosario rápido A–Z

Una línea por término. Para profundidad, ir al catálogo §2.

| Término | Definición en una línea |
| --- | --- |
| Abertura | Vano hospedado (puerta/ventana/otro) que descuenta terminaciones de muro. |
| Adicional / Extra | Cambio de alcance o spec respecto del baseline con delta de cantidad/dinero. |
| Agua caliente (ACS) | Subistema de generación y distribución de agua caliente sanitaria. |
| Agua fría | Subistema de alimentación y distribución de agua fría a puntos de consumo. |
| Aislación | Capas/materiales de control térmico y/o acústico. |
| Ambiente | Espacio tipificado por uso con área y reglas de terminación/instalaciones. |
| Ambiente húmedo | Ambiente con reglas reforzadas de agua, desagüe e impermeabilización. |
| ARS | Peso argentino; moneda de referencia del wedge. |
| Avance de obra | Progreso físico/contractual medido contra baseline. |
| Baseline | Alcance/versión aprobada de referencia para extras y certificaciones. |
| Binding | Asociación de material/oferta a elemento o línea en un escenario. |
| Calibración | Acto de fijar escala real del plano/medida. |
| Cambio | Modificación documentada que versiona hechos/alcance. |
| Cantidad | Magnitud con unidad (neta o comprable) antes del precio. |
| Cantidad comprable | Cantidad neta ajustada por desperdicio/redondeo de compra. |
| Cantidad neta | Medición/tipificación sin merma de compra. |
| Carpeta | Capa fina de nivelación bajo el solado. |
| Certificación | Reconocimiento económico de avance contra lo aprobado. |
| Cerámicos | Revestimientos en piezas para piso/pared con juntas. |
| Cliente | Comitente/demandante que aprueba dinero y baselines. |
| Cloacas | Red de desagües cloacales/servidos (distinta de pluvial). |
| Columna | Elemento estructural vertical. |
| Confidence | Grado de certeza comunicable de un hecho o documento. |
| Contrapiso | Capa gruesa de formación de solados. |
| Contratista | Ejecutor principal de obra que certifica y coordina. |
| Cubierta | Sistema de techo: estructura + impermeabilización + terminación. |
| Cómputo | Proyección ordenada de cantidades trazables a hechos. |
| Cómputo métrico | Sinónimo operativo de takeoff cuantitativo. |
| Desperdicio | Factor de merma de material hacia cantidad comprable. |
| Edificio | Volumen construible tipificado dentro del sitio. |
| Electricidad | Sistema de distribución eléctrica y puntos. |
| Escala | Relación dibujo↔metros; condición de medida. |
| Escenario | Alternativa constructiva/spec sobre base comparable. |
| Evidencia | Soporte perceptivo/documental; no hecho final solo. |
| Free/Pro/Enterprise | Empaque comercial de capacidades; no ontología. |
| Fundación | Apoyo al suelo del edificio (platea/zapatas/etc.). |
| Gas | Sistema de suministro de gas y artefactos asociados. |
| Hecho de obra | Atributo del MDO que afecta identidad, geometría medida, pertenencia o sello. |
| Hormigón | Material/sistema cementicio estructural (H°/H°A°) y paquetes asociados. |
| HVAC | Climatización y/o ventilación mecánica. |
| IA | Asistente que propone/explica con citas; no inventa cantidades ni firma dinero. |
| Impermeabilización | Barreras y detalles contra agua. |
| Instalación sanitaria | Paquete/sistema de aguas y desagües. |
| Ladrillo | Sistema/material de mampostería tradicional; escenario A canónico. |
| Losa | Elemento estructural horizontal de entrepiso/cubierta. |
| Mano de obra | Componente de trabajo humano/cuadrilla del renglón. |
| Material | Spec comprable bindeable a elementos/líneas. |
| MDO | Modelo Digital de la Obra; SoT conceptual de hechos. |
| Medianera | Muro de límite predial/unidad con reglas especiales de ownership. |
| ml | Metro lineal. |
| Muro | Elemento vertical de cerramiento/división, portante o no. |
| Nivel | Planta/piso del edificio. |
| Orden de compra (OC) | Pedido a proveedor anclado a líneas/specs. |
| Percepción | Capa que detecta/propone desde planos u obra; no SoT. |
| Piso | Solado de terminación horizontal. |
| Plano | Documento gráfico de referencia; no el modelo. |
| Portante | Rol estructural de muro/elemento que carga. |
| Presupuesto | Documento comercial cantidad×unitario sobre versión/escenario. |
| Proveedor | Suministrador de materiales/servicios/ofertas. |
| Provenance | Pedigrí de origen de un número/hecho. |
| Proyecto | Expediente de obra digital y comercial. |
| Puerta | Abertura de paso con hoja/marco/herrajes. |
| Retak | Sistema de bloques celulares; escenario C canónico. |
| Revoque | Terminación cementicia de paramentos. |
| Rubro | Capítulo comercial del presupuesto. |
| Sistema constructivo | Lógica de construcción con paquetes compatibles. |
| Sitio | Predio/lote de implantación. |
| Steel Frame | Sistema liviano de perfiles; escenario B canónico. |
| Subcontratista | Ejecutor especializado de un paquete/rubro. |
| Tabique | Muro no portante de división. |
| Takeoff | Extracción de cantidades desde hechos/plano interpretado. |
| Terminación | Acabado visible/usable de obra fina. |
| Timeline | Historia de hitos de negocio del proyecto. |
| Unitario | Precio por unidad de medida con fecha/moneda. |
| Ventana | Abertura de iluminación/ventilación con carpintería/vidrio. |
| Versión | Instantánea versionada de hechos; sellable. |
| Viga | Elemento estructural lineal que salva luces. |
| Zona | Agrupación lógica operativa; no siempre un ambiente. |

---

## 9. Criterios de conformidad

Cómo se chequea una feature, PR, prompt o decisión de producto contra este handbook (proceso de negocio, no checklist de código).

### 9.1 Preguntas obligatorias antes de adoptar una feature

1. ¿Qué conceptos de §2 toca por nombre?
2. ¿Introduce un sinónimo nuevo? Si sí → enmienda Apéndice E antes o junto.
3. ¿Quién es autoridad del hecho: MDO, percepción, humano, libro de precios?
4. ¿La IA puede escribir cantidades o dinero? Si puede → no conforme.
5. ¿Respeta inmutabilidad de sellos y baseline?
6. ¿Evita doble conteo y respeta unidades LATAM?
7. ¿Confunde empaque Free/Pro/Enterprise con ontología?
8. ¿Todo número cliente-facing obliga confidence/provenance o disclaimer?
9. ¿Las OC/certificaciones anclan a cómputo/baseline?
10. ¿El lenguaje UI/PDF usa los términos de §8 consistentemente?

### 9.2 Estados de conformidad

| Estado | Significado | Acción |
| --- | --- | --- |
| Conforme | Alineado al handbook | Seguir |
| Conforme con supuesto | Alineado si se documenta supuesto visible | Listar supuesto en proyecto |
| No conforme menor | Ambigüedad de wording sin corrupción de dinero | Corregir copy/docs |
| No conforme mayor | Puede corromper cantidades/dinero/sellos | Bloquear release conceptual hasta enmienda o rediseño |
| Fuera de dominio | Es CAD/ERP/cálculo legal/etc. | Rechazar como ARQ-IA core |

### 9.3 Ritual de review de dominio (humanos + AIs)

1. Leer el diff de nombres de negocio (UI, mensajes, PDFs, prompts), no solo de implementación.
2. Marcar cada nombre contra §2/§8.
3. Ejecutar las 10 preguntas de §9.1.
4. Si hay impacto Alto en matriz §5, exigir ejemplo LATAM (vivienda/PH/local) en la descripción de la feature.
5. Si hay conflicto con RFC, recordar: significado = handbook; construcción = RFC/Architecture.
6. Registrar decisión (conforme / enmienda / rechazo) en el PR o ADR de producto.

### 9.4 Conformidad de prompts y agentes

- El agente debe negarse a inventar cantidades.
- El agente debe citar versión/escenario/línea cuando hable de dinero.
- El agente debe usar español de obra AR/LATAM alineado al glosario.
- El agente no debe presentarse como certificador legal ni como calculista estructural.

### 9.5 Definición de «listo para cliente»

Un entregable numérico está listo para cliente solo si:

1. Está anclado a versión/escenario.
2. Tiene cómputo trazable.
3. Supera umbral de confidence o declara rangos/disclaimers.
4. Usa unitarios con fecha/moneda.
5. Lista exclusiones relevantes.
6. Fue aceptado por rol humano habilitado.

---

## Apéndice A — Tipologías de obra de referencia

Tipologías para pensar ejemplos y supuestos. No son taxonomía cerrada universal.

| Tipología | Rasgos de dominio | Riesgos típicos de cómputo | Escenarios frecuentes |
| --- | --- | --- | --- |
| Vivienda unifamiliar PB | Un nivel, húmedos pocos, cubierta simple o azotea | Escala de plano municipal; altura asumida | Ladrillo / steel / retak |
| Vivienda PB+1 | Losas, escalera, instalaciones verticales | Olvidar entrepiso y dobles alturas | HA + mampostería; híbridos |
| PH / multifamiliar chico | Unidades + comunes; acústica; medianeras internas | Mezclar comunes y privadas; bajadas | Muros + losa; packs por unidad |
| Local comercial PB | Diáfano, frente, depósito, toilette | Frente vidriado; fuerza eléctrica; marca | Terminaciones y MEP dominantes |
| Gastronomía | Cocina pesada, extracción, grasas | Subestimar MEP e impermeabilización | Adicionales HVAC/extracción |
| Remodelación / ampliación | Existente + nuevo | No tipificar existente; demoliciones | Escenario estado actual vs proyectado |
| Quincho / complemento | Segundo edificio en sitio | Fundaciones distintas; instalaciones largas | Sistemas livianos |
| Oficina pequeña | Open space + privados + toilette | Densidad eléctrica/datos | Drywall + cielo suspendido |

### A.1 Perfiles de usuario de oficio

| Perfil | Qué mira primero | Qué no tolera |
| --- | --- | --- |
| Arquitecto proyectista | Ambientes, aberturas, tipologías | Que el cómputo ignore el criterio de diseño |
| Jefe de obra | Muros, desperdicios, secuencia, certificables | Números sin provenance ni comprables |
| Sanitarista / electricista | Puntos, trazados, húmedos | Inventos de chat sin plano |
| Comitente | Totales, exclusiones, escenarios | Letra chica y cambios silenciosos |
| Proveedor de aberturas | Vanos, cantidades u, lead time | Medidas inestables post-OC |

---

## Apéndice B — Checklist jefe de obra al revisar un cómputo

Usar antes de comprar, certificar o pelear un adicional.

### B.1 Identidad y alcance

- [ ] ¿Está claro proyecto, versión y escenario head?
- [ ] ¿Hay baseline vigente si esto es obra en curso?
- [ ] ¿Se distingue obra nueva / existente / demolición?
- [ ] ¿PH/local: están separados privados vs comunes / público vs servicio?

### B.2 Medida

- [ ] ¿Escala/calibración aceptable y documentada?
- [ ] ¿Alturas globales o por ambiente coherentes con la realidad?
- [ ] ¿Muros sin doble conteo?
- [ ] ¿Aberturas descontadas una sola vez en terminaciones?
- [ ] ¿Cubierta medida por desarrollo si hay pendiente?
- [ ] ¿Cielorrasos con regla explícita?

### B.3 Oficio

- [ ] ¿Tabique vs portante clasificado en muros críticos?
- [ ] ¿Contrapiso / carpeta / piso / losa separados?
- [ ] ¿Húmedos con impermeabilización y desagües?
- [ ] ¿Cloacal distinto de pluvial?
- [ ] ¿Gas/eléctrico coherente con escenario de ACS/cocina?
- [ ] ¿HVAC con puntos eléctricos y condensados si aplica?

### B.4 Compra y dinero

- [ ] ¿Desperdicios visibles y razonables por familia?
- [ ] ¿Unitarios con fecha/moneda?
- [ ] ¿Rubros sin doble asignación?
- [ ] ¿Confidence insuficiente marcada (no maquillada)?
- [ ] ¿OC posibles anclables a líneas?
- [ ] ¿Exclusiones dichas al cliente?

### B.5 Obra en curso

- [ ] ¿Avance colocado distinto de material en obrador?
- [ ] ¿Certificación ≤ baseline + adicionales?
- [ ] ¿Extras con delta y aprobación?
- [ ] ¿Evidencia de campo cargada donde hay disputa?

### B.6 Señal de alarma inmediata

| Señal | Acción |
| --- | --- |
| Totales demasiado redondos sin tipología | Revisar escala y redondeos |
| Pintura ≈ piso en m² | Revisar paramentos |
| Escenario B más barato porque sí sin pack | Revisar bindings |
| Confidence alta con plano feo | Desconfiar; pedir calibración |
| Adicional escondido en desperdicio | Separar adicional |

---

## Apéndice C — Checklist arquitecto al pintar/interpretar plano

Protocolo de negocio de interpretación. Habla de roles de color/categoría conceptuales, no de valores HSV ni de implementación de visión.

### C.1 Antes de pintar/interpretar

- [ ] Identificar hoja (PB, PA, techos, instalaciones) y su escala.
- [ ] Verificar cota o escala gráfica utilizable.
- [ ] Acordar altura de nivel / excepciones.
- [ ] Listar ambientes y su tipificación (húmedo/seco/exterior/comercial).
- [ ] Declarar si se mide muro por eje, cara interior o criterio mixto del proyecto.

### C.2 Categorías conceptuales de pintura/interpretación

| Categoría conceptual | Qué significa en dominio | No confundir con |
| --- | --- | --- |
| Muro portante / estructural | Rol de carga | Grosor dibujado porque quedó lindo |
| Tabique / división | No portante | Material final (puede ser ladrillo o drywall) |
| Abertura puerta | Vano de paso | Mueble de placard dibujado como vano |
| Abertura ventana | Vano de luz/aire | Paño decorativo sin vano real |
| Ambiente seco | Terminaciones standard | Habitación sin uso |
| Ambiente húmedo | Reglas de agua | Patio descubierto |
| Exterior / semicubierto | Exposición climática | Interior con mucho vidrio |
| Circulación | Pasillos/halls | Local de ventas |
| Fuera de alcance | No se cuantifica | Zona gris sin marcar |

### C.3 Durante la interpretación

- [ ] Un vano = una abertura hospedada en un muro, no un hueco suelto.
- [ ] Medianeras tipificadas.
- [ ] Dobles alturas marcadas (no pintar como muro de altura simple).
- [ ] Escaleras: hueco de losa considerado.
- [ ] Locales diáfanos: no inventar tabiques fantasma para que cierre el Excel.
- [ ] Si hay duda de rol portante: marcar indeterminado, no adivinar con confianza alta.

### C.4 Después

- [ ] Revisar lista de ambientes vs nombres del plano.
- [ ] Revisar conteo de puertas/ventanas contra planilla rápida.
- [ ] Declarar supuestos en el expediente.
- [ ] Pedir revisión de jefe de obra en ítems Alto impacto (§5).
- [ ] No emitir a cliente si calibración o confidence fallan gates.

### C.5 Anti-patrones de interpretación

1. Pintar bonito sin categoría de dominio.
2. Usar una sola categoría para muros y aberturas.
3. Interpretar instalaciones como decoración de línea.
4. Cambiar criterio de medición a mitad de proyecto.
5. Dejar que la IA complete vanos no evidentes como certeza.

---

## Apéndice D — Escenarios constructivos canónicos

Significado de negocio de los escenarios A/B/C (+ HA como eje estructural). No es guía de cálculo ni de marca.

### D.1 Escenario A — Ladrillo / mampostería tradicional

| Dimensión | Significado de negocio |
| --- | --- |
| Qué compara | Alternativa familiar para cliente y gremios argentinos |
| Qué cambia vs base | Bindings de muro a ladrillo/bloque + morteros + revoques típicos |
| Qué no cambia | Geometría de vanos y ambientes, salvo espesores declarados |
| Implicancia de cómputo | m² de mampostería, consumos, revoques, encadenados |
| Implicancia de cronograma | Cuadrilla de albañilería; tiempos húmedos de mortero/revoque |
| Riesgo típico | Doble conteo y espesores mal tipificados |

### D.2 Escenario B — Steel Frame

| Dimensión | Significado de negocio |
| --- | --- |
| Qué compara | Alternativa industrializada más seca |
| Qué cambia | Paquete de perfiles, placas, aislaciones, barreras, anclajes |
| Qué no cambia | Layout de ambientes y aberturas base (si no hay rediseño) |
| Implicancia de cómputo | No usar ladrillos; medir capas del sistema |
| Implicancia de cronograma | Otra ruta crítica; más dependencia de provisión industrial |
| Riesgo típico | Olvidar aislación/barreras; convertir con factor mágico desde A |

### D.3 Escenario C — Retak / bloque celular

| Dimensión | Significado de negocio |
| --- | --- |
| Qué compara | Mampostería liviana alternativa al ladrillo común/hueco |
| Qué cambia | Bloques + juntas/adhesivos + detalles de fijación/terminación |
| Qué no cambia | Lógica de ambientes/aberturas base |
| Implicancia de cómputo | Consumos propios; no copiar A |
| Implicancia de cronograma | Ritmo distinto; coordinación de rozas/instalaciones |
| Riesgo típico | Unitarios de ladrillo aplicados a retak |

### D.4 Eje HA — Hormigón armado (estructural)

| Dimensión | Significado de negocio |
| --- | --- |
| Qué es | Paquete estructural (fundación/losa/viga/columna) frecuente en LATAM |
| Relación con A/B/C | Puede convivir (p. ej. losa HA + muros A/B/C) |
| Qué no es | Cálculo firmado ni detalle de armaduras ejecutivo completo |
| Implicancia | m³/kg/encofrado tipológicos con disclaimer |
| Riesgo típico | Mezclar HA estructural con carpetas en un solo renglón |

### D.5 Reglas de comparación canónica

1. Misma base geométrica o divergencia declarada.
2. Misma lista de ambientes y aberturas (salvo adicional explícito).
3. Precios con misma fecha o fecha mostrada por escenario.
4. Mostrar deltas de materiales, mano de obra y plazo, no solo total.
5. Un solo escenario se promueve a baseline de contrato.
6. Empaque comercial puede limitar N escenarios visibles; la definición A/B/C permanece.

### D.6 Híbridos

Los híbridos son legítimos (fachada ladrillo + tabiques steel; retak interior + medianera tradicional). Deben declararse por elemento/rol. Un híbrido no es un promedio de escenarios; es un head con bindings mixtos coherentes.

---

## Apéndice E — Approval / change control de este handbook

### E.1 Estado

| Campo | Valor |
| --- | --- |
| Documento | ARQ-IA — DOMAIN HANDBOOK |
| Estado | Official business reference |
| Fecha de corte | 2026-08-02 |
| Idioma | Español |
| Naturaleza | Negocio / semántica; sin implementación |

### E.2 Quién puede enmendar

| Rol | Facultad |
| --- | --- |
| Domain Owner Construction | Propone y valida semántica de oficio |
| CTO / Tech Lead | Valida impacto en arquitectura de verdad (MDO) y no contradicción con principios |
| Product | Valida lenguaje cliente y empaque vs ontología |
| Ingeniería | Señala ambigüedades; no redefine términos en silencio en código |

### E.3 Proceso de enmienda

1. Detectar hueco o conflicto de significado.
2. Redactar propuesta: término, definición, reglas, impacto 4 ejes, ejemplo LATAM.
3. Verificar que no viola principios D01–D25.
4. Actualizar §2/§3/§8/§5 según corresponda en un único cambio coherente.
5. Aprobación Domain Owner + CTO (y Product si toca lenguaje cliente).
6. Comunicar a builders: el significado viejo queda deprecated con fecha.

### E.4 Qué no es una enmienda válida

- Cambiar un término porque el front ya lo llamó distinto sin aprobación.
- Introducir APIs, tablas de base de datos o clases en este archivo.
- Relajar D03/D04 para demos.
- Convertir Free/Pro/Enterprise en tipos de muro/presupuesto.

### E.5 Relación con otros documentos oficiales

| Documento | Relación |
| --- | --- |
| Master Plan | Visión y principios de producto; este handbook semántiza el lenguaje de obra |
| Architecture | Cómo se construye el sistema; no manda sobre significado de muro/presupuesto |
| Engineering Roadmap | Secuencia de entrega |
| RFC-E01 | Fundaciones de plataforma; no redefine oficio |
| RFC-E02-MDO | Contrato del MDO; operacionaliza hechos; cede significado a este handbook en conflictos semánticos |

### E.6 Declaración de cierre

Este Domain Handbook es la biblia semántica de ARQ-IA para builders humanos y AIs. El MDO es la fuente de verdad conceptual de hechos de obra. La percepción propone. La IA no inventa cantidades. El humano decide el dinero. Free/Pro/Enterprise empaqueta capacidades; no crea ontología.

Fin del ARQ-IA — DOMAIN HANDBOOK.

