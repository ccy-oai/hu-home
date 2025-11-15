"""Utilities for broadcasting roster updates."""
from __future__ import annotations

from datetime import datetime
from typing import Dict

from .extensions import socketio
from .models import Family


def build_roster(family: Family) -> Dict[str, object]:
    return {
        "id": family.id,
        "name": family.name,
        "members": [member.to_dict() for member in family.members],
        "generated_at": datetime.utcnow().isoformat(),
    }


def broadcast_roster(family_id: str) -> None:
    family = Family.query.get(family_id)
    if not family:
        return
    socketio.emit("roster", build_roster(family), room=family_id)

