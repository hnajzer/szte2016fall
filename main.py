<<<<<<< HEAD
from flask import Flask, render_template, session, current_app, jsonify
import os
from functools import wraps
=======
from flask import Flask
import os
import cgi

>>>>>>> ebe78992850354071a21354319f314ff746c304c
from blueprints.movies import movies
from blueprints.series import series
from blueprints.users import users
from model.mongo import Movies
from model.mongo import Users
from model.series import Series

app = Flask(__name__)
app.movies = Movies()
app.series = Series()
<<<<<<< HEAD
app.users = Users()

app.secret_key = "ezkell"

@app.route('/')
def main():
	return render_template('index.html', output=session)
=======

@app.route('/')
def hello_world():
    return """
    <html>
        <head>
            <title>9. homework</title>
        </head>
    <body>
        <form method="post" action="">
            <input type="text" name="username">
            <input type="text" name="password">
            <input type="submit">
        </form>
    </body>
    </html>
    """
user = Users("ricsi123", "1234")
user.registration
>>>>>>> ebe78992850354071a21354319f314ff746c304c

@app.route('/register')
def register_form():
	return render_template('register.html')

@app.route('/login')
def login_form():
	return render_template('login.html')


app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(series, url_prefix='/series')

app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
    app.run()
