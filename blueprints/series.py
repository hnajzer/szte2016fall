from flask import Blueprint, current_app, jsonify, request

series = Blueprint('series', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('Serie already exists!', 409)


def incomplete():
    return get_error('Missing data!', 400)


def not_found():
    return get_error('Serie not found!', 404)


def ok():
    return jsonify({
        'message': 'ok',
        'code': 200
    }), 200

def parse_serie(data):
    serie = {}
    if 'title' in data:
        serie['title'] = data['title']
    else:
        return False
    if 'summary' in data:
        serie['summary'] = data['summary']
    else:
        return False
    if 'seasons' in data:
        serie['seasons'] = data['seasons']
    else:
        return False
    return serie


@series.route('/', methods=['GET'])
def get_serie_count():
    return jsonify([current_app.series._count()])


@series.route('/<int:id>', methods=['GET'])
def get_serie(id):
    serie = current_app.series.get_serie(id)
    if not serie:
        return not_found()
    return jsonify(serie)


@series.route('/', methods=['POST'])
def post_serie():
    serie_data = parse_serie(request.get_json())
    if not serie_data:
        return incomplete()
    serie = current_app.series.create_serie(serie_data)
    if not serie:
        return existing()
    return jsonify(serie)


@series.route('/<int:id>', methods=['PATCH'])
def patch_serie(id):
    serie_data = parse_serie(request.get_json())
#    if not serie_data:
#        return incomplete()
    serie = current_app.series.update_serie(id, serie_data)
    if not serie:
        return not_found()
    return jsonify(serie)


@series.route('/', methods=['DELETE'])
def delete_serie_anone():
    return ok()


@series.route('/<int:id>', methods=['DELETE'])
def delete_serie(id):
    serie = current_app.series.delete_serie(id)
    if not serie:
        return not_found()
    return jsonify(serie)


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
