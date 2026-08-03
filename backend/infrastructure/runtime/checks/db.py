"""Database readiness check — never used by /health liveness."""

from __future__ import annotations

import concurrent.futures
from typing import Any

from infrastructure.observability.setup import get_observability
from infrastructure.runtime.models import CheckResult


class SqlAlchemyDatabaseCheck:
    def __init__(self, engine: Any) -> None:
        self._engine = engine

    def check(self, timeout_ms: int) -> CheckResult:
        obs = get_observability()
        started = obs.clock.monotonic()

        def _ping() -> None:
            with self._engine.connect() as conn:
                conn.exec_driver_sql("SELECT 1")

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                fut = pool.submit(_ping)
                fut.result(timeout=max(timeout_ms, 1) / 1000.0)
            latency = round((obs.clock.monotonic() - started) * 1000, 3)
            return CheckResult(name="db", status="ok", latency_ms=latency)
        except concurrent.futures.TimeoutError:
            latency = round((obs.clock.monotonic() - started) * 1000, 3)
            return CheckResult(
                name="db",
                status="timeout",
                latency_ms=latency,
                error_class="db_timeout",
            )
        except Exception:
            latency = round((obs.clock.monotonic() - started) * 1000, 3)
            return CheckResult(
                name="db",
                status="fail",
                latency_ms=latency,
                error_class="db_unreachable",
            )
