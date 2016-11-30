from flask import Flask
import os

from blueprints.movies import movies
from model.movies import Movies

from blueprints.health import health
from model.health import Health

app = Flask(__name__)

app.movies = Movies()
app.health = Health()

@app.route('/')
def hello_world():
    return 'Hello, World!'


app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(health, url_prefix='/health')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
