import unittest

from assertpy import assert_that
from flask import json
from mock import Mock

import main
from model.movies import Movies


class MainTest(unittest.TestCase):
    def setUp(self):
        self.a_movie_data = {"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}

        self.frankenweenie_data = {"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"}
        self.donnie_darko_data = {"title": "Donnie Darko", "year": 2001, "director": "Richard Kelly"}
        self.interstellar_data = {"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}
        self.planet_of_the_apes_2001_data = {"title": "Planet of the Apes", "year": 2001, "director": "Tim Burton"}
        self.planet_of_the_apes_1968_data = {"title": "Planet of the Apes", "year": 1968, "director": "Franklin J. Schaffner"}

        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.app.application.movies = Movies()

    def test_hello(self):
        rv = self.app.get('/')
        assert "Hello, World!" in rv.data

    ####################################################################################################################
    #   Get movie tests
    ####################################################################################################################

    def test_get_movie_nonexisting(self):
        response = self.app.get('/movies/1')
        assert response.status_code == 404

    def test_get_movie_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps(self.a_movie_data)
                      , content_type='application/json')
        response = self.app.get('/movies/1')
        json_data = json.loads(response.data)

        assert response.status_code == 200
        assert json_data['title'] == "Interstellar"

    def test_get_movie_existing_without_post(self):
        self.app.application.movies.movies[1] = self.a_movie_data
        response = self.app.get('/movies/1')

        assert_that(response.status_code).is_equal_to(200)

    def test_get_movie_existing_with_mock(self):
        self.app.application.movies = Mock()
        self.app.application.movies.get_movie = Mock(return_value=self.a_movie_data)
        response = self.app.get('/movies/1')

        assert_that(response.status_code).is_equal_to(200)

    ####################################################################################################################
    #   Create movie tests
    ####################################################################################################################

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

    def test_create_movie_duplicate(self):
        res_first = self.app.post('/movies/'
                                 , data=json.dumps(self.a_movie_data)
                                 , content_type='application/json')

        res_duplicate = self.app.post('/movies/'
                                 , data=json.dumps(self.a_movie_data)
                                 , content_type='application/json')

        assert res_first.status_code == 200
        assert res_duplicate.status_code == 409

    ####################################################################################################################
    #   Update movie tests
    ####################################################################################################################

    def test_update_movie_existing(self):
        self.app.post('/movies/'
                    , data=json.dumps({"title": "Frankenweenieeeeee", "year": 2012, "director": "Tim Burton"})
                    , content_type='application/json')

        res_1 = self.app.get('/movies/1')
        res_data_1 = json.loads(res_1.data)

        self.app.patch('/movies/1'
                    , data=json.dumps({"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"})
                    , content_type='application/json')

        res_2 = self.app.get('/movies/1')
        res_data_2 = json.loads(res_2.data)

        assert_that(res_data_1['title']).is_equal_to('Frankenweenieeeeee')
        assert_that(res_data_2['title']).is_equal_to('Frankenweenie')

    def test_update_movie_nonexisting(self):
        res = self.app.patch('/movies/1'
                       , data=json.dumps({"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"})
                       , content_type='application/json')

        assert res.status_code == 404

    ####################################################################################################################
    #   Delete movie tests
    ####################################################################################################################
    def test_delete_movie_existing(self):
        self.app.post('/movies/'
                      , data=json.dumps({"title": "Frankenweenieeeeee", "year": 2012, "director": "Tim Burton"})
                      , content_type='application/json')

        res_get_before_delete = self.app.get('/movies/1')

        res_delete = self.app.delete('/movies/1'
                            , data=json.dumps({"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"})
                            , content_type='application/json')

        res_get_after_delete = self.app.get('/movies/1')

        assert res_get_before_delete.status_code == 200
        assert res_delete.status_code == 200
        assert res_get_after_delete.status_code == 404

    def test_delete_movie_nonexisting(self):
        res = self.app.delete('/movies/1'
                            , data=json.dumps({"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"})
                            , content_type='application/json')

        assert res.status_code == 404

if __name__ == '__main__':
    unittest.main()
