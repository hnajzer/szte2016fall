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
    return '9. homework - users, login'

menu = input("Please choose login or registration (L/R): ")
if menu=='L':
    username = input("Please enter username: ")
    password = input("Please enter password: ")
    user = Users(username, password)
    user.pw_hash
    login = user.check_password('123')
    print(login)
elif menu=='R':
    username = input("Please enter username: ")
    password = input("Please enter password: ")
    user = Users(username, password)
    reg = user.registration
    print(reg)
else:
    print("Wrong parameters")

app.register_blueprint(movies, url_prefix='/movies')

app.register_blueprint(series, url_prefix='/series')

app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
    app.run()
