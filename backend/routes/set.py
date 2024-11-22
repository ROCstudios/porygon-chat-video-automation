from flask import Blueprint, request, jsonify

set_routes = Blueprint('set', __name__)

@set_routes.route('/set/convo', methods=['POST'])
def set_convo():
    # Your existing set convo endpoint code here
    pass

@set_routes.route('/set/avatar', methods=['POST'])
def set_avatar():
    # Your existing set avatar endpoint code here
    pass

@set_routes.route('/set/audio', methods=['POST'])
def set_audio():
    # Your existing set audio endpoint code here
    pass
