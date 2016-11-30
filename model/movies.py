from pymongo import MongoClient
from model.users import Users

class Movies():
    def __init__(self):
        client = MongoClient('mongodb://szroli-piank:Eerie2eizeex@ds155747.mlab.com:55747/szroli-piank')
        db = client['szroli-piank']
        self.movies = db.movies
        self.id = self.movies.count()

    def _does_movie_exist(self, id):
        return id in self.movies

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

    def create_movie(self, data):
        # find_one: { azonositas kulcs-ertek alapjan, _id kizarasa (igy nem hal el a json decode) }
        if data and 'title' in data:
            existing = self.movies.find_one({'title': data['title']}, {'_id': False})
            if existing:
                return existing
        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId

        self.movies.insert_one(data)
        return self.get_movie(nextId)

    def get_movie(self, id):
        doc = self.movies.find_one({'id': id}, {'_id': False})
        if not doc:
            return False
        return doc

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'id': id}, data)

    def delete_movie(self, id):
        return self.movies.delete_one({'id': id})

    def truncate(self):
        self.id = 0
        return self.movies.drop()
