from flask import Blueprint, current_app, jsonify, request

series = Blueprint('series', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('series already exists!', 409)


def not_found():
    return get_error('series not found!', 404)

def asked_error():
    return get_error('asked error!', 400)

def parse_series(data):
    series = {}
    if 'title' in data:
        series['title'] = data['title']
    if 'summary' in data:
        series['summary'] = data['summary']
    if 'seasons' in data:
        series['seasons'] = data['seasons']
    return series


@series.route('/', methods=['GET'])
def get_all_series():
    series = []
    i = 1
    while i <= current_app.series.id:
        asd = current_app.series.get_series(i)
        if asd:
            series.append(asd)
        i += 1
    return jsonify(series)

@series.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    series = current_app.series.get_series(series_id)
    if not series:
        return not_found()
    return jsonify(series)

@series.route('/', methods=['POST'], strict_slashes=False)
def post_series():
    series_data = parse_series(request.get_json())
    if 'summary' not in series_data:
       return asked_error()
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

@series.route('/', methods=['DELETE'])
def delete_all():
    current_app.series.delete_all()
    return jsonify({})


@series.route('/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    series= current_app.series.delete_series(series_id)
    if not series:
        return not_found()
    return jsonify({})


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
