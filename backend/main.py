import base64
import hashlib
import hmac
import json
import os
import time
from io import StringIO
from datetime import datetime, timezone
from typing import Annotated

import stripe
import uvicorn
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Text, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker
from sqlalchemy.types import JSON

from motor_ia import procesar_plano_ia


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


DATABASE_URL = normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///./arq_ia.db"))
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
APP_URL = os.getenv("APP_URL", "http://localhost:3000")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")
FREE_MONTHLY_LIMIT = int(os.getenv("FREE_MONTHLY_LIMIT", "20"))
PAID_MONTHLY_LIMIT = int(os.getenv("PAID_MONTHLY_LIMIT", "500"))
APP_VERSION = os.getenv("APP_VERSION", "dev")


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
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "15"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


class Studio(Base):
    __tablename__ = "studios"

    id = Column(Integer, primary_key=True)
    name = Column(String(180), nullable=False)
    plan_status = Column(String(40), nullable=False, default="trial")
    monthly_limit = Column(Integer, nullable=False, default=FREE_MONTHLY_LIMIT)
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="studio")
    projects = relationship("Project", back_populates="studio")


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
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    project = relationship("Project", back_populates="processes")
    user = relationship("User", back_populates="processes")


class RegisterIn(BaseModel):
    studio_name: str
    name: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class ProjectIn(BaseModel):
    name: str
    client: str | None = None
    address: str | None = None


class BillingPortalIn(BaseModel):
    return_url: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


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
        "created_at": process.created_at.isoformat(),
        "user": process.user.name if process.user else None,
    }


def validate_upload(file: UploadFile, contenido: bytes):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Formato no soportado. Subi una imagen PNG, JPG o WEBP.")
    if len(contenido) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"El archivo supera el limite de {MAX_UPLOAD_MB} MB.")


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


@app.get("/")
async def root():
    return {"status": "ok", "service": "arq-ia-backend", "version": APP_VERSION, "health": "/health", "register": "/auth/register", "login": "/auth/login"}


@app.get("/api/health")
async def health_api():
    return {"status": "ok", "version": APP_VERSION}

@app.get("/health")
async def health():
    return {"status": "ok", "version": APP_VERSION}


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
        "studio": {
            "id": user.studio.id,
            "name": user.studio.name,
            "plan_status": user.studio.plan_status,
            "monthly_limit": user.studio.monthly_limit,
            "used_this_month": used,
        },
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
def export_project_csv(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    output = StringIO()
    output.write("obra,cliente,tipo_plano,archivo,categoria,item,valor_texto,total_numerico,escala_detectada_ia,fecha\n")
    processes = (
        db.query(Process)
        .filter(Process.project_id == project.id)
        .order_by(Process.created_at.asc())
        .all()
    )


    for process in processes:
        for item in process.items:
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
            escaped = ['"' + value.replace('"', '""') + '"' for value in row]
            output.write(",".join(escaped) + "\n")

    output.seek(0)
    filename = f"arq-ia-obra-{project.id}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    db.query(Process).filter(Process.project_id == project.id).delete()
    db.delete(project)
    db.commit()
    return {"ok": True}


@app.delete("/processes/{process_id}")
def delete_process(process_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    process = db.get(Process, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Analisis no encontrado.")
    project = db.get(Project, process.project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Analisis no encontrado.")

    db.delete(process)
    db.commit()
    return {"ok": True}


@app.post("/projects/{project_id}/calcular")
async def calcular_en_obra(
    project_id: int,
    file: UploadFile = File(...),
    referencia_metros: float = Form(...),
    sistema_muro: str = Form("ladrillo_hueco_12"),
    tipo_plano: str = Form("muros"),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)
    if not project or project.studio_id != user.studio_id:
        raise HTTPException(status_code=404, detail="Obra no encontrada.")

    ensure_usage_available(db, user.studio)
    contenido = await file.read()
    validate_upload(file, contenido)

    try:
        resultados = procesar_plano_ia(contenido, referencia_metros, sistema_muro, tipo_plano)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="No se pudo procesar el plano.") from exc

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
    )
    db.add(process)
    db.commit()
    db.refresh(process)
    return serialize_process(process)


@app.post("/calcular")
async def calcular_demo(
    file: UploadFile = File(...),
    referencia_metros: float = Form(...),
    sistema_muro: str = Form("ladrillo_hueco_12"),
    tipo_plano: str = Form("muros"),
):
    contenido = await file.read()
    validate_upload(file, contenido)
    try:
        return procesar_plano_ia(contenido, referencia_metros, sistema_muro, tipo_plano)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="No se pudo procesar el plano.") from exc


@app.post("/billing/create-checkout-session")
def create_checkout_session(user: User = Depends(current_user)):
    if not STRIPE_SECRET_KEY or not STRIPE_PRICE_ID:
        raise HTTPException(status_code=503, detail="Stripe todavia no esta configurado.")

    customer_id = user.studio.stripe_customer_id
    kwargs = {}
    if customer_id:
        kwargs["customer"] = customer_id
    else:
        kwargs["customer_email"] = user.email

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
        success_url=f"{APP_URL}?billing=success",
        cancel_url=f"{APP_URL}?billing=cancel",
        metadata={"studio_id": str(user.studio_id)},
        **kwargs,
    )
    return {"url": session.url}


@app.post("/billing/create-portal-session")
def create_portal_session(data: BillingPortalIn, user: User = Depends(current_user)):
    if not STRIPE_SECRET_KEY or not user.studio.stripe_customer_id:
        raise HTTPException(status_code=503, detail="No hay cliente de Stripe configurado para este estudio.")
    session = stripe.billing_portal.Session.create(
        customer=user.studio.stripe_customer_id,
        return_url=data.return_url or APP_URL,
    )
    return {"url": session.url}


@app.post("/billing/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook no configurado.")

    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, signature, STRIPE_WEBHOOK_SECRET)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Webhook invalido.") from exc

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        studio_id = data.get("metadata", {}).get("studio_id")
        if studio_id:
            studio = db.get(Studio, int(studio_id))
            if studio:
                studio.stripe_customer_id = data.get("customer")
                studio.stripe_subscription_id = data.get("subscription")
                studio.plan_status = "active"
                studio.monthly_limit = PAID_MONTHLY_LIMIT
                db.commit()

    if event_type in {"customer.subscription.deleted", "customer.subscription.paused"}:
        subscription_id = data.get("id")
        studio = db.query(Studio).filter(Studio.stripe_subscription_id == subscription_id).first()
        if studio:
            studio.plan_status = "inactive"
            studio.monthly_limit = FREE_MONTHLY_LIMIT
            db.commit()

    if event_type in {"customer.subscription.updated", "invoice.payment_succeeded"}:
        subscription_id = data.get("subscription") or data.get("id")
        studio = db.query(Studio).filter(Studio.stripe_subscription_id == subscription_id).first()
        if studio:
            studio.plan_status = "active"
            studio.monthly_limit = PAID_MONTHLY_LIMIT
            db.commit()

    return {"received": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
