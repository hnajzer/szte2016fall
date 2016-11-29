from flask import Blueprint, current_app, jsonify


health = Blueprint('health', __name__)


@health.route('/', methods=['GET'])
def get_health():
    descriptors = current_app.health.summary()

    # Sum up health tests
    v_health = True
    for item in descriptors:
        v_health = (v_health and descriptors[item])
    descriptors['health'] = v_health
    return jsonify(descriptors)
