"""Fase 1 — migraciones Alembic, columnas de contrato, independencia de imports."""

from __future__ import annotations

import ast
from pathlib import Path

from sqlalchemy import create_engine, inspect

from mdo.models import (
    Building,
    Discipline,
    Element,
    Level,
    ParameterSet,
    ProjectVersion,
    Site,
    Space,
)
from mdo.setup import run_mdo_migrations

BACKEND = Path(__file__).resolve().parents[1]
MDO_ROOT = BACKEND / "mdo"

FORBIDDEN_MDO_IMPORTS = {
    "motor_ia",
    "presupuesto_pdf",
    "billing_mp",
    "email_service",
    "main",
}

FORBIDDEN_REVERSE = {
    "mdo",
    "mdo.models",
    "mdo.service",
    "mdo.http",
}

REVERSE_SCAN_FILES = [
    "motor_ia.py",
    "presupuesto_pdf.py",
    "billing_mp.py",
    "email_service.py",
]

ENTITY_MODELS = [
    ProjectVersion,
    Site,
    Building,
    Level,
    Space,
    Discipline,
    Element,
    ParameterSet,
]

REQUIRED_AUDIT = {"created_at", "updated_at", "created_by", "updated_by", "deleted_at"}
REQUIRED_TENANT = {"studio_id", "project_id"}
REQUIRED_INTEGRATION = {"external_id"}
REQUIRED_DISPLAY = {"display_name"}


def test_alembic_creates_mdo_tables(tmp_path):
    url = f"sqlite:///{tmp_path / 'mdo_phase1.db'}"
    run_mdo_migrations(url)
    insp = inspect(create_engine(url))
    tables = set(insp.get_table_names())
    assert "mdo_alembic_version" in tables
    for name in (
        "mdo_project_versions",
        "mdo_sites",
        "mdo_buildings",
        "mdo_levels",
        "mdo_spaces",
        "mdo_disciplines",
        "mdo_elements",
        "mdo_parameter_sets",
        "mdo_domain_events",
    ):
        assert name in tables


def test_entities_have_audit_tenant_external_display():
    for model in ENTITY_MODELS:
        cols = set(model.__table__.columns.keys())
        missing_audit = REQUIRED_AUDIT - cols
        missing_tenant = REQUIRED_TENANT - cols
        assert not missing_audit, f"{model.__name__} falta audit: {missing_audit}"
        assert not missing_tenant, f"{model.__name__} falta tenant: {missing_tenant}"
        assert REQUIRED_INTEGRATION <= cols, f"{model.__name__} falta external_id"
        assert REQUIRED_DISPLAY <= cols, f"{model.__name__} falta display_name"


def test_element_has_split_classification_columns():
    cols = set(Element.__table__.columns.keys())
    assert "discipline_code" in cols
    assert "element_type" in cols
    assert "discipline_id" in cols


def test_discipline_table_not_system():
    assert Discipline.__tablename__ == "mdo_disciplines"
    assert not hasattr(__import__("mdo.models", fromlist=["System"]), "System")


def test_mdo_package_has_no_forbidden_imports():
    violations = []
    for path in MDO_ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        rel = path.relative_to(BACKEND).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root in FORBIDDEN_MDO_IMPORTS:
                        violations.append(f"{rel}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".")[0]
                if root in FORBIDDEN_MDO_IMPORTS:
                    violations.append(f"{rel}: from {node.module}")
    assert violations == []


def test_perception_and_adjacent_modules_do_not_import_mdo():
    violations = []
    for fname in REVERSE_SCAN_FILES:
        path = BACKEND / fname
        if not path.exists():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=fname)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] == "mdo":
                        violations.append(f"{fname}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split(".")[0] == "mdo":
                    violations.append(f"{fname}: from {node.module}")
    assert violations == []
