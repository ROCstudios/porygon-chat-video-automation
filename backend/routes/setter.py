from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import shutil
import time

set_routes = Blueprint('set', __name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads/audio'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

# Global storage dictionaries for non-file data
convo_data = {}
avatar_data = {}
audio_data = {}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@set_routes.route('/convo', methods=['POST'])
def set_convo():
    data = request.get_json()
    convo_data['convo'] = data.get('convo')
    return jsonify({"message": "Conversation data saved", "data": convo_data})

@set_routes.route('/avatar', methods=['POST'])
def set_avatar():
    data = request.get_json()
    name = data.get('name')
    file_name = data.get('avatar')
    
    if not name or not file_name:
        return jsonify({"error": "No name provided"}), 400
    
    # Store the name in your conversation_data dictionary
    avatar_data['avatar_name'] = name
    avatar_data['file_name'] = file_name
    
    return jsonify({
        "message": "Avatar name saved",
        "file_name": file_name
    })

@set_routes.route('/audio', methods=['POST'])
def set_audio():
    try:    
        data = request.get_json()
        audio_url = data.get('audio_url')
        
        if not audio_url:
            return jsonify({"error": "No audio URL provided"}), 400
        
        # Store the URL in the audio_data dictionary
        audio_data['audio_url'] = audio_url
        
        return jsonify({
            "message": "Audio URL saved",
            "url": audio_url
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

