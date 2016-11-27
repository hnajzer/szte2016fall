from flask import Blueprint, current_app, jsonify, request, session

health = Blueprint('health', __name__)

def get_error(message, code):
    return jsonify({
        'message': message,
        'code': code
    }), code

@health.route('/', methods=['GET'])
def health_is():
	if current_app.health.getDatabaseConn() == False:
		boolean=False
	else:
		boolean=True
	return jsonify({'health': boolean, 'database_connection': boolean})
