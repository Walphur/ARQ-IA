"""Stubs for components not configured until E03/E04."""

from __future__ import annotations

from infrastructure.runtime.models import CheckResult


class NotConfiguredComponentCheck:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def check(self) -> CheckResult:
        return CheckResult(
            name=self._name,
            status="skipped",
            reason="not_configured",
        )
