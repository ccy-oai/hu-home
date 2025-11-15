"""Family model."""
from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.database import db


class Family(db.Model):
    __tablename__ = "family"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(180), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    region = db.Column(db.String(120), nullable=True)
    zip = db.Column(db.String(40), nullable=True)
    country = db.Column(db.String(4), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship(
        "User",
        back_populates="family",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="User.created_at",
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Family {self.name} ({self.id})>"

    def update(self, **kwargs) -> None:
        for field in ("name", "address", "city", "region", "zip", "country", "phone"):
            if field in kwargs and kwargs[field] is not None:
                setattr(self, field, kwargs[field])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "region": self.region,
            "zip": self.zip,
            "country": self.country,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
