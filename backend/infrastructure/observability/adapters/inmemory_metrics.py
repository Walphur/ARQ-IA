"""In-process metrics behind MetricsPort. Exposition text is an adapter detail."""

from __future__ import annotations

import threading
from collections import defaultdict
from typing import DefaultDict, Dict, Tuple

from infrastructure.observability.taxonomy import filter_metric_labels

COMPONENT_ALLOWLIST = frozenset({"db", "object_storage", "broker", "platform"})
COMPONENT_STATUSES = frozenset({"ok", "fail", "skipped", "timeout", "unknown"})
PLATFORM_MODES = frozenset({"normal", "degraded", "maintenance", "readonly"})


class InMemoryMetrics:
    def __init__(self, *, service: str, environment: str, version: str) -> None:
        self._lock = threading.Lock()
        self._service = service
        self._environment = environment
        self._version = version
        self._counters: DefaultDict[Tuple[str, str, str], float] = defaultdict(float)
        self._latency_sum: DefaultDict[Tuple[str, str, str], float] = defaultdict(float)
        self._latency_count: DefaultDict[Tuple[str, str, str], float] = defaultdict(float)
        self._component_status: Dict[Tuple[str, str], float] = {}
        self._ready: float = 1.0
        self._mode_gauges: Dict[str, float] = {m: 0.0 for m in PLATFORM_MODES}
        self._mode_gauges["normal"] = 1.0

    def _base_labels(self, route_template: str, status_class: str) -> Dict[str, str]:
        return filter_metric_labels(
            {
                "service": self._service,
                "env": self._environment,
                "environment": self._environment,
                "route_template": route_template,
                "status_class": status_class,
                "version": self._version,
                "component": "api",
            }
        )

    def inc_request(self, *, route_template: str, status_class: str) -> None:
        labels = self._base_labels(route_template, status_class)
        key = (labels.get("route_template", "/"), labels.get("status_class", "2xx"), labels.get("env", "dev"))
        with self._lock:
            self._counters[key] += 1.0

    def observe_latency(self, seconds: float, *, route_template: str, status_class: str) -> None:
        labels = self._base_labels(route_template, status_class)
        key = (labels.get("route_template", "/"), labels.get("status_class", "2xx"), labels.get("env", "dev"))
        with self._lock:
            self._latency_sum[key] += max(0.0, float(seconds))
            self._latency_count[key] += 1.0

    def set_component_status(self, component: str, status: str) -> None:
        if component not in COMPONENT_ALLOWLIST or status not in COMPONENT_STATUSES:
            return
        with self._lock:
            for st in COMPONENT_STATUSES:
                self._component_status[(component, st)] = 1.0 if st == status else 0.0

    def set_ready(self, value: bool) -> None:
        with self._lock:
            self._ready = 1.0 if value else 0.0

    def set_platform_mode(self, mode: str) -> None:
        if mode not in PLATFORM_MODES:
            return
        with self._lock:
            for m in PLATFORM_MODES:
                self._mode_gauges[m] = 1.0 if m == mode else 0.0

    def render_exposition(self) -> str:
        lines = [
            "# HELP arqia_http_requests_total Count of HTTP requests",
            "# TYPE arqia_http_requests_total counter",
        ]
        with self._lock:
            for (route, status, env), value in sorted(self._counters.items()):
                lines.append(
                    f'arqia_http_requests_total{{service="{self._service}",env="{env}",'
                    f'route_template="{route}",status_class="{status}",version="{self._version}"}} {value}'
                )
            lines.append("# HELP arqia_http_request_duration_seconds_sum Latency sum")
            lines.append("# TYPE arqia_http_request_duration_seconds_sum counter")
            for (route, status, env), value in sorted(self._latency_sum.items()):
                lines.append(
                    f'arqia_http_request_duration_seconds_sum{{service="{self._service}",env="{env}",'
                    f'route_template="{route}",status_class="{status}",version="{self._version}"}} {value}'
                )
            lines.append("# HELP arqia_http_request_duration_seconds_count Latency count")
            lines.append("# TYPE arqia_http_request_duration_seconds_count counter")
            for (route, status, env), value in sorted(self._latency_count.items()):
                lines.append(
                    f'arqia_http_request_duration_seconds_count{{service="{self._service}",env="{env}",'
                    f'route_template="{route}",status_class="{status}",version="{self._version}"}} {value}'
                )
            lines.append("# HELP arqia_component_status Component runtime status (0/1)")
            lines.append("# TYPE arqia_component_status gauge")
            for (component, status), value in sorted(self._component_status.items()):
                lines.append(
                    f'arqia_component_status{{component="{component}",status="{status}",'
                    f'service="{self._service}",version="{self._version}"}} {value}'
                )
            lines.append("# HELP arqia_platform_ready Aggregate readiness (1=ready)")
            lines.append("# TYPE arqia_platform_ready gauge")
            lines.append(
                f'arqia_platform_ready{{service="{self._service}",version="{self._version}"}} {self._ready}'
            )
            lines.append("# HELP arqia_platform_mode Platform mode gauge (0/1)")
            lines.append("# TYPE arqia_platform_mode gauge")
            for mode, value in sorted(self._mode_gauges.items()):
                lines.append(
                    f'arqia_platform_mode{{mode="{mode}",service="{self._service}",'
                    f'version="{self._version}"}} {value}'
                )
        return "\n".join(lines) + "\n"
