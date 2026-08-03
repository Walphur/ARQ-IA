"""Fase 5 — ParameterSet limits + audit/tenant."""

from tests.mdo_test_utils import auth, mdo_client, register_and_project


def _site(client, token, project_id):
    h = auth(token)
    vid = client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=h).json()["version"]["id"]
    site = client.post(
        f"/v1/mdo/versions/{vid}/sites",
        headers=h,
        json={"display_name": "Lote"},
    ).json()
    return h, vid, site


def test_parameter_set_rejects_structural_and_accepts_params(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h, vid, site = _site(mdo_client, token, project_id)

    rejected = mdo_client.put(
        f"/v1/mdo/versions/{vid}/parameter-sets",
        headers=h,
        json={
            "owner_kind": "site",
            "owner_id": site["id"],
            "data": {"level_id": "should-fail", "params": {}},
        },
    )
    assert rejected.status_code == 400

    nested = mdo_client.put(
        f"/v1/mdo/versions/{vid}/parameter-sets",
        headers=h,
        json={
            "owner_kind": "site",
            "owner_id": site["id"],
            "data": {"params": {"geometry": {"x": 1}}, "metadata": {}},
        },
    )
    assert nested.status_code == 400

    ok = mdo_client.put(
        f"/v1/mdo/versions/{vid}/parameter-sets",
        headers=h,
        json={
            "owner_kind": "site",
            "owner_id": site["id"],
            "display_name": "Params lote",
            "external_id": "ps-1",
            "data": {"params": {"soil": "clay"}, "metadata": {"note": "manual"}},
        },
    )
    assert ok.status_code == 200, ok.text
    body = ok.json()
    assert body["data"]["params"]["soil"] == "clay"
    assert body["created_by"] is not None
    assert body["updated_by"] is not None
    assert body["studio_id"]
    assert body["project_id"] == project_id
    assert body["external_id"] == "ps-1"
    assert body["display_name"] == "Params lote"


def test_parameter_set_tenant_isolation_and_soft_delete(mdo_client):
    token_a, project_a = register_and_project(mdo_client, email="ps.a@example.com")
    h_a, vid, site = _site(mdo_client, token_a, project_a)
    ps = mdo_client.put(
        f"/v1/mdo/versions/{vid}/parameter-sets",
        headers=h_a,
        json={
            "owner_kind": "site",
            "owner_id": site["id"],
            "data": {"params": {"a": 1}, "metadata": {}},
        },
    ).json()

    token_b, _ = register_and_project(mdo_client, email="ps.b@example.com")
    assert mdo_client.delete(
        f"/v1/mdo/parameter-sets/{ps['id']}", headers=auth(token_b)
    ).status_code == 404

    deleted = mdo_client.delete(f"/v1/mdo/parameter-sets/{ps['id']}", headers=h_a)
    assert deleted.status_code == 200
    assert deleted.json()["deleted_at"] is not None
    tree = mdo_client.get(f"/v1/mdo/versions/{vid}/tree", headers=h_a).json()
    assert tree["parameter_sets"] == []


def test_parameter_set_requires_living_owner(mdo_client):
    token, project_id = register_and_project(mdo_client)
    h, vid, _site_row = _site(mdo_client, token, project_id)
    res = mdo_client.put(
        f"/v1/mdo/versions/{vid}/parameter-sets",
        headers=h,
        json={
            "owner_kind": "site",
            "owner_id": "00000000-0000-0000-0000-000000000001",
            "data": {"params": {}, "metadata": {}},
        },
    )
    assert res.status_code == 404
