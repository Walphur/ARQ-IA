"""Integración Geometry Engine — compute + list sobre versión MDO."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests
from infrastructure.runtime.mode import RuntimeSettings
from infrastructure.runtime.setup import configure_runtime, reset_runtime_for_tests
from geometry.setup import run_geometry_migrations
from mdo.setup import run_mdo_migrations
from tests.mdo_test_utils import auth, register_and_project


@pytest.fixture()
def geom_client(monkeypatch, tmp_path):
    db_path = tmp_path / "geom_test.db"
    url = f"sqlite:///{db_path}"
    monkeypatch.setenv("DATABASE_URL", url)
    monkeypatch.setenv("OBS_MODE", "off")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("PLATFORM_MODE", "normal")
    monkeypatch.setenv("SECRET_KEY", "test-secret-geom")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    monkeypatch.delenv("RENDER", raising=False)

    reset_observability_for_tests()
    configure_observability()

    import main

    engine = create_engine(
        url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    main.engine = engine
    main.SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    main.DATABASE_URL = url
    main.Base.metadata.create_all(bind=engine)
    run_mdo_migrations(url)
    run_geometry_migrations(url)

    reset_runtime_for_tests()
    configure_runtime(engine, RuntimeSettings.from_env())

    with TestClient(main.app) as c:
        yield c


def _seed_wall_version(client: TestClient, token: str, project_id: int) -> tuple[str, str]:
    headers = auth(token)
    ens = client.post(f"/v1/mdo/projects/{project_id}/ensure", headers=headers)
    assert ens.status_code == 200, ens.text
    version_id = ens.json()["version"]["id"]

    site = client.post(
        f"/v1/mdo/versions/{version_id}/sites",
        headers=headers,
        json={"display_name": "Sitio", "code": "S1"},
    )
    assert site.status_code == 200, site.text
    site_id = site.json()["id"]

    building = client.post(
        f"/v1/mdo/versions/{version_id}/buildings",
        headers=headers,
        json={"site_id": site_id, "display_name": "Edificio", "code": "B1"},
    )
    assert building.status_code == 200, building.text
    building_id = building.json()["id"]

    level = client.post(
        f"/v1/mdo/versions/{version_id}/levels",
        headers=headers,
        json={
            "building_id": building_id,
            "display_name": "PB",
            "code": "PB",
            "elevation_m": 0,
        },
    )
    assert level.status_code == 200, level.text
    level_id = level.json()["id"]

    space = client.post(
        f"/v1/mdo/versions/{version_id}/spaces",
        headers=headers,
        json={
            "level_id": level_id,
            "display_name": "Espacio",
            "code": "SP1",
            "area_m2": 40.0,
        },
    )
    assert space.status_code == 200, space.text
    space_id = space.json()["id"]

    disc = client.post(
        f"/v1/mdo/versions/{version_id}/disciplines",
        headers=headers,
        json={"code": "architecture", "display_name": "Arquitectura"},
    )
    assert disc.status_code == 200, disc.text
    disc_id = disc.json()["id"]

    wall = client.post(
        f"/v1/mdo/versions/{version_id}/elements",
        headers=headers,
        json={
            "display_name": "Muro",
            "code": "W1",
            "discipline_code": "architecture",
            "element_type": "wall.masonry.brick",
            "level_id": level_id,
            "space_id": space_id,
            "discipline_id": disc_id,
        },
    )
    assert wall.status_code == 200, wall.text
    wall_id = wall.json()["id"]

    ps = client.put(
        f"/v1/mdo/versions/{version_id}/parameter-sets",
        headers=headers,
        json={
            "owner_kind": "element",
            "owner_id": wall_id,
            "display_name": "Params muro",
            "data": {
                "params": {"wall_face_area_m2": 25.0, "wall_height_m": 2.5},
                "metadata": {},
            },
        },
    )
    assert ps.status_code == 200, ps.text
    return version_id, wall_id


def test_compute_and_list_geometry(geom_client: TestClient):
    token, project_id = register_and_project(geom_client, email="geom.owner@example.com")
    headers = auth(token)
    version_id, wall_id = _seed_wall_version(geom_client, token, project_id)

    empty = geom_client.get(f"/v1/geometry/versions/{version_id}", headers=headers)
    assert empty.status_code == 200, empty.text
    assert empty.json()["geometries"] == []

    compute = geom_client.post(f"/v1/geometry/versions/{version_id}/compute", headers=headers)
    assert compute.status_code == 200, compute.text
    body = compute.json()
    assert body["geometries_upserted"] == 1
    assert body["compute_run_id"]
    geom = body["geometries"][0]
    assert geom["element_id"] == wall_id
    assert geom["geom_type"] == "vertical_surface"
    assert geom["length_m"] == 10.0
    assert geom["area_m2"] == 25.0
    assert geom["height_m"] == 2.5
    assert geom["thickness_m"] is None
    assert geom["bbox"] is None
    assert geom["measure_meta"]["length_m"]["source"] == "computed"
    assert geom["measure_meta"]["length_m"]["derived"] is True
    assert body["issues_created"] >= 1

    listed = geom_client.get(f"/v1/geometry/versions/{version_id}", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()["geometries"]) == 1

    one = geom_client.get(
        f"/v1/geometry/versions/{version_id}/elements/{wall_id}",
        headers=headers,
    )
    assert one.status_code == 200
    assert one.json()["length_m"] == 10.0

    # Recompute replaces previous run (still one active geometry)
    again = geom_client.post(f"/v1/geometry/versions/{version_id}/compute", headers=headers)
    assert again.status_code == 200
    assert again.json()["geometries_upserted"] == 1
    listed2 = geom_client.get(f"/v1/geometry/versions/{version_id}", headers=headers)
    assert len(listed2.json()["geometries"]) == 1
    assert listed2.json()["geometries"][0]["compute_run_id"] == again.json()["compute_run_id"]


def test_compute_unknown_version_404(geom_client: TestClient):
    token, _project_id = register_and_project(geom_client, email="geom404@example.com")
    headers = auth(token)
    res = geom_client.post(
        "/v1/geometry/versions/00000000-0000-0000-0000-000000000000/compute",
        headers=headers,
    )
    assert res.status_code == 404
