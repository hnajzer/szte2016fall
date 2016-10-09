from flask import Flask
import os

from blueprints.movies import movies
from model.movies import Movies

app = Flask(__name__)

app.movies = Movies()

app.movies.add_imdb_id('tt1142977')
app.movies.add_imdb_id('tt0246578')
app.movies.add_imdb_id('tt0816692')
app.movies.add_imdb_id('tt0133152')
app.movies.add_imdb_id('tt0063442')

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
            <li><a href="http://127.0.0.1:5000/movies/1">Frankenweenie</a></li>
            <li><a href="http://127.0.0.1:5000/movies/2">Donnie Darko</a></li>
            <li><a href="http://127.0.0.1:5000/movies/3">Interstellar</a></li>
            <li><a href="http://127.0.0.1:5000/movies/4">Planet of the Apes</a></li>
            <li><a href="http://127.0.0.1:5000/movies/5">Planet of the Apes</a></li>
        </ul>
        <br>
        A feladathoz egy nem hivatalos json api-t használtam: http://omdbapi.com/
    </body>
    </html>
    """


app.register_blueprint(movies, url_prefix='/movies')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = os.getenv('PORT', None))
