"""Fase 3 — Site/Building/Level/Space: integridad, tenant, auditoría."""

from tests.mdo_test_utils import auth, mdo_client, register_and_project


def _ensure(client, token, project_id) -> str:
    return client.post(
        f"/v1/mdo/projects/{project_id}/ensure", headers=auth(token)
    ).json()["version"]["id"]


def _assert_audit_tenant(entity: dict, *, project_id: int):
    assert entity["studio_id"]
    assert entity["project_id"] == project_id
    assert entity["display_name"]
    assert "external_id" in entity
    assert entity["created_by"] is not None
    assert entity["updated_by"] is not None
    assert entity["created_at"]
    assert entity["updated_at"]
    assert entity["deleted_at"] is None


def test_spatial_hierarchy_integrity_and_audit(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = _ensure(mdo_client, token, project_id)

    site = mdo_client.post(
        f"/v1/mdo/versions/{vid}/sites",
        headers=h,
        json={"display_name": "Lote Norte", "code": "SITE-N", "external_id": "ext-site-1"},
    ).json()
    _assert_audit_tenant(site, project_id=project_id)
    assert site["external_id"] == "ext-site-1"

    building = mdo_client.post(
        f"/v1/mdo/versions/{vid}/buildings",
        headers=h,
        json={"site_id": site["id"], "display_name": "Edificio A", "typology": "housing"},
    ).json()
    _assert_audit_tenant(building, project_id=project_id)

    level = mdo_client.post(
        f"/v1/mdo/versions/{vid}/levels",
        headers=h,
        json={"building_id": building["id"], "display_name": "PB", "elevation_m": 0},
    ).json()
    _assert_audit_tenant(level, project_id=project_id)

    space = mdo_client.post(
        f"/v1/mdo/versions/{vid}/spaces",
        headers=h,
        json={
            "level_id": level["id"],
            "display_name": "Living",
            "space_type": "space.room",
            "area_m2": 24.5,
            "external_id": "space-1",
        },
    ).json()
    _assert_audit_tenant(space, project_id=project_id)
    assert space["area_m2"] == 24.5

    tree = mdo_client.get(f"/v1/mdo/versions/{vid}/tree", headers=h).json()
    assert len(tree["sites"]) == 1
    assert len(tree["buildings"]) == 1
    assert len(tree["levels"]) == 1
    assert len(tree["spaces"]) == 1


def test_spatial_rejects_cross_version_parent(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = _ensure(mdo_client, token, project_id)
    site = mdo_client.post(
        f"/v1/mdo/versions/{vid}/sites",
        headers=h,
        json={"display_name": "Lote"},
    ).json()
    # Fake foreign site id → 404 owned check
    bad = mdo_client.post(
        f"/v1/mdo/versions/{vid}/buildings",
        headers=h,
        json={"site_id": "00000000-0000-0000-0000-000000000099", "display_name": "X"},
    )
    assert bad.status_code == 404
    assert site["id"]


def test_spatial_tenant_isolation(mdo_client):
    token_a, project_a = register_and_project(mdo_client, email="sp.a@example.com")
    h_a = auth(token_a)
    vid = _ensure(mdo_client, token_a, project_a)
    site = mdo_client.post(
        f"/v1/mdo/versions/{vid}/sites",
        headers=h_a,
        json={"display_name": "Privado"},
    ).json()

    token_b, _ = register_and_project(mdo_client, email="sp.b@example.com")
    h_b = auth(token_b)
    assert mdo_client.patch(
        f"/v1/mdo/sites/{site['id']}",
        headers=h_b,
        json={"display_name": "Hack"},
    ).status_code == 404


def test_spatial_soft_delete_and_sealed_block(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = _ensure(mdo_client, token, project_id)
    site = mdo_client.post(
        f"/v1/mdo/versions/{vid}/sites",
        headers=h,
        json={"display_name": "Temporal"},
    ).json()
    deleted = mdo_client.delete(f"/v1/mdo/sites/{site['id']}", headers=h)
    assert deleted.status_code == 200
    assert deleted.json()["deleted_at"] is not None
    assert mdo_client.get(f"/v1/mdo/versions/{vid}/tree", headers=h).json()["sites"] == []

    site2 = mdo_client.post(
        f"/v1/mdo/versions/{vid}/sites",
        headers=h,
        json={"display_name": "Antes seal"},
    ).json()
    mdo_client.post(f"/v1/mdo/versions/{vid}/seal", headers=h, json={})
    blocked = mdo_client.patch(
        f"/v1/mdo/sites/{site2['id']}",
        headers=h,
        json={"display_name": "No"},
    )
    assert blocked.status_code == 409
