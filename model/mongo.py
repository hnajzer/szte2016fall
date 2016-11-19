from bson import json_util
from pymongo import MongoClient
import json

class Mongo():

    def __init__(self, what):
        client = MongoClient('ds155727.mlab.com', 55727)
        client['piank'].authenticate('dbuser', 'dbpassword')
        db = client['piank']
        what = 'test'
        self.col = db[what]

    def create(self, data):
        return self.col.insert_one(data).inserted_id

    def get(self, id):
        return self.col.find_one({'id': id})

    def update(self, id, data):
        return self.col.find_one_and_replace({'id': id}, data)

    def delete(self, id):
        return self.col.delete_one({'id': id})

# Only for testing
if __name__ == "__main__":
    movies = Mongo()
    new_id = movies.create_movie({"title": "Trainspotting", "year": 1995})
    print ("Created movie:", new_id)
    retrieved_movie = movies.get_movie(new_id)
    print ("Retrieved movie: ", retrieved_movie)
    movies.update_movie(new_id, {"title": "Trainspotting", "year": 1996})
    retrieved_movie = movies.get_movie(new_id)
    print ("Updated movie: ", retrieved_movie)
