import unittest

from assertpy import assert_that
from flask import json
from mock import Mock

import main
from model.movies import Movies


class MainTest(unittest.TestCase):
    def setUp(self):
        self.movies_data = [{"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}, 
			    {"title": "Frankenweenie", "year": 2012, "director":"Tim Burton"}, 
                            {"title": "Donnie Darko", "year": 2001, "director": "Richard Kelly"}, 
                            {"title": "Planet of the Apes", "year": 2001, "director": "Tim Burton"}, 
                            {"title": "Planet of the Apes", "year": 1968, "director": "Franklin J. Schaffner"}]
        self.a_movie_data = self.movies_data[0]

        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.app.application.movies = Movies()

    def test_hello(self):
        rv = self.app.get('/')
        assert b"8. hazi mongo db" in rv.data    

    def test_create_new_movie(self):
        response = self.app.post('/movies/'
                                 , data=json.dumps(self.a_movie_data)
                                 , content_type='application/json')
        assert response.status_code == 200

    def test_create_new_movie_with_mock(self):
        self.app.application.movies = Mock()
        self.app.application.movies.create_movie = Mock(return_value=self.a_movie_data)

        self.app.post('/movies/'
                      , data=json.dumps(self.a_movie_data)
                      , content_type='application/json')

        self.app.application.movies.create_movie.assert_called_once_with(self.a_movie_data)


if __name__ == '__main__':
    unittest.main()
