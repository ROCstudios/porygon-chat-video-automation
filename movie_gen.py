import os
from moviepy.editor import ImageSequenceClip, AudioFileClip

def create_video(folder_name):
    # Directory where images are stored
    output_video = f"{folder_name}/chat_conversation.mp4"

    # Get files
    audio_file = "trend.mp3"
    image_files = sorted([os.path.join(folder_name, img) for img in os.listdir(folder_name) if img.endswith(".png")])

    # Define video parameters
    # Frames per second; adjust based on how fast you want the conversation to flow
    fps = 1  
    duration = len(image_files) / fps

    # Create the video clip
    clip = ImageSequenceClip(image_files, fps=fps)
    audio = AudioFileClip(audio_file)
    clip = clip.set_audio(audio)
    clip = clip.set_duration(duration)

    # Save the video
    clip.write_videofile(output_video, codec="libx264")
    return output_video
