from flask import Blueprint, current_app, jsonify, request

seriesBP = Blueprint('series', __name__)


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
    if 'summary' in data:
        series['summary'] = data['summary']
    if 'seasons' in data:
        series['seasons'] = data['seasons']
    return series


@seriesBP.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    series = current_app.series.get_series(series_id)
    if not series:
        return not_found()
    return jsonify(series)


@seriesBP.route('/', methods=['GET'], strict_slashes=False)
def get_all_series():
    series = []
    i = 1
    while i <= current_app.series.id:
        resp = current_app.series.get_series(i)
        if resp:
            series.append(resp)
        i += 1
    return jsonify(series)


@seriesBP.route('/', methods=['POST'], strict_slashes=False)
def post_series():
    series_data = parse_series(request.get_json())
    if 'title' not in series_data or 'summary' not in series_data or 'seasons' not in series_data:
        return get_error('Bad Request', 400)
    series = current_app.series.create_series(series_data)
    if not series:
        return existing()
    return jsonify(series)


@seriesBP.route('/<int:series_id>', methods=['PATCH'])
def patch_series(series_id):
    series_data = parse_series(request.get_json())
    series = current_app.series.update_series(series_id, series_data)
    if not series:
        return not_found()
    return jsonify(series)


@seriesBP.route('/', methods=['DELETE'])
def delete_all_series():
    i = 1
    while i <= current_app.series.id:
        resp = current_app.series.get_series(i)
        if resp:
            current_app.series.delete_series(i)
        i += 1
    return jsonify({})


@seriesBP.route('/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    serie = current_app.series.delete_series(series_id)
    if not serie:
        return not_found()
    return jsonify({})


@seriesBP.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
