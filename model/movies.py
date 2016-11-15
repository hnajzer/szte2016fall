class Movies():
    def __init__(self):
        self.movies = {}
        self.id = 0

    def _does_movie_exist(self, id):
        return id in self.movies

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

    def create_movie(self, data):
        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId
        self.movies[nextId] = data
        return self.movies[nextId]

    def get_movie(self, id):
        if self._does_movie_exist(id):
            return self.movies[id]
        return False

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
