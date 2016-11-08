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

    def _is_duplicate(self, data):
        is_duplicate = False

        for key in self.movies:
            same_title = data['title'] == self.movies[key]['title']
            same_year = data['year'] == self.movies[key]['year']
            same_director = data['director'] == self.movies[key]['director']

            is_duplicate = True if same_title and same_year and same_director else is_duplicate

        return is_duplicate

    def reset(self):
        self.movies = {}
        self.id = 0

    def create_movie(self, data):
        is_duplicate = self._is_duplicate(data)

        if is_duplicate:
            return False
        else:
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
