from flask import Blueprint, current_app, jsonify, request
from pymongo import MongoClient

health = Blueprint('health', __name__)


@health.route("", methods=['GET'], strict_slashes=False)
def check():
    health = "true"

    try:
        client = MongoClient('mongodb://szroli-piank:Eerie2eizeex@ds155747.mlab.com:55747/szroli-piank')
#        client = MongoClient(os.environ.get('MONGODB_URL'))
        client.server_info()
        db_conn = "true"
    except:
        db_conn = "false"

    return jsonify({
        'health': health,
        'database_connection': db_conn
    })


@health.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
