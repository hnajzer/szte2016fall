from flask import Blueprint, current_app, jsonify, request, session
from functools import wraps

series = Blueprint('series', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('loggedin') is None and session.get('username') == None:
            return jsonify({'message': 'You must login to access this resource.'})     
        return f(*args, **kwargs)
    return decorated_function

def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('Serie already exists!', 409)


def not_found():
    return get_error('Serie not found!', 404)

def param_err():
    return get_error("Not enough param!", 400)

def parse_serie(data):
    serie = {}
    if 'title' in data:
        serie['title'] = data['title']
    if 'summary' in data:
        serie['summary'] = data['summary']
    if 'seasons' in data:
        serie['seasons'] = data['seasons']
    return serie

@series.route('/', methods=['GET'] , strict_slashes = False)
@login_required
def allseries():
    s = current_app.series.allSeries()
    return jsonify(s)

@series.route('/', methods=['DELETE'] , strict_slashes = False)
@login_required
def deleteseries():
    s = current_app.series.deleteAllSeries()
    return jsonify(s)

@series.route('/<int:serie_id>', methods=['GET'])
@login_required
def get_serie(serie_id):
    serie = current_app.series.get_serie(serie_id)
    if not serie:
        return not_found()
    return jsonify(serie)

@series.route('/', methods=['POST'], strict_slashes = False)
@login_required
def post_serie():
    serie_data = parse_serie(request.get_json())
    if len(serie_data) != 3:
        return param_err()
    serie = current_app.series.create_serie(serie_data)
    if not serie:
        return existing()
    return jsonify(serie)

@series.route('/<int:serie_id>', methods=['PATCH'])
@login_required
def patch_serie(serie_id):
    serie_data = parse_serie(request.get_json())
    serie = current_app.series.update_serie(serie_id, serie_data)
    if not serie:
        return not_found()
    return jsonify(serie)

@series.route('/<int:serie_id>', methods=['DELETE'])
@login_required
def delete_serie(serie_id):
    serie = current_app.series.delete_serie(serie_id)
    if not serie:
        return not_found()
    return jsonify({})


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
