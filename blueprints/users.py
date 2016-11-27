from flask import Blueprint, current_app, jsonify, request ,session
from werkzeug.security import generate_password_hash, \
     check_password_hash
users = Blueprint('users', __name__)

def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code

@users.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if username=='' or password=='':
        return get_error("Warning: Wrong parameters", 400)
    if current_app.users.isset_user(username) is not None:
        return get_error("Warning: Wrong parameters", 400)
    if session.get('login') is True and session.get('username') == username:
        return get_error("Warning: Wrong parameters", 400)
    
    user_doc = {"username": username, "password": generate_password_hash(password)}
    current_app.users.registration(user_doc)
    return jsonify({ 'message': 'User registration successfull' })

@users.route('/login', methods=['POST'])
def login():
    print(session)
    username = request.form.get('username')
    password = request.form.get('password')

    if username=='' or password=='':
        return get_error("Warning: Wrong parameters", 400)  
    if session.get('login') is True and session.get('username') != username:
        return get_error("Warning: Another user is login.", 400)
    if session.get('login') is True and session.get('username') == username:
        return get_error("Warning: You are already login.", 400)
    if current_app.users.login(username, password) is False:
        return get_error("Warning: Login failed.", 400)

    session['username'] = username
    session['login'] = True 
    return jsonify({ 'message': 'login successfull' })


@users.route('/logout')
def logout():
    username = session["username"]

    if username=='':
        return get_error("Warning: Wrong parameters", 400)
    if session.get('login') is True and session.get('username') != username:
        return get_error("Warning: Can't log out another user")     
    if session.get('login') is None and session.get('username') == None:
        return get_error("Warning: Already logged out")

    session.pop('username', None)
    session.pop('login', None)
    return jsonify({ 'message': 'Logged out successfull' })

@users.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)
