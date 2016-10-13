from flask import Flask
import os
import requests
import json

from blueprints.movies import movies
from model.movies import Movies

app = Flask(__name__)

app.movies = Movies()


@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <h3>Filmek</h3>
        <ul>
            <li><a href="http://127.0.0.1:5000/movies/tt1142977">Frankenweenie</a></li>
            <li><a href="http://127.0.0.1:5000/movies/tt0246578">Donnie Darko</a></li>
            <li><a href="http://127.0.0.1:5000/movies/tt0816692">Interstellar</a></li>
            <li><a href="http://127.0.0.1:5000/movies/tt0133152">Planet of the Apes</a></li>
            <li><a href="http://127.0.0.1:5000/movies/tt0063442">Planet of the Apes</a></li>
        </ul>
    </body>
    </html>
    """

@app.route('/movies/<movie_id>')
def request_movie_content(movie_id):
    json_content = get_json_by_id(movie_id)
    do_something_with_movie(json.loads(json_content))
    return json_content

def get_json_by_id(movie_id):
    return json.dumps(requests.get('http://www.omdbapi.com/?i=' + movie_id).json())

def do_something_with_movie(data):
    app.movies.create_movie(data)

app.register_blueprint(movies, url_prefix='/movies')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = os.getenv('PORT', None))
