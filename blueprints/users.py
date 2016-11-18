from flask import Blueprint, abort, current_app, jsonify, request, session, current_app

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
            return "You need to log in first\n"
    return decorated_function


def calculate_scrypt_hash(pwd, salt, hash_params):
    hash = pyscrypt.hash(str(pwd), str(salt), hash_params['N'], hash_params['r'], hash_params['p'], hash_params['dkLen'])
    hash = hash.encode('hex')
    return hash


@users.route('/logout', methods=['POST'])
def logout():
    if not session['loggedin']:
        return "You are not logged in.\n"
    session['loggedin'] = False
    return "You are now logged out."


@users.route('/login', methods=['POST'])
def do_login():
    data = request.get_json()
    #
    if 'username' not in data or 'password' not in data:
        return "Login attempt failure.\n"

    found_user = (current_app.users.get_user(data['username']))
    if not found_user:
        return "Login attempt failure.\n"

    hashed_input_pw = calculate_scrypt_hash(data['password'], str(found_user['salt']), found_user['hash_params'])
    if hashed_input_pw != found_user['hash']:
        return "Login attempt failure.\n"

    session['loggedin'] = True
    return "Logged in\n"


@users.route('/register', methods=['POST'])
def register_user():
    user = str(request.form['username'])
    pwd = str(request.form['password'])

    salt = str(''.join([random.choice(string.ascii_letters+string.digits) for i in range(10)]))
    hash_params = {'N': 1024, 'r': 1, 'p': 1, 'dkLen': 32}
    hash1 = calculate_scrypt_hash(pwd.encode('ascii'), salt.encode('ascii'), hash_params)
    data = {'user': user, 'salt': salt, 'hash': hash1, 'hash_params': hash_params}
    current_app.users.create_user(data)
    return "Registered\n"


@users.route('/login_user', methods=['POST'])
def login_user():
    user_name = request.form['username']
    pwd  = request.form['password']

    user_data=current_app.users.get_user(user_name)
    if not user_data:
        return "Can't find user\n"

    hash = calculate_scrypt_hash(pwd, user_data['salt'], user_data['hash_params'])

    if hash == user_data['hash']:
        session['loggedin'] = True
        return "Login succeeded - "+user_name+"\n"
    else:
        if 'loggedin' in session: del session['loggedin']
        return "Can't find user or bad password\n"

########################################### UNSAFE PARTS

@users.route('/json_login_user', methods=['POST'])
def login_user_json():
    data=request.json
    print(data)
    user_name = data['username']
    pwd       = data['password']

    user_data=current_app.users.get_user_with_pwd(user_name, pwd)


    if user_data:
        session['loggedin'] = True
        return "Login succeeded - "+user_name+"\n"
    else:
        if 'loggedin' in session: del session['loggedin']
        return "Can't find user or bad password\n"


@users.route('/raw_register', methods = ['POST'])
def register_user_raw():
    user = str(request.form['username'])
    pwd  = str(request.form['password'])

    data = {'user': user, 'pwd': pwd}
    current_app.users.create_user(data)
    return "Registered  - raw\n"
