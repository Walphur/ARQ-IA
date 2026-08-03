"""Wire runtime status service."""

from __future__ import annotations

from typing import Any, Optional

from infrastructure.observability.setup import get_observability
from infrastructure.runtime.checks.db import SqlAlchemyDatabaseCheck
from infrastructure.runtime.mode import RuntimeSettings
from infrastructure.runtime.service import RuntimeStatusService, default_extra_checks

_runtime: Optional[RuntimeStatusService] = None


def configure_runtime(engine: Any, settings: Optional[RuntimeSettings] = None) -> RuntimeStatusService:
    global _runtime
    cfg = settings or RuntimeSettings.from_env()
    if cfg.mode_was_invalid:
        get_observability().warning(
            "Invalid PLATFORM_MODE; defaulting to normal",
            feature="runtime",
            module="runtime",
        )
    _runtime = RuntimeStatusService(
        settings=cfg,
        db_check=SqlAlchemyDatabaseCheck(engine),
        extra_checks=default_extra_checks(),
    )
    get_observability().metrics.set_platform_mode(cfg.mode)
    return _runtime


def get_runtime() -> RuntimeStatusService:
    if _runtime is None:
        raise RuntimeError("RuntimeStatusService not configured; call configure_runtime(engine)")
    return _runtime


def reset_runtime_for_tests() -> None:
    global _runtime
    _runtime = None
