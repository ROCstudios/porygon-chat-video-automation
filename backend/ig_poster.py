import requests
import os

def upload_to_instagram(video_path, caption):
    print(f"📧 UPLOAD TO INSTAGRAM: Uploading video to Instagram with caption: {caption}")

    access_token = os.getenv('INSTAGRAM_TOKEN')
    
    # Get Instagram Business Account ID
    account_url = f"https://graph.facebook.com/v18.0/me/accounts?access_token={access_token}"
    account_response = requests.get(account_url, timeout=10)
    instagram_account_id = account_response.json()['data'][0]['id']
    
    # Step 1: Create container
    container_url = f"https://graph.facebook.com/v18.0/{instagram_account_id}/media"
    container_params = {
        'media_type': 'REELS',
        'video_url': video_path,
        'caption': caption,
        'access_token': access_token
    }
    
    container_response = requests.post(container_url, data=container_params, timeout=10)
    creation_id = container_response.json()['id']

    print(f"📧 UPLOAD TO INSTAGRAM: Creation ID: {creation_id}")
    
    # Step 2: Publish the container
    publish_url = f"https://graph.facebook.com/v18.0/{instagram_account_id}/media_publish"
    publish_params = {
        'creation_id': creation_id,
        'access_token': access_token
    }
    
    publish_response = requests.post(publish_url, data=publish_params, timeout=10)
    
    # Return the URL of the posted content
    post_id = publish_response.json()['id']
    print(f"📧 UPLOAD TO INSTAGRAM: Post ID: {post_id}")
    
    return f"https://www.instagram.com/p/{post_id}"
