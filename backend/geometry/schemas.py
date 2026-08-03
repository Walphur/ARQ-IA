from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ElementGeometryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    studio_id: int
    project_id: int
    version_id: str
    element_id: str
    geom_type: str
    units: str
    length_m: Optional[float] = None
    height_m: Optional[float] = None
    thickness_m: Optional[float] = None
    area_m2: Optional[float] = None
    volume_m3: Optional[float] = None
    bbox: Optional[Any] = None
    polygon: Optional[Any] = None
    centroid: Optional[Any] = None
    orientation_deg: Optional[float] = None
    measure_meta: dict[str, Any] = Field(default_factory=dict)
    quality_flags: list[Any] = Field(default_factory=list)
    computed_at: datetime
    compute_run_id: str
    created_at: datetime
    updated_at: datetime


class GeometryIssueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    studio_id: int
    project_id: int
    version_id: str
    element_id: Optional[str] = None
    element_geometry_id: Optional[str] = None
    code: str
    message: str
    severity: str
    source: str
    details: Optional[dict[str, Any]] = None
    compute_run_id: str
    created_at: datetime


class GeometryComputeResponse(BaseModel):
    version_id: str
    compute_run_id: str
    geometries_upserted: int = Field(ge=0)
    issues_created: int = Field(ge=0)
    geometries: list[ElementGeometryOut]
    issues: list[GeometryIssueOut]


class GeometryListResponse(BaseModel):
    version_id: str
    geometries: list[ElementGeometryOut]
    issues: list[GeometryIssueOut]


def serialize_geometry(row) -> dict[str, Any]:
    return ElementGeometryOut.model_validate(row).model_dump(mode="json")


def serialize_issue(row) -> dict[str, Any]:
    return GeometryIssueOut.model_validate(row).model_dump(mode="json")
