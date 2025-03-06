from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NotificationCreate(BaseModel):
    incident_id: int
    channel: str
    destination: str
    severity: str
    error: Optional[str] = None


class NotificationResponse(BaseModel):
    id: int
    incident_id: int
    channel: str
    destination: str
    sent_at: datetime
    severity: str
    error: Optional[str] = None

    class Config:
        orm_mode = True


class NotificationsListResponse(BaseModel):
    total: int
    items: List[NotificationResponse]
