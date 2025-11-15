"""Socket.IO helpers and presence registry."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Optional, Set, Tuple

from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room

from . import settings

socketio = SocketIO(async_mode="threading", cors_allowed_origins="*")

_FAMILY_ROOMS: Dict[str, Set[str]] = defaultdict(set)
_LAST_SEEN: Dict[str, datetime] = {}


def register_socketio_events() -> None:
    from app.services import family_service

    @socketio.on("join_family")
    def handle_join(data: Optional[dict] = None):
        family_id, user_id = _resolve_identifiers(data)
        if not family_id or not user_id:
            return

        touch_presence(family_id, user_id)
        join_room(family_id)
        emit("roster", family_service.roster_payload(family_service.get_family_or_404(family_id)), room=family_id)

    @socketio.on("leave_family")
    def handle_leave(data: Optional[dict] = None):
        family_id, user_id = _resolve_identifiers(data)
        if not family_id or not user_id:
            return
        leave_room(family_id)
        remove_presence(family_id, user_id)
        emit("roster", family_service.roster_payload(family_service.get_family_or_404(family_id)), room=family_id)

    @socketio.on("disconnect")
    def handle_disconnect():  # pragma: no cover - depends on socket layer
        family_id, user_id = _resolve_identifiers(None)
        if family_id and user_id:
            remove_presence(family_id, user_id)


def broadcast_roster(family_id: str) -> None:
    from app.services import family_service

    payload = family_service.roster_payload(family_service.get_family_or_404(family_id))
    socketio.emit("roster", payload, room=family_id)


def touch_presence(family_id: str, user_id: str) -> None:
    _FAMILY_ROOMS[family_id].add(user_id)
    _LAST_SEEN[user_id] = datetime.utcnow()
    cleanup_presence()


def remove_presence(family_id: str, user_id: str) -> None:
    if family_id in _FAMILY_ROOMS and user_id in _FAMILY_ROOMS[family_id]:
        _FAMILY_ROOMS[family_id].remove(user_id)
        if not _FAMILY_ROOMS[family_id]:
            del _FAMILY_ROOMS[family_id]
    _LAST_SEEN.pop(user_id, None)


def cleanup_presence() -> None:
    """Drop stale clients so rooms don't keep growing indefinitely."""
    threshold = datetime.utcnow() - timedelta(seconds=settings.PRESENCE_STALE_AFTER_SECONDS)
    stale_users = [user_id for user_id, seen in _LAST_SEEN.items() if seen < threshold]
    for user_id in stale_users:
        _LAST_SEEN.pop(user_id, None)
        for family_id, members in list(_FAMILY_ROOMS.items()):
            if user_id in members:
                members.remove(user_id)
            if not members:
                _FAMILY_ROOMS.pop(family_id, None)


def _resolve_identifiers(payload: Optional[dict]) -> Tuple[Optional[str], Optional[str]]:
    data = payload or {}
    family_id = data.get("familyId") or request.args.get("familyId")
    user_id = data.get("userId") or request.args.get("userId")
    return family_id, user_id
