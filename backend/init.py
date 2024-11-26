import os
from image_gen import verify_assets
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from routes.auth import auth_routes
from routes.generate import generate_routes
from routes.setter import set_routes

from routes.generate import generate_image

def create_app(config_name='default'):
    app = Flask(__name__)

    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "https://porygon-video-generation.web.app", "https://tiktok.oligarchventures.com/*"],  
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    try:
        verify_assets()
        print("✅ All required assets verified")
    except Exception as e:
        print(f"❌ Asset verification failed: {str(e)}")

    return app

app = create_app()
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(generate_routes, url_prefix='/generate')
app.register_blueprint(set_routes, url_prefix='/set')

def main():
    # Test parameters for image generation
    test_params = {
        "prompt": "a cute Porygon pokemon",
        "negative_prompt": "ugly, blurry",
        "num_inference_steps": 30,
        "guidance_scale": 7.5
    }
    
    # Generate the image
    result = generate_image(test_params)
    print("Image generated successfully!")
    print(f"Image saved at: {result['image_path']}")

if __name__ == "__main__":
    # Use PORT environment variable for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=True, threaded=False)
