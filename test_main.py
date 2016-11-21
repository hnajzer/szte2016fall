import unittest

from assertpy import assert_that
from flask import json
from mock import Mock
from bson import BSON
from bson import json_util

import main
from model.movies import Movies
from model.mongo import Movies
from model.users import Users

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
        assert response.status_code == 200

    #def test_create_new_movie_with_mock(self):
    #    self.app.application.movies = Mock()
    #    self.app.application.movies.create_movie = Mock(return_value=self.a_movie_data)

    #    self.app.post('/movies/'
    #                  , data=json.dumps(self.a_movie_data)
    #                  , content_type='application/json')

    #   self.app.application.movies.create_movie.assert_called_once_with(self.a_movie_data)


if __name__ == '__main__':
    unittest.main()
