"""REST API for Hu's Home."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from flask import Blueprint, abort, request

from .extensions import db
from .models import Family, Member
from .presence import broadcast_roster

api = Blueprint("api", __name__, url_prefix="/api")


def _payload() -> Dict[str, Any]:
    return request.get_json(force=True, silent=True) or {}


def _family_or_404(family_id: str) -> Family:
    family = Family.query.get(family_id)
    if not family:
        abort(404, description="Family not found.")
    return family


def _member_or_404(family_id: str, member_id: str) -> Member:
    member = Member.query.filter_by(id=member_id, family_id=family_id).first()
    if not member:
        abort(404, description="Member not found.")
    return member


@api.get("/health")
def healthcheck():
    return {"status": "ok"}


@api.get("/families")
def list_families():
    families = Family.query.order_by(Family.created_at).all()
    return {"families": [family.to_dict() for family in families]}


@api.post("/families")
def create_family():
    data = _payload()
    name = (data.get("name") or "").strip()
    if not name:
        abort(400, description="name is required")

    family = Family(name=name, description=data.get("description"))
    db.session.add(family)
    db.session.commit()
    return {"family": family.to_dict(include_members=True)}, 201


@api.get("/families/<family_id>")
def get_family(family_id: str):
    family = _family_or_404(family_id)
    return {"family": family.to_dict(include_members=True)}


@api.post("/families/<family_id>/members")
def create_member(family_id: str):
    family = _family_or_404(family_id)
    data = _payload()
    display_name = (data.get("display_name") or data.get("name") or "").strip()
    if not display_name:
        abort(400, description="display_name is required")

    member = Member(display_name=display_name, family_id=family.id)
    db.session.add(member)
    db.session.commit()
    broadcast_roster(family.id)
    return {"member": member.to_dict()}, 201


@api.get("/families/<family_id>/members")
def list_members(family_id: str):
    family = _family_or_404(family_id)
    return {"members": [member.to_dict() for member in family.members]}


@api.post("/families/<family_id>/members/<member_id>/ping")
def member_ping(family_id: str, member_id: str):
    member = _member_or_404(family_id, member_id)
    data = _payload()
    payload = {
        "status": data.get("status", "present"),
        "last_seen_at": datetime.utcnow(),
    }
    if "context" in data:
        payload["context"] = data.get("context")
    for key in ("latitude", "longitude", "accuracy"):
        if key in data:
            payload[key] = data.get(key)

    member.update_presence(**payload)
    db.session.commit()
    broadcast_roster(family_id)
    return {"member": member.to_dict()}

