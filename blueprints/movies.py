from flask import Blueprint, current_app, jsonify, request

movies = Blueprint('movies', __name__)

cache = {}

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

    cached_movie = get_movie_from_cache(movie_id)

    if cached_movie:
        movie = cached_movie
    elif current_app.movies.get_movie(movie_id):
        movie = current_app.movies.get_movie(movie_id)
        cache_movie(movie_id, movie)
    else:
        return not_found()

    return jsonify(movie)


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

    if get_movie_from_cache(movie_id):
        delete_movie_from_cache(movie_id)

    if not movie:
        return not_found()
    return jsonify(movie)


@movies.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = current_app.movies.delete_movie(movie_id)

    if (get_movie_from_cache(movie_id)):
        delete_movie_from_cache(movie_id)

    if not movie:
        return not_found()
    return jsonify({})

def get_movie_from_cache(movie_id):
    global cache

    if movie_id in cache:
        return cache[movie_id]
    else:
        return None

def delete_movie_from_cache(movie_id):
    del cache[movie_id]


def cache_movie(movie_id, movie):
    global cache
    cache[movie_id] = movie


@movies.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)














































import requests
import threading

class Movies():
    def __init__(self):
        self.movies = {}
        self.id = 0
        self.lock = threading.Lock()

    def _does_movie_exist(self, id):
        return id in self.movies

    def _get_next_id(self):
        self.id += 1
        return self.id

    def create_movie(self, data):
        nextId = self._get_next_id()
        self.movies[nextId] = data
        return self.movies[nextId]

    def get_movie(self, id):
        if self._does_movie_exist(id):
            return self.movies[id]
        return False

    def update_movie(self, id, data):
        if not self._does_movie_exist(id):
            return False

        self.lock.acquire()
        try:
            data["id"] = id
            self.movies[id] = data
        finally:
            self.lock.release()
        return self.movies[id]

    def delete_movie(self, id):
        if not self._does_movie_exist(id):
            return False

        self.lock.acquire()
        try:
            del self.movies[id]
        finally:
            self.lock.release()
        return True

    def add_imdb_id(self, id):
        self.create_movie(requests.get('http://www.omdbapi.com/?i=' + id + '&plot=short&r=json', auth=('', '')).json()['Title'])