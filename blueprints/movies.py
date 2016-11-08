from flask import Blueprint, current_app, jsonify, request
from threading import Lock


movies = Blueprint('movies', __name__)
mcache = {}
cache_limit = 50
cache_current = 1
lock = Lock()
cinit = False


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


def init_cache():
    global cache_limit, mcache
    i = 1
    while i <= cache_limit:
        mcache[i] = {}
        mcache[i]['id'] = -1
        i += 1


@movies.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    global lock, cinit
    if not cinit:
        init_cache()
        cinit = True
    lock.acquire()
    try:
        cached_movie = getCachedMovie(movie_id)
        if cached_movie:
            return jsonify(cached_movie)
        else:
            movie = current_app.movies.get_movie(movie_id)
    finally:
        lock.release()
    if not movie:
        return not_found()
    toCache(movie)
    return jsonify(movie)


@movies.route('/', methods=['POST'])
def post_movie():
    global lock, cinit
    if not cinit:
        init_cache()
        cinit = True
    lock.acquire()
    try:
        movie_data = parse_movie(request.get_json())
        movie = current_app.movies.create_movie(movie_data)
    finally:
        lock.release()
    if not movie:
        return existing()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
    global lock, cinit
    if not cinit:
        init_cache()
        cinit = True
    lock.acquire()
    try:
        movie_data = parse_movie(request.get_json())
        movie = current_app.movies.update_movie(movie_id, movie_data)
    finally:
        lock.release()
    if not movie:
        return not_found()

    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    global lock, cinit
    if not cinit:
        init_cache()
        cinit = True
    lock.acquire()
    try:
        movie = current_app.movies.delete_movie(movie_id)
    finally:
        lock.release()
    if not movie:
        return not_found()
    removeCached(movie_id)
    return jsonify({})


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)


def toCache(movie):
    global cache_current, cache_limit, mcache
    if not getCachedMovie(movie['id']):
        if cache_current == cache_limit:
            cache_current = 1
        mcache[cache_current] = movie
        cache_current += 1
    else:
        i = 1
        while i <= cache_limit:
            if mcache[i]['id'] == movie['id']:
                mcache[i] = movie
                return
            i += 1
    return


def getCachedMovie(movie_id):
    global cache_limit, mcache
    i = 1
    while i <= cache_limit:
        if mcache[i]['id'] == movie_id:
            return mcache[i]
        i += 1
    return False


def removeCached(movie_id):
    global mcache, cache_limit
    i = 1
    while i <= cache_limit:
        if mcache[i]['id'] == movie_id:
            mcache[i] = {}
            return
        i += 1
    return
