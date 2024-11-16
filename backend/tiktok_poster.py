import os
import requests

def get_video_size(video_path):
    return os.path.getsize(video_path)

def init_video_upload(access_token, video_size, chunk_size=10000000):
    url = 'https://open.tiktokapis.com/v2/post/publish/video/init/'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    
    total_chunks = -(-video_size // chunk_size)  # Ceiling division
    
    data = {
        "post_info": {
            "title": "this will be a funny #cat video on your @tiktok #fyp",
            "privacy_level": "MUTUAL_FOLLOW_FRIENDS", 
            "disable_duet": False,
            "disable_comment": True,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_size": video_size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunks
        }
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=10)
    return response.json()

def upload_video(access_token, video_path):
  response_json = init_video_upload(access_token, get_video_size(video_path))
  get_publish_id = response_json['publish_id']
  return get_publish_id
