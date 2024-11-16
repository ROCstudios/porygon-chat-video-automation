import argparse
from image_gen import draw_conversation
from movie_gen import create_video
from convo_gen import generate_conversation
from ig_poster import upload_to_instagram
import os
import requests
import secrets
import urllib

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


auth_url = 'https://www.tiktok.com/v2/auth/authorize/'


def get_tiktok_auth_token(code):
    '''
    get the auth token with our endpoint redirect url.
    '''
    open_url = 'https://open.tiktokapis.com/v2/oauth/token/'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache'
    }
    
    data = {
        'client_key': os.getenv('TIKTOK_CLIENT_KEY'),
        'client_secret': os.getenv('TIKTOK_CLIENT_SECRET'), 
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': os.getenv('TIKTOK_REDIRECT_URI')
    }
    
    response = requests.post(open_url, headers=headers, data=data, timeout=10)
    return response.json()

def generate_auth_url():
    '''
    generate the auth url that we will send to the user to login with
    '''
    csrf_token = secrets.token_hex(16)
    params = {
        'client_key': os.getenv('TIKTOK_CLIENT_KEY'),
        'redirect_uri': os.getenv('TIKTOK_REDIRECT_URI'),
        'response_type': 'code',
        'scope': 'video.publish',
        'state': csrf_token
    }
    url = auth_url + '?' + urllib.parse.urlencode(params)
    return url

@app.route('/auth', methods=['GET'])
def auth():
    generated_url = generate_auth_url()
    print(generated_url)
    return jsonify({'url': generated_url})

@app.route('/token', methods=['POST'])
def get_token_from_url(full_url):
    '''
    the url we generate here is manually navigated to by the user and then the code is sent back to us by cutting from the search bar.  Not ideal.
    '''
    code = full_url.split('code=')[1].split('&')[0]

    json_response = get_tiktok_auth_token(code)
    access_token = json_response['access_token']
    refresh_token = json_response['refresh_token']
    open_id = json_response['open_id']

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'open_id': open_id})


@app.route('/generate', methods=['POST'])
def generate_video():
    # Get parameters from JSON request
    data = request.get_json()
    topic = data.get('topic')
    turns = data.get('turns', 5)
    post_to_ig = data.get('post_to_ig', False)
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        conversation_data = generate_conversation(topic, turns)
        images_list = draw_conversation(conversation_data)
        temp_video_path = create_video(images_list)

        
        if post_to_ig:
            instagram_url = upload_to_instagram(
                video_path=temp_video_path,
                caption=f"AI generated conversation about {topic}"
            )

        return_data = send_file(
            temp_video_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f'conversation_{topic}.mp4'
        )

        if post_to_ig:
            return jsonify({
                'video': return_data,
                'ig_post_url': instagram_url
            })
            
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
    app.run(debug=True, host='0.0.0.0', port=port)
