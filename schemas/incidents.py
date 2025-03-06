from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime


class IncidentCreate(BaseModel):
    cluster: str
    namespace: str
    resource_type: str
    resource_name: str
    issue_type: str
    severity: str
    description: str
    logs: Optional[str] = None
    events: Optional[str] = None
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None
    first_detected: datetime
    last_detected: datetime
    occurrence_count: int
    resolved: bool


class IncidentUpdate(BaseModel):
    issue_type: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    logs: Optional[str] = None
    events: Optional[str] = None
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None
    last_detected: Optional[datetime] = None
    occurrence_count: Optional[int] = None
    resolved: Optional[bool] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None


class IncidentResponse(BaseModel):
    id: int
    cluster: str
    namespace: str
    resource_type: str
    resource_name: str
    issue_type: str
    severity: str
    description: str
    first_detected: datetime
    last_detected: datetime
    occurrence_count: int
    resolved: bool
    logs: Optional[Any] = None
    events: Optional[Any] = None
    diagnosis: Optional[str] = None
    recommendations: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

    class Config:
        orm_mode = True


class IncidentsListResponse(BaseModel):
    total: int
    items: List[IncidentResponse]
