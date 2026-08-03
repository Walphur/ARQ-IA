"""Readiness checks for /ready."""

import time

import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests
from infrastructure.runtime.checks.db import SqlAlchemyDatabaseCheck
from infrastructure.runtime.mode import RuntimeSettings
from infrastructure.runtime.models import CheckResult
from infrastructure.runtime.service import RuntimeStatusService, default_extra_checks
from infrastructure.runtime.setup import configure_runtime, get_runtime, reset_runtime_for_tests


class _FailEngine:
    def connect(self):
        raise ConnectionError("db down")


class _SlowEngine:
    def connect(self):
        time.sleep(2)

        class _Conn:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def exec_driver_sql(self, *_a, **_k):
                return None

        return _Conn()


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("PLATFORM_MODE", "normal")
    monkeypatch.setenv("READY_DB_TIMEOUT_MS", "500")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    reset_runtime_for_tests()
    configure_runtime(main.engine, RuntimeSettings.from_env())
    return TestClient(main.app)


def test_ready_ok_with_stubs(client):
    res = client.get("/ready")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ready"
    names = {c["name"]: c for c in body["checks"]}
    assert names["db"]["status"] == "ok"
    assert names["object_storage"]["status"] == "skipped"
    assert names["object_storage"]["reason"] == "not_configured"
    assert names["broker"]["status"] == "skipped"


def test_api_ready_mirror(client):
    a = client.get("/ready").json()
    b = client.get("/api/ready").json()
    assert a["status"] == b["status"] == "ready"
    assert {c["name"] for c in a["checks"]} == {c["name"] for c in b["checks"]}
    assert {c["name"]: c["status"] for c in a["checks"]} == {
        c["name"]: c["status"] for c in b["checks"]
    }


def test_ready_db_unreachable(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    reset_observability_for_tests()
    configure_observability()
    settings = RuntimeSettings.from_env()
    svc = RuntimeStatusService(
        settings=settings,
        db_check=SqlAlchemyDatabaseCheck(_FailEngine()),
        extra_checks=default_extra_checks(),
    )
    report = svc.readiness()
    assert report.http_status == 503
    assert report.status == "not_ready"
    assert report.checks[0].error_class == "db_unreachable"
    assert "postgres" not in str(report.to_public_dict()).lower()
    assert "password" not in str(report.to_public_dict()).lower()


def test_ready_db_timeout(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    reset_observability_for_tests()
    configure_observability()
    settings = RuntimeSettings(
        mode="normal",
        exports_enabled=True,
        ai_enabled=True,
        ready_db_timeout_ms=100,
        app_version="dev",
        api_version="v1",
        service_name="arq-ia-api",
    )
    svc = RuntimeStatusService(
        settings=settings,
        db_check=SqlAlchemyDatabaseCheck(_SlowEngine()),
        extra_checks=default_extra_checks(),
    )
    report = svc.readiness()
    assert report.http_status == 503
    assert report.checks[0].error_class == "db_timeout"


def test_ready_via_http_fail(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    reset_runtime_for_tests()
    configure_runtime(_FailEngine(), RuntimeSettings.from_env())
    res = TestClient(main.app).get("/ready")
    assert res.status_code == 503
    assert res.json()["status"] == "not_ready"
