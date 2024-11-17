import os
import argparse
from image_gen import draw_conversation
from movie_gen import create_video
from convo_gen import generate_conversation
from ig_poster import upload_to_instagram
from cloud_storage import upload_to_gcs
from tiktok_poster import init_video_upload, upload_video_chunk, check_post_status
from oauth import get_auth, get_token, get_refresh_token
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],  
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
load_dotenv()

@app.route('/tiktokauth', methods=['GET'])
def auth():
    generated_url = get_auth()
    return jsonify({'url': generated_url})

@app.route('/tiktoken', methods=['POST'])
def get_token_from_url(): 
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400

        access_token, refresh_token, open_id = get_token(code)

        return jsonify({
            'success': access_token is not None and refresh_token is not None and open_id is not None,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'open_id': open_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    return jsonify(get_refresh_token(refresh_token))

@app.route('/generate', methods=['POST'])
def generate_video():
    instagram_url = None
    tiktok_url = None
    cloud_video_path = None
    
    data = request.get_json()
    topic = data.get('topic')
    turns = data.get('turns', 5)
    caption = data.get('caption', f"Conversation about {topic}")
    post_to_ig = data.get('post_to_ig', False)
    post_to_tiktok = data.get('post_to_tiktok', False)
    tiktok_access_token = data.get('tiktok_access_token')
    print(f"tiktotken {tiktok_access_token}")

    # #! test code
    # post_to_ig = False
    # post_to_tiktok = False
    # tiktok_url = 'https://www.tiktok.com/@amohnjaca3y/video/7438099189084523831'
    # instagram_url = 'https://www.instagram.com/p/DCcFSiQJAFS/'
    # cloud_video_path = 'https://storage.googleapis.com/porygon-video-generation_cloudbuild/reels/20241117_115445_tmp5bap7mia.mp4'
    # #! end

    if not topic:
        return jsonify({'error': 'Information is required'}), 400
    
    try:
        conversation_data = generate_conversation(topic, turns)
        conversation_data = [{'speaker': 'Person 1', 'message': 'Do you believe in love at first sight?', 'timestamp': '11:00 AM'}, {'speaker': 'Person 2', 'message': 'Yes, I think it can happen.', 'timestamp': '11:02 AM'}, {'speaker': 'Person 1', 'message': "That's interesting. I feel the same way.", 'timestamp': '11:04 AM'}, {'speaker': 'Person 2', 'message': "It's a beautiful thing, isn't it?", 'timestamp': '11:06 AM'}, {'speaker': 'Person 1', 'message': 'Yes, it surely is.', 'timestamp': '11:08 AM'}]
        images_list = draw_conversation(conversation_data)
        temp_video_path = create_video(images_list)
        print('🚀 ~ file: init.py:77 ~ temp_video_path:', temp_video_path);
        cloud_video_path = upload_to_gcs(temp_video_path)
        print('🚀 ~ file: init.py:79 ~ cloud_video_path:', cloud_video_path);

        if post_to_ig:
            instagram_url = upload_to_instagram(cloud_video_path, caption)
            print(f"♻️ GENERATE: Instagram URL: {instagram_url}")

        if post_to_tiktok:
          publish_id, upload_url = init_video_upload(tiktok_access_token, temp_video_path)
          print('🚀 ~ file: init.py:87 ~ publish_id, upload_url:', publish_id, upload_url);
          upload_success = upload_video_chunk(upload_url, temp_video_path)
          status_response = check_post_status(tiktok_access_token, publish_id)

        response = jsonify({
            'status': 'success',
            'cloud_url': cloud_video_path,
            'ig_post_url': instagram_url,
            'tiktok_post_url': tiktok_url
        })
        return response
        
    except Exception as e:
        print('🚩 ~ file: init.py:113 ~ e:', e);
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
    
    #todo: upload to ig, include parameter to do boolean.

if __name__ == "__main__":
    # Use PORT environment variable for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=True)
