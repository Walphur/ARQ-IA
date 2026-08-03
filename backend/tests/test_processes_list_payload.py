"""Listado de procesos debe ser liviano (sin base64) para no tumbar el FE."""

from __future__ import annotations

from tests.mdo_test_utils import auth, mdo_client, register_and_project


def test_list_processes_omits_audit_image(mdo_client, monkeypatch):
    token, project_id = register_and_project(mdo_client, email="proc.list@example.com")
    headers = auth(token)

    # Seed un Process directo en DB (evita OCR).
    import main

    db = main.SessionLocal()
    try:
        proc = main.Process(
            project_id=project_id,
            user_id=db.query(main.User).filter(main.User.email == "proc.list@example.com").one().id,
            tipo_plano="muros",
            filename="plano.png",
            content_type="image/png",
            original_file=b"fake-png-bytes",
            items=[{"nom": "Muros", "val": 1000}],
            total=1000,
            audit_image_base64="a" * 5000,
            escala_detectada=50.0,
            result_meta={"ok": True},
        )
        db.add(proc)
        db.commit()
        db.refresh(proc)
        process_id = proc.id
    finally:
        db.close()

    listing = mdo_client.get(f"/projects/{project_id}/processes", headers=headers)
    assert listing.status_code == 200, listing.text
    body = listing.json()
    assert len(body) == 1
    assert body[0]["id"] == process_id
    assert body[0]["has_imagen"] is True
    assert body[0]["imagen"] is None
    assert body[0]["total"] == 1000
    assert body[0]["items"][0]["nom"] == "Muros"

    detail = mdo_client.get(f"/processes/{process_id}", headers=headers)
    assert detail.status_code == 200, detail.text
    full = detail.json()
    assert full["imagen"] == "a" * 5000
    assert full["has_imagen"] is True
