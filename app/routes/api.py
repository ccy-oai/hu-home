"""REST API for the Hu's Home platform."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.database import db
from app.models.family import Family
from app.models.location_event import LocationEvent
from app.services import family_service, location_service

blueprint = Blueprint("api", __name__, url_prefix="/api")


def _json_payload() -> dict:
    return request.get_json(silent=True) or {}


@blueprint.get("/health")
def healthcheck():
    return {"status": "ok"}


@blueprint.get("/families")
def list_families():
    families = [family.to_dict() for family in Family.query.order_by(Family.created_at.desc()).all()]
    return jsonify({"families": families})


@blueprint.post("/families")
def create_family():
    payload = _json_payload()
    family = family_service.create_family(payload)
    return family.to_dict(), 201


@blueprint.get("/families/<family_id>")
def get_family(family_id: str):
    family = family_service.get_family_or_404(family_id)
    return family.to_dict()


@blueprint.get("/families/<family_id>/members")
def list_members(family_id: str):
    family = family_service.get_family_or_404(family_id)
    return jsonify({"members": [member.to_dict() for member in family.members]})


@blueprint.post("/families/<family_id>/members")
def create_member(family_id: str):
    family = family_service.get_family_or_404(family_id)
    member = family_service.create_member(family, _json_payload())
    return {"member": member.to_dict(), "family": family.to_dict()}, 201


@blueprint.patch("/families/<family_id>/members/<member_id>")
def update_member(family_id: str, member_id: str):
    family = family_service.get_family_or_404(family_id)
    member = family_service.get_member_or_404(family, member_id)
    member.update_profile(**_json_payload())
    db.session.commit()
    return member.to_dict()


@blueprint.post("/families/<family_id>/members/<member_id>/locations")
def create_location(family_id: str, member_id: str):
    family = family_service.get_family_or_404(family_id)
    member = family_service.get_member_or_404(family, member_id)
    event = location_service.record_location(member, _json_payload())
    return {"event": event.to_dict(), "member": member.to_dict()}, 201


@blueprint.get("/families/<family_id>/roster")
def family_roster(family_id: str):
    family = family_service.get_family_or_404(family_id)
    return family_service.roster_payload(family)


@blueprint.get("/families/<family_id>/history")
def location_history(family_id: str):
    family_service.get_family_or_404(family_id)
    events = (
        LocationEvent.query.filter_by(family_id=family_id)
        .order_by(LocationEvent.created_at.desc())
        .limit(50)
        .all()
    )
    return {"events": [event.to_dict() for event in events]}
