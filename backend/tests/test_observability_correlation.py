import os

import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("LOG_FORMAT", "json")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    reset_observability_for_tests()
    configure_observability()
    return TestClient(main.app)


def test_generates_request_id_when_missing(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.headers.get("X-Request-Id")
    assert len(res.headers["X-Request-Id"]) >= 8


def test_reuses_inbound_request_id(client):
    res = client.get("/health", headers={"X-Request-Id": "client-req-123"})
    assert res.status_code == 200
    assert res.headers.get("X-Request-Id") == "client-req-123"


def test_rejects_malicious_request_id(client):
    res = client.get("/health", headers={"X-Request-Id": "bad id with spaces!!!"})
    assert res.status_code == 200
    assert res.headers.get("X-Request-Id") != "bad id with spaces!!!"
