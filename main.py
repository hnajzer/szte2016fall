from flask import Flask, render_template
import os

from blueprints.movies import movies
from blueprints.series import series
from model.mongo import Mongo
from model.movies import Movies
from model.series import Series

app = Flask(__name__)

app.movies = Movies()
app.series = Series()
app.Mongo = Mongo()



@app.route('/')
def hello_world():
    return '5. hazi lecci'

app.register_blueprint(movies, url_prefix='/movies')

app.register_blueprint(series, url_prefix='/series')

app.register_blueprint(series, url_prefix='/mongo')

if __name__ == '__main__':
    app.run()
