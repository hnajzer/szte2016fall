from flask import Blueprint, current_app, jsonify, request

movies = Blueprint('series', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('Serie already exists!', 409)


def not_found():
    return get_error('Serie not found!', 404)


def parse_serie(data):
    serie = {}
    if 'title' in data:
        serie['title'] = data['title']
    if 'start_year' in data:
        serie['start_year'] = data['start_year']
    if 'type' in data:
        serie['type'] = data['type']
    return serie


@series.route('/<int:serie_id>', methods=['GET'])
def get_serie(serie_id):
    serie = current_app.series.get_serie(serie_id)
    if not serie:
        return not_found()
    return jsonify(serie)


@series.route('/', methods=['POST'])
def post_serie():
    serie_data = parse_serie(request.get_json())
    sreie = current_app.series.create_serie(serie_data)
    if not serie:
        return existing()
    return jsonify(serie)


@series.route('/<int:serie_id>', methods=['PATCH'])
def patch_movie(serie_id):
    serie_data = parse_serie(request.get_json())
    serie = current_app.series.update_serie(serie_id, serie_data)
    if not serie:
        return not_found()
    return jsonify(serie)


@series.route('/<int:serie_id>', methods=['DELETE'])
def delete_serie(serie_id):
    serie = current_app.series.delete_serie(serie_id)
    if not serie:
        return not_found()
    return jsonify({})


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
