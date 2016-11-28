# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, escape, session, jsonify, session
from functools import wraps
import os

from blueprints.movies import movies
from blueprints.series import series
from blueprints.users import users
from model.movies import Movies
from model.series import Series
from model.users import Users

app = Flask(__name__)
app.secret_key = "asdas"
app.movies = Movies()
app.series = Series()
app.users  = Users()

@app.route('/')
def hello_world():
    return 'Hello continuous delivery!'


app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(series, url_prefix='/series')
app.register_blueprint(users, url_prefix='/users')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
