"""Runtime DTOs (no ORM)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str  # ok|fail|skipped|timeout
    latency_ms: Optional[float] = None
    reason: Optional[str] = None
    error_class: Optional[str] = None

    def to_public_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"name": self.name, "status": self.status}
        if self.latency_ms is not None:
            data["latency_ms"] = self.latency_ms
        if self.reason:
            data["reason"] = self.reason
        if self.error_class:
            data["error_class"] = self.error_class
        return data


@dataclass
class ReadyReport:
    status: str  # ready|not_ready
    version: str
    checks: list[CheckResult] = field(default_factory=list)
    http_status: int = 200

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "version": self.version,
            "checks": [c.to_public_dict() for c in self.checks],
        }


@dataclass
class PlatformCapabilities:
    reads: bool
    writes: bool
    calcular: bool
    exports: bool
    ai: bool

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass
class PlatformStatus:
    mode: str
    degraded: bool
    reasons: list[str]
    capabilities: PlatformCapabilities
    ready: bool
    version: str
    api_version: str
    generated_at: str
    request_id: Optional[str] = None

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "degraded": self.degraded,
            "reasons": list(self.reasons),
            "capabilities": self.capabilities.to_dict(),
            "ready": self.ready,
            "version": self.version,
            "api_version": self.api_version,
            "generated_at": self.generated_at,
            "request_id": self.request_id,
        }
