from pymongo import MongoClient
from bson.objectid import ObjectId

class Movies():

    def __init__(self):
        client = MongoClient('ds011495.mlab.com', 11495)
        client['szte2016fall'].authenticate('ricsi', 'ricsi123')
        db = client['szte2016fall']
        self.movies = db.movies

    def create_movie(self, data):
        return str(self.movies.insert_one(data).inserted_id)

    def get_movie(self, id):
        return self.movies.find_one({'_id': ObjectId(id)})

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'_id': ObjectId(id)}, data)

    def delete_movie(self, id):
        return self.movies.delete_one({'_id': ObjectId(id)})
