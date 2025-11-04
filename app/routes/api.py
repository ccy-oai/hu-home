from flask import Blueprint, request, abort
from app import settings
from firebase_admin import auth
from app.models.user import User
from app.models.family import Family
from app.database import db
from app.services.radar import radar_client

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/health')
def health_check():
    """Simple endpoint that upstream services can use for health probes."""
    return {
        'status': 'ok',
        'environment': settings.ENV,
        'debug': settings.DEBUG,
    }, 200


@blueprint.route('/client-config')
def client_config():
    return { 
        'firebase': settings.FIREBASE_CLIENT_CONFIG,
        'radar': settings.RADAR_PUBLISHABLE_KEY
    }

def list_users(fid):
    return list(map(lambda row: row.to_dict(), User.query.filter_by(family_id=fid)))

def add_user(id, email):
    user = User.query.get(id)
    if not user:
        user = User(username = email, firebase_id = id)
        db.session.add(user)
        db.session.commit()
    return user

@blueprint.route('/get-user')
def get_user():
    try:
        id_token = request.headers.get('Authorization', '').split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
    except:
        abort(401)

    uid = decoded_token['uid']
    email = decoded_token['email']

    me = add_user(uid, email)
    family = Family.query.get(me.family_id)
    profile = {
        'me': me.to_dict(),
    }
    if family:
        profile['family'] = family.to_dict()
        profile['members'] = list_users(me.family_id)
    return {'debug': decoded_token, 'profile': profile}, 200

@blueprint.route('/family', methods=['POST'])
def family():
    try:
        id_token = request.headers.get('Authorization', '').split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        user = User.query.get(decoded_token['uid'])
    except Exception as e:
        print(e)
        abort(401)

    if user and not user.family_id:
        payload = request.json
        family = Family(payload)
        user.family_id = family.id
        user.name = payload.get('name')
        db.session.add(family)
        search_result = radar_client.search.autocomplete(
            query=f'{family.address}, {family.city}, {family.zip}, {payload["country"]}',
            near=[payload['latitude'], payload['longitude']]
            )

        if not search_result:
            abort(404)
        address = search_result[0]
        create_result = radar_client.geofences.create({
            'description': family.name,
            'tag': 'home',
            'externalId': family.id,
            'type': 'circle',
            'radius': 100,
            'coordinates': [address.longitude, address.latitude],
            'enabled': True
        })
        family.geofence_id = create_result._id
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            radar_client.geofences.delete(create_result._id)
            abort(500)
        return { 'family_id': family.id }, 200
    
    return abort(409)

