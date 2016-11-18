from flask import Flask
import os

from blueprints.movies import movies
from blueprints.series import series
from model.movies import Movies
from model.series import Series

app = Flask(__name__)

app.movies = Movies()
app.series = Series()


@app.route('/')
def hello_world():
    return 'Hello, World!'


app.register_blueprint(movies, url_prefix='/movies')

app.register_blueprint(series, url_prefix='/series')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
