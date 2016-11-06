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


def parse_series(data):
    s = {}
    if 'title' in data:
        s['title'] = data['title']
    if 'summary' in data:
        s['summary'] = data['summary']
    if 'seasons' in data:
        s['seasons'] = data['seasons']
    return s


@series.route('/', methods=['GET'])
def get_all_series():
    s = current_app.series.get_all_series()
    return jsonify(s)


@series.route('/', methods=['POST'])
def post_series():
    series_data = parse_series(request.get_json())
    if len(series_data) != 3:
        return wrong_parameters()
    s = current_app.series.create_series(series_data)
    if not s:
        return existing()
    return jsonify(s)


@series.route('/', methods=['DELETE'])
def delete_all_series():
    current_app.series.delete_all_series()
    return jsonify([])


@series.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    s = current_app.series.get_series(series_id)
    if not s:
        return not_found()
    return jsonify(s)


@series.route('/<int:series_id>', methods=['PATCH'])
def patch_series(series_id):
    series_data = parse_series(request.get_json())
    s = current_app.series.update_series(series_id, series_data)
    if not s:
        return not_found()
    return jsonify(s)


@series.route('/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    s = current_app.series.delete_series(series_id)
    if not s:
        return not_found()
    return jsonify({})


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)