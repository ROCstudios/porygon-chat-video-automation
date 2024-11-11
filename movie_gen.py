import numpy as np
from moviepy.editor import ImageSequenceClip

def create_video(images_list):
    numpy_images = [np.array(img) for img in images_list]
    # Define video parameters
    # Frames per second; adjust based on how fast you want the conversation to flow
    fps = 1  
    duration = len(images_list) / fps

    # Create the video clip
    clip = ImageSequenceClip(numpy_images, fps=fps)
    clip = clip.set_duration(duration)

    return clip
