from flask import Blueprint, current_app, jsonify, request
from users import login_required

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
@login_required
def get_movie(movie_id):
    movie = current_app.movies.get_movie(movie_id)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/', methods=['POST'])
@login_required
def post_movie():
    movie_data = parse_movie(request.get_json())
    movie = current_app.movies.create_movie(movie_data)
    if not movie:
        return existing()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['PATCH'])
@login_required
def patch_movie(movie_id):
    movie_data = parse_movie(request.get_json())
    movie = current_app.movies.update_movie(movie_id, movie_data)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['DELETE'])
@login_required
def delete_movie(movie_id):
    movie = current_app.movies.delete_movie(movie_id)
    if not movie:
        return not_found()
    return jsonify({})


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
