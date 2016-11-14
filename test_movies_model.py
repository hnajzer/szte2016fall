import unittest

from assertpy import assert_that

from model.movies import Movies


class MoviesModelTest(unittest.TestCase):
    def setUp(self):
        self.frankenweenie_data = {"title": "Frankenweenie", "year": 2012, "director": "Tim Burton"}
        self.interstellar_data = {"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"}

        self.movie_model = Movies()

    def tearDown(self):
        pass

    ####################################################################################################################
    #   Get movie tests
    ####################################################################################################################

    def test_get_movie_nonexisting(self):
        result = self.movie_model.get_movie(1)

        assert_that(result).is_false()

    def test_get_movie_existing(self):
        self.movie_model.create_movie(self.frankenweenie_data)
        result = self.movie_model.get_movie(1)

        assert_that(result).contains_key('id')

    ####################################################################################################################
    #   Create movie tests
    ####################################################################################################################

    def test_create_movie_different_ids(self):
        frankenweenie_movie = self.movie_model.create_movie(self.frankenweenie_data)
        interstellar_movie = self.movie_model.create_movie(self.interstellar_data)

        assert_that(frankenweenie_movie['id']).is_not_equal_to(interstellar_movie['id'])

    def test_create_movie_duplicate(self):
        res = self.movie_model.create_movie(self.frankenweenie_data)
        res_duplicate = self.movie_model.create_movie(self.frankenweenie_data)

        assert_that(res).is_true()
        assert_that(res_duplicate).is_false()

    def test_create_movie_does_not_alter_data(self):
        moviedata = {}
        self.movie_model.create_movie(moviedata)

        assert_that(moviedata).does_not_contain_key('id')

    ####################################################################################################################
    #   Update movie tests
    ####################################################################################################################

    def test_update_movie_existing(self):
        wrong_data = {"title": "Frankenweenieeeeee", "year": 2012, "director": "Tim Burton"}
        self.movie_model.create_movie(wrong_data)
        self.movie_model.update_movie(1, self.frankenweenie_data)

        result = self.movie_model.get_movie(1)
        assert_that(result['title']).is_equal_to('Frankenweenie')

    def test_update_movie_nonexisting(self):
        result = self.movie_model.update_movie(1, self.frankenweenie_data)
        assert_that(result).is_false()

    ####################################################################################################################
    #   Delete movie tests
    ####################################################################################################################

    def test_delete_movie_existing(self):
        data = {"title": "Frankenweenie", "year": 2002, "director": "Tim Burton"}
        self.movie_model.create_movie(data)

        del_res = self.movie_model.delete_movie(1)
        get_res = self.movie_model.get_movie(1)

        assert_that(del_res).is_true()
        assert_that(get_res).is_false()

    def test_delete_movie_nonexisting(self):
        result = self.movie_model.delete_movie(1)
        assert_that(result).is_false()

if __name__ == '__main__':
    unittest.main()
