from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import tempfile
import shutil

set_routes = Blueprint('set', __name__)

# Global storage dictionaries for non-file data
conversation_data = {}

# Create temp directories if they don't exist
TEMP_DIR = tempfile.gettempdir()
TEMP_AVATAR_DIR = os.path.join(TEMP_DIR, 'avatars')
TEMP_AUDIO_DIR = os.path.join(TEMP_DIR, 'audio')

os.makedirs(TEMP_AVATAR_DIR, exist_ok=True)
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

@set_routes.route('/set/convo', methods=['POST'])
def set_convo():
    data = request.get_json()
    conversation_data.update(data)
    return jsonify({"message": "Conversation data saved", "data": conversation_data})

@set_routes.route('/set/avatar', methods=['POST'])
def set_avatar():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filename = secure_filename(file.filename)
        # Clear previous avatars
        shutil.rmtree(TEMP_AVATAR_DIR)
        os.makedirs(TEMP_AVATAR_DIR)
        
        filepath = os.path.join(TEMP_AVATAR_DIR, filename)
        file.save(filepath)
        
        return jsonify({
            "message": "Avatar saved",
            "filename": filename,
            "path": filepath
        })
    
    return jsonify({"error": "Invalid file type"}), 400

@set_routes.route('/set/audio', methods=['POST'])
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
