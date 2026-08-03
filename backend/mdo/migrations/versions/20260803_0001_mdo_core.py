"""MDO core schema v1 (E02-F01).

Revision ID: 20260803_0001
Revises:
Create Date: 2026-08-03

Tablas: mdo_project_versions, mdo_sites, mdo_buildings, mdo_levels,
mdo_spaces, mdo_disciplines, mdo_elements, mdo_parameter_sets, mdo_domain_events.

Nota: System del diseño inicial se materializa como Discipline.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260803_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mdo_project_versions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("parent_version_id", sa.String(length=36), nullable=True),
        sa.Column("code", sa.String(length=80), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["parent_version_id"], ["mdo_project_versions.id"]),
        sa.UniqueConstraint("project_id", "version_number", name="uq_mdo_version_project_number"),
    )
    op.create_index("ix_mdo_project_versions_studio_id", "mdo_project_versions", ["studio_id"])
    op.create_index("ix_mdo_project_versions_project_id", "mdo_project_versions", ["project_id"])
    op.create_index("ix_mdo_versions_project_status", "mdo_project_versions", ["project_id", "status"])
    op.create_index("ix_mdo_versions_external", "mdo_project_versions", ["studio_id", "external_id"])

    op.create_table(
        "mdo_sites",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("lot_ref", sa.String(length=180), nullable=True),
        sa.Column("area_m2", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["version_id"], ["mdo_project_versions.id"]),
    )
    op.create_index("ix_mdo_sites_version_id", "mdo_sites", ["version_id"])
    op.create_index("ix_mdo_sites_studio_id", "mdo_sites", ["studio_id"])
    op.create_index("ix_mdo_sites_project_id", "mdo_sites", ["project_id"])
    op.create_index("ix_mdo_sites_external", "mdo_sites", ["studio_id", "external_id"])

    op.create_table(
        "mdo_buildings",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("site_id", sa.String(length=36), nullable=False),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("typology", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["version_id"], ["mdo_project_versions.id"]),
        sa.ForeignKeyConstraint(["site_id"], ["mdo_sites.id"]),
    )
    op.create_index("ix_mdo_buildings_version_id", "mdo_buildings", ["version_id"])
    op.create_index("ix_mdo_buildings_site_id", "mdo_buildings", ["site_id"])
    op.create_index("ix_mdo_buildings_studio_id", "mdo_buildings", ["studio_id"])
    op.create_index("ix_mdo_buildings_project_id", "mdo_buildings", ["project_id"])
    op.create_index("ix_mdo_buildings_external", "mdo_buildings", ["studio_id", "external_id"])

    op.create_table(
        "mdo_levels",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("building_id", sa.String(length=36), nullable=False),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("elevation_m", sa.Float(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["version_id"], ["mdo_project_versions.id"]),
        sa.ForeignKeyConstraint(["building_id"], ["mdo_buildings.id"]),
    )
    op.create_index("ix_mdo_levels_version_id", "mdo_levels", ["version_id"])
    op.create_index("ix_mdo_levels_building_id", "mdo_levels", ["building_id"])
    op.create_index("ix_mdo_levels_studio_id", "mdo_levels", ["studio_id"])
    op.create_index("ix_mdo_levels_project_id", "mdo_levels", ["project_id"])
    op.create_index("ix_mdo_levels_external", "mdo_levels", ["studio_id", "external_id"])

    op.create_table(
        "mdo_spaces",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("level_id", sa.String(length=36), nullable=False),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("space_type", sa.String(length=80), nullable=True),
        sa.Column("area_m2", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["version_id"], ["mdo_project_versions.id"]),
        sa.ForeignKeyConstraint(["level_id"], ["mdo_levels.id"]),
    )
    op.create_index("ix_mdo_spaces_version_id", "mdo_spaces", ["version_id"])
    op.create_index("ix_mdo_spaces_level_id", "mdo_spaces", ["level_id"])
    op.create_index("ix_mdo_spaces_studio_id", "mdo_spaces", ["studio_id"])
    op.create_index("ix_mdo_spaces_project_id", "mdo_spaces", ["project_id"])
    op.create_index("ix_mdo_spaces_external", "mdo_spaces", ["studio_id", "external_id"])

    op.create_table(
        "mdo_disciplines",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["version_id"], ["mdo_project_versions.id"]),
        sa.UniqueConstraint("version_id", "code", name="uq_mdo_discipline_version_code"),
    )
    op.create_index("ix_mdo_disciplines_version_id", "mdo_disciplines", ["version_id"])
    op.create_index("ix_mdo_disciplines_studio_id", "mdo_disciplines", ["studio_id"])
    op.create_index("ix_mdo_disciplines_project_id", "mdo_disciplines", ["project_id"])
    op.create_index("ix_mdo_disciplines_external", "mdo_disciplines", ["studio_id", "external_id"])

    op.create_table(
        "mdo_elements",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("level_id", sa.String(length=36), nullable=True),
        sa.Column("space_id", sa.String(length=36), nullable=True),
        sa.Column("discipline_id", sa.String(length=36), nullable=True),
        sa.Column("discipline_code", sa.String(length=64), nullable=False),
        sa.Column("element_type", sa.String(length=120), nullable=False),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["version_id"], ["mdo_project_versions.id"]),
        sa.ForeignKeyConstraint(["level_id"], ["mdo_levels.id"]),
        sa.ForeignKeyConstraint(["space_id"], ["mdo_spaces.id"]),
        sa.ForeignKeyConstraint(["discipline_id"], ["mdo_disciplines.id"]),
    )
    op.create_index("ix_mdo_elements_version_id", "mdo_elements", ["version_id"])
    op.create_index("ix_mdo_elements_level_id", "mdo_elements", ["level_id"])
    op.create_index("ix_mdo_elements_space_id", "mdo_elements", ["space_id"])
    op.create_index("ix_mdo_elements_discipline_id", "mdo_elements", ["discipline_id"])
    op.create_index("ix_mdo_elements_discipline_code", "mdo_elements", ["discipline_code"])
    op.create_index("ix_mdo_elements_element_type", "mdo_elements", ["element_type"])
    op.create_index("ix_mdo_elements_studio_id", "mdo_elements", ["studio_id"])
    op.create_index("ix_mdo_elements_project_id", "mdo_elements", ["project_id"])
    op.create_index(
        "ix_mdo_elements_class",
        "mdo_elements",
        ["version_id", "discipline_code", "element_type"],
    )
    op.create_index("ix_mdo_elements_external", "mdo_elements", ["studio_id", "external_id"])

    op.create_table(
        "mdo_parameter_sets",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("owner_kind", sa.String(length=40), nullable=False),
        sa.Column("owner_id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=True),
        sa.Column("display_name", sa.String(length=180), nullable=True),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column("schema_version", sa.String(length=40), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["version_id"], ["mdo_project_versions.id"]),
    )
    op.create_index("ix_mdo_parameter_sets_version_id", "mdo_parameter_sets", ["version_id"])
    op.create_index("ix_mdo_parameter_sets_studio_id", "mdo_parameter_sets", ["studio_id"])
    op.create_index("ix_mdo_parameter_sets_project_id", "mdo_parameter_sets", ["project_id"])
    op.create_index("ix_mdo_parameter_sets_owner_id", "mdo_parameter_sets", ["owner_id"])
    op.create_index(
        "ix_mdo_params_owner",
        "mdo_parameter_sets",
        ["version_id", "owner_kind", "owner_id"],
    )
    op.create_index("ix_mdo_params_external", "mdo_parameter_sets", ["studio_id", "external_id"])

    op.create_table(
        "mdo_domain_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("studio_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("version_id", sa.String(length=36), nullable=True),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
    )
    op.create_index("ix_mdo_domain_events_studio_id", "mdo_domain_events", ["studio_id"])
    op.create_index("ix_mdo_domain_events_project_id", "mdo_domain_events", ["project_id"])
    op.create_index("ix_mdo_domain_events_version_id", "mdo_domain_events", ["version_id"])
    op.create_index("ix_mdo_domain_events_event_type", "mdo_domain_events", ["event_type"])


def downgrade() -> None:
    op.drop_table("mdo_domain_events")
    op.drop_table("mdo_parameter_sets")
    op.drop_table("mdo_elements")
    op.drop_table("mdo_disciplines")
    op.drop_table("mdo_spaces")
    op.drop_table("mdo_levels")
    op.drop_table("mdo_buildings")
    op.drop_table("mdo_sites")
    op.drop_table("mdo_project_versions")
