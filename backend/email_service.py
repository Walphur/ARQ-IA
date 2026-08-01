"""Envio de email via Resend (HTTPS). Si no hay API key, no envia (dev/fallback)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


RESEND_API_KEY = os.getenv("RESEND_API_KEY", "").strip()
EMAIL_FROM = os.getenv("EMAIL_FROM", "ARQ-IA <onboarding@resend.dev>").strip()
APP_NAME = os.getenv("APP_NAME", "ARQ-IA").strip()


def email_configured() -> bool:
    return bool(RESEND_API_KEY and EMAIL_FROM)


def send_email(*, to: str, subject: str, html: str, text: str | None = None) -> dict[str, Any]:
    """Envia un email. Devuelve {ok, id?} o {ok: False, error}."""
    if not email_configured():
        return {"ok": False, "error": "Email no configurado (falta RESEND_API_KEY).", "skipped": True}

    payload: dict[str, Any] = {
        "from": EMAIL_FROM,
        "to": [to],
        "subject": subject,
        "html": html,
    }
    if text:
        payload["text"] = text

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8") or "{}")
            return {"ok": True, "id": body.get("id")}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "error": f"Resend HTTP {exc.code}: {detail}"}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


def send_invite_email(*, to: str, studio_name: str, role: str, invite_url: str) -> dict[str, Any]:
    role_label = "solo lectura" if role == "viewer" else "editor"
    subject = f"Invitacion a {studio_name} en {APP_NAME}"
    text = (
        f"Te invitaron al estudio {studio_name} en {APP_NAME} como {role_label}.\n\n"
        f"Acepta la invitacion aqui:\n{invite_url}\n\n"
        f"El enlace vence en 7 dias."
    )
    html = f"""
    <div style="font-family:Arial,sans-serif;line-height:1.5;color:#111">
      <h2 style="margin:0 0 12px">{APP_NAME}</h2>
      <p>Te invitaron al estudio <strong>{studio_name}</strong> como <strong>{role_label}</strong>.</p>
      <p><a href="{invite_url}" style="display:inline-block;background:#d4af37;color:#111;padding:10px 16px;text-decoration:none;border-radius:6px;font-weight:700">Aceptar invitacion</a></p>
      <p style="color:#555;font-size:13px">O copia este enlace:<br/>{invite_url}</p>
      <p style="color:#777;font-size:12px">El enlace vence en 7 dias.</p>
    </div>
    """
    return send_email(to=to, subject=subject, html=html, text=text)


def send_password_reset_email(*, to: str, reset_url: str) -> dict[str, Any]:
    subject = f"Restablecer clave — {APP_NAME}"
    text = (
        f"Recibimos un pedido para restablecer tu clave en {APP_NAME}.\n\n"
        f"Usa este enlace (vale 1 hora):\n{reset_url}\n\n"
        f"Si no fuiste vos, ignora este mensaje."
    )
    html = f"""
    <div style="font-family:Arial,sans-serif;line-height:1.5;color:#111">
      <h2 style="margin:0 0 12px">{APP_NAME}</h2>
      <p>Recibimos un pedido para restablecer tu clave.</p>
      <p><a href="{reset_url}" style="display:inline-block;background:#d4af37;color:#111;padding:10px 16px;text-decoration:none;border-radius:6px;font-weight:700">Elegir nueva clave</a></p>
      <p style="color:#555;font-size:13px">O copia este enlace:<br/>{reset_url}</p>
      <p style="color:#777;font-size:12px">El enlace vence en 1 hora. Si no pediste esto, ignora el mensaje.</p>
    </div>
    """
    return send_email(to=to, subject=subject, html=html, text=text)
