import numpy as np
from moviepy.editor import ImageSequenceClip
import tempfile
import os

def create_video(images_list):
    numpy_images = [np.array(img) for img in images_list]
    fps = 1  
    duration = len(images_list) / fps

    clip = ImageSequenceClip(numpy_images, fps=fps)
    clip = clip.set_duration(duration)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_path = temp_file.name
        
    # Write to temporary file
    clip.write_videofile(temp_path, fps=fps, codec='libx264')
    clip.close()
    
    return temp_path
