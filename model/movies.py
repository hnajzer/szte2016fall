class Movies():
    def __init__(self):
        self.movies = {}
        self.id = 0

    def _does_movie_exist(self, id):
        return id in self.movies

    def _get_next_id(self):
        self.id += 1
        return self.id

    def create_movie(self, data):
        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId
        self.movies[nextId] = data
        return self.movies[nextId]

    def get_movie(self, identify):
        if self._does_movie_exist(identify):
            return self.movies[identify]
        return False

    def update_movie(self, identify, data):
        if not self._does_movie_exist(identify):
            return False

        self.movies[identify] = data
        return self.movies[identify]

    def delete_movie(self, identify):
        if not self._does_movie_exist(identify):
            return False

        del self.movies[identify]
        return True
