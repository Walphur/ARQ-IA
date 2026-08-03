"""Modelos SQLAlchemy del MDO (Base propia — fuera de create_all legacy)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import JSON

MdoBase = declarative_base()


def _uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AuditColumns:
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class TenantColumns:
    studio_id = Column(Integer, nullable=False, index=True)
    project_id = Column(Integer, nullable=False, index=True)


class ProjectVersion(MdoBase, AuditColumns, TenantColumns):
    __tablename__ = "mdo_project_versions"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_number = Column(Integer, nullable=False, default=1)
    status = Column(String(20), nullable=False, default="active")
    parent_version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=True)
    code = Column(String(80), nullable=True)
    display_name = Column(String(180), nullable=False, default="Versión 1")
    external_id = Column(String(120), nullable=True)
    summary = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("project_id", "version_number", name="uq_mdo_version_project_number"),
        Index("ix_mdo_versions_project_status", "project_id", "status"),
        Index("ix_mdo_versions_external", "studio_id", "external_id"),
    )

    sites = relationship("Site", back_populates="version")
    disciplines = relationship("Discipline", back_populates="version")
    elements = relationship("Element", back_populates="version")


class Site(MdoBase, AuditColumns, TenantColumns):
    __tablename__ = "mdo_sites"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=False, index=True)
    code = Column(String(80), nullable=True)
    display_name = Column(String(180), nullable=False)
    external_id = Column(String(120), nullable=True)
    lot_ref = Column(String(180), nullable=True)
    area_m2 = Column(Float, nullable=True)

    __table_args__ = (Index("ix_mdo_sites_external", "studio_id", "external_id"),)

    version = relationship("ProjectVersion", back_populates="sites")
    buildings = relationship("Building", back_populates="site")


class Building(MdoBase, AuditColumns, TenantColumns):
    __tablename__ = "mdo_buildings"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("mdo_sites.id"), nullable=False, index=True)
    code = Column(String(80), nullable=True)
    display_name = Column(String(180), nullable=False)
    external_id = Column(String(120), nullable=True)
    typology = Column(String(80), nullable=True)

    __table_args__ = (Index("ix_mdo_buildings_external", "studio_id", "external_id"),)

    site = relationship("Site", back_populates="buildings")
    levels = relationship("Level", back_populates="building")


class Level(MdoBase, AuditColumns, TenantColumns):
    __tablename__ = "mdo_levels"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=False, index=True)
    building_id = Column(String(36), ForeignKey("mdo_buildings.id"), nullable=False, index=True)
    code = Column(String(80), nullable=True)
    display_name = Column(String(180), nullable=False)
    external_id = Column(String(120), nullable=True)
    elevation_m = Column(Float, nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)

    __table_args__ = (Index("ix_mdo_levels_external", "studio_id", "external_id"),)

    building = relationship("Building", back_populates="levels")
    spaces = relationship("Space", back_populates="level")
    elements = relationship("Element", back_populates="level")


class Space(MdoBase, AuditColumns, TenantColumns):
    __tablename__ = "mdo_spaces"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=False, index=True)
    level_id = Column(String(36), ForeignKey("mdo_levels.id"), nullable=False, index=True)
    code = Column(String(80), nullable=True)
    display_name = Column(String(180), nullable=False)
    external_id = Column(String(120), nullable=True)
    space_type = Column(String(80), nullable=True)  # open string, not closed enum
    area_m2 = Column(Float, nullable=True)

    __table_args__ = (Index("ix_mdo_spaces_external", "studio_id", "external_id"),)

    level = relationship("Level", back_populates="spaces")
    elements = relationship("Element", back_populates="space")


class Discipline(MdoBase, AuditColumns, TenantColumns):
    """Agrupación por disciplina constructiva/MEP.

    Reemplaza el concepto ambiguo `System` del diseño inicial PASO 2
    para evitar colisión futura con 'system' de instalaciones como grafo
    de nodos/conexiones (RFC §2.4 — diferido).
    """

    __tablename__ = "mdo_disciplines"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=False, index=True)
    code = Column(String(64), nullable=False)
    display_name = Column(String(180), nullable=False)
    external_id = Column(String(120), nullable=True)
    description = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("version_id", "code", name="uq_mdo_discipline_version_code"),
        Index("ix_mdo_disciplines_external", "studio_id", "external_id"),
    )

    version = relationship("ProjectVersion", back_populates="disciplines")
    elements = relationship("Element", back_populates="discipline")


class Element(MdoBase, AuditColumns, TenantColumns):
    """Elemento constructivo.

    Clasificación en dos ejes (no enum monolítico):
    - discipline_code: disciplina (architecture, structure, plumbing, ...)
    - element_type: tipo concreto (wall.masonry.brick, opening.door, ...)
    """

    __tablename__ = "mdo_elements"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=False, index=True)
    level_id = Column(String(36), ForeignKey("mdo_levels.id"), nullable=True, index=True)
    space_id = Column(String(36), ForeignKey("mdo_spaces.id"), nullable=True, index=True)
    discipline_id = Column(String(36), ForeignKey("mdo_disciplines.id"), nullable=True, index=True)
    discipline_code = Column(String(64), nullable=False, index=True)
    element_type = Column(String(120), nullable=False, index=True)
    code = Column(String(80), nullable=True)
    display_name = Column(String(180), nullable=False)
    external_id = Column(String(120), nullable=True)

    __table_args__ = (
        Index("ix_mdo_elements_class", "version_id", "discipline_code", "element_type"),
        Index("ix_mdo_elements_external", "studio_id", "external_id"),
    )

    version = relationship("ProjectVersion", back_populates="elements")
    level = relationship("Level", back_populates="elements")
    space = relationship("Space", back_populates="elements")
    discipline = relationship("Discipline", back_populates="elements")


class ParameterSet(MdoBase, AuditColumns, TenantColumns):
    """Parámetros variables + metadata. NO hechos estructurales del grafo.

    Contrato de `data`:
      { "params": {...}, "metadata": {...} }
    Ver `typing_rules.normalize_parameter_set_data`.
    """

    __tablename__ = "mdo_parameter_sets"

    id = Column(String(36), primary_key=True, default=_uuid)
    version_id = Column(String(36), ForeignKey("mdo_project_versions.id"), nullable=False, index=True)
    owner_kind = Column(String(40), nullable=False)
    owner_id = Column(String(36), nullable=False, index=True)
    code = Column(String(80), nullable=True)
    display_name = Column(String(180), nullable=True)
    external_id = Column(String(120), nullable=True)
    schema_version = Column(String(40), nullable=False, default="1")
    data = Column(JSON, nullable=False, default=lambda: {"params": {}, "metadata": {}})

    __table_args__ = (
        Index("ix_mdo_params_owner", "version_id", "owner_kind", "owner_id"),
        Index("ix_mdo_params_external", "studio_id", "external_id"),
    )


class DomainEvent(MdoBase):
    """Log append-only de formas de evento (sin outbox/publisher — E04)."""

    __tablename__ = "mdo_domain_events"

    id = Column(String(36), primary_key=True, default=_uuid)
    studio_id = Column(Integer, nullable=False, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    version_id = Column(String(36), nullable=True, index=True)
    event_type = Column(String(80), nullable=False, index=True)
    payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    created_by = Column(Integer, nullable=True)
