"""geometry ElementGeometry + GeometryIssue + domain events

Revision ID: 20260405_1200
Revises:
Create Date: 2026-04-05
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260405_1200"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = ("geometry",)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "geometry_element_geometries",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("element_id", sa.String(length=36), nullable=False),
        sa.Column("geom_type", sa.String(length=40), nullable=False),
        sa.Column("units", sa.String(length=40), nullable=False),
        sa.Column("length_m", sa.Float(), nullable=True),
        sa.Column("height_m", sa.Float(), nullable=True),
        sa.Column("thickness_m", sa.Float(), nullable=True),
        sa.Column("area_m2", sa.Float(), nullable=True),
        sa.Column("volume_m3", sa.Float(), nullable=True),
        sa.Column("bbox", sa.JSON(), nullable=True),
        sa.Column("polygon", sa.JSON(), nullable=True),
        sa.Column("centroid", sa.JSON(), nullable=True),
        sa.Column("orientation_deg", sa.Float(), nullable=True),
        sa.Column("measure_meta", sa.JSON(), nullable=False),
        sa.Column("quality_flags", sa.JSON(), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("compute_run_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_geometry_element_geometries_studio_id",
        "geometry_element_geometries",
        ["studio_id"],
    )
    op.create_index(
        "ix_geometry_element_geometries_project_id",
        "geometry_element_geometries",
        ["project_id"],
    )
    op.create_index(
        "ix_geometry_element_geometries_version_id",
        "geometry_element_geometries",
        ["version_id"],
    )
    op.create_index(
        "ix_geometry_element_geometries_element_id",
        "geometry_element_geometries",
        ["element_id"],
    )
    op.create_index(
        "ix_geometry_element_geometries_compute_run_id",
        "geometry_element_geometries",
        ["compute_run_id"],
    )
    op.create_index(
        "ix_geom_eg_version_element",
        "geometry_element_geometries",
        ["version_id", "element_id"],
    )
    op.create_index(
        "ix_geom_eg_tenant_version",
        "geometry_element_geometries",
        ["studio_id", "project_id", "version_id"],
    )

    op.create_table(
        "geometry_issues",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("element_id", sa.String(length=36), nullable=True),
        sa.Column("element_geometry_id", sa.String(length=36), nullable=True),
        sa.Column("code", sa.String(length=80), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("source", sa.String(length=40), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("compute_run_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_geometry_issues_studio_id", "geometry_issues", ["studio_id"])
    op.create_index("ix_geometry_issues_project_id", "geometry_issues", ["project_id"])
    op.create_index("ix_geometry_issues_version_id", "geometry_issues", ["version_id"])
    op.create_index("ix_geometry_issues_element_id", "geometry_issues", ["element_id"])
    op.create_index(
        "ix_geometry_issues_element_geometry_id",
        "geometry_issues",
        ["element_geometry_id"],
    )
    op.create_index("ix_geometry_issues_code", "geometry_issues", ["code"])
    op.create_index("ix_geometry_issues_compute_run_id", "geometry_issues", ["compute_run_id"])
    op.create_index("ix_geom_issues_version_sev", "geometry_issues", ["version_id", "severity"])

    op.create_table(
        "geometry_domain_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=True),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
    )
    op.create_index(
        "ix_geometry_domain_events_studio_id",
        "geometry_domain_events",
        ["studio_id"],
    )
    op.create_index(
        "ix_geometry_domain_events_project_id",
        "geometry_domain_events",
        ["project_id"],
    )
    op.create_index(
        "ix_geometry_domain_events_version_id",
        "geometry_domain_events",
        ["version_id"],
    )
    op.create_index(
        "ix_geometry_domain_events_event_type",
        "geometry_domain_events",
        ["event_type"],
    )


def downgrade() -> None:
    op.drop_index("ix_geometry_domain_events_event_type", table_name="geometry_domain_events")
    op.drop_index("ix_geometry_domain_events_version_id", table_name="geometry_domain_events")
    op.drop_index("ix_geometry_domain_events_project_id", table_name="geometry_domain_events")
    op.drop_index("ix_geometry_domain_events_studio_id", table_name="geometry_domain_events")
    op.drop_table("geometry_domain_events")

    op.drop_index("ix_geom_issues_version_sev", table_name="geometry_issues")
    op.drop_index("ix_geometry_issues_compute_run_id", table_name="geometry_issues")
    op.drop_index("ix_geometry_issues_code", table_name="geometry_issues")
    op.drop_index("ix_geometry_issues_element_geometry_id", table_name="geometry_issues")
    op.drop_index("ix_geometry_issues_element_id", table_name="geometry_issues")
    op.drop_index("ix_geometry_issues_version_id", table_name="geometry_issues")
    op.drop_index("ix_geometry_issues_project_id", table_name="geometry_issues")
    op.drop_index("ix_geometry_issues_studio_id", table_name="geometry_issues")
    op.drop_table("geometry_issues")

    op.drop_index("ix_geom_eg_tenant_version", table_name="geometry_element_geometries")
    op.drop_index("ix_geom_eg_version_element", table_name="geometry_element_geometries")
    op.drop_index(
        "ix_geometry_element_geometries_compute_run_id",
        table_name="geometry_element_geometries",
    )
    op.drop_index(
        "ix_geometry_element_geometries_element_id",
        table_name="geometry_element_geometries",
    )
    op.drop_index(
        "ix_geometry_element_geometries_version_id",
        table_name="geometry_element_geometries",
    )
    op.drop_index(
        "ix_geometry_element_geometries_project_id",
        table_name="geometry_element_geometries",
    )
    op.drop_index(
        "ix_geometry_element_geometries_studio_id",
        table_name="geometry_element_geometries",
    )
    op.drop_table("geometry_element_geometries")
