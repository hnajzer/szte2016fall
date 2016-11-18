from pymongo import MongoClient

class Movies():

    def __init__(self):
        client = MongoClient('ds011495.mlab.com', 11495)
        client['szte2016fall'].authenticate('ricsi', 'ricsi123')
        db = client['szte2016fall']
        self.movies = {}
        self.id = 0

    def movie_next_id(self):
        self.id = self.id + 1
        return self.id

    def create_movie(self, data):
	nextId = self.movie_next_id()
	data = data.copy()	
        data['id'] = nextId
	self.movies[nextId] = data
        return self.movies[nextId]

    def get_movie(self, id):
        return self.movies.find_one({'_id': id})

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'_id': id}, data)

    def delete_movie(self, id):
        return self.movies.delete_one({'_id': id})
