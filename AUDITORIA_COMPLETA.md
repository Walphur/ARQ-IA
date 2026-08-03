# AUDITORÍA TÉCNICA COMPLETA — ARQ-IA

**Proyecto:** ARQ-IA (SaaS de cómputo de obra a partir de planos coloreados)  
**Dominio de producción (según configuración):** `https://arq-ia.pro` / API `https://api.arq-ia.pro`  
**Fecha de auditoría:** 2026-08-02  
**Alcance:** código presente en el repositorio en la rama `main` al momento del análisis  
**Método:** inspección estática del código fuente; **no se modificó el proyecto** (salvo la creación de este documento)  
**Principio:** todo lo afirmado se basa en archivos existentes; si algo no existe, se declara explícitamente  

---

## Índice

1. [Resumen general](#1-resumen-general)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Flujo completo del sistema](#3-flujo-completo-del-sistema)
4. [Frontend](#4-frontend)
5. [Backend](#5-backend)
6. [API](#6-api)
7. [Base de datos](#7-base-de-datos)
8. [Subida de planos](#8-subida-de-planos)
9. [Preprocesamiento de imagen](#9-preprocesamiento-de-imagen)
10. [Detección de escala](#10-detección-de-escala)
11. [OCR](#11-ocr)
12. [Detección de colores](#12-detección-de-colores)
13. [Paleta de colores](#13-paleta-de-colores)
14. [Motor de visión](#14-motor-de-visión)
15. [Geometría](#15-geometría)
16. [Detección de muros](#16-detección-de-muros)
17. [Detección de pisos](#17-detección-de-pisos)
18. [Detección de aberturas](#18-detección-de-aberturas)
19. [Instalaciones](#19-instalaciones)
20. [Losas / techos](#20-losas--techos)
21. [Motor de materiales](#21-motor-de-materiales)
22. [IA](#22-ia)
23. [Exportaciones](#23-exportaciones)
24. [Configuraciones](#24-configuraciones)
25. [Dependencias](#25-dependencias)
26. [Rendimiento](#26-rendimiento)
27. [Seguridad](#27-seguridad)
28. [Limitaciones](#28-limitaciones)
29. [Posibles errores](#29-posibles-errores)
30. [Precisión](#30-precisión)
31. [Casos de uso](#31-casos-de-uso)
32. [Roadmap técnico](#32-roadmap-técnico)
33. [Conclusión](#33-conclusión)

---

## 1. Resumen general

### 1.1 Objetivo del proyecto

ARQ-IA es una aplicación web multi-tenant pensada para **estudios de arquitectura / cómputo de obra**. El usuario sube un **plano en imagen** (PNG/JPG/WebP) previamente coloreado según una paleta fija; el backend aplica **visión por computadora clásica** (máscaras HSV + morfología + thinning + contornos) y **OCR (Tesseract)** para:

1. Calibrar la escala a partir de una **línea verde** y un número de cota.
2. Cuantificar elementos (muros, pisos, aberturas, cañerías, electricidad, techos, lotes).
3. Convertir cantidades en un **presupuesto estimado en ARS** (mano de obra + materiales) usando una tabla de precios.
4. Guardar historial por **obra**, exportar CSV/PDF, invitar equipo y monetizar con **Plan Pro (Mercado Pago)**.

### 1.2 Problema que resuelve

Automatiza un cómputo preliminar a partir de un plano “pintado”, evitando medir a mano cada muro/piso/caño. **No** interpreta planos CAD nativos ni dibujos sin codificar por color.

### 1.3 Flujo general (vista de pájaro)

```
Usuario (navegador)
    │
    ├─ Auth / Demo ──► Frontend React (CRA, App.js monolítico)
    │                      │
    │                      ▼  HTTPS / axios
    │                 Backend FastAPI (main.py)
    │                      │
    │         ┌────────────┼────────────┐
    │         ▼            ▼            ▼
    │    Postgres     motor_ia.py    Mercado Pago / Resend
    │    (SQLAlchemy)  OpenCV+OCR     (billing / email)
    │         │            │
    │         ▼            ▼
    │    Historial     Items + total + imagen auditoría (base64)
    └──────────────────────┘
```

### 1.4 Tecnologías utilizadas

| Capa | Tecnología | Evidencia |
|------|------------|-----------|
| Frontend | React 19, CRA (`react-scripts` 5), axios | `frontend/package.json` |
| Estilos | CSS propio (`App.css`), fuentes Inter + Bebas Neue | `App.css` |
| Backend | FastAPI 0.115.6, Uvicorn | `requirements.txt`, `Dockerfile` |
| Visión | OpenCV contrib headless 4.10 (`cv2.ximgproc.thinning`) | `motor_ia.py` |
| OCR | pytesseract + binario Tesseract (idioma spa instalado en Docker) | `Dockerfile`, `motor_ia.py` |
| DB | SQLAlchemy 2 + SQLite (dev) / PostgreSQL+psycopg (prod) | `main.py`, `render.yaml` |
| PDF | fpdf2 + DejaVu | `presupuesto_pdf.py`, `fonts/` |
| Billing | Mercado Pago Preapproval (HTTP API) | `billing_mp.py` |
| Email | Resend API | `email_service.py` |
| Deploy | Render (Docker API + static frontend + Postgres) | `render.yaml` |

### 1.5 Arquitectura general

- **Monolito backend** en un solo proceso FastAPI (`main.py` ~1383 líneas + módulos satélite).
- **Monolito frontend** en un solo componente raíz (`App.js` ~2558 líneas).
- **No hay** microservicios, colas (Celery/Redis), storage S3, workers asíncronos de visión, ni capa de IA generativa/neuronal.
- Multi-tenancy por **Studio** (estudio) → Users → Projects (obras) → Processes (análisis).

### 1.6 Componentes por dominio

| Dominio | ¿Existe? | Dónde |
|---------|----------|-------|
| Frontend SPA | Sí | `frontend/` |
| Backend API | Sí | `backend/` |
| Visión / cuantificación | Sí | `backend/motor_ia.py` |
| OCR | Sí (Tesseract) | `motor_ia.py` + apt en Docker |
| IA (LLM / YOLO / SAM / TF) | **No** | No aparece en deps ni imports |
| Base de datos | Sí | modelos en `main.py` |
| Exportaciones | Sí CSV + PDF | endpoints + `presupuesto_pdf.py` |
| Servicios externos | Sí | Google Sheets CSV precios, Mercado Pago, Resend |

---

## 2. Estructura del proyecto

### 2.1 Árbol relevante (excluye `node_modules` y `.git`)

```
/
├── AUDITORIA_COMPLETA.md          ← este documento
├── render.yaml                    ← Blueprint Render
├── package.json / package-lock.json  (raíz; no es el frontend CRA)
├── .gitignore / .gitattributes
├── .vscode/settings.json
├── backend/
│   ├── main.py                    ← API + modelos + auth + orquestación
│   ├── motor_ia.py                ← motor de visión y presupuesto
│   ├── billing_mp.py              ← Mercado Pago
│   ├── email_service.py           ← Resend
│   ├── presupuesto_pdf.py         ← PDF
│   ├── precios.json               ← LEGACY: NO es leído por el código Python
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── fonts/DejaVuSans*.ttf
│   ├── scripts/generar_plano_muestra.py
│   └── tests/                     ← pytest unitario parcial
└── frontend/
    ├── package.json
    ├── .env.example
    ├── public/                    ← assets estáticos + planos muestra
    └── src/
        ├── App.js                 ← UI completa
        ├── App.css
        ├── index.js
        └── ...
```

### 2.2 Carpetas solicitadas que **NO existen**

Las siguientes rutas **no están** en el repositorio:

| Carpeta pedida | Estado |
|----------------|--------|
| `src/` (raíz) | No existe (sí `frontend/src/`) |
| `vision/` | No existe (lógica en `motor_ia.py`) |
| `ai/` | No existe |
| `ocr/` | No existe (OCR embebido en `motor_ia.py`) |
| `workers/` | No existe |

### 2.3 Carpeta `backend/` — propósito y archivos

**Propósito:** API HTTP, persistencia, auth, billing, email, motor de cómputo.

| Archivo | Responsabilidad | Interacciones |
|---------|-----------------|---------------|
| `main.py` | App FastAPI, CORS, modelos ORM, endpoints, cuotas, RBAC, startup migrations | Importa `motor_ia`, `billing_mp`, `email_service`, `presupuesto_pdf` |
| `motor_ia.py` | Decodifica imagen, HSV, OCR escala, cuantifica por módulo, arma items y total | Usado solo desde `main.py` (y tests) |
| `billing_mp.py` | Checkout/cancel/webhook MP | Usado desde `main.py` |
| `email_service.py` | Envío invite/reset | Usado desde `main.py` |
| `presupuesto_pdf.py` | Genera bytes PDF | Usado desde endpoint export PDF |
| `precios.json` | Estructura antigua de precios por rubro | **No referenciado** por ningún `.py` |
| `Dockerfile` | Imagen Python 3.12 + Tesseract spa | Deploy Render |
| `requirements.txt` | Dependencias pinneadas | Build Docker / local |
| `scripts/generar_plano_muestra.py` | Genera PNG sintético de laboratorio | Escritura a `frontend/public/plano-sintetico-lab.png` |
| `tests/*.py` | Pruebas unitarias parciales | pytest |
| `fonts/` | TTF DejaVu para PDF Unicode | `presupuesto_pdf.py` |

### 2.4 Carpeta `frontend/` — propósito y archivos

**Propósito:** SPA de usuario (auth, demo, workspace).

| Archivo / carpeta | Responsabilidad |
|-------------------|-----------------|
| `src/App.js` | Toda la UI: auth, demo, obras, módulos, escala, historial, billing, invites |
| `src/App.css` | Design system oscuro + dorado |
| `src/index.js` | `createRoot` + StrictMode |
| `src/banner-fondo.jpg` | Fondo de headers |
| `public/plano-muestra-*.png` | Planos de referencia por módulo |
| `public/plantilla-paleta-arq-ia.svg` | Paleta descargable |
| `public/icons/modulo-*.svg` | Íconos de módulos |
| `public/logo.png`, `favicon.png` | Branding |
| `plano-muestra.png`, `plano-sintetico-lab.png` | Presentes en disco; **no referenciados** en `App.js` |

### 2.5 `render.yaml`

Define tres recursos:

1. **Web Docker** `arq-ia-api` → `backend/`, health `/health`, env de DB/MP/Resend/límites.
2. **Static** `arq-ia-web` → build CRA, `REACT_APP_API_URL=https://api.arq-ia.pro`.
3. **Database** `arq-ia-db` plan starter.

---

## 3. Flujo completo del sistema

### 3.1 Usuario abre la aplicación

1. El navegador carga el static de Render (`arq-ia.pro`).
2. React monta `App`.
3. Lee `localStorage.arqia_token`.
4. Resuelve candidatos de API (`buildApiCandidates`) y hace probe `GET /health`.
5. Consulta públicos: `GET /precios-info`, `GET /billing/info`.
6. Si hay `?invite=` o `?reset=` en la URL, entra a flujos especiales.

### 3.2 Autenticación (estudio)

1. Login `POST /auth/login` o register `POST /auth/register`.
2. Backend valida password (PBKDF2), emite token HMAC (14 días).
3. Frontend guarda token y llama `GET /me`, `GET /projects`.

### 3.3 Modo demo (sin cuenta)

1. “Probar sin cuenta” → `demoMode=true`.
2. Upload → `POST /calcular` (público, rate-limit por IP).
3. Resultados solo en memoria (`demoRuns`, máx. 6). **No** se persisten ni exportan.

### 3.4 Creación de obra y subida de plano (workspace)

```
Seleccionar / crear obra
        │
        ▼
Elegir módulo (muros|agua|luz|techo|terreno)
        │
        ├─ Si módulo PRO y plan != active → UI bloquea / API 402
        │
        ▼
Validar metros de escala en formulario (frontend)
        │
        ▼
POST /projects/{id}/calcular  (multipart)
        │
        ▼
validate_upload (content-type + tamaño)
ensure_usage_available (usage_events del mes)
ensure_module_allowed
        │
        ▼
procesar_plano_ia(bytes, referencia, sistema, tipo, altura, forzar?)
        │
        ├─ decode BGR
        ├─ HSV
        ├─ máscara verde → thinning → px_v
        ├─ OCR número junto al verde (o manual / forzado)
        ├─ escala = metros / px_v  (fallback 0.02)
        ├─ rama según tipo_plano
        ├─ items + total + imagen auditoría PNG base64
        │
        ▼
Persistir Process + UsageEvent
Responder serialize_process
        │
        ▼
Frontend refresca historial / KPIs / cupo
```

### 3.5 Recalcular escala

`POST .../processes/{pid}/recalcular` reusa `original_file` guardado, puede forzar metros manuales, **no consume** otro crédito de cupo.

### 3.6 Exportación

- CSV: `GET /projects/{id}/export.csv`
- PDF: `GET /projects/{id}/export.pdf` → `build_project_pdf_bytes`

### 3.7 Pasos que el usuario pidió y **no existen** como tales

| Paso hipotético | Estado en código |
|-----------------|------------------|
| Vectorización CAD | **No existe** |
| Segmentación semántica (ML) | **No existe** |
| Lectura DWG/DXF/PDF plano | **No existe** (solo raster) |
| “Motor de IA” generativo | **No existe** |

---

## 4. Frontend

### 4.1 Estructura

- **Create React App** clásico.
- **Sin React Router**, **sin Redux/Zustand/Context**, **sin TypeScript**.
- Un archivo dominante: `App.js`.

### 4.2 Modos de pantalla (no hay rutas)

| Modo | Condición | Contenido |
|------|-----------|-----------|
| Auth | `!token && !demoMode` | Login / registro / forgot / reset / invite |
| Demo | `!token && demoMode` | Cómputo sin persistencia |
| Workspace | `token` | Obras, módulos, historial, billing, invites |

Query params: `?invite=`, `?reset=`.

### 4.3 Componentes (todos en `App.js` o anidados)

| Componente | Propósito |
|------------|-----------|
| `ColorGuidePanel` | Guía de colores |
| `PlansPanel` | Free vs Pro |
| `ConfirmModal` | Confirmaciones (eliminar / cancelar plan) |
| `ComparePanel` | Comparar 2 análisis |
| `ScalePanel` | Escala manual + readout OCR |
| `ComputeOptionsPanel` | Sistema muro + altura |
| `ModuleIconSvg` | Ícono SVG por módulo |

### 4.4 Estado principal (`useState`)

Incluye (lista no exhaustiva pero representativa del código):  
`token`, `authMode`, `authForm`, `me`, `projects`, `activeProjectId`, `processes`, `referencia`, `sistemaMuro`, `alturaMuro`, `demoMode`, `demoRuns`, `loading`, `error`, `billingPublic`, `preciosInfo`, `invitations`, `confirmDlg`, `obraMenuId`, `editObraOpen`, `ayudaOpen`, `compareIds`, `lastUploadByProject`, `apiBase`, flags de onboarding (`paletteDescargada`, etc.).

### 4.5 Comunicación con backend

- Instancia axios autenticada con Bearer.
- Failover multi-host (prioriza `api.{dominio}`; `*.onrender.com` al final por adblockers).
- Timeouts: auth 45s, general 30s, calcular/recalcular **180s**.
- Tras `calcular` exitoso, inserta el proceso en UI aunque falle el refresh (mitiga “Procesando…” eterno).

### 4.6 Módulos Free vs Pro (UI)

| tipo | Título UI | Plan |
|------|-----------|------|
| muros | Estructura y terminaciones | free |
| agua | Instalacion sanitaria y gas | pro |
| luz | Instalacion electrica | pro |
| techo | Techos y losas | pro |
| terreno | Medicion de terrenos y lotes | free |

En **demo**, no se aplica el gate Pro.

### 4.7 Topbar (estado actual)

Cupo mensual + menú **Ayuda** (guía, paleta, planes, cancelar plan, soporte) + botón **Pro** si no es Pro + Salir.  
El formulario grande de edición de obra solo aparece al elegir **Editar** en el menú `⋮` de la lista de obras.

---

## 5. Backend

### 5.1 Estructura lógica

```
main.py
  ├── CORS / app FastAPI
  ├── Modelos SQLAlchemy
  ├── Auth (PBKDF2 + token HMAC)
  ├── RBAC (owner/editor/viewer)
  ├── Cupo (usage_events)
  ├── CRUD obras / procesos
  ├── calcular / recalcular → motor_ia.procesar_plano_ia
  ├── Export CSV / PDF
  ├── Invites + password reset
  └── Billing Mercado Pago + webhook
```

### 5.2 Roles

| Rol | Capacidades |
|-----|-------------|
| `owner` | Todo + invites + billing |
| `editor` | Subir/borrar/recalcular/crear obras |
| `viewer` | Lectura / export |

### 5.3 Cupo mensual

- Tabla **`usage_events`** append-only.
- Cada `POST .../calcular` autenticado inserta un evento tras guardar el `Process`.
- **Borrar un análisis no elimina eventos** → el cupo no baja.
- Free: `FREE_MONTHLY_LIMIT` default **20**.
- Pro activo: `monthly_limit` pasa a `PAID_MONTHLY_LIMIT` default **200**.
- `recalcular` **no** consume cupo.
- Demo `/calcular` **no** consume cupo de estudio (sí rate-limit IP).

### 5.4 Startup

`create_all` + ALTERs defensivos + backfill de `usage_events` en **thread daemon** (no bloquea healthcheck).

---

## 6. API

### 6.1 Convenciones

- Algunos endpoints tienen alias `/api/...`; **otros no** (`/me`, list/create projects, delete process, calcular-en-obra, recalcular).
- El frontend mitiga 404 reintentando con prefijo `/api` en helpers públicos/auth/demo.

### 6.2 Catálogo de endpoints

#### Salud y precios

| Método | Ruta | Auth | Body/Params | Respuesta |
|--------|------|------|-------------|-----------|
| GET | `/`, `/health`, `/api/health` | No | — | status/version |
| GET | `/precios-info`, `/api/precios-info` | No | — | meta cache precios |

#### Auth

| Método | Ruta | Auth | Body | Errores |
|--------|------|------|------|---------|
| POST | `/auth/register` (+`/api`) | No | studio_name, name, email, password | 400 email existe / clave corta |
| POST | `/auth/login` (+`/api`) | No | email, password | 401 |
| POST | `/auth/forgot-password` (+`/api`) | No | email | 200 genérico |
| POST | `/auth/reset-password` (+`/api`) | No | token, password | 400 enlace inválido |
| POST | `/auth/register-invite` (+`/api`) | No | token, name, password | 400 |

#### Sesión / obras / procesos

| Método | Ruta | Auth | Notas |
|--------|------|------|-------|
| GET | `/me` | Bearer | studio + used_this_month |
| GET | `/projects` | Bearer | lista + process_count |
| POST | `/projects` | Bearer+edit | crea obra |
| PATCH/PUT | `/projects/{id}` (+`/api`) | Bearer+edit | edita |
| DELETE | `/projects/{id}` | Bearer+edit | borra obra+procesos |
| GET | `/projects/{id}/processes` | Bearer | historial |
| DELETE | `/processes/{id}` | Bearer+edit | borra análisis; cupo intacto |
| GET | `/projects/{id}/export.csv` (+`/api`) | Bearer | CSV |
| GET | `/projects/{id}/export.pdf` (+`/api`) | Bearer | PDF |

#### Cálculo

| Método | Ruta | Auth | Multipart | Errores típicos |
|--------|------|------|-----------|-----------------|
| POST | `/projects/{id}/calcular` | Bearer+edit+cupo+módulo | file, referencia_metros, sistema_muro, tipo_plano, altura_muro, forzar_escala_manual | 400/402/413/500 |
| POST | `/projects/{id}/processes/{pid}/recalcular` | Bearer+edit+módulo | sin file; forzar default 1 | 400/404/500 |
| POST | `/calcular`, `/api/calcular` | Público + rate limit | igual multipart | 429/400/500 |

#### Equipo

| Método | Ruta | Auth |
|--------|------|------|
| GET/POST | `/studio/invitations` (+`/api`) | owner |
| DELETE | `/studio/invitations/{id}` (+`/api`) | owner |
| GET | `/invites/verify` (+`/api`) | público `?token=` |

#### Billing

| Método | Ruta | Auth |
|--------|------|------|
| GET | `/billing/info` (+`/api`) | público |
| POST | `/billing/create-checkout-session` (+`/api`) | owner |
| POST | `/billing/create-portal-session` (+`/api`) | owner |
| POST | `/billing/cancel` (+`/api`) | owner |
| POST | `/billing/webhook` (+`/api`) | firma MP |

### 6.3 Multipart de cálculo (campos)

| Campo | Tipo | Default | Notas |
|-------|------|---------|-------|
| `file` | UploadFile | requerido en calcular | PNG/JPEG/WEBP |
| `referencia_metros` | str→float | — | acepta `7,3` |
| `sistema_muro` | str | `ladrillo_hueco_12` | o `ladrillo_comun_12` |
| `tipo_plano` | str | `muros` | muros/agua/luz/techo/terreno |
| `altura_muro` | str→float | `2.60` | [1.8, 6.0] |
| `forzar_escala_manual` | str | `0` (`1` en recalcular) | pisa OCR |

### 6.4 Forma típica de respuesta de cálculo

```json
{
  "id": 123,
  "tipo": "muros",
  "filename": "...",
  "items": [{"nom": "...", "val": 1234.5, "origen": "..."}],
  "total": 6834193,
  "imagen": "<png base64>",
  "escala_detectada": 7.3,
  "meta": {
    "escala_modo": "ocr",
    "metros_referencia_usados": 7.3,
    "avisos": [],
    "sistema_muro": "ladrillo_hueco_12",
    "altura_muro": 2.6,
    "precios_info": {}
  }
}
```

(Demo `/calcular` devuelve el dict de `procesar_plano_ia` directamente, sin wrapper `Process`.)

---

## 7. Base de datos

### 7.1 Motor

- Dev default: SQLite `sqlite:///./arq_ia.db`
- Prod Render: Postgres (`postgresql+psycopg://...`)
- **No hay Alembic**; esquema vía `create_all` + ALTER ad-hoc.

### 7.2 Diagrama entidad-relación (texto)

```
studios 1──* users
studios 1──* projects
studios 1──* studio_invites
studios 1──* usage_events
projects 1──* processes
users 1──* processes
users 1──* password_reset_tokens
```

### 7.3 Tablas

#### `studios`

| Columna | Tipo | Rol |
|---------|------|-----|
| id | PK | |
| name | str(180) | Nombre estudio |
| plan_status | str(40) | `trial` / `active` / `paused` / `inactive` |
| monthly_limit | int | Cupo (20 o 200) |
| usage_month_key | str(7) | Legacy YYYY-MM |
| usage_count | int | Legacy |
| stripe_* | str | Legacy no usado en runtime |
| mp_preapproval_id | str | Suscripción MP |
| created_at | datetime tz | |

#### `usage_events`

| Columna | Rol |
|---------|-----|
| id | PK |
| studio_id | FK |
| kind | `calcular` / `backfill` |
| process_id | opcional |
| created_at | indexado; define mes UTC |

#### `users`

email único, `password_hash`, `role`, `is_active`, `studio_id`.

#### `projects`

name, client, address, studio_id.

#### `processes`

tipo_plano, filename, content_type, **original_file (LargeBinary)**, audit_image_base64, items (JSON/JSONB), total, escala_detectada, result_meta, created_at.

#### `studio_invites`

email, role, token_hash (SHA-256), expires_at (+7 días), accepted_at.

#### `password_reset_tokens`

token_hash, expires_at (+1 hora), used_at.

### 7.4 Migraciones

Funciones en startup:

- `ensure_process_result_meta_column`
- `ensure_studio_mp_preapproval_column`
- `ensure_studio_usage_columns`
- `ensure_usage_events_backfill` (thread)

---

## 8. Subida de planos

### 8.1 Formatos aceptados

Definidos en `main.py`:

```text
image/png, image/jpeg, image/jpg, image/webp
```

Máximo: `MAX_UPLOAD_MB` (default **15**).

### 8.2 Formatos **NO** aceptados

| Formato | Estado |
|--------|--------|
| PDF | No |
| DWG / DXF | No |
| SVG como input de cómputo | No (solo paleta SVG descargable) |
| TIFF / BMP | No en allowlist |

Mensaje de error sugiere exportar desde CAD como imagen.

### 8.3 Validación y decodificación

1. `content_type` ∈ allowlist → else 400.  
2. `len(bytes) ≤ MAX_UPLOAD_BYTES` → else 413.  
3. `cv2.imdecode(..., IMREAD_COLOR)` → BGR; si falla → `ValueError`.

### 8.4 Persistencia

El binario original se guarda en `processes.original_file` para permitir **recalcular** sin re-subir.

---

## 9. Preprocesamiento de imagen

### 9.1 Pipeline global (todos los módulos)

1. Bytes → `np.frombuffer` → `cv2.imdecode` BGR.  
2. `cv2.cvtColor(BGR→HSV)`.  
3. Máscaras por `cv2.inRange`.  
4. Operaciones específicas por módulo (thinning, morfología, contornos).  
5. Copia `img_audit` coloreada + encode PNG base64.

### 9.2 Preprocesamiento orientado a OCR (escala)

En ROI alrededor/bajo la línea verde (`extraer_numero_escala` / `_preparaciones_ocr`):

| Preparación | Descripción |
|-------------|-------------|
| otsu / otsu_inv | Threshold Otsu sobre gris (o invertido si fondo oscuro) |
| adapt / adapt_inv | Adaptive Gaussian threshold |
| b0 / b0_inv | Otsu directo sobre gris |
| amarillo | Máscara HSV amarilla dilatada + invertida (refuerzo) |
| upsample | Escala gris si lado máx &lt; 160 px (`INTER_CUBIC`) |
| rotaciones 90° | Reintentos OCR |

**No** hay pipeline genérico de denoise/CLAHE/LAB sobre el plano completo fuera del OCR.

### 9.3 Morfología usada fuera de OCR

| Uso | Operación |
|-----|-----------|
| Electricidad (bocas) | `MORPH_OPEN` elipse 5×5 |
| Auditoría muros | dilate kernel 15×15 sobre thinning rojo |
| Auditoría escala | dilate kernel 15×15 sobre thinning verde |

---

## 10. Detección de escala

### 10.1 Línea verde

```text
HSV lower [40, 150, 50]
HSV upper [80, 255, 255]
```

- Thinning de la máscara → conteo de píxeles `px_v` (longitud aproximada en px del eje).
- Contorno de mayor área → bounding box de la traza.

### 10.2 Número (OCR)

1. ROI prioritaria **debajo** del verde.  
2. ROI amplia de respaldo.  
3. Múltiples preps + PSM + whitelist dígitos.  
4. Scoring (debajo verde, decimales, rango 1–40 m, votos).  
5. Agrupa por `round(valor, 2)`.

### 10.3 Conversión píxel → metro

```text
metros_reales =
  ref_manual                         si forzar_escala_manual
  escala_leida                       si OCR ok
  ref_manual                         si OCR falla

escala_m_por_px = metros_reales / px_v   si px_v > 0
                = 0.02                   si no hay línea verde

escala_m2 = escala_m_por_px ** 2
```

### 10.4 Modos (`escala_modo`)

| Modo | Condición |
|------|-----------|
| `ocr` | OCR leyó número y no se forzó manual |
| `manual` | Hay línea verde, OCR falló, se usó formulario |
| `manual_forzada` | Usuario aplicó escala forzada |
| `sin_linea` | `px_v == 0` |

### 10.5 Errores / avisos

- Sin verde → aviso + escala default 0.02 m/px (puede distorsionar todo).  
- OCR falla → aviso + manual.  
- OCR lee mal (ej. 4.00 vs 7.30) → usuario debe forzar manual.

---

## 11. OCR

| Aspecto | Valor en código |
|---------|-----------------|
| Librería Python | `pytesseract==0.3.13` |
| Binario | `TESSERACT_CMD` / apt `tesseract-ocr` + `tesseract-ocr-spa` |
| OEM | 3 |
| PSM probados | 7, 8, 6, 11 |
| Whitelist | `0123456789.,` |
| Idioma explícito en llamada | **No** se pasa `-l spa` en `image_to_string` (usa default del binario) |
| Uso | **Solo** lectura del número de escala junto al verde |
| No usa OCR para | etiquetas de ambientes, cotas de muros, textos generales del plano |

Limitaciones: sensible a compresión JPG, tipografía, ticks de cota, contraste; no hay modelo ML de detección de texto.

---

## 12. Detección de colores

### 12.1 Espacio

Trabajo principal en **HSV OpenCV** (`H:0–179`, `S/V:0–255`) tras `BGR→HSV`.

### 12.2 Mecanismo

`cv2.inRange(hsv, lower, upper)` → máscara binaria.  
No hay clustering (k-means), ni LAB distance matching, ni aprendizaje de paleta por imagen.

### 12.3 Ruido / JPG

- Contornos con filtro de área (bocas &gt; 10 px, lotes &gt; 500 px).  
- Thinning reduce grosor.  
- No hay corrección explícita de artefactos JPEG (bloques 8×8).  
Colores cercanos pueden solaparse (naranja pisos vs marrón cloaca vs amarillo OCR).

### 12.4 Si el color cambia

Si el usuario pinta fuera del rango HSV → el elemento **no se detecta** (cantidad 0). No hay calibración adaptativa por imagen.

---

## 13. Paleta de colores

### 13.1 Tabla operativa (motor `motor_ia.py`)

Los HEX de UI son orientativos (guía frontend); el motor usa HSV.

| Elemento | HSV lower | HSV upper | HEX guía UI (`PALETA_GUIA`) | Módulo |
|----------|-----------|-----------|-----------------------------|--------|
| Escala (verde) | [40,150,50] | [80,255,255] | `#00ff5c` | todos |
| Muros (rojo) | [0,150,50] | [10,255,255] | `#d32f2f` | muros |
| Aberturas (cian) | [85,150,50] | [105,255,255] | `#00bcd4` | muros |
| Pisos gris | [0,0,180] | [179,30,230] | `#9e9e9e` | muros |
| Pisos naranja | [10,150,150] | [25,255,255] | `#ff9800` | muros |
| Agua fría (azul) | [100,100,50] | [140,255,255] | `#1e88e5` | agua |
| Agua caliente (magenta) | [140,100,100] | [170,255,255] | `#e040fb` | agua |
| Cloaca (marrón/naranja) | [10,150,100] | [25,255,255] | `#795548` | agua |
| Electricidad (amarillo) | [15,80,50] | [45,255,255] | `#ffeb3b` | luz |
| Techo (violeta) | [125,100,100] | [160,255,255] | `#b388ff` | techo |
| Terreno (gris oscuro) | [0,0,40] | [179,50,150] | `#424242` | terreno |
| Amarillo OCR (aux) | [10,55,55] | [50,255,255] | — | escala OCR |

**Tolerancia:** implícita en el ancho del intervalo HSV; no hay parámetro de “±ΔE”.

**Nota:** rojo de muros solo cubre el tramo H 0–10 (no el wrap 170–179). Rojos muy “frambuesa” pueden fallar.

### 13.2 Paleta SVG descargable

`public/plantilla-paleta-arq-ia.svg` — hexes ligeramente distintos a la guía UI; el título interno del SVG aún dice “ARC-IA” (inconsistencia cosmética).

---

## 14. Motor de visión

### 14.1 Naturaleza

Motor **clásico de CV**, no deep learning.

### 14.2 Algoritmos usados

| Técnica | API OpenCV | Uso |
|---------|------------|-----|
| Conversión color | `cvtColor` | BGR↔HSV, gris |
| Thresholding | `threshold`, `adaptiveThreshold` | OCR |
| Máscara | `inRange` | segmentación por color |
| Thinning | `ximgproc.thinning` | metros lineales |
| Contornos | `findContours` | aberturas, bocas, lotes, verde |
| Morfología | `morphologyEx OPEN`, `dilate` | bocas eléctricas, audit |
| Aprox. polígono | `approxPolyDP` | lados de lote |
| Esquinas | `goodFeaturesToTrack` | codos de cañería |
| Grafo local | `filter2D` 3×3 | nodos de caño |

### 14.3 Flujo por módulo (ASCII)

```
imagen
  → HSV
  → mask color
  → (thinning | contours | morph)
  → cantidad_px o N_contornos
  → * escala o escala_m2
  → * precios
  → items[]
```

### 14.4 Vectorización

**No existe** exportación a DXF/SVG de geometría detectada. Solo imagen de auditoría raster.

---

## 15. Geometría

### 15.1 Escala lineal y de área

- Metro lineal ≈ `N_px_thinned * escala`  
- Metro cuadrado ≈ `N_px_mask * escala²`

### 15.2 Muros (superficie vertical)

```text
m_lineales ≈ px_thinned_rojo * escala
m2_muros = m_lineales * altura_muro
m2_revoques = m2_muros * 2
```

### 15.3 Pisos

```text
m2_pisos = (px_gris + px_naranja) * escala_m2
```

No separa ambientes por etiqueta; es área de máscara.

### 15.4 Aberturas

Conteo de contornos externos cian → **unidades**, no ancho×alto real.

### 15.5 Cañerías / electricidad

```text
ml = px_thinned * escala
```

Nodos: grado 1 = punta/boca, grado 3 = tee, grado 4 cuenta como 2 tees; codos ≈ corners no nodales.

### 15.6 Techo

```text
m2_techo = px_violeta * escala_m2
ml_perfil = m2_techo * 2.5
tornillos = m2_techo * 5
```

### 15.7 Terreno

```text
area_m2 = contourArea * escala_m2
perimetro_m = arcLength * escala
lados: approxPolyDP(epsilon=0.02*perimetro), distancias entre vértices * escala
```

Lotes ordenados por coordenada X del bounding box; etiquetados L1, L2, …

### 15.8 Centroides

Usados para dibujar número de lote en auditoría (`moments`), no para presupuesto.

### 15.9 Volúmenes

**No se calculan** volúmenes 3D explícitos (m³ hormigón, etc.) salvo implícitos vía dosificaciones por m².

---

## 16. Detección de muros

1. Máscara HSV rojo.  
2. Thinning → píxeles del eje.  
3. `m_lineales = px * escala`.  
4. `m2 = m_lineales * altura` (altura formulario, default 2.60).  
5. Sistema: `ladrillo_hueco_12` (15 u/m²) o `ladrillo_comun_12` (60 u/m²).  

**No diferencia** muros interiores/exteriores, portantes/tabiques, encuentros L/T, vanos restados del muro (las aberturas se cobran aparte por unidad, no se restan del área de muro).

**Bug/observación de código:** la mano de obra de muros **siempre** multiplica por `mo_muro_hueco_m2`, incluso si el sistema es ladrillo común (existe `mo_muro_comun_m2` en precios offline pero no se usa en ese ítem).

---

## 17. Detección de pisos

1. Unión de máscaras gris claro + naranja.  
2. Área = suma de píxeles * `escala_m2`.  
3. Se aplica paquete contrapiso + carpeta + cerámico (MO y materiales).  

**No** clasifica por ambiente, **no** resta espesores de muros, **no** distingue material por color más allá de sumar ambas máscaras.

---

## 18. Detección de aberturas

1. Máscara cian.  
2. `findContours` externos.  
3. `unid_aberturas = len(contornos)` (sin filtro de área mínimo).  
4. Precio: `unid * mo_abertura_unid` y `unid * mat_abertura_promedio`.  

**No mide** ancho/alto de vano; no distingue puerta vs ventana.

---

## 19. Instalaciones

### 19.1 Agua (`tipo_plano=agua`) — Plan Pro en API autenticada

| Red | Color HSV | Métrica |
|-----|-----------|---------|
| Fría | azul | ml thinning + nodos |
| Caliente | magenta | ml thinning + nodos |
| Cloaca | marrón/naranja | ml thinning (sin grafo de nodos) |

Ítems generados (si ml agua &gt; 0): caño termo, codos, tees, MO tendido, MO bocas; si cloaca &gt; 0: mat+MO cloaca.

### 19.2 Electricidad (`luz`) — Plan Pro

| Elemento | Método |
|----------|--------|
| Caño corrugado | thinning máscara amarilla → ml |
| Bocas | MORPH_OPEN + contornos área &gt; 10 |

### 19.3 Gas

**No hay** módulo ni máscara específica de gas. El título UI dice “sanitaria y gas”, pero el motor solo modela agua fría/caliente/cloaca.

---

## 20. Losas / techos

Módulo `techo` (Pro):

- Máscara violeta → m².  
- Perfilería empírica `2.5 ml / m²`.  
- Tornillos `5 / m²`.  
- Chapas, aislación, MO por m² según claves `TECH-*`.  

**No** distingue losa hormigón vs cubierta liviana geométricamente; es “área violeta = techo”.

---

## 21. Motor de materiales

### 21.1 Fuente de precios

1. Intento CSV Google Sheets (`PRECIOS_CSV_URL` o URL default en código).  
2. Cache en memoria `PRECIOS_CACHE_SEGUNDOS` (300s).  
3. Fallback dict offline en `motor_ia._precios_base_offline()`.  
4. Archivo `precios.json` **no se carga**.

### 21.2 Dosificaciones muros (por m² de muro vertical)

Sea `cem = precio_bolsa_25kg/25`, `cal = bolsa_cal/25`, `peg = pegamento_30kg/30`.

| Concepto | Fórmula (ARS/m² aprox) |
|----------|-------------------------|
| Material muro | `cant_ladrillos * P[ladrillo] + 4*cem + 0.015*P[arena_m3]` |
| Material revoque | `5*cem + 3*cal + 0.02*P[arena]` |
| Contrapiso | `7.5*cem + 3.5*cal + 0.035*arena + 0.07*escombro` |
| Carpeta | `10.5*cem + 0.03*arena` |
| Cerámico | `1.05*P[ceramico_m2] + 4*peg` |

`cant_ladrillos = 15` (hueco) o `60` (común).

### 21.3 Mano de obra muros

| Ítem | Fórmula |
|------|---------|
| MO Muros | `m2_muros * mo_muro_hueco_m2` |
| MO Revoques | `m2_revoques * mo_revoque_doble_m2` |
| MO Pisos | `m2_pisos * (mo_contrapiso + mo_carpeta + mo_ceramico)` |
| MO Aberturas | `unidades * mo_abertura_unid` |

### 21.4 Materiales aberturas / instalaciones / techo

Precios unitarios o por ml/m² según claves `AGUA-*`, `CLOA-*`, `LUZ-*`, `TECH-*` (ver sección 6 del análisis de `motor_ia`).

### 21.5 Qué **no** calcula el motor actual

Hierro de construcción detallado, hormigón m³ de losa, pintura m² de cielorraso, mesada, sanitarios catalogados, etc. Solo lo cableado en `procesar_plano_ia`.

---

## 22. IA

### 22.1 Declaración explícita

**No existe un subsistema de IA moderna** en el repositorio.

| Tecnología | Presente |
|------------|----------|
| OpenAI / Anthropic / Gemini | No |
| Ollama / LLM local | No |
| TensorFlow / PyTorch / Keras | No |
| YOLO / Ultralytics | No |
| SAM / CLIP / Detectron | No |
| Prompts | No |

### 22.2 Qué hay en su lugar

- Visión clásica OpenCV.  
- OCR Tesseract.  
- El nombre del producto y de la función `procesar_plano_ia` usa “IA” en sentido de **automatización**, no de modelo neuronal.

---

## 23. Exportaciones

| Formato | Endpoint | Contenido |
|--------|----------|-----------|
| CSV | `GET /projects/{id}/export.csv` | Filas por ítem de cada proceso; columnas obra, cliente, tipo, archivo, categoría, ítem, valor, total módulo, escala, fecha. **Sin** base64 de imagen |
| PDF | `GET /projects/{id}/export.pdf` | Presupuesto Unicode (DejaVu), secciones por tipo_plano, totales (excluye terreno del gran total) |
| JSON | Implícito en API REST | Respuestas de procesos |
| Imagen auditoría | Campo `imagen` base64 en proceso | PNG coloreado |
| Excel (xlsx) | **No existe** | — |

Demo: sin exportaciones.

---

## 24. Configuraciones

### 24.1 Variables de entorno relevantes

| Variable | Uso |
|----------|-----|
| `DATABASE_URL` | Conexión DB |
| `SECRET_KEY` | Firma tokens |
| `APP_URL` | Links email / back_url MP |
| `ALLOWED_ORIGINS` / `ALLOWED_ORIGIN_REGEX` | CORS |
| `MAX_UPLOAD_MB` | Límite upload |
| `DEMO_RATE_*` | Rate limit demo |
| `FREE_MONTHLY_LIMIT` / `PAID_MONTHLY_LIMIT` | Cupos |
| `TESSERACT_CMD` | Binario OCR |
| `PRECIOS_CSV_URL` / `PRECIOS_CACHE_SEGUNDOS` / `SHEETS_TIMEOUT_SEC` | Precios |
| `MP_*` | Mercado Pago |
| `RESEND_API_KEY` / `EMAIL_FROM` / `APP_NAME` | Email |
| `REACT_APP_API_URL` | Frontend build |
| `REACT_APP_SITE_NAME` / `REACT_APP_SUPPORT_WHATSAPP` | Branding UI |

### 24.2 Constantes de negocio en código

- `PRO_ONLY_MODULES = {agua, luz, techo}`  
- Sistemas muro: `ladrillo_hueco_12`, `ladrillo_comun_12`  
- Token sesión: 14 días  
- Invite: 7 días; reset password: 1 hora  
- PBKDF2: 180000 iteraciones  

### 24.3 Archivos de config

- `backend/.env.example`, `frontend/.env.example`  
- `render.yaml`  
- `precios.json` (huérfano)  

---

## 25. Dependencias

### 25.1 Backend (`requirements.txt`)

| Dependencia | Versión | Uso | Importancia |
|-------------|---------|-----|-------------|
| fastapi | 0.115.6 | API | Crítica |
| uvicorn[standard] | 0.34.0 | Server | Crítica |
| python-multipart | 0.0.20 | Uploads | Crítica |
| numpy | 2.2.1 | Arrays imagen | Crítica |
| opencv-contrib-python-headless | 4.10.0.84 | Visión + thinning | Crítica |
| pytesseract | 0.3.13 | OCR | Crítica (escala) |
| SQLAlchemy | 2.0.36 | ORM | Crítica |
| psycopg[binary] | 3.2.3 | Postgres | Crítica en prod |
| pydantic[email] | 2.10.4 | Validación | Alta |
| fpdf2 | 2.8.2 | PDF | Alta |
| pytest | 8.3.4 | Tests | Dev |

Sistema: Tesseract OCR (+ spa) vía apt en Docker.

### 25.2 Frontend (`package.json`)

| Dependencia | Versión | Uso |
|-------------|---------|-----|
| react / react-dom | ^19.2.5 | UI |
| react-scripts | 5.0.1 | Build CRA |
| axios | ^1.16.0 | HTTP |
| testing-library / web-vitals | varias | Test/métricas |

---

## 26. Rendimiento

### 26.1 Observaciones derivadas del código

| Aspecto | Situación |
|---------|-----------|
| Procesamiento visión | Síncrono en el request HTTP (hasta timeout cliente 180s) |
| OCR | Múltiples PSM × preps × ROI → puede ser el cuello de botella |
| Imagen auditoría | PNG base64 en JSON/DB → payloads grandes |
| `original_file` | BLOB completo en Postgres |
| Workers GPU | No |
| Cache precios | 300s en memoria de proceso |
| Cold start Render | Puede demorar health/login |

### 26.2 Cuellos de botella probables

1. Tesseract multi-pass.  
2. Thinning en máscaras grandes.  
3. Serialización base64 de auditoría.  
4. Lectura/escritura BLOB en DB.  
5. Un solo worker Uvicorn por defecto en CMD (sin `-w N` explícito).

### 26.3 Métricas

**No hay** telemetría APM, timings estructurados ni benchmarks automatizados de latencia en el repo.

---

## 27. Seguridad

### 27.1 Controles existentes

| Control | Implementación |
|---------|----------------|
| Passwords | PBKDF2-HMAC-SHA256, 180k iter, salt 16B |
| Sesión | Token firmado HMAC, exp 14d |
| RBAC | owner/editor/viewer |
| Upload | allowlist MIME + tamaño |
| CORS | origins + regex |
| Demo abuse | rate limit IP en memoria |
| Webhook MP | HMAC opcional (`MP_WEBHOOK_SECRET`) |
| Invites/reset | token opaco hasheado SHA-256 |

### 27.2 Riesgos / huecos observados en código

| Riesgo | Detalle |
|--------|---------|
| `SECRET_KEY` `generateValue: true` en Render | Redeploys pueden invalidar sesiones si la key rota |
| Webhook sin secret | Acepta notificaciones sin verificar |
| Token no JWT estándar | Sin kid/rotación; logout solo borra localStorage |
| Archivos en DB | BLOB + base64 aumentan superficie de exfiltración si hay IDOR (hay check de studio_id) |
| Rate limit demo | En memoria de proceso (no compartido entre réplicas) |
| `/calcular` demo | No aplica gate Pro (intencional) |
| XSS | React escapa texto; `dangerouslySetInnerHTML` no aparece |
| CSRF | API Bearer (menos expuesta que cookies), sin cookies de sesión |

### 27.3 Validaciones de negocio

Altura, referencia, sistema muro, tipo módulo Pro, cupo 402.

---

## 28. Limitaciones

Lista de lo que **hoy NO hace** (sin proponer implementación):

1. No lee DWG/DXF/PDF de plano.  
2. No vectoriza a CAD.  
3. No usa redes neuronales / LLM.  
4. No distingue puerta vs ventana.  
5. No resta vanos del área de muro.  
6. No clasifica muros interior/exterior.  
7. No calcula estructuras de hormigón armado detalladas.  
8. No hay módulo gas real separado.  
9. No hay módulo de pintura/cielorrasos dedicado.  
10. No hay Excel xlsx.  
11. No hay app móvil nativa.  
12. No hay multi-idioma.  
13. No hay React Router / modularización frontend.  
14. No hay Alembic/migraciones versionadas.  
15. No hay cola asíncrona de procesamiento.  
16. No hay storage objeto (S3) para planos.  
17. No usa `precios.json`.  
18. Rojo HSV sin wrap high-H.  
19. Escala por defecto 0.02 m/px si falta verde (peligroso).  
20. Tests no cubren API E2E ni módulos agua/luz/techo de punta a punta.  
21. Demo no exporta.  
22. No hay firma digital ni versionado de presupuesto.  
23. No hay colaboración en tiempo real.  
24. No hay OCR de cotas distintas a la verde de escala.

---

## 29. Posibles errores

| Síntoma | Causa probable en código |
|---------|--------------------------|
| Login “API no respondió” | Cold start / host caído / adblock a onrender / timeout |
| “Procesando…” largo | OCR+OpenCV síncrono; timeout 180s |
| 401 tras deploy | `SECRET_KEY` regenerada; token viejo |
| Escala 4.00 en vez de 7.30 | OCR incorrecto; requiere forzar manual |
| Totales absurdos | Sin línea verde → escala 0.02 |
| Módulo Pro 402 | `plan_status != active` |
| Cupo 402 | `usage_events` del mes ≥ limit |
| Demo 429 | Rate limit IP |
| Upload 400 | MIME no permitido |
| Upload 413 | &gt; MAX_UPLOAD_MB |
| Cero detección | Color fuera de HSV / compresión / alpha |
| Sidebar dice N análisis y panel 0 | Fallo al refrescar processes (401/red) tras calcular |
| Precios offline | Fallo fetch Sheets |

---

## 30. Precisión

### 30.1 Factores que afectan

| Factor | Impacto |
|--------|---------|
| Exactitud de la cota OCR | Escala global (error relativo en todo) |
| Calidad de pintura del plano | Falsos positivos/negativos de máscara |
| Grosor de trazo muro | Thinning mitiga pero no elimina |
| JPG | Sangrado de color en bordes |
| Resolución | OCR y thinning sensibles a px |
| Altura muro asumida uniforme | No lee alturas distintas por local |
| Aberturas por conteo | Ignora tamaño real del vano |
| Fórmulas de dosificación fijas | Estimación, no cómputo de obra certificado |

### 30.2 Precisión OCR

Mejorada con scoring multi-candidato; sigue siendo el punto más frágil de la calibración.

### 30.3 Precisión geométrica

Depende linealmente de `metros/px`. Un error del 10% en escala ⇒ ~10% en ml y ~21% en m².

---

## 31. Casos de uso

| Usuario | Encaje actual |
|---------|---------------|
| Arquitectos / estudios chicos | Alto: cómputo rápido Free (muros/terreno) |
| MMO / cómputo | Medio: sirve como estimación, no pliego oficial |
| Constructoras | Medio-bajo: falta detalle estructural/instalaciones avanzadas |
| Particulares | Medio: demo + Free |
| Empresas grandes | Bajo: falta SSO, colas, auditoría enterprise, CAD nativo |

Requisitos de uso real: el plano **debe** respetar la paleta; no es “subí cualquier PDF del municipio”.

---

## 32. Roadmap técnico

> Solo descripción; **sin implementación** en esta auditoría.

### Alta prioridad

1. Migraciones versionadas (Alembic) y `SECRET_KEY` estable en prod.  
2. Jobs asíncronos de visión (cola) + progreso real de “Procesando”.  
3. Hardening OCR de escala (tests con fixtures reales WhatsApp/JPG).  
4. Cobertura E2E API (auth, calcular, cupo, Pro gate).  
5. Modularizar `App.js` / separar cliente API.  
6. Storage externo para BLOB + thumbnails (no base64 gigante en listados).  
7. Completar aliases `/api` faltantes o documentar contrato único.  
8. Usar `mo_muro_comun_m2` cuando el sistema es ladrillo común.  
9. Rojo HSV con wrap (0–10 ∪ 170–179).  
10. Telemetría de errores/latencia (Sentry/OpenTelemetry).

### Media prioridad

1. Distinguir puerta/ventana y restar vanos.  
2. Export Excel; presupuesto editable.  
3. Lectura PDF rasterizado (páginas→imagen).  
4. Calibración de paleta por sampler en UI.  
5. Módulo gas real / desambiguar naranja pisos vs cloaca (planos separados ya ayudan).  
6. Caché Redis para rate-limit demo y precios.  
7. i18n.  
8. Tests de regresión visual de auditoría.  
9. CI (GitHub Actions) lint+pytest+build.  
10. Documentar contrato OpenAPI publicado.

### Baja prioridad

1. Ingesta DXF simplificada.  
2. Vectorización SVG de máscaras.  
3. Modelos ML opcionales (segmentación) detrás de feature flag.  
4. App móvil.  
5. Colaboración multi-cursor.  
6. Versionado de presupuestos / comparación histórica avanzada.  
7. Marketplace de precios regionales.  
8. PWA offline demo.

---

## 33. Conclusión

### 33.1 Nivel de madurez

**MVP productivo / early product** con usuarios reales, billing y deploy cloud, pero con arquitectura aún **monolítica y acoplada**, y un motor de visión **basado en reglas de color** (adecuado al producto “plano pintado”, no a planos genéricos).

### 33.2 Calidad del código

| Dimensión | Evaluación |
|-----------|------------|
| Claridad del dominio | Media-alta en `motor_ia` (módulos explícitos) |
| Modularidad frontend | Baja (`App.js` &gt; 2500 líneas) |
| Modularidad backend | Media (main grande + satélites claros) |
| Tests | Parciales; no E2E |
| Deuda | `precios.json` huérfano; inconsistencias MO común; aliases API incompletos |

### 33.3 Escalabilidad

- Vertical: limitada por OCR+OpenCV síncronos y BLOBs en DB.  
- Horizontal: rate-limit y cache precios en memoria de proceso; sessions stateless (OK).  
- Sin cola, el throughput de cómputos concurrentes es el de workers Uvicorn × CPU.

### 33.4 Mantenibilidad

Aceptable para un equipo pequeño que conoce el monolito; costosa para onboarding sin este documento. La paleta HSV es el “contrato” crítico no tipado.

### 33.5 Fortalezas

1. Producto end-to-end usable (auth, obras, cupo, Pro, export, demo).  
2. Motor de cuantificación comprensible y auditable (imagen coloreada).  
3. Recalcular sin re-subir ni gastar cupo.  
4. Cupo append-only (`usage_events`).  
5. Failover de API y timeouts largos en cliente.  
6. PDF Unicode con DejaVu.  
7. Deploy reproducible vía `render.yaml` + Docker.

### 33.6 Debilidades

1. Dependencia total de que el usuario pinte bien.  
2. OCR de escala frágil.  
3. Frontend monolítico.  
4. Sin migraciones formales.  
5. Payloads base64 pesados.  
6. Cobertura de tests incompleta.  
7. “IA” en el nombre no corresponde a ML real (puede generar expectativas incorrectas).

### 33.7 Riesgos técnicos

| Riesgo | Severidad |
|--------|-----------|
| Error de escala → presupuesto erróneo silencioso | Alta |
| Rotación de `SECRET_KEY` | Alta (sesiones) |
| Adblockers / DNS custom flaky | Media (UX login/upload) |
| Crecimiento de BLOBs en Postgres | Media |
| Solapamiento HSV entre módulos | Media |
| Expectativa de precisión de cómputo oficial | Alta (negocio/legal) |

### 33.8 Veredicto profesional

ARQ-IA es un **SaaS de estimación por visión clásica sobre planos codificados por color**, con capa comercial (Free/Pro + Mercado Pago) y operación multi-usuario por estudio. Es coherente y entregable como producto de nicho **si** se comunica claramente el protocolo de pintado y el carácter estimativo del resultado. Para evolucionar a plataforma de cómputo industrial se requiere desacoplar el procesamiento, fortalecer calibración/escala, versionar esquema, y ampliar cobertura de ensayos — sin confundir el motor actual con un sistema de IA/ML.

---

## Apéndice A — Inventario de tipos de plano

| `tipo_plano` | Gate Pro (API auth) | Consume cupo | Total monetario |
|--------------|---------------------|--------------|-----------------|
| muros | No | Sí | Sí |
| agua | Sí | Sí | Sí |
| luz | Sí | Sí | Sí |
| techo | Sí | Sí | Sí |
| terreno | No | Sí | No (`total=0`, vals texto) |

## Apéndice B — Claves de precios offline (motor)

`mat_cemento_25kg`, `mat_cal_25kg`, `mat_arena_m3`, `mat_escombro_m3`, `mat_ladrillo_hueco_18cm`, `mat_ladrillo_hueco_12cm`, `mat_ladrillo_comun_12cm`, `mat_ceramico_m2`, `mat_pegamento_30kg`, `mat_abertura_promedio`, `mo_muro_hueco_m2`, `mo_muro_comun_m2`, `mo_revoque_doble_m2`, `mo_contrapiso_m2`, `mo_carpeta_m2`, `mo_ceramico_m2`, `mo_abertura_unid`, `AGUA-MAT-01`, `AGUA-ACC-CODO`, `AGUA-ACC-TE`, `AGUA-MO-01`, `AGUA-BOCA-01`, `CLOA-MAT-01`, `CLOA-MO-01`, `LUZ-MAT-01`, `LUZ-MO-01`, `LUZ-MAT-02`, `LUZ-MO-02`, `TECH-CHAP-01`, `TECH-PERF-01`, `TECH-AISL-01`, `TECH-TORN-01`, `TECH-MO-01`.

## Apéndice C — Contadores de líneas (orden de magnitud)

| Archivo | Líneas (aprox.) |
|---------|-----------------|
| `frontend/src/App.js` | 2558 |
| `frontend/src/App.css` | 1738 |
| `backend/main.py` | 1383 |
| `backend/motor_ia.py` | 719 |
| `backend/billing_mp.py` | 144 |
| `backend/presupuesto_pdf.py` | 134 |
| `backend/email_service.py` | 91 |

## Apéndice D — Ausencias explícitas pedidas en el brief

| Pedido de auditoría | Hallazgo |
|---------------------|----------|
| Carpeta `vision/`, `ai/`, `ocr/`, `workers/` | No existen |
| YOLO / SAM / CLIP / TF | No existen |
| OpenAI / Ollama | No existen |
| DWG/DXF input | No existe |
| Vectorización | No existe |
| Excel export | No existe |
| Gas como red propia | No existe (solo naming UI) |

---

*Fin del documento de auditoría. Generado únicamente a partir del código presente en el repositorio; sin modificaciones funcionales al sistema.*
