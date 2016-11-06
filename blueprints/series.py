from flask import Blueprint, current_app, jsonify, request

movies = Blueprint('series', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('Series already exists!', 409)


def not_found():
    return get_error('Series not found!', 404)


def parse_series(data):
    series = {}
    if 'title' in data:
        series['title'] = data['title']
    if 'start_year' in data:
        series['summary'] = data['summary']
    if 'type' in data:
        series['seasons'] = data['seasons']
    return series


@series.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    series = current_app.series.get_series(series_id)
    if not series:
        return not_found()
    return jsonify(series)


@series.route('/', methods=['POST'])
def post_series():
    series_data = parse_series(request.get_json())
    series = current_app.series.create_series(series_data)
    if not series:
        return existing()
    return jsonify(series)


@series.route('/<int:series_id>', methods=['PATCH'])
def patch_movie(series_id):
    series_data = parse_series(request.get_json())
    series = current_app.series.update_series(series_id, series_data)
    if not series:
        return not_found()
    return jsonify(series)


@series.route('/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    series = current_app.series.delete_series(series_id)
    if not series:
        return not_found()
    return jsonify({})


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
