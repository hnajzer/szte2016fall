from flask import Flask
import os
import web

from blueprints.movies import movies
from blueprints.series import series
from blueprints.users import users
from model.mongo import Movies
from model.mongo import Users
from model.series import Series

app = Flask(__name__)

render = web.template.render('templates/')

app.movies = Movies()
app.series = Series()

class Index(object):
    def GET(self):
        form = web.input(name="Nobody")
        username = form.username
        return username


app.register_blueprint(movies, url_prefix='/movies')

app.register_blueprint(series, url_prefix='/series')

app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
    app.run()
