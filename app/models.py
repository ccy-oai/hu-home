"""Database models for families and members."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from .extensions import db


class TimestampMixin:
    """Adds created/updated timestamps to a model."""

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Family(TimestampMixin, db.Model):
    """A collection of members that share their location."""

    __tablename__ = "families"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))

    members = db.relationship(
        "Member",
        backref="family",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self, include_members: bool = False) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_members:
            payload["members"] = [member.to_dict() for member in self.members]
        return payload


class Member(TimestampMixin, db.Model):
    """Individual that belongs to a family."""

    __tablename__ = "members"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    display_name = db.Column(db.String(120), nullable=False)
    family_id = db.Column(db.String(36), db.ForeignKey("families.id"), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="unknown")
    context = db.Column(db.String(255))

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    accuracy = db.Column(db.Float)
    last_seen_at = db.Column(db.DateTime)

    def update_presence(self, **data: Any) -> None:
        if "status" in data and data["status"]:
            self.status = data["status"]
        if "context" in data:
            self.context = data["context"]
        if "latitude" in data:
            self.latitude = data["latitude"]
        if "longitude" in data:
            self.longitude = data["longitude"]
        if "accuracy" in data:
            self.accuracy = data["accuracy"]
        self.last_seen_at = data.get("last_seen_at", datetime.utcnow())

    def to_dict(self) -> Dict[str, Optional[Any]]:
        return {
            "id": self.id,
            "display_name": self.display_name,
            "family_id": self.family_id,
            "status": self.status,
            "context": self.context,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy,
            "last_seen_at": self.last_seen_at.isoformat() if self.last_seen_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

