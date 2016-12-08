from flask import Blueprint, current_app, jsonify, request, session
from functools import wraps
import string
import random
import hashlib

users = Blueprint('users', __name__)


def generatehash(password, salt=None):
    if salt is None:
        salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return hash, salt


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code


def parse_user(data):
    user = {}
    if 'username' in data:
        user['username'] = data['username']
    if 'password' in data:
        user['password'] = data['password']
    if len(user) == 2:
        return user
    else:
        return False


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return jsonify({'message': 'You need to log in'})
        return f(*args, **kwargs)
    return decorated_function


@users.route('/register', methods=['POST'])
def register_user():
    data = parse_user(request.get_json())
    if not data:
        return get_error('Bad request', 400)
    hash, salt = generatehash(data['password'])
    data.update({'password': hash, 'salt': salt})
    if current_app.users.create_user(data):
        return jsonify({'message': 'Registration OK'})
    else:
        return jsonify({'message': 'User exists'})


@users.route('/login', methods=['POST'])
def login_user():
    data = parse_user(request.get_json())
    if not data:
        return get_error('Bad request', 400)
    user = current_app.users.get_user(data['username'])
    if user is None:
        return jsonify({'message': 'Bad username/password'})
    hash = generatehash(data['password'], user['salt'])[0]
    if hash == user['password']:
        session['user'] = user['username']
        return jsonify({'message': 'Login OK'})
    else:
        return jsonify({'message': 'Bad username/password'})


@users.route('/logout', methods=['GET'])
def logout_user():
    if session.get('user'):
        session.pop('user')
        return jsonify({'message': 'Logout OK'})
    else:
        return jsonify({'message': 'User not logged in'})