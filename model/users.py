from pymongo import MongoClient
import crypt

class Users():
    logged_username = ''

    def __init__(self):
        self.salt = 'xv}^8bqs!gS&hDV[|T~VvHpl| zv:}/gqK(<|$=Vo=jgYS=9U`9T4TB_L||[%<$}'
        client = MongoClient('mongodb://szroli-piank:Eerie2eizeex@ds155747.mlab.com:55747/szroli-piank')
        db = client['szroli-piank']
        self.users = db.users
        self.id = self.users.count()

    def _does_user_exist(self, id):
        return id in self.users

    def _get_next_id(self):
        self.id = self.id + 1
        return self.id

    def register_user(self, data):
        if not 'name' in data:
            return False
        nextId = self._get_next_id()
        data = data.copy()
        data['id'] = nextId
        data['pass'] = crypt.crypt(data['pass'], '$6$' + self.salt)

        # check username
        doc = self.users.find_one({'name': data['name']}, {'_id': False})
        if doc:
            print("User already exists: " + data['name'])
            return False

        self.users.insert_one(data)
        print("User registered successfully: " + data['name'])
        return self.get_user(data)

    def login_user(self, data):
        if not data:
            return False
        if not 'name' in data:
            return False
        if not 'pass' in data:
            return False

        data = data.copy()
        data['pass'] = crypt.crypt(data['pass'], '$6$' + self.salt)
        login_data = self.get_user(data)
        if login_data:
            Users.logged_username = login_data['name']
            print("User logged in: " + login_data['name'])
            return login_data
        else:
            return False

    def logout_user(self):
        if not self.check_logged_user():
            return False

        print("User logged out: " + Users.logged_username)
        Users.logged_username = ''
        return True

    def get_user(self, data):
        doc = self.users.find_one({'name': data['name'], 'pass': data['pass']}, {'_id': False})
        if not doc:
            return False
        return doc

    @staticmethod
    def check_logged_user():
        if not Users.logged_username:
            return False
        else:
            return True

    def truncate(self):
        self.id = 0
        return self.users.drop()
