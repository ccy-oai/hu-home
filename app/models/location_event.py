"""Location event model that stores individual pings."""
from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.database import db


class LocationEvent(db.Model):
    __tablename__ = "location_event"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    family_id = db.Column(db.String(36), db.ForeignKey("family.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=True)
    source = db.Column(db.String(40), nullable=False, default="manual")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="locations")
    family = db.relationship("Family", backref=db.backref("location_events", lazy=True))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "family_id": self.family_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
