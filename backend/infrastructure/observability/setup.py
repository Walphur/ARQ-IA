"""Wire OBS_MODE to concrete adapters. Only place that selects vendors."""

from __future__ import annotations

from typing import Optional

from infrastructure.observability.adapters.clock import SystemClock
from infrastructure.observability.adapters.ids import UuidIdGenerator
from infrastructure.observability.adapters.inmemory_metrics import InMemoryMetrics
from infrastructure.observability.adapters.null import NullLogger, NullMetrics, NullTracer
from infrastructure.observability.adapters.otel import build_tracer
from infrastructure.observability.adapters.stdlib_logging import StdlibLoggerAdapter
from infrastructure.observability.config import ObservabilitySettings
from infrastructure.observability.service import ObservabilityService

_service: Optional[ObservabilityService] = None


def configure_observability(settings: Optional[ObservabilitySettings] = None) -> ObservabilityService:
    global _service
    cfg = settings or ObservabilitySettings.from_env()
    clock = SystemClock()
    ids = UuidIdGenerator()

    if cfg.mode == "off":
        logger = StdlibLoggerAdapter(level="WARNING", fmt="text", service=cfg.service_name)
        tracer = NullTracer()
        metrics = NullMetrics()
    else:
        logger = StdlibLoggerAdapter(level=cfg.log_level, fmt=cfg.log_format, service=cfg.service_name)
        export = cfg.mode == "full" and bool(cfg.otel_endpoint)
        tracer = build_tracer(
            mode=cfg.mode,
            service_name=cfg.service_name,
            endpoint=cfg.otel_endpoint,
            export=export,
        )
        metrics = InMemoryMetrics(
            service=cfg.service_name,
            environment=cfg.environment,
            version=cfg.app_version,
        )
        if cfg.mode == "full" and not cfg.otel_endpoint:
            logger.emit(
                "warning",
                "OBS_MODE=full without OTEL_EXPORTER_OTLP_ENDPOINT; tracing stays in-process",
                {"feature": "observability", "module": "setup", "environment": cfg.environment},
            )

    _service = ObservabilityService(
        settings=cfg,
        clock=clock,
        ids=ids,
        logger=logger,
        tracer=tracer,
        metrics=metrics,
    )
    return _service


def get_observability() -> ObservabilityService:
    global _service
    if _service is None:
        return configure_observability()
    return _service


def reset_observability_for_tests() -> None:
    global _service
    _service = None
