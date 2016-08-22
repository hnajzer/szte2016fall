from pymongo import MongoClient

class Movies():

    def __init__(self):
        client = MongoClient('ds013456.mlab.com', 13456)
        client['piank-test'].authenticate('test', 'test')
        db = client['piank-test']
        self.movies = db.movies

    def create_movie(self, data):
        return self.movies.insert_one(data).inserted_id

    def get_movie(self, id):
        return self.movies.find_one({'_id': id})

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'_id': id}, data)

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
