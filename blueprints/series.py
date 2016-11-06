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


def parse_series(data):
    series = {}
    if 'title' in data:
        series['title'] = data['title']
    if 'summary' in data:
        series['summary'] = data['summary']
    if 'season' in data:
        series['season'] = data['season']
    return series


@series.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    series = current_app.series.series(series_id)
    if not series:
        return not_found()
    return jsonify(series)

#GET ALL SERIES
@series.route('/', methods=['GET'])
def get_all_series(series_id):
    for i in current_app.series.get_series(series_id):
        series = current_app.series.series(series_id)
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
def patch_series(series_id):
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

#DELETE ALL SERIES
@series.route('/', methods=['DELETE'])
def delete_all_series(series_id):
    # if there is no series return with no_found error
    series = current_app.series.delete_series(series_id)
    if not series:
        return not_found()
    for i in current_app.series.id:
        current_app.series.delete_series(i)
    return jsonify({})

@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
