from flask import Flask
import os

from blueprints.movies import movies
from model.movies import Movies

app = Flask(__name__)

app.movies = Movies()

+app.movies.create_movie (
			{"title": "Planet of the Apes", 
			"year": 1968, 
			"director": "Franklin J. Schaffner"
			}
	)

+app.movies.create_movie (
			{"title": "Planet of the Apes", 
			"year": 2001, 
			"director": "Tim Burton"
			}
	)

+app.movies.create_movie (
			{"title": "Interstellar", 
			"year": 2014, 
			"director": "Christopher Nolan"
			}
	)

+app.movies.create_movie (
			{"title": "Frankenweenie - Ebcsont beforr", 
			"year": 2012, 
			"director": "Tim Burton"}
	)

+app.movies.create_movie (
			{"title": "Donnie Darko", 
			"year": 2001, 
			"director": "Richard Kelly"}
	)

@app.route('/')
def hello_world():
    return 'Hello continuous delivery!'


app.register_blueprint(movies, url_prefix='/movies')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', None))
