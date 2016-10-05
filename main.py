from flask import Flask
import os

from blueprints.movies import movies
from model.movies import Movies

#app = Flask(__name__)

#app.movies = Movies()


@app.route('/')
def hello_proba():
    print 'Ha ezt látod, akkor minden jó!'
    return;

hello_proba()

#app.register_blueprint(movies, url_prefix='/movies')

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
