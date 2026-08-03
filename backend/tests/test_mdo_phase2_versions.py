"""Fase 2 — ProjectVersion ensure/seal: integridad, tenant, auditoría."""

from tests.mdo_test_utils import auth, mdo_client, register_and_project

client = mdo_client  # pytest fixture alias via param name in tests


def test_ensure_creates_version_with_audit_and_display(mdo_client):
    token, project_id = register_and_project(mdo_client)
    res = mdo_client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=auth(token))
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["created"] is True
    v = body["version"]
    assert v["version_number"] == 1
    assert v["status"] == "active"
    assert v["display_name"]
    assert v["created_by"] is not None
    assert v["updated_by"] is not None
    assert v["created_at"]
    assert v["updated_at"]
    assert v["deleted_at"] is None
    assert "external_id" in v
    assert v["studio_id"]
    assert v["project_id"] == project_id

    again = mdo_client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=auth(token))
    assert again.json()["created"] is False
    assert again.json()["version"]["id"] == v["id"]


def test_list_and_get_version_tenant_scoped(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = mdo_client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=h).json()["version"]["id"]
    items = mdo_client.get(f"/v1/mdo/projects/{project_id}/versions", headers=h).json()["items"]
    assert len(items) == 1
    got = mdo_client.get(f"/v1/mdo/versions/{vid}", headers=h)
    assert got.status_code == 200
    assert got.json()["id"] == vid


def test_seal_is_idempotent_block_on_further_mutation_signal(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    vid = mdo_client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=h).json()["version"]["id"]
    sealed = mdo_client.post(
        f"/v1/mdo/versions/{vid}/seal",
        headers=h,
        json={"summary": "baseline"},
    )
    assert sealed.status_code == 200
    assert sealed.json()["status"] == "sealed"
    assert sealed.json()["updated_by"] is not None

    # Re-seal must conflict (no longer mutable)
    again = mdo_client.post(
        f"/v1/mdo/versions/{vid}/seal",
        headers=h,
        json={"summary": "again"},
    )
    assert again.status_code == 409


def test_version_tenant_isolation(mdo_client):
    token_a, project_a = register_and_project(mdo_client, email="a.mdo@example.com")
    h_a = auth(token_a)
    vid = mdo_client.post(f"/v1/mdo/projects/{project_a}/ensure", headers=h_a).json()["version"]["id"]

    token_b, _ = register_and_project(mdo_client, email="b.mdo@example.com")
    h_b = auth(token_b)
    assert mdo_client.get(f"/v1/mdo/versions/{vid}", headers=h_b).status_code == 404
    assert mdo_client.post(f"/v1/mdo/projects/{project_a}/ensure", headers=h_b).status_code == 404


def test_ensure_emits_domain_event(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    mdo_client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=h)
    events = mdo_client.get(f"/v1/mdo/projects/{project_id}/events", headers=h).json()["items"]
    assert any(e["event_type"] == "mdo.version.ensured" for e in events)
    assert all(e["studio_id"] for e in events)
    assert all(e.get("created_by") is not None for e in events)


def test_process_path_untouched(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h = auth(token)
    mdo_client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=h)
    listing = mdo_client.get(f"/projects/{project_id}/processes", headers=h)
    assert listing.status_code == 200
    assert listing.json() == []
