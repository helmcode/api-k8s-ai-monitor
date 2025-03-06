from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy import select
from schemas.notifications import NotificationCreate, NotificationsListResponse, NotificationResponse
from models.incident_notifications import IncidentNotification
from models.incidents import Incident
from config.db import SessionLocal


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=NotificationResponse, status_code=201)
def create_notification(notification: NotificationCreate):
    """
    Create a new notification.
    """
    try:
        db = SessionLocal()
        incident = db.query(Incident).filter(Incident.id == notification.incident_id).first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        new_notification = IncidentNotification(
            incident_id=notification.incident_id,
            channel=notification.channel,
            destination=notification.destination,
            severity=notification.severity,
            status="sent",
            error=notification.error
        )

        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
        return new_notification
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/", response_model=NotificationsListResponse)
def read_notifications(
    incident_id: Optional[int] = None,
    channel: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Retrieve notifications with optional filtering.
    """
    try:
        db = SessionLocal()
        query = select(IncidentNotification)
        if incident_id:
            query = query.filter_by(incident_id=incident_id)
        if channel:
            query = query.filter_by(channel=channel)
        if status:
            query = query.filter_by(status=status)
        notifications = db.execute(query).scalars().all()
        return {"total": len(notifications), "items": notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/{notification_id}", response_model=NotificationResponse)
def read_notification(notification_id: int):
    """
    Get a specific notification by ID.
    """
    try:
        db = SessionLocal()
        notification = db.query(IncidentNotification).filter(IncidentNotification.id == notification_id).first()

        if not notification:
            return JSONResponse(status_code=204, content={"message": "Notification not found"})
        return notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.delete("/{notification_id}", status_code=204)
def delete_notification(notification_id: int):
    """
    Delete a notification.
    """
    try:
        db = SessionLocal()
        notification = db.query(IncidentNotification).filter(IncidentNotification.id == notification_id).first()

        if not notification:
            return JSONResponse(status_code=204, content={"message": "Notification not found"})
        db.delete(notification)
        db.commit()
        return JSONResponse(status_code=204, content={"message": "Notification deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
