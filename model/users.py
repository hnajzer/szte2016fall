from pymongo import MongoClient

class Users():

    def __init__(self):
        client = MongoClient('ds013456.mlab.com', 13456)
        client['piank-test'].authenticate('test', 'test')
        db = client['piank-test']
        self.users = db.users

    def create_user(self, user):
        return self.users.insert_one(user).inserted_id

    def get_user(self, name):
        return self.users.find_one({'user': name})

    def get_user_with_pwd(self, name, pwd):
        return self.users.find_one({'user': name, 'pwd': pwd} )