from flask import Flask
import os

from blueprints.movies import movies
from blueprints.health import health
from blueprints.users import users, login_required
from model.movies import Movies
from model.users import Users
from model.health import Health

app = Flask(__name__)

app.movies = Movies()
app.users = Users()
app.health = Health()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/secret')
@login_required
def secret():
    return 'Secret!\n'

app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(health, url_prefix='/health')

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'secretttt'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
