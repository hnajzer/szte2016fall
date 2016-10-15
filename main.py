# coding=utf-8
from flask import Flask
import os
import requests

from blueprints.movies import movies
from model.movies import Movies

app = Flask(__name__)

app.movies = Movies()

app.movies.create_movie(requests.get('http://www.omdbapi.com/?i=tt1142977&plot=short&r=json', auth=('', '')).json())
app.movies.create_movie(requests.get('http://www.omdbapi.com/?i=tt0246578&plot=short&r=json', auth=('', '')).json())
app.movies.create_movie(requests.get('http://www.omdbapi.com/?i=tt0816692&plot=short&r=json', auth=('', '')).json())
app.movies.create_movie(requests.get('http://www.omdbapi.com/?i=tt0133152&plot=short&r=json', auth=('', '')).json())
app.movies.create_movie(requests.get('http://www.omdbapi.com/?i=tt0063442&plot=short&r=json', auth=('', '')).json())

@app.route('/')
def hello_world():
    return 'Hello continuous delivery'
    #
    #return """
    #<!DOCTYPE html>
    #<html>
    #<head>
    #    <meta charset="utf-8">
    #</head>
    #<body>
    #    <h3>Filmek</h3>
    #    <ul>
    #        <li><a href="http://szte-numichi-pinkapp.herokuapp.com/movies/1">Frankenweenie</a></li>
    #        <li><a href="http://szte-numichi-pinkapp.herokuapp.com/movies/2">Donnie Darko</a></li>
    #        <li><a href="http://szte-numichi-pinkapp.herokuapp.com/movies/3">Interstellar</a></li>
    #        <li><a href="http://szte-numichi-pinkapp.herokuapp.com/movies/4">Planet of the Apes</a></li>
    #        <li><a href="http://szte-numichi-pinkapp.herokuapp.com/movies/5">Planet of the Apes</a></li>
    #    </ul>
    #    <br>
    #    A feladathoz egy nem hivatalos json api-t hasznaltam: http://omdbapi.com/
    #</body>
    #</html>"""



app.register_blueprint(movies, url_prefix='/movies')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = os.getenv('PORT', None))
