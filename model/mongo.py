from pymongo import MongoClient
from os import getenv


class Movies():

    def __init__(self):
        client = MongoClient(getenv('MONGO_SERVER'), int(getenv('MONGO_PORT')))
        db = client[getenv('MONGO_DB')]
        db.authenticate(getenv('MONGO_USER'), getenv('MONGO_PASS'))
        self.movies = db.movies
        d = self.movies.find_one(sort=[('_id', -1)])
        if d is None:
            self.id = 0
        else:
            self.id = int(d['id'])

    def create_movie(self, data):
        self.id += 1
        data['id'] = str(self.id)
        self.movies.insert_one(data)
        return self.movies.find_one(data, projection={'_id': False})

    def get_movie(self, id):
        return self.movies.find_one({'id': str(id)}, projection={'_id': False})

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'id': str(id)}, data)

    def delete_movie(self, id):
        return self.movies.find_one_and_delete({'id': str(id)}, projection={'_id': False})
