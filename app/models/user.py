"""User (family member) model."""
from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    family_id = db.Column(db.String(36), db.ForeignKey("family.id"), nullable=False)
    status_message = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(24), nullable=True)
    last_latitude = db.Column(db.Float, nullable=True)
    last_longitude = db.Column(db.Float, nullable=True)
    last_accuracy = db.Column(db.Float, nullable=True)
    last_seen_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    family = db.relationship("Family", back_populates="members")
    locations = db.relationship(
        "LocationEvent",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="desc(LocationEvent.created_at)",
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<User {self.email} ({self.id})>"

    def update_profile(self, **kwargs) -> None:
        for field in ("email", "name", "status_message", "color"):
            if field in kwargs and kwargs[field] is not None:
                setattr(self, field, kwargs[field])

    def update_location(self, latitude: float, longitude: float, accuracy: float | None = None) -> None:
        self.last_latitude = latitude
        self.last_longitude = longitude
        self.last_accuracy = accuracy
        self.last_seen_at = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "family_id": self.family_id,
            "status_message": self.status_message,
            "color": self.color,
            "last_latitude": self.last_latitude,
            "last_longitude": self.last_longitude,
            "last_accuracy": self.last_accuracy,
            "last_seen_at": self.last_seen_at.isoformat() if self.last_seen_at else None,
        }
