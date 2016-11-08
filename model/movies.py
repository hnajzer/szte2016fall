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