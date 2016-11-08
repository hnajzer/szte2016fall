import time
from flask import Blueprint, current_app, jsonify, request

movies = Blueprint('movies', __name__)
movies_cache = {}
movies_cache_timestamps = {}
movies_cache_time_frame = 60000


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


@movies.route('/reset', methods=['GET'])
def reset_movies():
    current_app.movies.reset();
    return jsonify({'message': 'all movies has been deleted'})


@movies.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    # movie = current_app.movies.get_movie(movie_id)

    cached_movie = check_movies_cache(movie_id)

    if cached_movie:
        print 'it was in the cache'
        movie = cached_movie
    elif current_app.movies.get_movie(movie_id):
        print 'it was not in the cache'
        movie = current_app.movies.get_movie(movie_id)
        cache_movie(movie_id, movie)
    else:
        print 'it was not found'
        return not_found()

    return jsonify(movie)


def cache_movie(movie_id, movie):
    global movies_cache, movies_cache_timestamps
    time_stamp = int(round(time.time() * 1000))

    movies_cache_timestamps[movie_id] = time_stamp
    movies_cache[movie_id] = movie


def un_cache_movie(movie_id):
    global movies_cache, movies_cache_timestamps

    del movies_cache[movie_id]
    del movies_cache_timestamps[movie_id]


def check_movies_cache(movie_id):
    global movies_cache, movies_cache_timestamps, movies_cache_time_frame

    if movie_id in movies_cache:
        movie = movies_cache[movie_id]
        cache_time_stamp = movies_cache_timestamps[movie_id]
        current_time_stamp = int(round(time.time() * 1000))

        cache_expired = True if cache_time_stamp + movies_cache_time_frame <= current_time_stamp else None

        return movie if not cache_expired else None
    else:
        return None


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

    cached_movie = check_movies_cache(movie_id)
    if cached_movie:
        print 'the modified movie was in the cache, now it is removed'
        un_cache_movie(movie_id)

    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = current_app.movies.delete_movie(movie_id)

    cached_movie = check_movies_cache(movie_id)
    if cached_movie:
        print 'the deleted movie was in the cache, now it is removed'
        un_cache_movie(movie_id)

    if not movie:
        return not_found()
    return jsonify({})


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
