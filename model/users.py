from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

class Users():

    def __init__(self):
        client = MongoClient('ds013456.mlab.com', 13456)
        client['piank-test'].authenticate('test', 'test')
        db = client['piank-test']
        self.users = db.users

        def set_pass(self, password):
            self.pw_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.pw_hash, password)

        def create(self, data):
            data['password'] = self.set_pass(data['password'])
            return self.users.insert_one(data).insert_id

