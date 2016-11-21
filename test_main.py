import unittest

from assertpy import assert_that
from flask import json
from mock import Mock
from pymongo import MongoClient

import main
from model.movies import Movies


class MainTest(unittest.TestCase):
    def setUp(self):
        self.a_movie_data = {"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}

        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.app.application.movies = Movies()

    def test_hello(self):
        rv = self.app.get('/')
        assert "Hello, continuous delivery!" in rv.data


if __name__ == '__main__':
    unittest.main()
