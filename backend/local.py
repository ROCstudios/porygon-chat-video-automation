import os
from image_gen import verify_assets
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from routes.auth import auth_routes
from routes.generate import generate_routes
from routes.setter import set_routes
from ai_gen import generate_image

from image_gen import draw_conversation

def local_screenshot_gen():
    
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

def local_image_gen():
    prompt = "A woman and her sister are discussing their favorite color one of them is wearing a red dress"
    result = generate_image(prompt)
    print(result)

if __name__ == "__main__":
    local_image_gen()
