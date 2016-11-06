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


def invalid_parameter_number():
    return get_error("Invalid parameter number!", 400)

def validate_serie_content(content):
    if not 'title' in content:
        invalid_parameter_number()
    if not 'summary' in content:
        invalid_parameter_number()
    if not 'seasons' in content:
        invalid_parameter_number()
    return True


def parse_series(data):
    serie = {}
    if 'title' in data:
        serie['title'] = data['title']
    if 'summary' in data:
        serie['summary'] = data['summary']
    if 'seasons' in data:
        serie['seasons'] = data['seasons']
    return serie


@series.route('/', methods=['GET'])
def get_all_series():
    s = current_app.series.get_all_series()
    return jsonify(s)


@series.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    requested_serie = current_app.series.get_series(series_id)
    if not requested_serie:
        return not_found()
    return jsonify(requested_serie)


@series.route('/', methods=['POST'])
def post_series():
    content = parse_series(request.get_json())
    validate_serie_content(content)
    created_serie = current_app.series.create_series(content)
    if not created_serie:
        return existing()
    return jsonify(created_serie)


@series.route('/', methods=['DELETE'])
def delete_series():
    current_app.series.delete_series()
    return jsonify([])


@series.route('/<int:series_id>', methods=['PATCH'])
def patch_series(series_id):
    content = parse_series(request.get_json())
    updated_serie = current_app.series.update_series(series_id, content)
    if not updated_serie:
        return not_found()
    return jsonify(updated_serie)


@series.route('/<int:serie_id>', methods=['DELETE'])
def delete_serie(serie_id):
    deleted_serie = current_app.series.delete_serie(serie_id)
    if not deleted_serie:
        return not_found()
    return jsonify({})


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)