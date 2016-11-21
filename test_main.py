import unittest

from assertpy import assert_that
from flask import json
from mock import Mock
from bson import BSON
from bson import json_util

import main
from model.movies import Movies
from model.mongo import Users

class MainTest(unittest.TestCase):
    def setUp(self):
        self.a_user_data = {"username": "ricsi123", "password": "123", "login": 0}
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.app.application.users = Users()

    def test_hello(self):
        rv = self.app.get('/')
        assert b"9. homework - users, login" in rv.data    

    def test_register_new_user(self):
        response = self.app.post('/users/'
                                 , data=json.dumps(self.a_user_data)
                                 , content_type='application/json')
        #assert response.status_code == 200

    def test_create_new_user_with_mock(self):
        self.app.application.users = Mock()
        self.app.application.users.register_user = Mock(return_value=self.a_user_data)

        self.app.post('/users/'
                      , data=json.dumps(self.a_user_data)
                      , content_type='application/json')

        self.app.application.users.register_user.assert_called_once_with(self.a_user_data)


if __name__ == '__main__':
    unittest.main()
