"""Platform status projection — no own checks; banner contract."""

import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests
from infrastructure.runtime.mode import RuntimeSettings
from infrastructure.runtime.setup import configure_runtime, reset_runtime_for_tests


@pytest.fixture()
def app_client(monkeypatch):
    def _make(mode: str):
        monkeypatch.setenv("OBS_MODE", "basic")
        monkeypatch.setenv("APP_ENV", "dev")
        monkeypatch.setenv("PLATFORM_MODE", mode)
        monkeypatch.setenv("API_VERSION", "v1")
        monkeypatch.delenv("METRICS_TOKEN", raising=False)
        reset_observability_for_tests()
        configure_observability()
        import main

        reset_runtime_for_tests()
        configure_runtime(main.engine, RuntimeSettings.from_env())
        return TestClient(main.app)

    return _make


def test_status_normal(app_client):
    client = app_client("normal")
    res = client.get("/v1/platform/status")
    assert res.status_code == 200
    body = res.json()
    assert body["mode"] == "normal"
    assert body["degraded"] is False
    assert body["api_version"] == "v1"
    assert "generated_at" in body
    assert "capabilities" in body
    assert "checks" not in body


def test_status_degraded_modes(app_client):
    for mode in ("degraded", "maintenance", "readonly"):
        body = app_client(mode).get("/v1/platform/status").json()
        assert body["mode"] == mode
        assert body["degraded"] is True
        assert body["reasons"]


def test_status_does_not_run_db_when_unsampled(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("PLATFORM_MODE", "normal")
    reset_observability_for_tests()
    configure_observability()

    class BoomEngine:
        def connect(self):
            raise AssertionError("status must not open DB")

    from infrastructure.runtime.service import RuntimeStatusService, default_extra_checks
    from infrastructure.runtime.checks.db import SqlAlchemyDatabaseCheck

    svc = RuntimeStatusService(
        settings=RuntimeSettings.from_env(),
        db_check=SqlAlchemyDatabaseCheck(BoomEngine()),
        extra_checks=default_extra_checks(),
    )
    status = svc.platform_status(request_id="r1")
    assert status.ready is True
    assert "readiness_unsampled" in status.reasons


def test_status_projects_last_ready(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    reset_observability_for_tests()
    configure_observability()
    import main

    reset_runtime_for_tests()
    configure_runtime(main.engine, RuntimeSettings.from_env())
    client = TestClient(main.app)
    assert client.get("/ready").status_code == 200
    body = client.get("/v1/platform/status").json()
    assert body["ready"] is True
    assert "readiness_unsampled" not in body["reasons"]


def test_version_endpoint(app_client):
    body = app_client("normal").get("/v1/platform/version").json()
    assert body["api_compat"] == "v1"
    assert body["service"] == "arq-ia-api"


def test_invalid_mode_defaults_normal(monkeypatch):
    monkeypatch.setenv("PLATFORM_MODE", "nope")
    settings = RuntimeSettings.from_env()
    assert settings.mode == "normal"
    assert settings.mode_was_invalid is True
