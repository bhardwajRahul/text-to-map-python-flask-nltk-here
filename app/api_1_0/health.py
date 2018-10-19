
from flask import jsonify
from flask import current_app as app

from . import api


def get_app_id():
    return app.config['HERE_APP_ID']

def get_app_code():
    return app.config['HERE_APP_CODE']


@api.route('/health', methods=['GET'])
def handle_health():

    health = {}
    health['app_id'] = get_app_id()
    health['app_code'] = get_app_code()

    return jsonify(health)

