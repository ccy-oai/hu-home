"""Business logic helpers for family/member management."""
from __future__ import annotations

from random import choice
from typing import Iterable

from flask import abort

from app.database import db
from app.models.family import Family
from app.models.user import User

_COLOR_POOL = [
    "#ea4aaa",
    "#a972cb",
    "#ef4e4e",
    "#f1a10a",
    "#0d99ff",
    "#0ba95b",
]


def _pick_color(existing: Iterable[str]) -> str:
    available = [color for color in _COLOR_POOL if color not in existing]
    return choice(available or _COLOR_POOL)


def create_family(payload: dict) -> Family:
    name = (payload.get("name") or "").strip()
    if not name:
        abort(400, "Family name is required")

    family = Family(
        name=name,
        address=payload.get("address"),
        city=payload.get("city"),
        region=payload.get("region"),
        zip=payload.get("zip"),
        country=payload.get("country"),
        phone=payload.get("phone"),
    )
    db.session.add(family)
    db.session.commit()
    return family


def get_family_or_404(family_id: str) -> Family:
    family = Family.query.get(family_id)
    if not family:
        abort(404, "Family not found")
    return family


def create_member(family: Family, payload: dict) -> User:
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    if not name or not email:
        abort(400, "Name and email are required")

    member = User(name=name, email=email, family_id=family.id)
    member.color = _pick_color([m.color for m in family.members if m.color])
    db.session.add(member)
    db.session.commit()
    return member


def get_member_or_404(family: Family, member_id: str) -> User:
    member = User.query.filter_by(family_id=family.id, id=member_id).first()
    if not member:
        abort(404, "Member not found")
    return member


def roster_payload(family: Family) -> dict:
    family_dict = family.to_dict()
    return {
        "family": family_dict,
        "members": [member.to_dict() for member in family.members],
    }
