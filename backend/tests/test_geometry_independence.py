"""Independencia de imports del dominio Geometry."""

from __future__ import annotations

import ast
from pathlib import Path

GEOMETRY_ROOT = Path(__file__).resolve().parents[1] / "geometry"

FORBIDDEN_PREFIXES = (
    "motor_ia",
    "mdo.perception_map",
    "mdo.perception_ingest",
    "mdo.service",
    "mdo.http",
)


def _iter_py_files():
    for path in GEOMETRY_ROOT.rglob("*.py"):
        if path.parent.name == "versions":
            continue
        yield path


def _imported_names(tree: ast.AST) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
            for alias in node.names:
                found.add(f"{node.module}.{alias.name}")
    return found


def _is_forbidden(name: str) -> bool:
    for prefix in FORBIDDEN_PREFIXES:
        if name == prefix or name.startswith(prefix + "."):
            return True
    return False


def test_geometry_does_not_import_perception_or_motor():
    violations: list[str] = []
    for path in _iter_py_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for name in sorted(_imported_names(tree)):
            if _is_forbidden(name):
                rel = path.relative_to(GEOMETRY_ROOT.parent)
                violations.append(f"{rel} → {name}")
    assert violations == [], "Imports prohibidos:\n" + "\n".join(violations)


def test_geometry_package_importable():
    import geometry
    from geometry import bind_geometry_deps, run_geometry_migrations

    assert callable(bind_geometry_deps)
    assert callable(run_geometry_migrations)
    assert geometry.__doc__
