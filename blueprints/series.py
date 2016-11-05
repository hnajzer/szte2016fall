from flask import Blueprint, current_app, jsonify, request
from model.film import Film

series = Blueprint('series', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('Movie already exists!', 409)


def not_found():
    return get_error('Movie not found!', 404)


def error_400():
    return get_error('Error: 400', 400)


def data2obj(data):
    film = Film()
    if 'title' in data:
        film.name = data['title']
    if 'year' in data:
        film.year = data['year']
    if 'director' in data:
        film.director = data['director']
    if 'summary' in data:
        film.summary = data['summary']
    if 'seasons' in data:
        film.seasons = data['seasons']
    if 'description' in data:
        film.description = data['description']
    return film


def obj2data(FilmObj):
    series = {}
    series["id"] = FilmObj.id
    series["director"] = FilmObj.director
    series["title"] = FilmObj.name
    series["year"] = FilmObj.year
    series["summary"] = FilmObj.summary
    series["description"] = FilmObj.description
    series["seasons"] = FilmObj.seasons
    return series


@series.route('/', methods=['GET'], strict_slashes = False)
def get_all_series():
    ret = []
    for index in range(current_app.series.get_data_lenght()):
        ret.append(current_app.series.data[index].name)
    json = {"ezalista": ret}
    return jsonify(json)


@series.route('/<int:id>', methods=['GET'], strict_slashes = False)
def get_id_series(id):
    film = current_app.series.get_series(id)
    if film == False:
        return not_found()
    return jsonify(obj2data(film))


@series.route('/', methods=['POST'], strict_slashes = False)
def post_a_series():
    film = data2obj(request.get_json())
    film = current_app.series.create_series(film)
    ret = {"id": film.id}
    if film.summary == "null" or film.seasons == "null":
        current_app.series.delete_series(film.id)
        return error_400()
    return jsonify(ret)


@series.route('/<int:id>', methods=['PATCH'])
def patch_series(id):
    json = request.get_json()
    film = current_app.series.get_series(id)
    if film == False:
        return not_found()
    if "summary" in json:
        film.summary = json["summary"]
    return "success"


@series.route('/', methods=['DELETE'], strict_slashes = False)
def delete_all_series():
    current_app.series.delete_all()
    return jsonify({})


@series.route('/<int:id>', methods=['DELETE'], strict_slashes = False)
def delete_a_series(id):
    if current_app.series.delete_series(id):
        return jsonify({})
    else:
        return not_found()


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
