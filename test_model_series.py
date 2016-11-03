import unittest

from model.film import Film
from model.series import Series


class FilmModelAtomTest(unittest.TestCase):
    def setUp(self):
        self.series = Series()
        self.film = Film()
        self.a_film = Film()
        self.a_film.description = "description"
        self.a_film.director = "director"
        self.a_film.name = "name"
        self.a_film.seasons = "season"
        self.a_film.year = "2016"
        self.other_film = Film()
        self.other_film.description = "description_other"
        self.other_film.director = "director_other"
        self.other_film.name = "name_other"
        self.other_film.seasons = "season_other"
        self.other_film.year = "2017"

    def tearDown(self):
        pass

    def test_create_a_series(self):
        self.series.create_series(self.a_film)
        film = self.series.get_series(1)
        self.assertEqual(film.name, "name")

    def test_update_a_series(self):
        self.series.create_series(self.a_film)
        self.series.create_series(self.other_film)
        film = self.series.update_series(2, self.a_film)
        self.assertEqual(film.name, "name")
        self.assertEqual(self.series.get_data_lenght(), 2)

    def test_delete(self):
        self.series.create_series(self.a_film)
        self.series.delete_series(1)
        self.assertEqual(self.series.get_data_lenght(), 0)


if __name__ == '__main__':
    unittest.main()
