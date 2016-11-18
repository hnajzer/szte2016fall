from behave import given, when, then
from assertpy import assert_that
import requests

@given(u'the database is empty')
def step_impl(context):
    response = requests.delete(context.url + '/series/')
    assert_that(response.status_code).is_equal_to(200)

@when(u'I request all series')
def step_impl(context):
    context.response = requests.get(context.url + '/series/')

@given(u'I create a series called "{title}" with summary "{summary}" and with {seasons:d} seasons')
@when(u'I create a series called "{title}" with summary "{summary}" and with {seasons:d} seasons')
def step_impl(context, title, summary, seasons):
    payload = {'title': title, 'summary': summary, 'seasons': seasons}
    context.response = requests.post(context.url + '/series/', json=payload)
    context.lastSeriesId = str(context.response.json()['id'])

@when(u'I create a series called "{title}"')
def step_impl(context, title):
    payload = {'title': title}
    context.response = requests.post(context.url + '/series/', json=payload)
    if 'id' in context.response.json():
        context.lastSeriesId = str(context.response.json()['id'])
    else:
        context.lastSeriesId = None

@when(u'I get this series back')
def step_impl(context):
    context.response = requests.get(context.url + '/series/' + context.lastSeriesId)
    context.lastSeries = context.response.json()

@when(u'I delete this series')
def step_impl(context):
    context.response = requests.delete(context.url + '/series/' + context.lastSeriesId)

@when(u'I modify the summary to "{summary}"')
def step_impl(context, summary):
    payload = {'summary': summary}
    context.response = requests.patch(context.url + '/series/' + context.lastSeriesId, json=payload)

@then(u'there are {count:d} series')
def step_impl(context, count):
    response = requests.get(context.url + '/series/')
    assert_that(response.json()).is_type_of(dict)
    assert_that(response.json()).is_length(count)

@then(u'I receive a {code:d} status code response')
def step_impl(context, code):
    assert_that(context.response.status_code).is_equal_to(code)

@then(u'the series title is "{title}"')
def step_impl(context, title):
    assert_that(context.lastSeries).is_type_of(dict)
    assert_that(context.lastSeries["title"]).is_equal_to(title)

@then(u'the series summary is "{summary}"')
def step_impl(context, summary):
    assert_that(context.lastSeries).is_type_of(dict)
    assert_that(context.lastSeries["summary"]).is_equal_to(summary)

@then(u'the series has {seasons:d} seasons')
def step_impl(context, seasons):
    assert_that(context.lastSeries).is_type_of(dict)
    assert_that(context.lastSeries["seasons"]).is_equal_to(seasons)