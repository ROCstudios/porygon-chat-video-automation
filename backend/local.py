import os
from image_gen import verify_assets
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from routes.auth import auth_routes
from routes.generate import generate_routes
from routes.setter import set_routes

from image_gen import draw_conversation

def main():
    
    # Generate the image
    result = draw_conversation(
        [
            {
                "speaker": "Person 1",
                "message": "Hello, how are you?",
                "timestamp": "12:00 PM"
            },
            {
                "speaker": "Person 2",
                "message": "I'm doing great, thanks for asking!",
                "timestamp": "12:05 PM"
            },
            {
                "speaker": "Person 1",
                "message": "What's your favorite color?",
                "timestamp": "12:10 PM"
            },
            {
                "speaker": "Person 2",
                "message": "I like blue.",
                "timestamp": "12:15 PM"
            }
        ],
        "Porygon",
        "icons8-circled-user-female-skin-type-4-96.png"
    )
    print("Images generated successfully!")
    for i, img in enumerate(result):
        img.show() # This will open each image in the default image viewer
        print(f"Showing image {i+1} of {len(result)}")

if __name__ == "__main__":
    main()
