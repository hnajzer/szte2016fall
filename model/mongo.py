from pymongo import MongoClient
from werkzeug.security import generate_password_hash, \
     check_password_hash
import copy
class Movies():

#    def __init__(self):
#	client = MongoClient('ds011495.mlab.com', 11495)
#	client['szte2016fall'].authenticate('ricsi', 'ricsi123')
#	db = client['szte2016fall']
#	self.movies = db.movies

    def create_movie(self, data):
        return self.movies.insert_one(data).inserted_id

    def get_movie(self, id):
        return self.movies.find_one({'_id': id})

    def update_movie(self, id, data):
       return self.movies.find_one_and_replace({'_id': id}, data)

    def delete_movie(self, id):
        return self.movies.delete_one({'_id': id})

class Users(object):

	def __init__(self, username, password):
		self.username = username
		self.set_password(password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def registration(self):
		client = MongoClient('ds011495.mlab.com', 11495)
		client['szte2016fall'].authenticate('ricsi', 'ricsi123')
		db = client['szte2016fall']		
		self.users = db.users
		new_user_doc = {"username": self.username, "password": self.pw_hash}
		id = users.insert_one(new_user_doc).inserted_id
		return id

#Only for testing

#if __name__ == "__main__":
#users = Users()
#log_user = users.login_user(
#    movies = Movies()
#    new_id = movies.create_movie({"title": "Trainspotting", "year": 1995})
#    print ("Created movie:", new_id)
#    retrieved_movie = movies.get_movie(new_id)
#    print ("Retrieved movie: ", retrieved_movie)
#    movies.update_movie(new_id, {"title": "Trainspotting", "year": 1996})
#    retrieved_movie = movies.get_movie(new_id)
#    print ("Updated movie: ", retrieved_movie)
