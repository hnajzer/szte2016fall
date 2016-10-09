from flask import Blueprint, current_app, jsonify, request, json
movies = Blueprint('movies', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('Movie already exists!', 409)


def not_found():
    return get_error('Movie not found!', 404)


def parse_movie(data):
    movie = {}
    if 'title' in data:
        movie['title'] = data['title']
    if 'year' in data:
        movie['year'] = data['year']
    if 'director' in data:
        movie['director'] = data['director']
    return movie


@movies.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = current_app.movies.get_movie(movie_id)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/setup', methods=['GET'])
def setup():
    movie_data = parse_movie({"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"})
    current_app.movies.create_movie(movie_data)
    movie_data = parse_movie({"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"})
    current_app.movies.create_movie(movie_data)
    movie_data = parse_movie({"title": "Donnie Darko", "year": 2001, "director": "Richard Kelly"})
    current_app.movies.create_movie(movie_data)
    movie_data = parse_movie({"title": "Planet of the Apes", "year": 2001, "director": "Tim Burton"})
    current_app.movies.create_movie(movie_data)
    movie_data = parse_movie({"title": "Planet of the Apes", "year": 1968, "director": "Franklin J. Schaffner"})
    current_app.movies.create_movie(movie_data)
    return 'Success'


@movies.route('/', methods=['POST'])
def post_movie():
    movie_data = parse_movie(request.get_json())
    movie = current_app.movies.create_movie(movie_data)
    if not movie:
        return existing()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
    movie_data = parse_movie(request.get_json())
    movie = current_app.movies.update_movie(movie_id, movie_data)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = current_app.movies.delete_movie(movie_id)
    if not movie:
        return not_found()
    return jsonify({})


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
