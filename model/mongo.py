from pymongo import MongoClient
from werkzeug.security import generate_password_hash, \
     check_password_hash
import copy
class Movies():

    def __init__(self):
        client = MongoClient('ds011495.mlab.com', 11495)
        client['szte2016fall'].authenticate('ricsi', 'ricsi123')
        db = client['szte2016fall']
        self.movies = db.movies

    def create_movie(self, data):
        return self.movies.insert_one(data).inserted_id

    def get_movie(self, id):
        return self.movies.find_one({'_id': id})

    def update_movie(self, id, data):
        return self.movies.find_one_and_replace({'_id': id}, data)

    def delete_movie(self, id):
        return self.movies.delete_one({'_id': id})

class Users():

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

class Health():
	def getDatabaseConn(self):
		try:
			client = MongoClient('ds011495.mlab.com', 11495)
			client['szte2016fall'].authenticate('ricsi', 'ricsi123')
			return True
		except:  
			return False 
