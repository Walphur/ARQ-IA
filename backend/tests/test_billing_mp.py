"""Tests unitarios de helpers Mercado Pago (sin red)."""

import hashlib
import hmac

import billing_mp


def test_verify_webhook_signature_ok(monkeypatch):
    monkeypatch.setattr(billing_mp, "MP_WEBHOOK_SECRET", "sec-test")
    data_id = "abc123"
    request_id = "req-1"
    ts = "1700000000"
    manifest = f"id:{data_id};request-id:{request_id};ts:{ts};"
    v1 = hmac.new(b"sec-test", manifest.encode(), hashlib.sha256).hexdigest()
    assert billing_mp.verify_webhook_signature(
        x_signature=f"ts={ts},v1={v1}",
        x_request_id=request_id,
        data_id=data_id,
    )


def test_verify_webhook_signature_bad(monkeypatch):
    monkeypatch.setattr(billing_mp, "MP_WEBHOOK_SECRET", "sec-test")
    assert not billing_mp.verify_webhook_signature(
        x_signature="ts=1,v1=deadbeef",
        x_request_id="r",
        data_id="x",
    )


def test_billing_public_info_shape():
    info = billing_mp.billing_public_info()
    assert info["provider"] == "mercadopago"
    assert "configured" in info
    assert info["currency"]


def test_mp_configured_requires_token(monkeypatch):
    monkeypatch.setattr(billing_mp, "MP_ACCESS_TOKEN", "")
    assert not billing_mp.mp_configured()
    monkeypatch.setattr(billing_mp, "MP_ACCESS_TOKEN", "APP_USR-test")
    monkeypatch.setattr(billing_mp, "MP_AMOUNT_ARS", 1000.0)
    monkeypatch.setattr(billing_mp, "MP_PREAPPROVAL_PLAN_ID", "")
    assert billing_mp.mp_configured()


def test_sanitize_back_url_strips_query():
    assert billing_mp._sanitize_back_url("https://arq-ia.pro?billing=success") == "https://arq-ia.pro/"
    assert billing_mp._sanitize_back_url("arq-ia.pro") == "https://arq-ia.pro/"


def test_billing_info_incluye_limites(monkeypatch):
    monkeypatch.setenv("FREE_MONTHLY_LIMIT", "20")
    monkeypatch.setenv("PAID_MONTHLY_LIMIT", "200")
    info = billing_mp.billing_public_info()
    assert info["free_monthly_limit"] == 20
    assert info["paid_monthly_limit"] == 200
