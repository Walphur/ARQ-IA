"""Explicit RuntimeStatusService — announces mode/status; never enforces app behavior."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from infrastructure.observability.setup import get_observability
from infrastructure.runtime.checks.stubs import NotConfiguredComponentCheck
from infrastructure.runtime.mode import RuntimeSettings, capabilities_for, reasons_for
from infrastructure.runtime.models import PlatformStatus, ReadyReport
from infrastructure.runtime.ports import ComponentCheckPort, DatabaseCheckPort


class RuntimeStatusService:
    def __init__(
        self,
        *,
        settings: RuntimeSettings,
        db_check: DatabaseCheckPort,
        extra_checks: Optional[list[ComponentCheckPort]] = None,
    ) -> None:
        self.settings = settings
        self._db_check = db_check
        self._extra_checks = list(extra_checks or [])
        self._last_ready: Optional[bool] = None

    def liveness(self) -> dict:
        """Process up only — no DB, storage, broker, or mode evaluation."""
        return {"status": "ok", "version": self.settings.app_version}

    def readiness(self) -> ReadyReport:
        """Deep checks for traffic readiness. Updates component metrics."""
        obs = get_observability()
        db = self._db_check.check(self.settings.ready_db_timeout_ms)
        checks = [db]
        for component in self._extra_checks:
            checks.append(component.check())

        db_ok = db.status == "ok"
        # skipped extras never block readiness
        ready = db_ok
        report = ReadyReport(
            status="ready" if ready else "not_ready",
            version=self.settings.app_version,
            checks=checks,
            http_status=200 if ready else 503,
        )

        obs.metrics.set_component_status("db", "ok" if db.status == "ok" else db.status)
        for c in checks:
            if c.name != "db":
                obs.metrics.set_component_status(c.name, c.status)
        obs.metrics.set_ready(ready)
        obs.metrics.set_platform_mode(self.settings.mode)
        self._last_ready = ready

        obs.info(
            "runtime_readiness",
            feature="runtime",
            module="runtime",
            ready=ready,
            db_status=db.status,
            platform_mode=self.settings.mode,
        )
        return report

    def platform_status(self, request_id: Optional[str] = None) -> PlatformStatus:
        """
        Product/UX projection of runtime state.

        Does NOT execute dependency checks. Projects PLATFORM_MODE + the last
        readiness snapshot produced by `/ready` (RuntimeStatusService.readiness).
        If readiness was never sampled, `ready` stays true and a reason is added
        — status never opens DB/storage/broker connections.
        """
        obs = get_observability()
        mode = self.settings.mode
        caps = capabilities_for(self.settings)
        reasons = reasons_for(mode)
        if self._last_ready is None:
            ready = True
            reasons = [*reasons, "readiness_unsampled"]
        else:
            ready = bool(self._last_ready)
            if not ready:
                reasons = [*reasons, "runtime_not_ready"]

        degraded = mode != "normal"
        generated_at = datetime.now(timezone.utc).isoformat()

        obs.metrics.set_platform_mode(mode)
        return PlatformStatus(
            mode=mode,
            degraded=degraded,
            reasons=reasons,
            capabilities=caps,
            ready=ready,
            version=self.settings.app_version,
            api_version=self.settings.api_version,
            generated_at=generated_at,
            request_id=request_id,
        )

    def platform_version(self, request_id: Optional[str] = None) -> dict:
        return {
            "version": self.settings.app_version,
            "service": self.settings.service_name,
            "api_compat": self.settings.api_version,
            "request_id": request_id,
        }


def default_extra_checks() -> list[ComponentCheckPort]:
    return [
        NotConfiguredComponentCheck("object_storage"),
        NotConfiguredComponentCheck("broker"),
    ]
