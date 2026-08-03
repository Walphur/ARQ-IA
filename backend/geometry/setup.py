"""Wire Geometry: migraciones Alembic + HTTP deps (composition root en main)."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from alembic import command
from alembic.config import Config

_GEOMETRY_ROOT = Path(__file__).resolve().parent


def run_geometry_migrations(database_url: str) -> None:
    """Aplica migraciones Alembic del dominio Geometry (`geometry_alembic_version`)."""
    ini = _GEOMETRY_ROOT / "alembic.ini"
    cfg = Config(str(ini))
    cfg.set_main_option("script_location", str(_GEOMETRY_ROOT / "migrations"))
    cfg.set_main_option("sqlalchemy.url", database_url)
    cfg.set_main_option("version_table", "geometry_alembic_version")
    import sys

    backend_root = str(_GEOMETRY_ROOT.parent)
    if backend_root not in sys.path:
        sys.path.insert(0, backend_root)
    command.upgrade(cfg, "head")


def bind_geometry_deps(
    *,
    get_db: Callable,
    current_user: Callable,
    require_can_edit: Callable,
    project_belongs_to_studio: Callable,
) -> None:
    from geometry.http import bind_http_deps

    bind_http_deps(
        get_db=get_db,
        current_user=current_user,
        require_can_edit=require_can_edit,
        project_belongs_to_studio=project_belongs_to_studio,
    )
