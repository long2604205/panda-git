from flask import Flask
from app.api.v1 import v1_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # CORS(app, resources={
    #     r"/api/*": {
    #         "origins": ["http://localhost:5173"],
    #         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    #         "allow_headers": ["Content-Type", "Authorization"]
    #     }
    # })
    CORS(app)
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')
    return app
