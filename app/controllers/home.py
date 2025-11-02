from app.models.family import Family
from flask import Blueprint, render_template, request

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
def index():
    family = Family.query.first()
    family_id = family.id if family else None
    return render_template(
        'home/client.html',
        ip=request.remote_addr,
        familyId=family_id
    )
