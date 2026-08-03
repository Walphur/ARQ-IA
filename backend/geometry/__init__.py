"""Geometry Engine — dominio independiente (E03-F02 / Roadmap E06 thin slice).

Lee MDO, calcula medidas, persiste ElementGeometry/GeometryIssue.
No importa motor_ia ni mdo.perception_*.
"""

from geometry.setup import bind_geometry_deps, run_geometry_migrations

__all__ = ["bind_geometry_deps", "run_geometry_migrations"]
