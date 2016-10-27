from flask import Flask
import os

# series imports
from blueprints.series import series
from model.series import Series
# movies imports
from blueprints.movies import movies
from model.movies import Movies

app = Flask(__name__)

app.series = Series()
app.movies = Movies()


@app.route('/')
def hello_world():
    return 'Hello, World!'


app.register_blueprint(series, url_prefix='/series')
app.register_blueprint(movies, url_prefix='/movies')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
