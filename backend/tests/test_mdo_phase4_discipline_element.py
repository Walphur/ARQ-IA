"""Fase 4 — Discipline + Element tipado: integridad, tenant, auditoría."""

from tests.mdo_test_utils import auth, mdo_client, register_and_project


def _vid(client, token, project_id) -> str:
    return client.post(
        f"/v1/mdo/projects/{project_id}/ensure", headers=auth(token)
    ).json()["version"]["id"]


def test_discipline_replaces_system_with_audit(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = _vid(mdo_client, token, project_id)
    res = mdo_client.post(
        f"/v1/mdo/versions/{vid}/disciplines",
        headers=h,
        json={
            "code": "structure",
            "display_name": "Estructura",
            "external_id": "disc-str",
        },
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["code"] == "structure"
    assert body["display_name"] == "Estructura"
    assert body["external_id"] == "disc-str"
    assert body["created_by"] is not None
    assert body["studio_id"]
    assert body["project_id"] == project_id
    tree = mdo_client.get(f"/v1/mdo/versions/{vid}/tree", headers=h).json()
    assert len(tree["disciplines"]) == 1
    # No endpoint System
    assert mdo_client.post(f"/v1/mdo/versions/{vid}/systems", headers=h, json={}).status_code == 404


def test_element_split_classification_integrity(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = _vid(mdo_client, token, project_id)
    disc = mdo_client.post(
        f"/v1/mdo/versions/{vid}/disciplines",
        headers=h,
        json={"code": "architecture", "display_name": "Arquitectura"},
    ).json()

    bad = mdo_client.post(
        f"/v1/mdo/versions/{vid}/elements",
        headers=h,
        json={
            "discipline_code": "architecture",
            "element_type": "WALL",
            "display_name": "Muro malo",
        },
    )
    assert bad.status_code == 400

    el = mdo_client.post(
        f"/v1/mdo/versions/{vid}/elements",
        headers=h,
        json={
            "discipline_code": "architecture",
            "element_type": "wall.masonry.brick",
            "display_name": "Muro Living",
            "discipline_id": disc["id"],
            "external_id": "el-1",
        },
    )
    assert el.status_code == 200, el.text
    body = el.json()
    assert body["discipline_code"] == "architecture"
    assert body["element_type"] == "wall.masonry.brick"
    assert body["created_by"] is not None
    assert body["updated_by"] is not None
    assert body["external_id"] == "el-1"
    assert body["project_id"] == project_id


def test_element_discipline_mismatch_rejected(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = _vid(mdo_client, token, project_id)
    disc = mdo_client.post(
        f"/v1/mdo/versions/{vid}/disciplines",
        headers=h,
        json={"code": "structure", "display_name": "Estructura"},
    ).json()
    res = mdo_client.post(
        f"/v1/mdo/versions/{vid}/elements",
        headers=h,
        json={
            "discipline_code": "architecture",
            "element_type": "wall.drywall",
            "display_name": "Mismatch",
            "discipline_id": disc["id"],
        },
    )
    assert res.status_code == 400


def test_element_tenant_isolation_and_soft_delete(mdo_client):
    token_a, project_a = register_and_project(mdo_client, email="el.a@example.com")
    h_a = auth(token_a)
    vid = _vid(mdo_client, token_a, project_a)
    el = mdo_client.post(
        f"/v1/mdo/versions/{vid}/elements",
        headers=h_a,
        json={
            "discipline_code": "architecture",
            "element_type": "opening.door",
            "display_name": "Puerta",
        },
    ).json()

    token_b, _ = register_and_project(mdo_client, email="el.b@example.com")
    assert mdo_client.delete(
        f"/v1/mdo/elements/{el['id']}", headers=auth(token_b)
    ).status_code == 404

    deleted = mdo_client.delete(f"/v1/mdo/elements/{el['id']}", headers=h_a)
    assert deleted.status_code == 200
    assert deleted.json()["deleted_at"] is not None
    tree = mdo_client.get(f"/v1/mdo/versions/{vid}/tree", headers=h_a).json()
    assert tree["elements"] == []
