import requests
import os
import time

def get_video_size(video_path):
    return os.path.getsize(video_path)

def init_video_upload(access_token, video_path):
    chunk_size = 10000000
    video_size = get_video_size(video_path)
    print(f"🚨 TIKTOK POST: init_video_upload: {access_token}, {video_size}, {chunk_size}")

    url = 'https://open.tiktokapis.com/v2/post/publish/video/init/'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    
    # Videos under 5MB must be uploaded as one chunk
    if video_size < 5_000_000:
        chunk_size = video_size
    # Videos over 64MB must be chunked
    elif video_size > 64_000_000:
        chunk_size = 10_000_000  # Default 10MB chunks for large files
    # For videos between 5-64MB, use provided chunk size
    else:
        chunk_size = chunk_size
    total_chunks = -(-video_size // chunk_size)  # Ceiling division
    
    data = {
        "post_info": {
            "title": "this will be a funny #cat video on your @tiktok #fyp",
            "privacy_level": "SELF_ONLY", 
            "disable_duet": False,
            "disable_comment": True,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunks
        }
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=10)
    response_json = response.json()
    print(f"🚨 TIKTOK POST: resoibse fir yokiad: {response_json}")

    get_publish_id = response_json['data']['publish_id']
    get_upload_url = response_json['data']['upload_url']

    return get_publish_id, get_upload_url

def upload_video_chunk(upload_url, video_path):
    print(f"🚨 TIKTOK POST: upload_video_chunk: {upload_url}, {video_path}")

    # Get file size for Content-Range header
    file_size = os.path.getsize(video_path)
    
    headers = {
        'Content-Type': 'video/mp4',
        'Content-Range': f'bytes 0-{file_size-1}/{file_size}'
    }
    
    with open(video_path, 'rb') as video_file:
        video_data = video_file.read()
        response = requests.put(upload_url, headers=headers, data=video_data, timeout=10)
        print(f"🚨 TIKTOK POST: upload_video_chunk: {response.status_code}")
        
    return response.status_code == 200

def check_post_status(access_token, publish_id, max_attempts=30):
    print(f"🚨 TIKTOK POST: check_post_status: {access_token}, {publish_id}")

    url = 'https://open.tiktokapis.com/v2/post/publish/status/fetch/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data = {
        'publish_id': publish_id
    }

    attempts = 0
    while attempts < max_attempts:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response_json = response.json()
        
        if 'data' not in response_json:
            print("Error: Unexpected response format")
            return response_json
            
        status = response_json['data'].get('status')
        
        if status == 'FAILED':
            print(f"Upload failed. Reason: {response_json['data'].get('fail_reason')}")
            return response_json
        elif status == 'PUBLISH_COMPLETE':
            print("Upload completed successfully!")
            return response_json
        elif status in ['PROCESSING_UPLOAD', 'PROCESSING_DOWNLOAD', 'SEND_TO_USER_INBOX']:
            print(f"Status: {status}. Uploaded bytes: {response_json['data'].get('uploaded_bytes', 0)}")
            time.sleep(2)  # Wait 2 seconds before checking again
        else:
            print(f"Unknown status: {status}")
            return response_json
            
        attempts += 1
    
    print("Maximum attempts reached. Upload status check timed out.")
    return response_json['data']['status']
