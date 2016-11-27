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

<<<<<<< HEAD
class Users():
=======
class Users(object):

	def __init__(self, username, password):
		self.username = username
		self.set_password(password)
		client = MongoClient('ds011495.mlab.com', 11495)
		client['szte2016fall'].authenticate('ricsi', 'ricsi123')
		db = client['szte2016fall']		
		self.users = db.users

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def registration(self):		
		new_user_doc = {"name": self.username, "pass": self.pw_hash}
		return self.users.insert_one(new_user_doc).inserted_id

#Only for testing
>>>>>>> ebe78992850354071a21354319f314ff746c304c

	def __init__(self):
		client = MongoClient('ds011495.mlab.com', 11495)
		client['szte2016fall'].authenticate('ricsi', 'ricsi123')
		db = client['szte2016fall']		
		self.users = db.users

	def isset_user(self, username):
		return self.users.find_one({'username': username})

	def registration(self, new_user_doc):
		return self.users.insert_one(new_user_doc).inserted_id

	def login(self, username, password):
		user_doc = self.users.find_one({'username': username})
		if user_doc is None:
			return False
		elif check_password_hash(user_doc['password'], password) is True:
			return True
		else:
			return False
