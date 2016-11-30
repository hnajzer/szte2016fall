from flask import Blueprint, current_app, jsonify, request, sessions, url_for
from functools import wraps


users = Blueprint('users', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if sessions.get('login') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@users.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    data = {"username": username, "password": password}
    current_app.users.create(data)
    return jsonify({'message': 'Sucessfully registered!'})

@users.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if current_app.users.check_password(username, password) is True:
        return jsonify({'message': 'Sucessfully logged in!'})

@users.route('/logout', methods=['POST'])
@login_required
def logout():
    sessions.pop('username', None)
    sessions.pop('password', None)

    return jsonify({'message': 'Sucessfully logged out!'})
