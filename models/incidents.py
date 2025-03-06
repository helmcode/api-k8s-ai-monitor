from sqlalchemy import Column, String, Boolean, DateTime, Text, Index, UniqueConstraint, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base, engine
import json
import uuid

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cluster = Column(String(100), nullable=False, index=True)
    namespace = Column(String(100), nullable=False, index=True)

    resource_type = Column(String(50), nullable=False)
    resource_name = Column(String(255), nullable=False)

    issue_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)
    description = Column(Text, nullable=False)

    logs = Column(Text)
    events = Column(Text)
    diagnosis = Column(Text)
    recommendations = Column(Text)

    first_detected = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_detected = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    occurrence_count = Column(Integer, default=1)

    resolved = Column(Boolean, default=False, index=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)

    notifications = relationship("IncidentNotification", back_populates="incident", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('cluster', 'namespace', 'resource_type', 'resource_name', 'issue_type', name='uix_incident'),
        Index('idx_incident_lookup', 'cluster', 'namespace', 'resource_type', 'resource_name', 'issue_type'),
        Index('idx_incident_time', 'last_detected'),
    )

    def to_dict(self):
        result = {
            "id": self.id,
            "cluster": self.cluster,
            "namespace": self.namespace,
            "resource_type": self.resource_type,
            "resource_name": self.resource_name,
            "issue_type": self.issue_type,
            "severity": self.severity,
            "description": self.description,
            "first_detected": self.first_detected.isoformat(),
            "last_detected": self.last_detected.isoformat(),
            "occurrence_count": self.occurrence_count,
            "resolved": self.resolved,
        }

        if self.resolved and self.resolved_at:
            result["resolved_at"] = self.resolved_at.isoformat()
        if self.resolution_notes:
            result["resolution_notes"] = self.resolution_notes
        if self.logs:
            try:
                result["logs"] = json.loads(self.logs)
            except:
                result["logs"] = self.logs
        if self.events:
            try:
                result["events"] = json.loads(self.events)
            except:
                result["events"] = self.events
        if self.diagnosis:
            result["diagnosis"] = self.diagnosis
        if self.recommendations:
            result["recommendations"] = self.recommendations
        return result
