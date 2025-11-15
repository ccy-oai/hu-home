"""Helpers for persisting and broadcasting location updates."""
from __future__ import annotations

from flask import abort

from app.database import db
from app.models.location_event import LocationEvent
from app.models.user import User
from app.socketio import broadcast_roster, touch_presence


def record_location(member: User, payload: dict) -> LocationEvent:
    try:
        latitude = float(payload["latitude"])
        longitude = float(payload["longitude"])
    except (KeyError, ValueError, TypeError):
        abort(400, "Latitude and longitude are required")

    accuracy = payload.get("accuracy")
    if accuracy is not None:
        try:
            accuracy = float(accuracy)
        except (TypeError, ValueError):
            abort(400, "Accuracy must be numeric")

    event = LocationEvent(
        family_id=member.family_id,
        user_id=member.id,
        latitude=latitude,
        longitude=longitude,
        accuracy=accuracy,
        source=(payload.get("source") or "manual"),
    )

    member.update_location(latitude=latitude, longitude=longitude, accuracy=accuracy)
    db.session.add(event)
    db.session.commit()

    touch_presence(member.family_id, member.id)
    broadcast_roster(member.family_id)
    return event
