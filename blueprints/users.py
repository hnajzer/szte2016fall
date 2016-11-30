from flask import Blueprint, current_app, jsonify, request

users = Blueprint('users', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def existing():
    return get_error('User already exists!', 409)


def ok():
    return get_error('OK', 200)


def not_found():
    return get_error('User not found!', 404)


def parse_user(data):
    user = {}
    if data and 'name' in data:
        user['name'] = data['name']
    else:
        return False
    if data and 'pass' in data:
        user['pass'] = data['pass']
    else:
        return False
    return user


@users.route("/register", methods=['POST'], strict_slashes=False)
def post_register():
    user_data = parse_user(request.get_json())
    if not user_data:
        return get_error('Invalid input!', 500);
    user = current_app.users.register_user(user_data)
    if not user:
        return get_error('Failed to register user!', 500)
    return jsonify(user)


@users.route("/login", methods=['POST'], strict_slashes=False)
def post_login():
    if current_app.users.check_logged_user():
        return get_error('User already logged in', 200)

    user_data = parse_user(request.get_json())
    user = current_app.users.login_user(user_data)
    if not user:
        return get_error('User with this password not found!', 404)
    return jsonify(user)


@users.route("/logout", methods=['POST'], strict_slashes=False)
def post_logout():
    user = current_app.users.logout_user()
    if not user:
        return get_error('Failed to logout user!', 500)
    return ok()


@users.route('/truncate', methods=['GET'], strict_slashes=False)
def truncate_users():
    current_app.users.truncate()
    return ok()


@users.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
