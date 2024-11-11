import openai
import json
from datetime import datetime, timedelta
import os
from PIL import Image, ImageDraw
import textwrap
import os
import moviepy.editor as mp
from moviepy.editor import ImageSequenceClip, AudioFileClip
import gspread
from google.oauth2.service_account import Credentials

from image_gen import draw_conversation
from movie_gen import create_video


sheet_url = 'https://docs.google.com/spreadsheets/d/10Z9U6qeP_fSlf8I0q4ZFyxqd-RgUo36KwEjdMSDZ7Qw/edit?usp=sharing'
sheet_name = 'Sheet1'

# Google Sheets authentication setup
def get_google_sheet(sheet_url, sheet_name):
    # Set up the required scopes for Google Sheets API
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        'porygon-video-generation-77fa8b367ac4.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    return worksheet

def main():
    conversation_data = generate_conversation(topic, num_turns=5)
    image_folder = draw_conversation(conversation_data)
    video_destination = create_video(image_folder)

if __name__ == "__main__":
    main()
