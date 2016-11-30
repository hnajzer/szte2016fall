from pymongo import MongoClient

class Movies():
    def __init__(self):
        client = MongoClient('mongodb://szroli-piank:Eerie2eizeex@ds155747.mlab.com:55747/szroli-piank')
        db = client['szroli-piank']
        self.movies = db.movies
#        self.movies = {}
        self.id = self.movies.count()

    def _does_movie_exist(self, id):
        return id in self.movies

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

#    def create_movie(self, data):
#        existing = self.movies.find_one({'_id': id})
#        if existing:
#            return existing
#
#        nextId = self._get_next_id()
#        data = data.copy()
#        data['id'] = nextId
#        self.movies[nextId] = data
#        return self.movies[nextId]

#    def get_movie(self, id):
#        if self._does_movie_exist(id):
#            return self.movies[id]
#        return False

#    def update_movie(self, id, data):
#        if not self._does_movie_exist(id):
#            return False
#
#        self.movies[id] = data
#        return self.movies[id]

#    def delete_movie(self, id):
#        if not self._does_movie_exist(id):
#            return False
#
#        del self.movies[id]
#        return True

    def create_movie(self, data):
        existing = self.movies.find_one({'title': data['title']})
        if existing:
            return 

        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId

        self.movies.insert_one(data).inserted_id
        return nextId

    def get_movie(self, id):
        doc = self.movies.find_one({'id': id})
        if not doc:
            return

        res = {}
        res['title'] = doc['title']
        res['year'] = doc['year']
        res['director'] = doc['director']
        return res

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'id': id}, data)

    def delete_movie(self, id):
        return self.movies.delete_one({'id': id})
