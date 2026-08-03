"""Ports for runtime checks. No vendor imports."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from infrastructure.runtime.models import CheckResult


@runtime_checkable
class DatabaseCheckPort(Protocol):
    def check(self, timeout_ms: int) -> CheckResult: ...


@runtime_checkable
class ComponentCheckPort(Protocol):
    @property
    def name(self) -> str: ...

    def check(self) -> CheckResult: ...
