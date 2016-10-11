import json
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
        self.assertEqual(result, False)

    def test_get_movie_existing(self):
        self.movie_model.create_movie(self.a_movie_data)
        result = self.movie_model.get_movie(1)
        self.assertFalse('id' in result)

    def test_create_movie_different_ids(self):
        a_movie = self.movie_model.create_movie(self.a_movie_data)
        other_movie = self.movie_model.create_movie(self.other_movie_data)
        movie1 = 'id' in a_movie
        movie2 = 'id' in other_movie
        self.assertFalse(movie1 or movie2)

    def test_create_movie_does_not_alter_data(self):
        moviedata = {}
        self.movie_model.create_movie(moviedata)
        assert_that(moviedata).does_not_contain_key('id')

    def test_get_movie_id_1(self):
        self.movie_model.create_movie("""{"Title":"Frankenweenie","Year":"2012","Rated":"PG","Released":"05 Oct 2012","Runtime":"87 min","Genre":"Animation, Comedy, Family","Director":"Tim Burton","Writer":"Leonard Ripps, Tim Burton (original idea), John August (screenplay)","Actors":"Catherine O'Hara, Martin Short, Martin Landau, Charlie Tahan","Plot":"Young Victor conducts a science experiment to bring his beloved dog Sparky back to life, only to face unintended, sometimes monstrous, consequences.","Language":"English","Country":"USA","Awards":"Nominated for 1 Oscar. Another 11 wins & 47 nominations.","Poster":"https://images-na.ssl-images-amazon.com/images/M/MV5BMTk1MjYzMjY2N15BMl5BanBnXkFtZTgwNzg2NjAwMzE@._V1_SX300.jpg","Metascore":"74","imdbRating":"7.0","imdbVotes":"75,188","imdbID":"tt1142977","Type":"movie","Response":"True"}""")
        self.assertEqual(json.loads(self.movie_model.get_movie(1))["Title"], "Frankenweenie")



if __name__ == '__main__':
    unittest.main()
