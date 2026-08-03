"""MDO setup — migraciones formales Alembic (Fase 1).

HTTP binding se agrega en Fase 2; este módulo no importa routers ni main.
"""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config

_MDO_ROOT = Path(__file__).resolve().parent


def run_mdo_migrations(database_url: str) -> None:
    """Aplica migraciones Alembic del dominio MDO (tabla `mdo_alembic_version`).

    El resto del proyecto puede seguir con create_all(); MDO no usa create_all.
    Plan: cuando Identity/legacy migre a Alembic global, este historial
    puede consolidarse o quedar como branch labels `mdo` aislado.
    """
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
