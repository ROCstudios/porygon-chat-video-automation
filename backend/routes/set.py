from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import tempfile
import shutil

set_routes = Blueprint('set', __name__)

# Global storage dictionaries for non-file data
conversation_data = {}
avatar_data = {}

@set_routes.route('/convo', methods=['POST'])
def set_convo():
    data = request.get_json()
    conversation_data.update(data)
    return jsonify({"message": "Conversation data saved", "data": conversation_data})

@set_routes.route('/avatar', methods=['POST'])
def set_avatar():
    data = request.get_json()
    name = data.get('name')
    file_name = data.get('avatar')
    
    if not name or not file_name:
        return jsonify({"error": "No name provided"}), 400
    
    # Store the name in your conversation_data dictionary
    avatar_data['avatar_name'] = name
    avatar_data['avatar_file_name'] = file_name
    
    return jsonify({
        "message": "Avatar name saved",
        "file_name": file_name
    })

@set_routes.route('/audio', methods=['POST'])
def set_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and file.filename.lower().endswith('.mp3'):
        filename = secure_filename(file.filename)
        # Clear previous audio files
        shutil.rmtree(TEMP_AUDIO_DIR)
        os.makedirs(TEMP_AUDIO_DIR)
        
        filepath = os.path.join(TEMP_AUDIO_DIR, filename)
        file.save(filepath)
        
        return jsonify({
            "message": "Audio saved",
            "filename": filename,
            "path": filepath
        })
    
    return jsonify({"error": "Invalid file type"}), 400

# Optional: Add cleanup function if needed
def cleanup_temp_files():
    """Clean up temporary files when needed"""
    if os.path.exists(TEMP_AVATAR_DIR):
        shutil.rmtree(TEMP_AVATAR_DIR)
    if os.path.exists(TEMP_AUDIO_DIR):
        shutil.rmtree(TEMP_AUDIO_DIR)
