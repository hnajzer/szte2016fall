from pymongo import MongoClient
from passlib.apps import custom_app_context as pwd_context

class Users():

    def __init__(self):
        client = MongoClient('ds031912.mlab.com', 31912)
        client['sztefall'].authenticate('vektor112', 'piank123')
        db = client['sztefall']
        self.users = db.users

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def auth_user(self, username, password):
        user = self.check_if_user_exist(username)
        if user is None:
            return False
        return pwd_context.verify(password, user["password"])

    def check_if_user_exist(self, username):
        return self.users.find_one({'username': username})

    def create_user(self, data):
        data['password'] = self.hash_password(data['password'])
        return self.users.insert_one(data).inserted_id
        