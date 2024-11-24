import os
from image_gen import verify_assets
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from routes.auth import auth_routes
from routes.generate import generate_routes
from routes.set import set_routes

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
    pass

if __name__ == "__main__":
    # Use PORT environment variable for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=True)
