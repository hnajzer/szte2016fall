from behave import given, when, then
from assertpy import assert_that

import main


@given(u'The app is running')
def step_impl(context):
    main.app.config['TESTING'] = True
    context.app = main.app.test_client()


@given(u'I have no movies in the database')
def step_impl(context):
    pass


@given(u'I have a movie called "{title}", {year:d} directed by "{director}" under ID {movie_id}')
def step_impl(context, title, year, director, movie_id):
    data = {
        "title": title,
        "year": year,
        "director": director,
        "id": movie_id
    }
    context.app.application.movies.create_movie(data)


@when(u'I request the movie with ID {movie_id}')
def step_impl(context, movie_id):
    context.response = context.app.get('/movies/' + movie_id)


@then(u'I receive a {code:d} status code response')
def step_impl(context, code):
    assert_that(context.response.status_code).is_equal_to(code)
