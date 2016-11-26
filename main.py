from flask import Flask
import os

from blueprints.movies import movies
from blueprints.series import series
from blueprints.users import users
from model.mongo import Movies
from model.mongo import Users
from model.series import Series

app = Flask(__name__)

app.movies = Movies()
app.series = Series()

@app.route('/')
def hello_world():
    return """
    <html>
        <head>
            <title>9. homework</title>
        </head>
    <body>
        <form>
            <input type="text" name="username">
            <input type="submit">
        </form>
    </body>
    </html>
    """
    



app.register_blueprint(movies, url_prefix='/movies')

app.register_blueprint(series, url_prefix='/series')

app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
    app.run()
