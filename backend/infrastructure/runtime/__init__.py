"""Runtime status: liveness, readiness, platform mode projection (E01-F02)."""

from infrastructure.runtime.setup import configure_runtime, get_runtime, reset_runtime_for_tests

__all__ = ["configure_runtime", "get_runtime", "reset_runtime_for_tests"]
