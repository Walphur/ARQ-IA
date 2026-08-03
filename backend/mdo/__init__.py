"""Modelo Digital de la Obra (MDO) — dominio SoT de la obra digital.

E02-F01 / Roadmap E07-F01: estructura de datos core.
Independiente de percepción, materiales, costos, IA y frontend.
"""

from mdo.setup import bind_mdo_deps, configure_mdo, run_mdo_migrations

__all__ = ["bind_mdo_deps", "configure_mdo", "run_mdo_migrations"]
