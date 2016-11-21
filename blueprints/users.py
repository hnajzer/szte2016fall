from flask import Blueprint, current_app, jsonify, request

users = Blueprint('users', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('User already exists!', 409)


def not_found():
    return get_error('User not found!', 404)


def parse_user(data):
    user = {}
    if 'username' in data:
        user['username'] = data['username']
    if 'pass' in data:
        user['pass'] = data['pass']
    if 'login' in data:
        user['login'] = data['login']
    return user


@users.route('/<int:user_id>', methods=['POST'])
def get_user(user_id):
    user = current_app.users.get_user(user_id)
    if not user:
        return not_found()
    return jsonify(user)


@users.route('/', methods=['POST'])
def post_user():
    user_data = parse_user(request.get_json())
    #itt kell az str hogy ne legyen ObjectId TypeError hiba!!
    user = str(current_app.users.register_user(user_data))
    if not user:
        return existing()
    return jsonify(user)


#@movies.route('/<int:user_id>', methods=['PATCH'])
#def patch_movie(movie_id):
#    movie_data = parse_movie(request.get_json())
#    movie = current_app.movies.update_user(movie_id, movie_data)
#    if not movie:
#        return not_found()
#    return jsonify(movie)


#@movies.route('/<int:user_id>', methods=['DELETE'])
#def delete_movie(user_id):
#   user = current_app.users.delete_user(movie_id)
#    if not movie:
#        return not_found()
#    return jsonify({})


@users.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
