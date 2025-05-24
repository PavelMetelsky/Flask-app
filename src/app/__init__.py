from flask import Flask
from flasgger import Swagger

from app.extensions import redis_client
from app.config import Config
from app.api.routes import api_bp
from app.auth.routes import auth_bp

def create_app(config_class=Config):
    """Create and configure a Flask application instance"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    redis_client.init_app(app)
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    Swagger(app, config=swagger_config)
    
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    
    return app
