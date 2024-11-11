import argparse
from image_gen import draw_conversation
from movie_gen import create_video
from convo_gen import generate_conversation

import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_video():
    # Get parameters from JSON request
    data = request.get_json()
    topic = data.get('topic')
    turns = data.get('turns', 5)
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        conversation_data = generate_conversation(topic, turns)
        images_list = draw_conversation(conversation_data)
        temp_video_path = create_video(images_list)
        
        # Send file and then delete it after the response
        return_data = send_file(
            temp_video_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f'conversation_{topic}.mp4'
        )
            
        return return_data
        
    except Exception as e:
        # Clean up the temp file if there's an error
        if 'temp_video_path' in locals():
            try:
                os.remove(temp_video_path)
            except:
                pass
        return jsonify({'error': str(e)}), 500

def main():
    parser = argparse.ArgumentParser(description='Generate conversation videos')
    parser.add_argument('--topic', type=str, required=True, help='Topic for the conversation')
    parser.add_argument('--turns', type=int, default=5, help='Number of conversation turns (default: 5)')
    
    # Parse arguments
    args = parser.parse_args()

    conversation_data = generate_conversation(args.topic, args.turns)
    images_list = draw_conversation(conversation_data)
    video_destination = create_video(images_list)

if __name__ == "__main__":
    # Use PORT environment variable for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
