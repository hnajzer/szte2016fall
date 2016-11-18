import unittest

from assertpy import assert_that
from flask import json
from bson.objectid import ObjectId

import main
from model.mongo import Movies


class MainTest(unittest.TestCase):
    def setUp(self):
        self.a_movie_data = {"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}

        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.app.application.movies = Movies()

    def test_get_movie_nonexisting(self):
        response = self.app.get('/movies/' + '5825f31b7560a429547a4317')
        assert response.status_code == 404

    def test_get_movie_existing(self):
        movie_id = self.app.post('/movies/'
                      , data=json.dumps(self.a_movie_data)
                      , content_type='application/json')
       # response = self.app.get('/movies/' + str(movie_id))
        json_data = json.loads(movie_id.data)

        assert movie_id.status_code == 200
        assert json_data['title'] == "Interstellar"

    def test_get_movie_existing_without_post(self):
        #self.app.application.movies.movies[1] = self.a_movie_data
        movie_id = str(self.app.application.movies.movies.insert_one(self.a_movie_data).inserted_id)
        print('/movies' + movie_id)
        response = self.app.get('/movies/' + movie_id)

        assert_that(response.status_code).is_equal_to(200)

    def test_create_new_movie(self):
        response = self.app.post('/movies/'
                                 , data=json.dumps(self.a_movie_data)
                                 , content_type='application/json')
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
