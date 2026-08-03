"""Modelos SQLAlchemy del dominio Geometry (Base propia)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import JSON

GeometryBase = declarative_base()


def _uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ElementGeometry(GeometryBase):
    __tablename__ = "geometry_element_geometries"

    id = Column(String(36), primary_key=True, default=_uuid)
    studio_id = Column(Integer, nullable=False, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    version_id = Column(String(36), nullable=False, index=True)
    element_id = Column(String(36), nullable=False, index=True)
    geom_type = Column(String(40), nullable=False)
    units = Column(String(40), nullable=False, default="m")
    length_m = Column(Float, nullable=True)
    height_m = Column(Float, nullable=True)
    thickness_m = Column(Float, nullable=True)
    area_m2 = Column(Float, nullable=True)
    volume_m3 = Column(Float, nullable=True)
    bbox = Column(JSON, nullable=True)
    polygon = Column(JSON, nullable=True)
    centroid = Column(JSON, nullable=True)
    orientation_deg = Column(Float, nullable=True)
    measure_meta = Column(JSON, nullable=False, default=dict)
    quality_flags = Column(JSON, nullable=False, default=list)
    computed_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    compute_run_id = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_geom_eg_version_element", "version_id", "element_id"),
        Index("ix_geom_eg_tenant_version", "studio_id", "project_id", "version_id"),
    )


class GeometryIssue(GeometryBase):
    __tablename__ = "geometry_issues"

    id = Column(String(36), primary_key=True, default=_uuid)
    studio_id = Column(Integer, nullable=False, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    version_id = Column(String(36), nullable=False, index=True)
    element_id = Column(String(36), nullable=True, index=True)
    element_geometry_id = Column(String(36), nullable=True, index=True)
    code = Column(String(80), nullable=False, index=True)
    message = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # info|warning|error
    source = Column(String(40), nullable=False)  # validator|compute|ingest
    details = Column(JSON, nullable=True)
    compute_run_id = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_geom_issues_version_sev", "version_id", "severity"),
    )


class GeometryDomainEvent(GeometryBase):
    __tablename__ = "geometry_domain_events"

    id = Column(String(36), primary_key=True, default=_uuid)
    studio_id = Column(Integer, nullable=False, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    version_id = Column(String(36), nullable=True, index=True)
    event_type = Column(String(80), nullable=False, index=True)
    payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    created_by = Column(Integer, nullable=True)
