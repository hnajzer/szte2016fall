from flask import Blueprint, current_app, jsonify, request ,session

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

def wrong_param():
    return get_error('Wrong parameters', 400)

def already_logged_out():
    return get_error('U are already logged out', 400)

def already_logged_in():
    return get_error('U are already logged out', 400)                 

def invalid_credentials():
    return get_error('Invalid username or password.', 400)

def logout_before_login_anotheruser():
    return get_error('Logout before login another user.', 400)

def cant_logout_another_user():
    return get_error('Cant logout another user.', 400)        

# def parse_user(data):
#     # movie = {}
#     # if 'title' in data:
#     #     movie['title'] = data['title']
#     # if 'year' in data:
#     #     movie['year'] = data['year']
#     # if 'director' in data:
#     #     movie['director'] = data['director']
#     return movie

@users.route('/logout', methods=['POST'])
def logout():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None:
        return wrong_param() # missing arguments
    if session.get('loggedin') is True and session.get('username') != username:
        return cant_logout_another_user() # wrong username/password       
    if session.get('loggedin') is None and session.get('username') == None:
        return already_logged_out() # wrong username/password

    session.pop('username', None)
    session.pop('loggedin', None)
    return jsonify({ 'message': 'logged out' })

@users.route('/login', methods=['POST'])
def login():
    print(session)
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return wrong_param() # missing arguments
    if current_app.users.auth_user(username, password) is False:
        return invalid_credentials() # wrong username/password
    if session.get('loggedin') is True and session.get('username') != username:
        return logout_before_login_anotheruser() # wrong username/password    
    if session.get('loggedin') is True and session.get('username') == username:
        return already_logged_in() # wrong username/password

    session['username'] = username
    session['loggedin'] = True 
    return jsonify({ 'message': 'logged in' })

@users.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return wrong_param() # missing arguments
    if session.get('loggedin') is True and session.get('username') == username:
        return already_logged_in()     
    if current_app.users.check_if_user_exist(username) is not None:
        return existing() # existing user
       
    data = {"username": username, "password": password}
    current_app.users.create_user(data)
    return jsonify({ 'message': 'user created' })

@users.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
