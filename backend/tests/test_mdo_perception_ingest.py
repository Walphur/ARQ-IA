"""E03-F01 Fase 2 — dual-write Perception → MDO en /calcular (Process legacy intacto)."""

from __future__ import annotations

import cv2
import numpy as np

from tests.mdo_test_utils import auth, mdo_client, register_and_project


def _png_muros():
    img = np.ones((420, 520, 3), dtype=np.uint8) * 255
    cv2.line(img, (40, 360), (220, 360), (0, 255, 0), 8)
    cv2.putText(img, "5", (235, 368), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    cv2.line(img, (80, 80), (80, 300), (0, 0, 255), 5)
    cv2.rectangle(img, (120, 100), (280, 220), (200, 200, 200), -1)
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_calcular_dual_writes_mdo_and_keeps_process(mdo_client):
    token, project_id = register_and_project(mdo_client, email="perc.mdo@example.com")
    h = auth(token)
    png = _png_muros()
    res = mdo_client.post(
        f"/projects/{project_id}/calcular",
        headers=h,
        files={"file": ("plano.png", png, "image/png")},
        data={
            "referencia_metros": "5",
            "sistema_muro": "ladrillo_hueco_12",
            "tipo_plano": "muros",
            "altura_muro": "2.60",
        },
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["items"]
    assert "total" in body
    meta = body.get("meta") or {}
    mdo = meta.get("mdo") or {}
    assert mdo.get("ok") is True, mdo
    assert mdo.get("version_id")
    assert mdo.get("building_id")
    assert mdo.get("level_id")
    assert mdo.get("space_ids")
    assert mdo.get("element_ids")

    # Tree MDO refleja entidades
    tree = mdo_client.get(f"/v1/mdo/versions/{mdo['version_id']}/tree", headers=h).json()
    assert len(tree["buildings"]) >= 1
    assert len(tree["levels"]) >= 1
    assert len(tree["spaces"]) >= 1
    assert len(tree["elements"]) >= 1
    # Sin precios en parameter sets
    for ps in tree["parameter_sets"]:
        blob = str(ps.get("data") or {})
        assert "mo_muro" not in blob
        assert "mat_" not in blob

    # Process listado legacy sigue
    procs = mdo_client.get(f"/projects/{project_id}/processes", headers=h).json()
    assert len(procs) >= 1
    assert procs[0]["id"] == body["id"]


def test_calcular_idempotent_upsert_on_recalcular(mdo_client):
    token, project_id = register_and_project(mdo_client, email="perc.recalc@example.com")
    h = auth(token)
    png = _png_muros()
    first = mdo_client.post(
        f"/projects/{project_id}/calcular",
        headers=h,
        files={"file": ("plano.png", png, "image/png")},
        data={
            "referencia_metros": "5",
            "sistema_muro": "ladrillo_hueco_12",
            "tipo_plano": "muros",
            "altura_muro": "2.60",
        },
    )
    assert first.status_code == 200, first.text
    process_id = first.json()["id"]
    mdo1 = (first.json().get("meta") or {}).get("mdo") or {}

    second = mdo_client.post(
        f"/projects/{project_id}/processes/{process_id}/recalcular",
        headers=h,
        data={
            "referencia_metros": "5",
            "sistema_muro": "ladrillo_hueco_12",
            "altura_muro": "2.60",
            "forzar_escala_manual": "1",
        },
    )
    assert second.status_code == 200, second.text
    mdo2 = (second.json().get("meta") or {}).get("mdo") or {}
    assert mdo2.get("ok") is True
    assert mdo2.get("version_id") == mdo1.get("version_id")
    assert mdo2.get("building_id") == mdo1.get("building_id")
