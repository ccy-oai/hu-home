"""Socket.IO handlers."""
from __future__ import annotations

from flask import request
from flask_socketio import emit, join_room, leave_room

from .extensions import socketio
from .models import Family
from .presence import build_roster


def _family_or_error(family_id: str):
    family = Family.query.get(family_id)
    if not family:
        emit("error", {"message": "Unknown family."}, room=request.sid)
        return None
    return family


@socketio.on("join")
def handle_join(data):
    family_id = data.get("familyId") if isinstance(data, dict) else None
    if not family_id:
        emit("error", {"message": "familyId is required."}, room=request.sid)
        return

    family = _family_or_error(family_id)
    if not family:
        return

    join_room(family_id)
    emit("roster", build_roster(family), room=request.sid)


@socketio.on("leave")
def handle_leave(data):
    family_id = data.get("familyId") if isinstance(data, dict) else None
    if family_id:
        leave_room(family_id)


@socketio.on("disconnect")
def handle_disconnect():
    # Nothing to clean up because membership is tracked in the database.
    pass

