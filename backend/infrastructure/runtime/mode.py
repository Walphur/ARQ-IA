"""PLATFORM_MODE parsing and capability announcement (no enforcement)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

PlatformMode = Literal["normal", "degraded", "maintenance", "readonly"]
VALID_MODES = frozenset({"normal", "degraded", "maintenance", "readonly"})


def _env_bool(name: str, default: bool = True) -> bool:
    raw = (os.getenv(name) or "").strip().lower()
    if not raw:
        return default
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return default


@dataclass(frozen=True)
class RuntimeSettings:
    mode: PlatformMode
    exports_enabled: bool
    ai_enabled: bool
    ready_db_timeout_ms: int
    app_version: str
    api_version: str
    service_name: str

    @staticmethod
    def from_env() -> "RuntimeSettings":
        raw = (os.getenv("PLATFORM_MODE") or "normal").strip().lower()
        mode: PlatformMode
        if raw not in VALID_MODES:
            mode = "normal"
        else:
            mode = raw  # type: ignore[assignment]
        timeout_raw = (os.getenv("READY_DB_TIMEOUT_MS") or "500").strip()
        try:
            timeout_ms = max(50, min(int(timeout_raw), 10_000))
        except ValueError:
            timeout_ms = 500
        return RuntimeSettings(
            mode=mode,
            exports_enabled=_env_bool("PLATFORM_EXPORTS_ENABLED", True),
            ai_enabled=_env_bool("PLATFORM_AI_ENABLED", True),
            ready_db_timeout_ms=timeout_ms,
            app_version=(os.getenv("APP_VERSION") or "dev").strip(),
            api_version=(os.getenv("API_VERSION") or "v1").strip(),
            service_name=(os.getenv("OTEL_SERVICE_NAME") or "arq-ia-api").strip(),
        )

    @property
    def mode_was_invalid(self) -> bool:
        raw = (os.getenv("PLATFORM_MODE") or "normal").strip().lower()
        return raw not in VALID_MODES


def capabilities_for(settings: RuntimeSettings):
    from infrastructure.runtime.models import PlatformCapabilities

    mode = settings.mode
    exports = settings.exports_enabled
    ai = settings.ai_enabled

    if mode == "normal":
        return PlatformCapabilities(
            reads=True, writes=True, calcular=True, exports=exports, ai=ai
        )
    if mode == "degraded":
        return PlatformCapabilities(
            reads=True, writes=True, calcular=True, exports=exports, ai=ai
        )
    if mode == "maintenance":
        return PlatformCapabilities(
            reads=True, writes=False, calcular=False, exports=False, ai=False
        )
    # readonly
    return PlatformCapabilities(
        reads=True, writes=False, calcular=False, exports=exports, ai=False
    )


def reasons_for(mode: PlatformMode) -> list[str]:
    if mode == "normal":
        return []
    return [f"platform_mode_{mode}"]
