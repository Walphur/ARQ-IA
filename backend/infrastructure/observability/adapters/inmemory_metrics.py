"""In-process metrics behind MetricsPort. Exposition text is an adapter detail."""

from __future__ import annotations

import threading
from collections import defaultdict
from typing import DefaultDict, Dict, Tuple

from infrastructure.observability.taxonomy import filter_metric_labels


class InMemoryMetrics:
    def __init__(self, *, service: str, environment: str, version: str) -> None:
        self._lock = threading.Lock()
        self._service = service
        self._environment = environment
        self._version = version
        self._counters: DefaultDict[Tuple[str, str, str], float] = defaultdict(float)
        self._latency_sum: DefaultDict[Tuple[str, str, str], float] = defaultdict(float)
        self._latency_count: DefaultDict[Tuple[str, str, str], float] = defaultdict(float)

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
        return "\n".join(lines) + "\n"
