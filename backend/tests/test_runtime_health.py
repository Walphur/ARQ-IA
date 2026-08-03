"""Liveness: /health never depends on external resources."""

import time

import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests
from infrastructure.runtime.mode import RuntimeSettings
from infrastructure.runtime.setup import configure_runtime, reset_runtime_for_tests


class _HangingEngine:
    def connect(self):
        time.sleep(5)
        raise RuntimeError("should not be reached by /health")


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("PLATFORM_MODE", "maintenance")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    reset_runtime_for_tests()
    configure_runtime(main.engine, RuntimeSettings.from_env())
    return TestClient(main.app)


def test_health_shape(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "version": res.json()["version"]}
    assert "checks" not in res.json()


def test_api_health_identical(client):
    a = client.get("/health").json()
    b = client.get("/api/health").json()
    assert a == b


def test_health_ignores_platform_mode(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_health_does_not_use_hanging_db(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "off")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("PLATFORM_MODE", "normal")
    reset_observability_for_tests()
    configure_observability()
    import main

    reset_runtime_for_tests()
    configure_runtime(_HangingEngine(), RuntimeSettings.from_env())
    client = TestClient(main.app)
    started = time.monotonic()
    res = client.get("/health")
    elapsed = time.monotonic() - started
    assert res.status_code == 200
    assert elapsed < 0.5
