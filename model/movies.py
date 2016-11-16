from pymongo import MongoClient

class Movies():
    # mongo ds155727.mlab.com:55727/piank1773 -u <dbuser> -p <dbpassword>'
    def __init__(self):
        client = MongoClient('ds155727.mlab.com', 55727)
        client['piank1773'].authenticate('admin', 'admin')
        db = client['piank1773']
        self.movies = db.movies
        self.create_movie({"title": "aSD", "year": 1995})

    def create_movie(self, data):
        return self.movies.insert_one(data).inserted_id

    def get_movie(self, id):
        return self.movies.find_one({'_id': id})

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'_id': id}, data)

    def delete_movie(self, id):
        return self.movies.delete_one({'_id': id})
