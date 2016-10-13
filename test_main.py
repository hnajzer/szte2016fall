import unittest

from assertpy import assert_that
from flask import json
from mock import Mock

import main
from model.movies import Movies


class MainTest(unittest.TestCase):
    def setUp(self):
        self.a_movie_data = {"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}
        self.b_movie_data = {"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"}
        self.c_movie_data = {"title": "Donnie Darko", "year": 2001, "director": "Richard Kelly"}
        self.d_movie_data = {"title": "Planet of the Apes", "year": 2001, "director": "Tim Burton"}
        self.e_movie_data = {"title": "Planet of the Apes", "year": 1968, "director": "Franklin J. Schaffner"}

        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.app.application.movies = Movies()
        
    def test_get_default_movie_1_nonexisting(self):
        response = self.app.get('/movies/1')
        assert response.status_code == 404

    def test_get_default_movie_2_nonexisting(self):
        response = self.app.get('/movies/2')
        assert response.status_code == 404

    def test_get_default_movie_3_nonexisting(self):
        response = self.app.get('/movies/3')
        assert response.status_code == 404

    def test_get_default_movie_4_nonexisting(self):
        response = self.app.get('/movies/4')
        assert response.status_code == 404

    def test_get_default_movie_5_nonexisting(self):
        response = self.app.get('/movies/5')
        assert response.status_code == 404

    def test_get_movie_1_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps(self.a_movie_data)
                      , content_type='application/json')
        response = self.app.get('/movies/1')
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert json_data['title'] == "Interstellar"

    def test_get_movie_2_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps(self.b_movie_data)
                      , content_type='application/json')
        response = self.app.get('/movies/1')
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert json_data['title'] == "Frankenweenie"

    def test_get_movie_3_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps(self.c_movie_data)
                      , content_type='application/json')
        response = self.app.get('/movies/1')
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert json_data['title'] == "Donnie Darko"

    def test_get_movie_4_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps(self.d_movie_data)
                      , content_type='application/json')
        response = self.app.get('/movies/1')
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert json_data['title'] == "Planet of the Apes"
        assert json_data['year'] == 2001

    def test_get_movie_5_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps(self.e_movie_data)
                      , content_type='application/json')
        response = self.app.get('/movies/1')
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert json_data['title'] == "Planet of the Apes"
        assert json_data['year'] == 1968

    def test_get_all_movies_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps(self.a_movie_data)
                      , content_type='application/json')
        self.app.post('/movies/'
                      , data=json.dumps(self.b_movie_data)
                      , content_type='application/json')
        self.app.post('/movies/'
                      , data=json.dumps(self.c_movie_data)
                      , content_type='application/json')
        self.app.post('/movies/'
                      , data=json.dumps(self.d_movie_data)
                      , content_type='application/json')
        self.app.post('/movies/'
                      , data=json.dumps(self.e_movie_data)
                      , content_type='application/json')
        response = self.app.get('/movies/5')
        #Ha letezik 5-os ID-val film, akkor az alatta levo 4 ID-n is letezik film
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert json_data['title'] == "Planet of the Apes"
        assert json_data['year'] == 1968

    def test_get_movie_existing_without_post(self):
        self.app.application.movies.movies[1] = self.a_movie_data
        response = self.app.get('/movies/1')

        assert_that(response.status_code).is_equal_to(200)

    def test_get_movie_existing_with_mock(self):
        self.app.application.movies = Mock()
        self.app.application.movies.get_movie = Mock(return_value=self.a_movie_data)
        response = self.app.get('/movies/1')

        assert_that(response.status_code).is_equal_to(200)

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
