class Movies():
    def __init__(self):
        self.movies = {}
        self.id = 0

        # http://www.imdb.com/title/tt1142977/
        self.create_movie({
            "title": "Frankenweenie",
            "year": 2012,
            "director": "Tim Burton"
        })

        # http://www.imdb.com/title/tt0246578/
        self.create_movie({
            "title": "Donnie Darko",
            "year": 2001,
            "director": "Richard Kelly"
        })

        # http://www.imdb.com/title/tt0816692/
        self.create_movie({
            "title": "Interstellar",
            "year": 2014,
            "director": " Christopher Nolan "
        })

        # http://www.imdb.com/title/tt0133152/
        self.create_movie({
            "title": "Planet of the Apes",
            "year": 2001,
            "director": "Tim Burton"
        })

        # http://www.imdb.com/title/tt0063442/
        self.create_movie({
            "title": "Planet of the Apes",
            "year": 1968,
            "director": "Franklin J. Schaffner"
        })

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
