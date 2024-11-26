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
conversation_data = [
    {
        "speaker": "Person 1",
        "message": "Hey, do you think it's easy to become rich?",
        "timestamp": "11:07 AM"
    },
    {
        "speaker": "Person 2",
        "message": "Well, I think it can be hard for some people.",
        "timestamp": "11:12 AM"
    },
    {
        "speaker": "Person 1",
        "message": "I guess it takes a lot of hard work, right?",
        "timestamp": "11:45 AM"
    },
    {
        "speaker": "Person 2",
        "message": "Yes, and smart decisions too!",
        "timestamp": "12:03 PM"
    },
    {
        "speaker": "Person 1",
        "message": "Maybe having a good education helps too?",
        "timestamp": "12:21 PM"
    },
    {
        "speaker": "Person 2",
        "message": "Sure, that can open up a lot of opportunities!",
        "timestamp": "01:10 PM"
    },
    {
        "speaker": "Person 1",
        "message": "Do you think it's easy to become rich?",
        "timestamp": "01:30 PM"
    },
    {
        "speaker": "Person 2",
        "message": "I don't think so. It needs hard work.",
        "timestamp": "01:33 PM"
    },
    {
        "speaker": "Person 1",
        "message": "But some people get rich fast, right?",
        "timestamp": "01:45 PM"
    },
    {
        "speaker": "Person 2",
        "message": "Yes, but it's so common.",
        "timestamp": "02:00 PM"
    },
    {
        "speaker": "Person 1",
        "message": "What's the best way to get rich?",
        "timestamp": "02:30 PM"
    },
]
avatar_data = {}
audio_data = {}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@set_routes.route('/convo', methods=['POST'])
def set_convo():
    data = request.get_json()
    conversation_data = data
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
    avatar_data['file_name'] = file_name
    
    return jsonify({
        "message": "Avatar name saved",
        "file_name": file_name
    })

@set_routes.route('/audio', methods=['POST'])
def set_audio():
    try:    
        if 'audio' not in request.files:
            return jsonify({"error": "No file provided"}), 400
    
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if audio_file != '' and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)

            timestamp = str(int(time.time()))
            filename = f"{timestamp}-{filename}"
            
            # Clear previous audio files
            shutil.rmtree(UPLOAD_FOLDER)
            os.makedirs(UPLOAD_FOLDER)
            
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            audio_file.save(filepath)

            audio_data['audio_file_name'] = filename
            audio_data['audio_file_path'] = filepath
            
            return jsonify({
                "message": "Audio saved",
                "filename": filename,
                "path": filepath
            })
        
        return jsonify({"error": "Invalid file type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
