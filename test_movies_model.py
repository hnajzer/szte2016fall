import unittest

from assertpy import assert_that

from model.movies import Movies


class MoviesModelTest(unittest.TestCase):
    def setUp(self):
        self.a_movie_data = {"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}
        self.other_movie_data = {"title": "Interstellar1", "year": 2015, "director": "Christopher Nolagn"}
        self.movie_model = Movies()

    def tearDown(self):
        pass

    def test_get_movie_nonexisting(self):
        result = self.movie_model.get_movie('0123456789abcdef01234567')

        assert_that(result).is_false()

    def test_get_movie_existing(self):
        m_id = self.movie_model.create_movie(self.a_movie_data)
        result = self.movie_model.get_movie(m_id)

        assert_that(result).contains_key('_id')

    def test_create_movie_different_ids(self):
        a_movie = self.movie_model.create_movie(self.a_movie_data)
        other_movie = self.movie_model.create_movie(self.other_movie_data)

        assert_that(a_movie).is_not_equal_to(other_movie)

    def test_create_movie_does_not_alter_data(self):
        moviedata = {}
        self.movie_model.create_movie(moviedata)

        assert_that(moviedata).does_not_contain_key('_id')

if __name__ == '__main__':
    unittest.main()
