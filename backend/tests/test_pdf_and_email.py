"""PDF Unicode + helpers de email (sin red)."""

from types import SimpleNamespace
from datetime import datetime, timezone

import presupuesto_pdf
import email_service


def test_pdf_incluye_acentos():
    project = SimpleNamespace(name="Obra Niño", client="José Pérez", address="Av. Córdoba 123")
    processes = [
        SimpleNamespace(
            tipo_plano="muros",
            filename="plano-níño.png",
            created_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
            escala_detectada=5.0,
            result_meta={"sistema_muro": "ladrillo_hueco_12", "altura_muro": 2.6},
            total=12345.0,
            items=[{"nom": "Mano Obra: Muros", "val": 1000}],
        )
    ]
    raw = presupuesto_pdf.build_project_pdf_bytes(project, processes)
    assert isinstance(raw, (bytes, bytearray))
    assert raw[:4] == b"%PDF"
    assert len(raw) > 500


def test_email_not_configured(monkeypatch):
    monkeypatch.setattr(email_service, "RESEND_API_KEY", "")
    r = email_service.send_invite_email(
        to="a@b.com",
        studio_name="Studio",
        role="editor",
        invite_url="https://arq-ia.pro/?invite=x",
    )
    assert r["ok"] is False
    assert r.get("skipped") is True
