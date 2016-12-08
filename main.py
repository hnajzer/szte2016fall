from flask import Flask, jsonify
import os

from blueprints.movies import movies
from model.mongo import Movies
from model.mongo import Health

app = Flask(__name__)

app.movies = Movies()
app.health = Health()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/health')
def health():
    h = {'health': True}
    h.update({'database_connection': app.health.check_connection()})
    for k, v in h.items():
        if not v:
            h['health'] = False
            break
    return jsonify(h)

app.register_blueprint(movies, url_prefix='/movies')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
