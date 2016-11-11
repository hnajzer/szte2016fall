from pymongo import MongoClient
from bson.objectid import ObjectId

class Movies():
    def __init__(self):
        client = MongoClient('ds147487.mlab.com', 47487)
        client['piank_hazi_8'].authenticate('test_user', 'testpass')
        db = client['piank_hazi_8']
        self.movies = db.movies

    def create_movie(self, data):
        return self.movies.insert_one(data).inserted_id

    def get_movie(self, id):
        return self.movies.find_one({'_id': ObjectId(id)})

    def update_movie(self, id, data):
        #find_one_and_replace helyett update, igy konnyebben frissitunk egy-egy "mezot"
        return self.movies.find_one_and_update({'_id': id}, {'$set': data})

    def delete_movie(self, id):
        return self.movies.delete_one({'_id': id})

# Only for testing
if __name__ == "__main__":
    movies = Movies()
    new_id = movies.create_movie({"title": "Trainspotting", "year": 1995})
    print ("Created movie:", new_id)
    retrieved_movie = movies.get_movie(new_id)
    print ("Retrieved movie: ", retrieved_movie)
    movies.update_movie(new_id, {"title": "Trainspotting", "year": 1996})
    retrieved_movie = movies.get_movie(new_id)
    print ("Updated movie: ", retrieved_movie)
