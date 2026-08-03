"""Ensure domain modules do not import vendor observability SDKs."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN = {
    "opentelemetry",
    "opentelemetry.trace",
    "opentelemetry.sdk",
    "prometheus_client",
}

ALLOWED_PREFIX = "infrastructure/observability/adapters/"


def _iter_py_files():
    root = Path(__file__).resolve().parents[1]
    for path in root.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("tests/"):
            continue
        yield path, rel


def test_no_vendor_imports_outside_adapters():
    violations = []
    for path, rel in _iter_py_files():
        if rel.startswith(ALLOWED_PREFIX):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name
                    if name in FORBIDDEN or name.startswith("opentelemetry"):
                        violations.append(f"{rel}: import {name}")
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if mod in FORBIDDEN or mod.startswith("opentelemetry") or mod.startswith("prometheus_client"):
                    violations.append(f"{rel}: from {mod}")
    assert violations == []
