from flask import Blueprint, current_app, jsonify, request

health = Blueprint('health', __name__)

@health.route('/', methods=['GET'])
def get_health():
    if current_app.health.get_status_health() == True :
        health = True
    else:
        health = False
    return jsonify({'health': health, 'db_conn': current_app.health.get_status_health()})
