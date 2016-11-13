from flask import Flask

from blueprints.movies import movies
from blueprints.users import users, login_required
from model.movies import Movies
from model.users import Users

app = Flask(__name__)

app.movies = Movies()
app.users = Users()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/secret')
@login_required
def secret():
    return 'Secret!'


app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(users, url_prefix='/users')

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'secretttt'

if __name__ == '__main__':
    app.run(debug=True)
