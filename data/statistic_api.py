import flask
from data import db_session
from data.users_uuid import User_uuid
import json

blueprint = flask.Blueprint(
    'stats_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/player/stats/<string:nick>', methods=['GET'])
def get_one_stats(nick):
    db_sess = db_session.create_session()
    user = db_sess.query(User_uuid.uuid).filter(User_uuid.name == nick).first()
    if not user:
        return 'Not found (404)'
    with open(f'MinecraftServer/world/stats/{user[0]}.json', 'r') as jsonf:
        f = json.load(jsonf)
        return f


@blueprint.route('/player/advancements/<string:nick>', methods=['GET'])
def get_one_adch(nick):
    db_sess = db_session.create_session()
    user = db_sess.query(User_uuid.uuid).filter(User_uuid.name == nick).first()
    if not user:
        return 'Not found (404)'
    with open(f'MinecraftServer/world/advancements/{user[0]}.json', 'r') as jsonf:
        f = json.load(jsonf)
        return f
