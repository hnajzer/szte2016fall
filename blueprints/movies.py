from flask import Blueprint, current_app, jsonify, request, session

movies = Blueprint('movies', __name__)

#flask-login.readthedocs.io/en/latest/_modules/flask_login/utils.html alapjan
from functools import wraps

def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code

def fresh_login_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if session.get('login') is None and session.get('username') == None:
			return get_error({'message': 'Access denied.'}, 400)
		return func(*args, **kwargs)
	return decorated_view

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
@fresh_login_required
def get_movie(movie_id):
    movie = current_app.movies.get_movie(movie_id)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/', methods=['POST'])
@fresh_login_required
def post_movie():
    movie_data = parse_movie(request.get_json())
    #itt kell az str hogy ne legyen ObjectId TypeError hiba!!
    movie = str(current_app.movies.create_movie(movie_data))
    if not movie:
        return existing()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['PATCH'])
@fresh_login_required
def patch_movie(movie_id):
    movie_data = parse_movie(request.get_json())
    movie = current_app.movies.update_movie(movie_id, movie_data)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['DELETE'])
@fresh_login_required
def delete_movie(movie_id):
    movie = current_app.movies.delete_movie(movie_id)
    if not movie:
        return not_found()
    return jsonify({})


@movies.app_errorhandler(500)
@fresh_login_required
def page_not_found(e):
    return get_error('Internal server error', 500)
