from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base, engine

class IncidentNotification(Base):
    __tablename__ = "incident_notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)

    channel = Column(String(100), nullable=False)
    destination = Column(String(255), nullable=False)
    sent_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    severity = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="sent")
    error = Column(Text, nullable=True)

    incident = relationship("Incident", back_populates="notifications")

    def to_dict(self):
        return {
            "id": self.id,
            "incident_id": self.incident_id,
            "channel": self.channel,
            "destination": self.destination,
            "sent_at": self.sent_at.isoformat(),
            "severity": self.severity,
            "status": self.status,
            "error": self.error
        }
