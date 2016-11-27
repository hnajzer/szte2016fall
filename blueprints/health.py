from flask import Blueprint, current_app, jsonify, request

health = Blueprint('health', __name__)


def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code

@health.route('/', methods=['GET'])
def health_check():
    if current_app.health.get_databaseconnection_status() == True :
        health = True
    else :
        health = False    
    return jsonify({
        'health': health,
        'database_connection': current_app.health.get_databaseconnection_status() 
        })

@health.app_errorhandler(500)
def page_not_found(e):
    return get_error('Internal server error', 500)    