from pymongo import MongoClient
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

    def register_user(self, data):
        return self.users.insert_one(data).inserted_id

    def get_user(self, id):
        return self.users.find_one({'_id': id})

    def login_user(self, username, password):
	#login valtozo: 1 - ez jelzi azt hogy valaki jelenleg be van jelentkezve - 0 vagy sem (mint egy session)
	user_doc = self.users.find_one({'username': username, 'pass': password, 'login': 0})
	if not user_doc:
          return False
        else:
	  new_user_doc = copy.deepcopy(user_doc)
          new_user_doc["login"] = 1
          new_user_doc["_id"] = user_doc["_id"]
	  self.users.update({'_id': user_doc['_id']}, new_user_doc)	
          return True

   def logout_user(self, username):
       user_doc = self.users.find_one({'username': username, 'login': 1})
       if not user_doc:
          return False
       else:
          out_user = copy.deepcopy(user_doc)
          out_user["login"] = 0
          out_user["_id"] = user_doc["_id"]
          self.users.update({'id': user_doc['_id']}, out_user)
	  return True

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
