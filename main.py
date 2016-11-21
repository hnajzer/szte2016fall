from flask import Flask, render_template
import os

from blueprints.movies import movies
from blueprints.series import series
from blueprints.ursers import users
from model.mongo import Movies
from model.series import Series

app = Flask(__name__)

app.movies = Movies()
app.series = Series()
app.users  = Users()

@app.route('/')
def hello_world():
    return '9. homework - users, login'

app.register_blueprint(movies, url_prefix='/movies')

app.register_blueprint(series, url_prefix='/series')

app.register_blueprint(series, url_prefix='/users')

if __name__ == '__main__':
    app.run()
