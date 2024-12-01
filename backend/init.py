import os
from flask import Flask
from flask_cors import CORS

from routes.auth import auth_routes
from routes.generate import generate_routes
from routes.setter import set_routes
from routes.getter import getter_routes
def create_app(config_name='default'):
    app = Flask(__name__)

    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "https://automated-marketing-442414.web.app", "https://automated-marketing-442414.firebaseapp.com"],  
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type"],
        }
    })
    return app

app = create_app()
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(generate_routes, url_prefix='/generate')
app.register_blueprint(set_routes, url_prefix='/set')
app.register_blueprint(getter_routes, url_prefix='/getter')
if __name__ == "__main__":
    # Use PORT environment variable for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=True, threaded=False)
