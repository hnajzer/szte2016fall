from flask import Blueprint, current_app, jsonify, request

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
    movie['_id'] = id
    return movie


@movies.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    adat = current_app.movies.get_movie(movie_id)
    if not adat:
        return not_found()
    movie = parse_movie(data, movie_id)
    if not movie: return not found()
    return jsonify(movie)


@movies.route('/', methods=['POST'])
def post_movie():
    movie_data = parse_movie(request.get_json())
    # ide kell azt str() fuggveny a TypeError ObjectId miatt (Tamas help e-mailben)
    movie = str(current_app.movies.create_movie(movie_data))
    if not movie:
        return existing()
    completed_create_movie = parse_movie(current_app.movies.get_movie(movie), movie)
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
    movie_data = parse_movie(request.get_json())
    current_app.movies.update_movie(ObjectId(movie_id), movie_data)
    movie = parse_movie(current_app.movies.get_movie(movie_id), movie_id)
    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    #fontos az ObjectId kulonben TypeError JSON not serializable error-al elszall
    movie = current_app.movies.delete_movie(ObjectId(movie_id))
    if not movie:
        return not_found()
    return jsonify({})


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
