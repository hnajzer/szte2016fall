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
def get_series2():
    series = current_app.series.get_series2()
    return jsonify(series)

@series.route('/<int:series_id>', methods=['GET'])
def get_series(series_id):
    series = current_app.series.get_series(series_id)
    if not series:
        return not_found()
    return jsonify(series)


@series.route('/', methods=['GET'], strict_slashes = False)
def get_all_series():
     ret = []
     for index in range(current_app.series.get_data_lenght()):
        ret.append(current_app.series.data[index].name)
     json = {"wtf": ret}
     return jsonify(json)

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
