import unittest

from assertpy import assert_that

from model.movies import Movies


class MoviesModelTest(unittest.TestCase):
    def setUp(self):
        self.a_movie_data = {}
        self.other_movie_data = {}
        self.movie_model = Movies()

    def tearDown(self):
        pass

    def test_get_movie_nonexisting(self):
        result = self.movie_model.get_movie(1)

        assert_that(result).is_false()

    def test_get_movie_existing(self):
        self.movie_model.create_movie(self.a_movie_data)
        result = self.movie_model.get_movie(1)

        assert_that(result).contains_key('id')

    def test_create_movie_different_ids(self):
        a_movie = self.movie_model.create_movie(self.a_movie_data)
        other_movie = self.movie_model.create_movie(self.other_movie_data)

        assert_that(a_movie['id']).is_not_equal_to(other_movie['id'])

    def test_create_movie_does_not_alter_data(self):
        moviedata = {}
        self.movie_model.create_movie(moviedata)

        assert_that(moviedata).does_not_contain_key('id')

    def test_delete_movie_existing(self):
        self.movie_model.create_movie(self.a_movie_data)
        result = self.movie_model.delete_movie(1)
        assert_that(result).is_true()

    def test_delete_movie_nonexisting(self):
        result = self.movie_model.delete_movie(1)
        assert_that(result).is_false()

    def test_update_movie_existing(self):
        original = self.movie_model.create_movie(self.a_movie_data)
        result = self.movie_model.update_movie(original['id'], original)
        assert_that(result['id']).is_equal_to(original['id'])

    def test_update_movie_nonexisting(self):
        result = self.movie_model.update_movie(1, self.a_movie_data)
        assert_that(result).is_false()

if __name__ == '__main__':
    unittest.main()
