"""Typed observability settings from environment."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, Optional

ObsMode = Literal["off", "basic", "full"]


@dataclass(frozen=True)
class ObservabilitySettings:
    mode: ObsMode
    log_level: str
    log_format: str
    service_name: str
    environment: str
    app_version: str
    metrics_token: str
    require_metrics_token: bool
    otel_enabled: bool
    otel_endpoint: str
    component: str

    @staticmethod
    def from_env() -> "ObservabilitySettings":
        raw_mode = (os.getenv("OBS_MODE") or "basic").strip().lower()
        if raw_mode not in {"off", "basic", "full"}:
            raw_mode = "basic"
        env_name = (os.getenv("APP_ENV") or os.getenv("ENVIRONMENT") or "dev").strip().lower()
        metrics_token = (os.getenv("METRICS_TOKEN") or "").strip()
        require_token = env_name in {"prod", "production", "staging"} or bool(os.getenv("RENDER"))
        otel_endpoint = (os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") or "").strip()
        # OTEL_ENABLED may force export attempt in full; basic keeps in-process only.
        otel_flag = (os.getenv("OTEL_ENABLED") or "").strip().lower() in {"1", "true", "yes"}
        return ObservabilitySettings(
            mode=raw_mode,  # type: ignore[arg-type]
            log_level=(os.getenv("LOG_LEVEL") or "INFO").strip().upper(),
            log_format=(os.getenv("LOG_FORMAT") or ("json" if env_name != "dev" else "text")).strip().lower(),
            service_name=(os.getenv("OTEL_SERVICE_NAME") or "arq-ia-api").strip(),
            environment=env_name,
            app_version=(os.getenv("APP_VERSION") or "dev").strip(),
            metrics_token=metrics_token,
            require_metrics_token=require_token,
            otel_enabled=otel_flag or raw_mode == "full",
            otel_endpoint=otel_endpoint,
            component="api",
        )
