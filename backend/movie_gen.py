import subprocess
import numpy as np
from moviepy.editor import ImageSequenceClip
import tempfile
import os
import shutil

def save_with_temp_file(video_file, fps):
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_path = temp_file.name
        video_file.write_videofile(temp_path, fps=fps, codec='libx264')
    return temp_path

def create_video(images_list):
    print(f"🎥 CREATE VIDEO: Creating video with {len(images_list)} images")
    numpy_images = [np.array(img) for img in images_list]
    fps = 1  
    duration = len(images_list) / fps

    clip = ImageSequenceClip(numpy_images, fps=fps)
    clip = clip.set_duration(duration)
    
    temp_path = save_with_temp_file(clip, fps)
    print(f"🎥 CREATE VIDEO: Video created at {temp_path}")
    
    return temp_path


def convert_to_9_16_ratio(input_video, output_video):
    """
    Convert video to 9:16 aspect ratio (1080x1920 for Instagram)
    """
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_path = temp_file.name

        ffmpeg_path = 'ffmpeg'
        if not shutil.which('ffmpeg'):
            print("FFmpeg is not installed or not in PATH. Please install FFmpeg first.")
            ffmpeg_path = '/usr/bin/ffmpeg'
            
        command = [
            ffmpeg_path,
            '-y',
            '-i', input_video,
            '-vf', 'scale=1080:1920',
            '-c:a', 'copy',
            temp_path
        ]


        try:
            subprocess.run(command, check=True)
            # Move temp file to final output location
            os.replace(temp_path, output_video)
            print(f"Successfully converted video to 9:16 ratio: {output_video}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting video: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
