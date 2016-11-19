# coding=utf-8
from flask import Flask
import os

from blueprints.movies import movies
from blueprints.series import series
from model.movies import Movies
from model.series import Series
from model.mongo import Mongo

app = Flask(__name__)

app.cachetime = 3600 # 1 óra
app.movies = Movies(app.cachetime, Mongo('movies'))
app.series = Series(Mongo('series'))



@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SZTE - PIANK - @Numichi</title>
    </head>
    <body>
        <h1>SZTE - PIANK - @Numichi</h1>
        <h2>Homework list:</h2>
        <ul>
            <li>1. Homework: Git / GitHub</li>
            <li>2. Homework: Heroku -> Hello World</li>
            <li>3. Homework: Unit test</li>
            <li>4. Homework: CI/CD (GitHub => Travis CI => Heroku)</li>
            <li>5. Homework: RESTful API</li>
            <li>6. Homework: Competition</li>
            <li>7. Homework: Clojure</li>
            <li>8. Homework: NoSQL / MongoDB</li>
            <li>9. Homework: Securty</li>
        </ul>
    </body>
    </html>
    """

app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(series, url_prefix='/series')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = os.getenv('PORT', None))
