from flask import Blueprint, current_app, jsonify, request

series = Blueprint('series', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('Series already exists!', 409)


def not_found():
    return get_error('Series not found!', 404)


def wrong_parameters():
    return get_error("Wrong parameters!", 400)


@series.route('/', methods=['GET'])
def get_all_series():
    s = current_app.series.get_all_series()
    return jsonify(s)


@series.route('/', methods=['POST'])
def post_series():
    s_data = parse_series(request.get_json())
    if len(s_data) != 3:
        return wrong_parameters()
    serias = current_app.series.create_series(s_data)
    if not serias:
        return existing()
    return jsonify(serias)

def parse_series(adat):
    film = {}
    if 'title' in adat:
        film['title'] = adat['title']
    if 'summary' in adat:
        film['summary'] = adat['summary']
    if 'seasons' in adat:
        film['seasons'] = adat['seasons']
    return film

@series.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    s = current_app.series.get_series(series_id)
    if not s:
        return not_found()
    return jsonify(s)


@series.route('/<int:series_id>', methods=['PATCH'])
def patch_series(s_id):
    s_data = parse_series(request.get_json())
    serias = current_app.series.update_series(s_id, s_data)
    if not serias:
        return not_found()
    return jsonify(serias)

@series.route('/', methods=['DELETE'])
def delete_all_series():
    current_app.series.delete_all_series()
    return jsonify([])

@series.route('/<int:series_id>', methods=['DELETE'])
def delete_series(s_id):
    serias = current_app.series.delete_series(s_id)
    if not serias:
        return not_found()
    return jsonify({})


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
