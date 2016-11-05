import requests


class Movies():
    def __init__(self):
        self.movies = {}
        self.id = 0
        #self._selfinit()

    def _selfinit(self):
        self.create_movie(requests.get('http://www.omdbapi.com/?i=tt1142977&plot=short&r=json', auth=('', '')).json())
        self.create_movie(requests.get('http://www.omdbapi.com/?i=tt0246578&plot=short&r=json', auth=('', '')).json())
        self.create_movie(requests.get('http://www.omdbapi.com/?i=tt0816692&plot=short&r=json', auth=('', '')).json())
        self.create_movie(requests.get('http://www.omdbapi.com/?i=tt0133152&plot=short&r=json', auth=('', '')).json())
        self.create_movie(requests.get('http://www.omdbapi.com/?i=tt0063442&plot=short&r=json', auth=('', '')).json())

    def _does_movie_exist(self, id):
        return id in self.movies

    def _get_next_id(self):
        self.id += 1
        return self.id

    def create_movie(self, data):
        next_id = self._get_next_id()
        datacopy = data.copy()
        datacopy['id'] = next_id
        self.movies[next_id] = datacopy
        return self.movies[next_id]

    def get_movie(self, id):
        if self._does_movie_exist(id):
            return self.movies[id]
        return None

    def update_movie(self, id, data):
        if not self._does_movie_exist(id):
            return False
        self.movies[id] = data
        return self.movies[id]

    def delete_movie(self, id):
        if not self._does_movie_exist(id):
            return False
        del self.movies[id]
        return True
