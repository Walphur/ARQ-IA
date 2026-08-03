"""Wire MDO: migraciones Alembic + HTTP deps (composition root en main)."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import Engine

_MDO_ROOT = Path(__file__).resolve().parent
_configured = False


def run_mdo_migrations(database_url: str) -> None:
    """Aplica migraciones Alembic del dominio MDO (tabla `mdo_alembic_version`)."""
    ini = _MDO_ROOT / "alembic.ini"
    cfg = Config(str(ini))
    cfg.set_main_option("script_location", str(_MDO_ROOT / "migrations"))
    cfg.set_main_option("sqlalchemy.url", database_url)
    cfg.set_main_option("version_table", "mdo_alembic_version")
    import sys

    backend_root = str(_MDO_ROOT.parent)
    if backend_root not in sys.path:
        sys.path.insert(0, backend_root)
    command.upgrade(cfg, "head")


def bind_mdo_deps(
    *,
    get_db: Callable,
    current_user: Callable,
    require_can_edit: Callable,
    project_belongs_to_studio: Callable,
) -> None:
    from mdo.http import bind_http_deps

    bind_http_deps(
        get_db=get_db,
        current_user=current_user,
        require_can_edit=require_can_edit,
        project_belongs_to_studio=project_belongs_to_studio,
    )


def configure_mdo(
    *,
    database_url: str,
    get_db: Callable,
    current_user: Callable,
    require_can_edit: Callable,
    project_belongs_to_studio: Callable,
    engine: Optional[Engine] = None,
    run_migrations: bool = True,
) -> None:
    global _configured
    bind_mdo_deps(
        get_db=get_db,
        current_user=current_user,
        require_can_edit=require_can_edit,
        project_belongs_to_studio=project_belongs_to_studio,
    )
    if run_migrations:
        run_mdo_migrations(database_url)
    _configured = True
    _ = engine


def reset_mdo_for_tests() -> None:
    global _configured
    _configured = False
