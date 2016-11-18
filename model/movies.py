class Movies():
    def __init__(self):
        self.movies = {}
        self.id = 0

    def movie_next_id(self):
        self.id = self.id + 1
        return self.id

    def not_isset_movie(self, id):
        return id in self.movies

    def create_movie(self, data):
	nextId = self.movie_next_id()
	data = data.copy()	
        data['id'] = nextId
	self.movies[nextId] = data
        return self.movies[nextId]

    def get_movie(self, id):
        #return self.movies.find_one({'_id': id})
        if self.not_isset_movie(id): return self.movies[id]
        return False

    def update_movie(self, id, data):
        #return self.movies.find_one_and_replace({'_id': id}, data)
	if not self.not_isset_movie(id): 
        	return False

	self.movies[id] = data
        return self.movies[id]

    def delete_movie(self, id):
        #return self.movies.delete_one({'_id': id})
	if not self.not_isset_movie(id): 
           return False
        del self.movies[id]
           return True
        return False
