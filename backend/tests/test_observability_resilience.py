import concurrent.futures

import pytest
from fastapi.testclient import TestClient

from infrastructure.observability import context as obs_context
from infrastructure.observability.adapters.ids import UuidIdGenerator
from infrastructure.observability.setup import configure_observability, get_observability, reset_observability_for_tests


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    return TestClient(main.app)


def test_health_still_ok_when_obs_basic(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert "version" in res.json()


def test_oversized_request_id_sanitized(client):
    huge = "a" * 500
    res = client.get("/health", headers={"X-Request-Id": huge})
    assert res.status_code == 200
    assert res.headers["X-Request-Id"] != huge
    assert len(res.headers["X-Request-Id"]) <= 128


def test_id_generator_sanitize():
    gen = UuidIdGenerator()
    assert gen.sanitize_request_id("ok-id_1") == "ok-id_1"
    assert gen.sanitize_request_id("no spaces") != "no spaces"


def test_contextvars_isolation_1000_concurrent():
    """At least 1000 concurrent operations must not cross request_id contextvars."""
    reset_observability_for_tests()
    configure_observability()
    obs = get_observability()
    seen = {}
    errors = []

    def worker(i: int):
        rid = f"t-{i:04d}"
        token = obs.bind(
            request_id=rid,
            feature="observability",
            module="test",
            component="api",
            user_id=f"u-{i}",
            organization_id=f"org-{i % 7}",
        )
        try:
            import time

            time.sleep(0.0005)
            current = obs_context.get_field("request_id")
            user = obs_context.get_field("user_id")
            if current != rid or user != f"u-{i}":
                errors.append((i, current, user))
            else:
                seen[i] = current
        finally:
            obs.reset(token)

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        list(pool.map(worker, range(1000)))

    assert errors == []
    assert len(seen) == 1000
    for i, value in seen.items():
        assert value == f"t-{i:04d}"


def test_http_request_id_roundtrip_batch(client):
    """Sequential HTTP batch: each response echoes its own X-Request-Id."""
    for i in range(100):
        rid = f"http-{i:04d}"
        res = client.get("/health", headers={"X-Request-Id": rid})
        assert res.status_code == 200
        assert res.headers.get("X-Request-Id") == rid
