from flask import Flask, render_template
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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Richardson35 házi</title>
    </head>
    <body>
        <p>TesztTeszt</p>
    </body>
    </html>
    """

app.register_blueprint(movies, url_prefix='/movies')

app.register_blueprint(series, url_prefix='/series')

if __name__ == '__main__':
    app.run()
