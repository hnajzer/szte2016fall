import unittest

from assertpy import assert_that
from flask import json
from mock import Mock

import main
from model.movies import Movies


class MainTest(unittest.TestCase):
    def setUp(self):
        self.movie_data = [{
            "title": "Frankenweenie",
            "year": 2012,
            "director": "Tim Burton"
        },
        {
            "title": "Donnie Darko",
            "year": 2001,
            "director": "Richard Kelly"
        },
        {
            "title": "Interstellar",
            "year": 2014,
            "director": " Christopher Nolan "
        },
        {
            "title": "Planet of the Apes",
            "year": 2001,
            "director": "Tim Burton"
        },
        {
            "title": "Planet of the Apes",
            "year": 1968,
            "director": "Franklin J. Schaffner"
        }]
        self.movies = Movies()

        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.app.application.movies = Movies()

    def test_hello(self):
        rv = self.app.get('/')
        assert "Hello continuous delivery" in rv.data

    def test_get_movie_nonexisting(self):
        i = 0
        while True:
            movie = self.movies.get_movie(i+1)
            if movie is False:
                break
            response = self.app.get('/movies/' + str(i+1))
            assert response.status_code != 404
            i = i + 1

    def test_get_movie_existing(self):
        i = 0
        while True:
            movie = self.movies.get_movie(i+1)
            if movie is False:
                break
            self.app.post('/movies/'
                          , data=json.dumps(movie)
                          , content_type='application/json')
            response = self.app.get('/movies/' + str(i+1))
            json_data = json.loads(response.data)

            assert response.status_code == 200
            assert json_data['title'] == self.movie_data[i]['title']
            i = i + 1

    def test_get_movie_existing_without_post(self):
        i = 0
        while True:
            movie = self.movies.get_movie(i+1)
            if movie is False:
                break
            # self.app.application.movies.movies[1] = movie
            response = self.app.get('/movies/' + str(i+1))

            assert_that(response.status_code).is_equal_to(200)
            i = i + 1

    def test_get_movie_existing_with_mock(self):
        i = 0
        while True:
            movie = self.movies.get_movie(i+1)
            if movie is False:
                break
            self.app.application.movies = Mock()
            self.app.application.movies.get_movie = Mock(return_value=movie)
            response = self.app.get('/movies/' + str(i+1))

            assert_that(response.status_code).is_equal_to(200)
            i = i + 1

    def test_create_new_movie(self):
        response = self.app.post('/movies/'
                                 , data=json.dumps(self.movies.get_movie(1))
                                 , content_type='application/json')
        assert response.status_code == 200

    def test_create_new_movie_with_mock(self):
        self.app.application.movies = Mock()
        self.app.application.movies.create_movie = Mock(return_value=self.movie_data[0])

        # print movie
        self.app.post('/movies/'
                      , data=json.dumps(self.movie_data[0])
                      , content_type='application/json')

        self.app.application.movies.create_movie.assert_called_once_with(self.movie_data[0])


if __name__ == '__main__':
    unittest.main()
