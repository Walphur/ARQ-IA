import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.setup import configure_observability, get_observability, reset_observability_for_tests
from infrastructure.runtime.mode import RuntimeSettings
from infrastructure.runtime.setup import configure_runtime, reset_runtime_for_tests


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("PLATFORM_MODE", "degraded")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    reset_runtime_for_tests()
    configure_runtime(main.engine, RuntimeSettings.from_env())
    return TestClient(main.app)


def test_ready_updates_platform_ready_metric(client):
    assert client.get("/ready").status_code == 200
    text = client.get("/metrics").text
    assert "arqia_platform_ready" in text
    assert 'arqia_platform_mode{mode="degraded"' in text or 'mode="degraded"' in text
    assert "arqia_component_status" in text


def test_component_allowlist_rejects_unknown():
    reset_observability_for_tests()
    configure_observability()
    obs = get_observability()
    obs.metrics.set_component_status("not_a_real_component", "ok")
    text = obs.metrics.render_exposition()
    assert "not_a_real_component" not in text
