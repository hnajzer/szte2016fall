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
    series['id'] = FilmObj.id
    series['director'] = FilmObj.director
    series['title'] = FilmObj.name
    series['year'] = FilmObj.year
    series['summary'] = FilmObj.summary
    series['description'] = FilmObj.description
    return series


def obj2json(FilmObj):
    return jsonify(obj2data(FilmObj))


@series.route('/<int:id>', methods=['GET'], strict_slashes = False)
def get_movie(id):
    film = current_app.series.get_series(id)
    if not film or film.id == None:
        return not_found()
    return obj2json(film)


@series.route('/', methods=['POST'], strict_slashes = False)
def post_movie():
    film = current_app.series.create_series(data2obj(request.get_json()))
    if not film:
        return existing()
    return obj2json(film)


@series.route('/<int:id>', methods=['PATCH'], strict_slashes = False)
def patch_movie(id):
    film = current_app.seriesupdate_series(id, data2obj(request.get_json()))
    if not film:
        return not_found()
    return obj2json(film)


@series.route('/<int:id>', methods=['DELETE'], strict_slashes = False)
def delete_movie(movie_id):
    film = current_app.series.delete_series(id)
    if not film:
        return not_found()
    return jsonify({})


@series.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
