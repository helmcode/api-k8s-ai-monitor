from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
from sqlalchemy import select, desc, asc
from schemas.incidents import IncidentCreate, IncidentsListResponse, IncidentResponse, IncidentUpdate
from models.incidents import Incident
from config.db import SessionLocal


router = APIRouter(
    prefix="/incidents",
    tags=["incidents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=IncidentResponse, status_code=201)
def create_incident(incident: IncidentCreate):
    """
    Create a new incident.
    """
    try:
        db = SessionLocal()
        new_incident = Incident(
            cluster=incident.cluster,
            namespace=incident.namespace,
            resource_type=incident.resource_type,
            resource_name=incident.resource_name,
            issue_type=incident.issue_type,
            severity=incident.severity,
            description=incident.description,
            logs=incident.logs,
            events=incident.events,
            diagnosis=incident.diagnosis,
            recommendations=incident.recommendations,
            first_detected=datetime.utcnow(),
            last_detected=datetime.utcnow(),
            occurrence_count=1,
            resolved=False,
        )

        db.add(new_incident)
        db.commit()
        db.refresh(new_incident)
        return new_incident
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/", response_model=IncidentsListResponse)
def read_incidents(
    cluster: Optional[str] = None,
    namespace: Optional[str] = None,
    resource_type: Optional[str] = None,
    issue_type: Optional[str] = None,
    resolved: Optional[bool] = None,
    sort_by: str = "last_detected",
    sort_desc: bool = True
):
    """
    Retrieve incidents with optional filtering and sorting.
    """
    try:
        db = SessionLocal()
        query = select(Incident)
        if cluster:
            query = query.filter_by(cluster=cluster)
        if namespace:
            query = query.filter_by(namespace=namespace)
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if issue_type:
            query = query.filter_by(issue_type=issue_type)
        if resolved is not None:
            query = query.filter_by(resolved=resolved)
        query = query.order_by(desc(sort_by) if sort_desc else asc(sort_by))
        incidents = db.execute(query).scalars().all()
        return {"total": len(incidents), "items": incidents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/{incident_id}", response_model=IncidentResponse)
def read_incident(incident_id: int):
    """
    Get a specific incident by ID.
    """
    try:
        db = SessionLocal()
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if incident is None:
            return JSONResponse(status_code=204, detail="Incident not found")
        return incident
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int):
    """
    Delete an incident.
    """
    try:
        db = SessionLocal()
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if incident is None:
            return JSONResponse(status_code=204, detail="Incident not found")
        db.delete(incident)
        db.commit()
        return JSONResponse(status_code=204, detail="Incident deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, incident_update: IncidentUpdate):
    """
    Update an incident.
    """
    try:
        db = SessionLocal()
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if incident is None:
            return JSONResponse(status_code=204, detail="Incident not found")
        incident.issue_type = incident_update.issue_type
        incident.severity = incident_update.severity
        incident.description = incident_update.description
        incident.logs = incident_update.logs
        incident.events = incident_update.events
        incident.diagnosis = incident_update.diagnosis
        incident.recommendations = incident_update.recommendations
        incident.last_detected = incident_update.last_detected
        incident.occurrence_count = incident_update.occurrence_count
        incident.resolved = incident_update.resolved
        incident.resolved_at = incident_update.resolved_at
        incident.resolution_notes = incident_update.resolution_notes
        db.commit()
        return incident
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
