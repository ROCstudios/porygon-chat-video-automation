import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image, ImageDraw

def create_video(images_list: list[Image]):
    # Directory where images are stored
    output_video = f"chat_conversation.mp4"

    # Get files
    audio_file = "trend.mp3"
    numpy_images = [np.array(img) for img in images_list]
    # Define video parameters
    # Frames per second; adjust based on how fast you want the conversation to flow
    fps = 1  
    duration = len(images_list) / fps

    # Create the video clip
    clip = ImageSequenceClip(numpy_images, fps=fps)
    audio = AudioFileClip(audio_file)
    clip = clip.set_audio(audio)
    clip = clip.set_duration(duration)

    # Save the video
    clip.write_videofile(output_video, codec="libx264")
    return output_video
