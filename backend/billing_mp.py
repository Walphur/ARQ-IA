"""Cobros recurrentes con Mercado Pago (Argentina / ARS).

Flujo:
1) POST /preapproval (status pending) → init_point (checkout hospedado)
2) Webhook subscription_preapproval → GET /preapproval/{id} → activar/pausar estudio
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import urllib.error
import urllib.request
from typing import Any


MP_API = "https://api.mercadopago.com"
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "").strip()
MP_WEBHOOK_SECRET = os.getenv("MP_WEBHOOK_SECRET", "").strip()
MP_PREAPPROVAL_PLAN_ID = os.getenv("MP_PREAPPROVAL_PLAN_ID", "").strip()
MP_AMOUNT_ARS = float(os.getenv("MP_AMOUNT_ARS", "14999"))
MP_REASON = os.getenv("MP_REASON", "ARQ-IA Plan Pro (mensual)")
MP_CURRENCY = os.getenv("MP_CURRENCY", "ARS")


def mp_configured() -> bool:
    return bool(MP_ACCESS_TOKEN) and (bool(MP_PREAPPROVAL_PLAN_ID) or MP_AMOUNT_ARS > 0)


def _request(method: str, path: str, body: dict | None = None) -> dict[str, Any]:
    if not MP_ACCESS_TOKEN:
        raise RuntimeError("MP_ACCESS_TOKEN no configurado")
    data = None
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{MP_API}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Mercado Pago HTTP {exc.code}: {detail}") from exc


def _sanitize_back_url(back_url: str) -> str:
    url = (back_url or "").strip()
    if not url:
        raise RuntimeError("back_url vacia: configura APP_URL=https://arq-ia.pro en Render.")
    if "://" not in url:
        url = f"https://{url.lstrip('/')}"
    # MP suele rechazar query/fragment en preapproval.
    url = url.split("#", 1)[0].split("?", 1)[0]
    if not url.endswith("/"):
        url = f"{url}/"
    if not (url.startswith("http://") or url.startswith("https://")):
        raise RuntimeError(f"back_url invalida: {back_url!r}")
    return url


def create_subscription_checkout(
    *,
    payer_email: str,
    external_reference: str,
    back_url: str,
) -> dict[str, Any]:
    """Crea preapproval pending y devuelve init_point para redirigir al usuario."""
    safe_back_url = _sanitize_back_url(back_url)
    payload: dict[str, Any] = {
        "reason": MP_REASON,
        "external_reference": str(external_reference),
        "payer_email": payer_email,
        "back_url": safe_back_url,
        "status": "pending",
    }
    if MP_PREAPPROVAL_PLAN_ID:
        payload["preapproval_plan_id"] = MP_PREAPPROVAL_PLAN_ID
    else:
        payload["auto_recurring"] = {
            "frequency": 1,
            "frequency_type": "months",
            "transaction_amount": MP_AMOUNT_ARS,
            "currency_id": MP_CURRENCY,
        }
    return _request("POST", "/preapproval", payload)


def get_preapproval(preapproval_id: str) -> dict[str, Any]:
    return _request("GET", f"/preapproval/{preapproval_id}")


def cancel_preapproval(preapproval_id: str) -> dict[str, Any]:
    return _request("PUT", f"/preapproval/{preapproval_id}", {"status": "cancelled"})


def verify_webhook_signature(
    *,
    x_signature: str,
    x_request_id: str,
    data_id: str,
) -> bool:
    """Valida x-signature de notificaciones MP. Si no hay secret, acepta (dev)."""
    if not MP_WEBHOOK_SECRET:
        return True
    if not x_signature or not data_id:
        return False
    parts = {}
    for chunk in x_signature.split(","):
        if "=" in chunk:
            k, v = chunk.split("=", 1)
            parts[k.strip()] = v.strip()
    ts = parts.get("ts", "")
    v1 = parts.get("v1", "")
    if not ts or not v1:
        return False
    manifest = f"id:{data_id};request-id:{x_request_id};ts:{ts};"
    expected = hmac.new(
        MP_WEBHOOK_SECRET.encode("utf-8"),
        manifest.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, v1)


def billing_public_info() -> dict[str, Any]:
    free_limit = int(os.getenv("FREE_MONTHLY_LIMIT", "20"))
    paid_limit = int(os.getenv("PAID_MONTHLY_LIMIT", "200"))
    return {
        "provider": "mercadopago",
        "configured": mp_configured(),
        "currency": MP_CURRENCY,
        "amount": MP_AMOUNT_ARS if not MP_PREAPPROVAL_PLAN_ID else None,
        "reason": MP_REASON,
        "has_plan_id": bool(MP_PREAPPROVAL_PLAN_ID),
        "free_monthly_limit": free_limit,
        "paid_monthly_limit": paid_limit,
    }
