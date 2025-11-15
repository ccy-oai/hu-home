"""HTML views for the lightweight client."""
from __future__ import annotations

from flask import Blueprint, render_template

from app.models.family import Family

blueprint = Blueprint("home", __name__)


@blueprint.route("/")
def index():
    families = Family.query.order_by(Family.created_at.desc()).all()
    default_family = families[0] if families else None
    return render_template(
        "home/dashboard.html",
        families=families,
        default_family=default_family,
    )
