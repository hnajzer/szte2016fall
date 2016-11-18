from flask import Blueprint, current_app, jsonify, request
from bson.objectid import ObjectId

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


def retrieve_movie(data, id):
    movie = {}
    if 'title' in data:
        movie['title'] = data['title']
    if 'year' in data:
        movie['year'] = data['year']
    if 'director' in data:
        movie['director'] = data['director']
    movie['_id'] = id
    return movie


@movies.route('/<string:movie_id>', methods=['GET'])
def get_movie(movie_id):
    mdata = current_app.movies.get_movie(movie_id)
    if not mdata:
        return not_found()
    movie = retrieve_movie(mdata, movie_id)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/', methods=['POST'])
def post_movie():
    movie_data = parse_movie(request.get_json())

    print("movie data:", movie_data)
    #ObjectId(' ... ') -bol kinyerjuk stringkent az azonositot:
    movie_id = str(current_app.movies.create_movie(movie_data))
    print("id: ", movie_id)
    print(current_app.movies.get_movie(movie_id))
    if not movie_id:
        return existing()
    created_movie = retrieve_movie(current_app.movies.get_movie(movie_id), movie_id)
    return jsonify(created_movie)


@movies.route('/<string:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
    movie_data = parse_movie(request.get_json())
    current_app.movies.update_movie(ObjectId(movie_id), movie_data)

    movie = retrieve_movie(current_app.movies.get_movie(movie_id), movie_id)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/<string:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = current_app.movies.delete_movie(ObjectId(movie_id))
    if not movie:
        return not_found()
    return jsonify({})


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
