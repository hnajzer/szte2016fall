from flask import Blueprint, abort, current_app, jsonify, request, session, current_app
import model.users
from functools import wraps
import random
import string
import pyscrypt

users = Blueprint('users', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' in session and session['loggedin']:
            return f(*args, **kwargs)
        else:
            return "You need to log in first"
    return decorated_function

def calculate_scrypt_hash(pwd, salt, hash_params):
    hash = pyscrypt.hash(pwd, salt, hash_params['N'], hash_params['r'], hash_params['p'], hash_params['dkLen'])
    hash = hash.encode('hex')
    return hash

@users.route('/login', methods = ['GET'])
def do_login():
    session['loggedin'] = True
    return "Logged in"

@users.route('/register', methods = ['POST'])
def register_user():
    user = str(request.form['username'])
    pwd  = str(request.form['password'])

    salt = ''.join([ random.choice(string.ascii_letters+string.digits) for i in range(10) ])
    hash_params={'N': 1024, 'r':1, 'p':1, 'dkLen':32}
    hash = calculate_scrypt_hash(pwd, salt, hash_params)
    data = {'user': user, 'salt': salt, 'hash': hash, 'hash_params': hash_params}
    current_app.users.create_user(data)
    return str(data)

@users.route('/login_user', methods = ['POST'])
def login_user():
    user_name = str(request.form['username'])
    pwd  = str(request.form['password'])

    user_data=current_app.users.get_user(user_name)
    if not user_data:
        return "Can't find user"

    hash = calculate_scrypt_hash(pwd, user_data['salt'], user_data['hash_params'])

    if (hash == user_data['hash']):
        session['loggedin'] = True
        return "Ok"
    else:
        return "Error"