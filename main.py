from flask import Flask, request, redirect,  session
import os

from blueprints.movies import movies
from model.movies import Movies

form
var = blueprints.users
import users
from model.users import Users

app = Flask(__name__)

app.movies = Movies()

app.users = Users()
app.secret_key = 'encrypted_text'

@app.route('/')
def hello_world():
    return 'Hello, World!'


app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
