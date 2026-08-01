import base64
import hashlib
import hmac
import json
import os
import secrets
import threading
import time
from io import BytesIO, StringIO
from datetime import datetime, timedelta, timezone
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Text, create_engine, inspect, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker
from sqlalchemy.types import JSON

from billing_mp import (
    billing_public_info,
    cancel_preapproval,
    create_subscription_checkout,
    get_preapproval,
    mp_configured,
    verify_webhook_signature,
)
from email_service import email_configured, send_invite_email, send_password_reset_email
from motor_ia import get_precios_info, obtener_precios_en_vivo, procesar_plano_ia
from presupuesto_pdf import build_project_pdf_bytes


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


DATABASE_URL = normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///./arq_ia.db"))
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
def normalize_app_url(raw: str | None) -> str:
    """Mercado Pago exige back_url absoluta http(s) sin basura."""
    value = (raw or "").strip().rstrip("/")
    if not value:
        return "https://arq-ia.pro"
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return f"https://{value.lstrip('/')}"


APP_URL = normalize_app_url(os.getenv("APP_URL", "https://arq-ia.pro"))
FREE_MONTHLY_LIMIT = int(os.getenv("FREE_MONTHLY_LIMIT", "20"))
PAID_MONTHLY_LIMIT = int(os.getenv("PAID_MONTHLY_LIMIT", "500"))
APP_VERSION = os.getenv("APP_VERSION", "dev")
DEMO_RATE_WINDOW_SEC = int(os.getenv("DEMO_RATE_WINDOW_SEC", "3600"))
DEMO_RATE_MAX = int(os.getenv("DEMO_RATE_MAX", "30"))


if os.getenv("RENDER") and DATABASE_URL.startswith("sqlite"):
    print("[WARN] DATABASE_URL no configurada en Render: usando SQLite efimera. Configura PostgreSQL para persistencia.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
JsonColumn = JSONB if DATABASE_URL.startswith("postgresql") else JSON

app = FastAPI(title="ARQ-IA API")

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
if APP_URL:
    allowed_origins.append(APP_URL.rstrip("/"))
    if APP_URL.startswith("https://") and "www." not in APP_URL:
        allowed_origins.append(APP_URL.replace("https://", "https://www.", 1).rstrip("/"))
allowed_origins = sorted(set(allowed_origins))

allowed_origin_regex = os.getenv("ALLOWED_ORIGIN_REGEX", r"https://((.*\.onrender\.com)|((.*\.)?arq-ia\.pro))$")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "15"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

_demo_rate_lock = threading.Lock()
_demo_rate_hits: dict[str, list[float]] = {}


def client_ip(request: Request) -> str:
    xf = (request.headers.get("x-forwarded-for") or "").split(",")[0].strip()
    if xf:
        return xf
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def check_demo_rate_limit(request: Request):
    if DEMO_RATE_MAX <= 0:
        return
    ip = client_ip(request)
    now = time.time()
    with _demo_rate_lock:
        hits = _demo_rate_hits.setdefault(ip, [])
        cutoff = now - DEMO_RATE_WINDOW_SEC
        while hits and hits[0] < cutoff:
            hits.pop(0)
        if len(hits) >= DEMO_RATE_MAX:
            raise HTTPException(
                status_code=429,
                detail=f"Demasiados analisis en modo demo desde esta IP. Limite: {DEMO_RATE_MAX} cada {DEMO_RATE_WINDOW_SEC // 60} minutos. Probá mas tarde o crea un estudio.",
            )
        hits.append(now)

class Studio(Base):
    __tablename__ = "studios"

    id = Column(Integer, primary_key=True)
    name = Column(String(180), nullable=False)
    plan_status = Column(String(40), nullable=False, default="trial")
    monthly_limit = Column(Integer, nullable=False, default=FREE_MONTHLY_LIMIT)
    # Legacy Stripe (ya no se usa; se mantiene por DBs existentes).
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    mp_preapproval_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="studio")
    projects = relationship("Project", back_populates="studio")
    invites = relationship("StudioInvite", back_populates="studio")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)
    name = Column(String(180), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(40), nullable=False, default="owner")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    studio = relationship("Studio", back_populates="users")
    processes = relationship("Process", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)
    name = Column(String(180), nullable=False)
    client = Column(String(180), nullable=True)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    studio = relationship("Studio", back_populates="projects")
    processes = relationship("Process", back_populates="project")


class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tipo_plano = Column(String(40), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(80), nullable=False)
    original_file = Column(LargeBinary, nullable=False)
    audit_image_base64 = Column(Text, nullable=False)
    items = Column(JsonColumn, nullable=False)
    total = Column(Float, nullable=False, default=0)
    escala_detectada = Column(Float, nullable=True)
    result_meta = Column(JsonColumn, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    project = relationship("Project", back_populates="processes")
    user = relationship("User", back_populates="processes")


class StudioInvite(Base):
    __tablename__ = "studio_invites"

    id = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    role = Column(String(40), nullable=False)
    token_hash = Column(String(80), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    accepted_at = Column(DateTime(timezone=True), nullable=True)

    studio = relationship("Studio", back_populates="invites")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    token_hash = Column(String(80), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")


class RegisterIn(BaseModel):
    studio_name: str
    name: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    token: str
    password: str


class ProjectIn(BaseModel):
    name: str
    client: str | None = None
    address: str | None = None


class BillingPortalIn(BaseModel):
    return_url: str | None = None


class InviteCreateIn(BaseModel):
    email: EmailStr
    role: str = "editor"


class RegisterInviteIn(BaseModel):
    token: str
    name: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    ensure_process_result_meta_column()
    ensure_studio_mp_preapproval_column()


def ensure_process_result_meta_column():
    inspector = inspect(engine)
    if "processes" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("processes")}
    if "result_meta" in cols:
        return
    if DATABASE_URL.startswith("sqlite"):
        ddl = "ALTER TABLE processes ADD COLUMN result_meta TEXT"
    elif "postgresql" in DATABASE_URL:
        ddl = "ALTER TABLE processes ADD COLUMN result_meta JSONB"
    else:
        ddl = "ALTER TABLE processes ADD COLUMN result_meta JSON"
    with engine.begin() as conn:
        conn.execute(text(ddl))


def ensure_studio_mp_preapproval_column():
    inspector = inspect(engine)
    if "studios" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("studios")}
    if "mp_preapproval_id" in cols:
        return
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE studios ADD COLUMN mp_preapproval_id VARCHAR(255)"))


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 180_000)
    return f"pbkdf2_sha256$180000${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(dk).decode()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        _, iterations, salt_b64, hash_b64 = stored_hash.split("$", 3)
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        expected = base64.urlsafe_b64decode(hash_b64.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def create_token(user_id: int) -> str:
    payload = {"sub": user_id, "exp": int(time.time()) + 60 * 60 * 24 * 14}
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode()
    signature = hmac.new(SECRET_KEY.encode(), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{signature}"


def read_token(token: str) -> int:
    try:
        body, signature = token.rsplit(".", 1)
        expected = hmac.new(SECRET_KEY.encode(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("bad signature")
        payload = json.loads(base64.urlsafe_b64decode(body.encode()))
        if payload["exp"] < int(time.time()):
            raise ValueError("expired")
        return int(payload["sub"])
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Sesion invalida o vencida.") from exc


def current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Inicia sesion para continuar.")
    user_id = read_token(authorization.removeprefix("Bearer ").strip())
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no encontrado.")
    return user


def require_studio_owner(user: User) -> User:
    if user.role != "owner":
        raise HTTPException(status_code=403, detail="Solo el dueño del estudio puede gestionar invitaciones.")
    return user


def require_can_edit(user: User) -> User:
    """Owner y editor pueden mutar obras/analisis; viewer es solo lectura."""
    if user.role == "viewer":
        raise HTTPException(
            status_code=403,
            detail="Tu rol es solo lectura. Pedile al dueño del estudio un rol editor para subir o borrar planos.",
        )
    return user


def require_can_bill(user: User) -> User:
    if user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Solo el dueño del estudio puede gestionar la suscripcion.",
        )
    return user


def serialize_process(process: Process) -> dict:
    return {
        "id": process.id,
        "project_id": process.project_id,
        "tipo": process.tipo_plano,
        "filename": process.filename,
        "items": process.items,
        "total": process.total,
        "imagen": process.audit_image_base64,
        "escala_detectada": process.escala_detectada,
        "meta": process.result_meta or {},
        "created_at": process.created_at.isoformat(),
        "user": process.user.name if process.user else None,
    }


def validate_upload(file: UploadFile, contenido: bytes):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Usa PNG, JPG/JPEG o WEBP (exporta tu plano como imagen desde el CAD).",
        )
    if len(contenido) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"El archivo supera {MAX_UPLOAD_MB} MB. Comprimí la imagen o subi menor resolucion.",
        )


def month_start() -> datetime:
    now = datetime.now(timezone.utc)
    return datetime(now.year, now.month, 1, tzinfo=timezone.utc)


def ensure_usage_available(db: Session, studio: Studio):
    used = (
        db.query(Process)
        .join(Project)
        .filter(Project.studio_id == studio.id, Process.created_at >= month_start())
        .count()
    )
    if used >= studio.monthly_limit:
        raise HTTPException(
            status_code=402,
            detail=f"Tu plan permite {studio.monthly_limit} planos por mes. Actualiza la suscripcion para seguir.",
        )


# Modulos incluidos solo en Plan Pro (Mercado Pago activo).
PRO_ONLY_MODULES = frozenset({"agua", "luz", "techo"})


def ensure_module_allowed(studio: Studio, tipo_plano: str):
    tipo = (tipo_plano or "").strip().lower()
    if tipo in PRO_ONLY_MODULES and studio.plan_status != "active":
        raise HTTPException(
            status_code=402,
            detail="Este modulo es Plan Pro (agua, electricidad o techos). Activa la suscripcion con Mercado Pago.",
        )


@app.get("/")
async def root():
    return {"status": "ok", "service": "arq-ia-backend", "version": APP_VERSION, "health": "/health", "precios_info": "/precios-info", "register": "/auth/register", "login": "/auth/login"}


@app.get("/api/health")
async def health_api():
    return {"status": "ok", "version": APP_VERSION}

@app.get("/health")
async def health():
    return {"status": "ok", "version": APP_VERSION}


@app.get("/precios-info")
@app.get("/api/precios-info")
def precios_info():
    """Ultima lectura de tabla de precios (cache + fuente). No requiere auth."""
    obtener_precios_en_vivo()
    return get_precios_info()


@app.post("/auth/register")
@app.post("/api/auth/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="La clave debe tener al menos 8 caracteres.")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese email.")

    studio = Studio(name=data.studio_name.strip(), monthly_limit=FREE_MONTHLY_LIMIT)
    db.add(studio)
    db.flush()

    user = User(
        studio_id=studio.id,
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(data.password),
        role="owner",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user.id), "user": {"name": user.name, "email": user.email}}


@app.post("/auth/login")
@app.post("/api/auth/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email o clave incorrectos.")
    return {"token": create_token(user.id), "user": {"name": user.name, "email": user.email}}


@app.post("/auth/forgot-password")
@app.post("/api/auth/forgot-password")
def forgot_password(data: ForgotPasswordIn, db: Session = Depends(get_db)):
    """Siempre responde ok para no filtrar si el email existe."""
    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email, User.is_active.is_(True)).first()
    email_sent = False
    email_error = None
    if user:
        raw = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw.encode()).hexdigest()
        now = datetime.now(timezone.utc)
        # Invalidar tokens previos sin usar.
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        ).update({"used_at": now})
        row = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=now + timedelta(hours=1),
        )
        db.add(row)
        db.commit()
        reset_url = f"{APP_URL.rstrip('/')}/?reset={raw}"
        mail = send_password_reset_email(to=email, reset_url=reset_url)
        email_sent = bool(mail.get("ok"))
        email_error = None if mail.get("ok") else mail.get("error")
        if not email_configured():
            # En dev sin Resend, devolvemos el link para no bloquear pruebas locales.
            return {
                "ok": True,
                "email_sent": False,
                "email_configured": False,
                "detail": "Email no configurado. Usa el enlace de desarrollo.",
                "dev_reset_url": reset_url,
            }
    return {
        "ok": True,
        "email_sent": email_sent,
        "email_configured": email_configured(),
        "detail": "Si el email existe, enviamos un enlace para restablecer la clave.",
        "email_error": email_error,
    }


@app.post("/auth/reset-password")
@app.post("/api/auth/reset-password")
def reset_password(data: ResetPasswordIn, db: Session = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="La clave debe tener al menos 8 caracteres.")
    token_hash = hashlib.sha256(data.token.strip().encode()).hexdigest()
    row = db.query(PasswordResetToken).filter(PasswordResetToken.token_hash == token_hash).first()
    now = datetime.now(timezone.utc)
    if not row or row.used_at or row.expires_at < now:
        raise HTTPException(status_code=400, detail="Enlace invalido o vencido. Pedi uno nuevo.")
    user = db.get(User, row.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Usuario no encontrado.")
    user.password_hash = hash_password(data.password)
    row.used_at = now
    db.commit()
    return {"ok": True, "detail": "Clave actualizada. Ya podes ingresar."}


@app.get("/me")
def me(user: User = Depends(current_user), db: Session = Depends(get_db)):
    used = (
        db.query(Process)
        .join(Project)
        .filter(Project.studio_id == user.studio_id, Process.created_at >= month_start())
        .count()
    )
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "can_edit": user.role in ("owner", "editor"),
        "can_manage_invites": user.role == "owner",
        "can_manage_billing": user.role == "owner",
        "studio": {
            "id": user.studio.id,
            "name": user.studio.name,
            "plan_status": user.studio.plan_status,
            "monthly_limit": user.studio.monthly_limit,
            "used_this_month": used,
            "has_subscription": bool(user.studio.mp_preapproval_id),
        },
        "billing": billing_public_info(),
    }


@app.get("/projects")
def list_projects(user: User = Depends(current_user), db: Session = Depends(get_db)):
    projects = (
        db.query(Project)
        .filter(Project.studio_id == user.studio_id)
        .order_by(Project.created_at.desc())
        .all()
    )
    return [
        {
            "id": p.id,
            "name": p.name,
            "client": p.client,
            "address": p.address,
            "created_at": p.created_at.isoformat(),
            "process_count": len(p.processes),
        }
        for p in projects
    ]


@app.post("/projects")
def create_project(data: ProjectIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_can_edit(user)
    project = Project(
        studio_id=user.studio_id,
        name=data.name.strip(),
        client=(data.client or "").strip() or None,
        address=(data.address or "").strip() or None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name, "client": project.client, "address": project.address}


@app.patch("/projects/{project_id}")
@app.put("/projects/{project_id}")
@app.patch("/api/projects/{project_id}")
@app.put("/api/projects/{project_id}")
def update_project(project_id: int, data: ProjectIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_can_edit(user)
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")
    name = (data.name or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="El nombre de la obra es obligatorio.")
    project.name = name
    project.client = (data.client or "").strip() or None
    project.address = (data.address or "").strip() or None
    db.commit()
    db.refresh(project)
    return {
        "id": project.id,
        "name": project.name,
        "client": project.client,
        "address": project.address,
    }


@app.get("/projects/{project_id}/processes")
def list_processes(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")
    processes = (
        db.query(Process)
        .filter(Process.project_id == project.id)
        .order_by(Process.created_at.desc())
        .all()
    )
    return [serialize_process(process) for process in processes]


@app.get("/projects/{project_id}/export.csv")
@app.get("/api/projects/{project_id}/export.csv")
def export_project_csv(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    output = StringIO()
    # 10 columnas: no incluir audit_image_base64 (rompe Excel y pesa megas).
    output.write(
        "obra,cliente,tipo_plano,archivo,categoria,item,valor_texto,total_modulo,escala_detectada_ia,fecha\n"
    )
    processes = (
        db.query(Process)
        .filter(Process.project_id == project.id)
        .order_by(Process.created_at.asc())
        .all()
    )

    for process in processes:
        for item in process.items or []:
            nombre = str(item.get("nom", ""))
            categoria, detalle = (nombre.split(":", 1) + [""])[:2] if ":" in nombre else ("General", nombre)
            valor_txt = str(item.get("val", ""))
            row = [
                project.name,
                project.client or "",
                process.tipo_plano,
                process.filename,
                categoria.strip(),
                detalle.strip(),
                valor_txt,
                f"{float(process.total or 0):.2f}",
                str(process.escala_detectada or ""),
                process.created_at.isoformat(),
            ]
            escaped = ['"' + str(value).replace('"', '""') + '"' for value in row]
            output.write(",".join(escaped) + "\n")

    output.seek(0)
    filename = f"arq-ia-obra-{project.id}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/projects/{project_id}/export.pdf")
@app.get("/api/projects/{project_id}/export.pdf")
def export_project_pdf(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")
    processes = (
        db.query(Process)
        .filter(Process.project_id == project.id)
        .order_by(Process.created_at.asc())
        .all()
    )
    pdf_bytes = build_project_pdf_bytes(project, processes)
    filename = f"arq-ia-obra-{project.id}.pdf"
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/studio/invitations")
@app.get("/api/studio/invitations")
def list_studio_invitations(user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_studio_owner(user)
    rows = (
        db.query(StudioInvite)
        .filter(StudioInvite.studio_id == user.studio_id)
        .order_by(StudioInvite.created_at.desc())
        .limit(80)
        .all()
    )
    return [
        {
            "id": r.id,
            "email": r.email,
            "role": r.role,
            "created_at": r.created_at.isoformat(),
            "expires_at": r.expires_at.isoformat(),
            "accepted": r.accepted_at is not None,
        }
        for r in rows
    ]


@app.post("/studio/invitations")
@app.post("/api/studio/invitations")
def create_studio_invitation(data: InviteCreateIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_studio_owner(user)
    role = (data.role or "editor").strip().lower()
    if role not in ("editor", "viewer"):
        raise HTTPException(status_code=400, detail='Rol invalido. Usa "editor" o "viewer".')
    email = data.email.lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Ese email ya tiene cuenta. Inicia sesion; no hace falta invitacion.")
    now = datetime.now(timezone.utc)
    pending = (
        db.query(StudioInvite)
        .filter(
            StudioInvite.studio_id == user.studio_id,
            StudioInvite.email == email,
            StudioInvite.accepted_at.is_(None),
            StudioInvite.expires_at > now,
        )
        .first()
    )
    if pending:
        raise HTTPException(status_code=400, detail="Ya existe una invitacion pendiente para ese email.")
    raw = secrets.token_urlsafe(24)
    token_hash = hashlib.sha256(raw.encode()).hexdigest()
    inv = StudioInvite(
        studio_id=user.studio_id,
        email=email,
        role=role,
        token_hash=token_hash,
        expires_at=now + timedelta(days=7),
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    base = APP_URL.rstrip("/")
    invite_url = f"{base}/?invite={raw}"
    mail = send_invite_email(
        to=email,
        studio_name=user.studio.name if user.studio else "estudio",
        role=role,
        invite_url=invite_url,
    )
    return {
        "id": inv.id,
        "email": email,
        "role": role,
        "expires_at": inv.expires_at.isoformat(),
        "invite_url": invite_url,
        "email_sent": bool(mail.get("ok")),
        "email_error": None if mail.get("ok") else mail.get("error"),
        "email_configured": email_configured(),
    }


@app.delete("/studio/invitations/{invite_id}")
@app.delete("/api/studio/invitations/{invite_id}")
def delete_studio_invitation(invite_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_studio_owner(user)
    inv = db.get(StudioInvite, invite_id)
    if not inv or inv.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Invitacion no encontrada.")
    if inv.accepted_at:
        raise HTTPException(status_code=400, detail="Esta invitacion ya fue aceptada.")
    db.delete(inv)
    db.commit()
    return {"ok": True}


@app.get("/invites/verify")
@app.get("/api/invites/verify")
def verify_invitation(token: str, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(token.strip().encode()).hexdigest()
    inv = db.query(StudioInvite).filter(StudioInvite.token_hash == token_hash).first()
    now = datetime.now(timezone.utc)
    if not inv or inv.accepted_at or inv.expires_at < now:
        raise HTTPException(status_code=404, detail="Invitacion invalida o vencida.")
    studio = db.get(Studio, inv.studio_id)
    return {"studio_name": studio.name if studio else "", "email": inv.email, "role": inv.role}


@app.post("/auth/register-invite")
@app.post("/api/auth/register-invite")
def register_with_invitation(data: RegisterInviteIn, db: Session = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="La clave debe tener al menos 8 caracteres.")
    if not data.name.strip():
        raise HTTPException(status_code=400, detail="Ingresa tu nombre.")
    token_hash = hashlib.sha256(data.token.strip().encode()).hexdigest()
    inv = db.query(StudioInvite).filter(StudioInvite.token_hash == token_hash).first()
    now = datetime.now(timezone.utc)
    if not inv or inv.accepted_at or inv.expires_at < now:
        raise HTTPException(status_code=400, detail="Invitacion invalida o vencida.")
    email = inv.email.lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Ese email ya tiene cuenta. Inicia sesion.")
    user = User(
        studio_id=inv.studio_id,
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(data.password),
        role=inv.role,
    )
    db.add(user)
    inv.accepted_at = now
    db.commit()
    db.refresh(user)
    return {"token": create_token(user.id), "user": {"name": user.name, "email": user.email}}


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_can_edit(user)
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    db.query(Process).filter(Process.project_id == project.id).delete()
    db.delete(project)
    db.commit()
    return {"ok": True}


@app.delete("/processes/{process_id}")
def delete_process(process_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_can_edit(user)
    process = db.get(Process, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Analisis no encontrado.")
    project = db.get(Project, process.project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Analisis no encontrado.")

    db.delete(process)
    db.commit()
    return {"ok": True}


def _parse_altura_muro(altura_muro: float) -> float:
    try:
        h = float(altura_muro)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Altura de muro invalida.") from exc
    if h < 1.8 or h > 6.0:
        raise HTTPException(status_code=400, detail="Altura de muro debe estar entre 1.8 y 6.0 metros.")
    return h


def _parse_sistema_muro(sistema_muro: str) -> str:
    sistema = (sistema_muro or "ladrillo_hueco_12").strip().lower()
    if sistema not in ("ladrillo_hueco_12", "ladrillo_comun_12"):
        raise HTTPException(
            status_code=400,
            detail='Sistema de muro invalido. Usa "ladrillo_hueco_12" o "ladrillo_comun_12".',
        )
    return sistema


@app.post("/projects/{project_id}/calcular")
async def calcular_en_obra(
    project_id: int,
    file: UploadFile = File(...),
    referencia_metros: float = Form(...),
    sistema_muro: str = Form("ladrillo_hueco_12"),
    tipo_plano: str = Form("muros"),
    altura_muro: float = Form(2.60),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    require_can_edit(user)
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    ensure_usage_available(db, user.studio)
    ensure_module_allowed(user.studio, tipo_plano)
    contenido = await file.read()
    validate_upload(file, contenido)
    sistema = _parse_sistema_muro(sistema_muro)
    altura = _parse_altura_muro(altura_muro)

    try:
        resultados = procesar_plano_ia(
            contenido,
            referencia_metros,
            sistema,
            tipo_plano,
            altura_muro=altura,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar la imagen. Revisa formato, tamano y que el servicio de OCR este disponible.",
        ) from exc

    result_meta = {
        "escala_modo": resultados.get("escala_modo"),
        "metros_referencia_usados": resultados.get("metros_referencia_usados"),
        "precios_info": resultados.get("precios_info"),
        "avisos": resultados.get("avisos") or [],
        "sistema_muro": sistema,
        "altura_muro": altura,
    }
    process = Process(
        project_id=project.id,
        user_id=user.id,
        tipo_plano=tipo_plano,
        filename=file.filename or "plano",
        content_type=file.content_type or "application/octet-stream",
        original_file=contenido,
        audit_image_base64=resultados["imagen"],
        items=resultados["items"],
        total=float(resultados.get("total") or 0),
        escala_detectada=resultados.get("escala_detectada"),
        result_meta=result_meta,
    )
    db.add(process)
    db.commit()
    db.refresh(process)
    return serialize_process(process)


@app.post("/calcular")
@app.post("/api/calcular")
async def calcular_demo(
    request: Request,
    file: UploadFile = File(...),
    referencia_metros: float = Form(...),
    sistema_muro: str = Form("ladrillo_hueco_12"),
    tipo_plano: str = Form("muros"),
    altura_muro: float = Form(2.60),
):
    contenido = await file.read()
    validate_upload(file, contenido)
    check_demo_rate_limit(request)
    sistema = _parse_sistema_muro(sistema_muro)
    altura = _parse_altura_muro(altura_muro)
    try:
        return procesar_plano_ia(
            contenido,
            referencia_metros,
            sistema,
            tipo_plano,
            altura_muro=altura,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar la imagen. Proba con otro PNG/JPG o mas tarde.",
        ) from exc


def _apply_preapproval_status(studio: Studio, status: str, preapproval_id: str | None = None):
    status_norm = (status or "").strip().lower()
    if preapproval_id:
        studio.mp_preapproval_id = preapproval_id
    if status_norm == "authorized":
        studio.plan_status = "active"
        studio.monthly_limit = PAID_MONTHLY_LIMIT
    elif status_norm in {"paused", "cancelled", "canceled"}:
        studio.plan_status = "inactive" if status_norm.startswith("cancel") else "paused"
        if status_norm.startswith("cancel"):
            studio.monthly_limit = FREE_MONTHLY_LIMIT


def _studio_from_preapproval(db: Session, preapproval: dict) -> Studio | None:
    pref = str(preapproval.get("external_reference") or "").strip()
    if pref.startswith("studio_"):
        pref = pref.removeprefix("studio_")
    if pref.isdigit():
        studio = db.get(Studio, int(pref))
        if studio:
            return studio
    pre_id = preapproval.get("id")
    if pre_id:
        return db.query(Studio).filter(Studio.mp_preapproval_id == str(pre_id)).first()
    return None


@app.get("/billing/info")
@app.get("/api/billing/info")
def billing_info():
    return billing_public_info()


@app.post("/billing/create-checkout-session")
@app.post("/api/billing/create-checkout-session")
def create_checkout_session(user: User = Depends(current_user), db: Session = Depends(get_db)):
    """Crea suscripcion Mercado Pago y devuelve init_point (checkout ARS)."""
    require_can_bill(user)
    if not mp_configured():
        raise HTTPException(
            status_code=503,
            detail="Mercado Pago todavia no esta configurado. Pedile al admin que cargue MP_ACCESS_TOKEN.",
        )

    try:
        # MP preapproval rechaza back_url con querystring en varios casos.
        back_url = f"{APP_URL.rstrip('/')}/"
        sub = create_subscription_checkout(
            payer_email=user.email,
            external_reference=f"studio_{user.studio_id}",
            back_url=back_url,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    init_point = sub.get("init_point") or sub.get("sandbox_init_point")
    if not init_point:
        raise HTTPException(
            status_code=502,
            detail="Mercado Pago no devolvio enlace de pago. Revisa el plan o el monto configurado.",
        )

    studio = user.studio
    if sub.get("id"):
        studio.mp_preapproval_id = str(sub["id"])
        db.commit()

    return {"url": init_point, "provider": "mercadopago", "preapproval_id": sub.get("id")}


@app.post("/billing/create-portal-session")
@app.post("/api/billing/create-portal-session")
def create_portal_session(data: BillingPortalIn, user: User = Depends(current_user)):
    """Mercado Pago no tiene Customer Portal: reabre el checkout de la suscripcion."""
    require_can_bill(user)
    if not user.studio.mp_preapproval_id:
        raise HTTPException(status_code=404, detail="Este estudio aun no tiene suscripcion de Mercado Pago.")
    try:
        pre = get_preapproval(user.studio.mp_preapproval_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    url = pre.get("init_point") or pre.get("sandbox_init_point") or (data.return_url or APP_URL)
    return {"url": url, "provider": "mercadopago", "status": pre.get("status")}


@app.post("/billing/cancel")
@app.post("/api/billing/cancel")
def cancel_billing(user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_can_bill(user)
    pre_id = user.studio.mp_preapproval_id
    if not pre_id:
        raise HTTPException(status_code=404, detail="No hay suscripcion activa para cancelar.")
    try:
        cancel_preapproval(pre_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    studio = user.studio
    _apply_preapproval_status(studio, "cancelled", pre_id)
    db.commit()
    return {"ok": True, "plan_status": studio.plan_status}


@app.post("/billing/webhook")
@app.post("/api/billing/webhook")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook MP: subscription_preapproval (y legacy topic/resource)."""
    body = await request.json()
    x_signature = request.headers.get("x-signature", "")
    x_request_id = request.headers.get("x-request-id", "")

    event_type = body.get("type") or body.get("action") or body.get("topic") or ""
    data_id = str((body.get("data") or {}).get("id") or body.get("id") or "")
    if not data_id and isinstance(body.get("resource"), str) and "/" in body["resource"]:
        data_id = body["resource"].rstrip("/").split("/")[-1]

    # Querystring style: ?data.id=...
    if not data_id:
        data_id = str(request.query_params.get("data.id") or request.query_params.get("id") or "")

    if not verify_webhook_signature(x_signature=x_signature, x_request_id=x_request_id, data_id=data_id):
        raise HTTPException(status_code=401, detail="Firma de webhook invalida.")

    # Solo sincronizamos ciclo de vida de suscripcion (preapproval).
    interesting = (
        "subscription_preapproval" in str(event_type)
        or str(event_type) in {"subscription_preapproval", "preapproval"}
        or str(body.get("topic", "")) in {"subscription_preapproval", "preapproval"}
    )
    if not interesting and not data_id:
        return {"received": True, "ignored": True}

    if not data_id:
        return {"received": True, "ignored": True}

    try:
        preapproval = get_preapproval(data_id)
    except RuntimeError:
        # Puede ser authorized_payment u otro recurso; ignoramos sin fallar el retry storm.
        return {"received": True, "ignored": True}

    studio = _studio_from_preapproval(db, preapproval)
    if not studio:
        return {"received": True, "studio": None}

    _apply_preapproval_status(studio, str(preapproval.get("status") or ""), str(preapproval.get("id") or data_id))
    db.commit()
    return {"received": True, "studio_id": studio.id, "status": studio.plan_status}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
