from flask import Flask
import os

from blueprints.movies import movies
from model.movies import Movies

app = Flask(__name__)

app.movies = Movies()

app.movies.create_movie({"title": "Planet of the Apes", "year": 1968, "director": "Franklin J. Schaffner"})
app.movies.create_movie({"title": "Planet of the Apes", "year": 2001, "director": "Tim Burton"})
app.movies.create_movie({"title": "Interstellar", "year": 2014, "director": "Christopher Nolan"})
app.movies.create_movie({"title": "Frankenweenie - Ebcsont beforr", "year": 2012, "director": "Tim Burton"})
app.movies.create_movie({"title": "Donnie Darko", "year": 2001, "director": "Richard Kelly"})

@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
    <head>
        <title> My movie database </title>
        <meta charset="UTF-8">
    </head>
    <body>
            <h2><bold> Movie database list:</bold></h2>
            <lu><h4>
                <a href="http://0.0.0.0:5000/movies/1"><li> Planet of the Apes /1986/</li></a>
                <a href="http://0.0.0.0:5000/movies/2"><li> Planet of the Apes /2001/</li></a>
                <a href="http://0.0.0.0:5000/movies/3"><li> Interstellar</li></a>
                <a href="http://0.0.0.0:5000/movies/4"><li> Frankeenweenie - Ebcsont beforr</li></a>
                <a href="http://0.0.0.0:5000/movies/5"><li> Donnie Darko </li></a>
            </lu></h4>
    </body>
    </html>
    """

app.register_blueprint(movies, url_prefix='/movies')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
