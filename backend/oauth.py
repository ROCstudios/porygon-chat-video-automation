import os
import requests
import secrets
import urllib
from flask import Flask, jsonify
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)


# user will call in from the client, we need to have a flask endpoint that will recquest the initial login information

# we will then send the oauth information to the client, from there the user will be directed to the redirect url

# we will take that url and extract the code in the client

# we will then send that code to our backend and we will use that code to get the access token and refresh token

# this will be stored locally for subsequent requests until an error is thrown.
