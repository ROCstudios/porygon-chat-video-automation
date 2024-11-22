from flask import Blueprint, request, jsonify

generate_routes = Blueprint('generate', __name__)

@generate_routes.route('/generate/convo', methods=['POST'])
def generate():
    # Your existing generate endpoint code here
    pass

@generate_routes.route('/generate/movie', methods=['POST'])
def generate_movie():
    # Your existing generate movie endpoint code here
    pass

@generate_routes.route('/generate/posts', methods=['POST'])
def generate_posts():
    # Your existing generate posts endpoint code here
    pass
