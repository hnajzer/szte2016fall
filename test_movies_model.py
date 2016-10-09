import unittest

from assertpy import assert_that

from model.movies import Movies


class MoviesModelTest(unittest.TestCase):
    def setUp(self):
        self.a_movie_data = {}
        self.other_movie_data = {}
        self.movie_model = Movies()
        self.movie_model.add_imdb_id('tt1142977')
        self.movie_model.add_imdb_id('tt0246578')
        self.movie_model.add_imdb_id('tt0816692')
        self.movie_model.add_imdb_id('tt0133152')
        self.movie_model.add_imdb_id('tt0063442')

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

    #def test_get_movie_id_1(self):



if __name__ == '__main__':
    unittest.main()
