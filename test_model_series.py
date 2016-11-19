import unittest

from assertpy import assert_that

from model.film import Film
from model.series import Series
from model.mongo import Mongo


class FilmModelAtomTest(unittest.TestCase):
    def setUp(self):
        self.series = Series(Mongo('movies'))
        self.a_film = Film()
        self.a_film.id = 1
        self.a_film.description = "description"
        self.a_film.director = "director"
        self.a_film.name = "name"
        self.a_film.seasons = "season"
        self.a_film.year = "2016"
        self.other_film = Film()
        self.other_film.id = 2
        self.other_film.description = "description_other"
        self.other_film.director = "director_other"
        self.other_film.name = "name_other"
        self.other_film.seasons = "season_other"
        self.other_film.year = "2017"

    def tearDown(self):
        pass

    def test_create_a_series(self):
        self.series.create_series(self.a_film)
        assert_that(self.series.get_series(self.a_film.id)).is_not_equal_to(None)

    def test_update_a_series(self):
        self.series.create_series(self.a_film)
        self.series.create_series(self.other_film)
        a = self.series.get_series(self.a_film.id)
        b = self.series.get_series(self.other_film.id)
        assert_that(a).is_not_equal_to(b)

    def test_delete(self):
        self.series.create_series(self.a_film)
        self.series.delete_series(self.a_film.id)
        result = self.series.get_series(self.a_film.id)
        assert_that(result).is_equal_to(False)


if __name__ == '__main__':
    unittest.main()
