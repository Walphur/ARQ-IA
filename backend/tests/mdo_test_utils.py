"""Helpers compartidos para tests MDO por fase."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests
from infrastructure.runtime.mode import RuntimeSettings
from infrastructure.runtime.setup import configure_runtime, reset_runtime_for_tests
from mdo.setup import run_mdo_migrations


@pytest.fixture()
def mdo_client(monkeypatch, tmp_path):
    db_path = tmp_path / "mdo_test.db"
    url = f"sqlite:///{db_path}"
    monkeypatch.setenv("DATABASE_URL", url)
    monkeypatch.setenv("OBS_MODE", "off")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("PLATFORM_MODE", "normal")
    monkeypatch.setenv("SECRET_KEY", "test-secret-mdo")
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

    reset_runtime_for_tests()
    configure_runtime(engine, RuntimeSettings.from_env())

    with TestClient(main.app) as c:
        yield c


def register_and_project(client: TestClient, *, email: str = "mdo.owner@example.com") -> tuple[str, int]:
    res = client.post(
        "/auth/register",
        json={
            "studio_name": "Studio MDO",
            "name": "Owner MDO",
            "email": email,
            "password": "secret12345",
        },
    )
    assert res.status_code == 200, res.text
    token = res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    proj = client.post(
        "/projects",
        headers=headers,
        json={"name": "Obra Test", "client": "Cliente", "address": "Calle 1"},
    )
    assert proj.status_code == 200, proj.text
    return token, proj.json()["id"]


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
