from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from .config import Config
from .models import db

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Handle PostgreSQL URL format for Render
    if app.config['SQLALCHEMY_DATABASE_URI'] and \
       app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            "postgres://", "postgresql://", 1
        )

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Configure CORS
    CORS(
        app,
        resources={r"/*": {"origins": app.config['CORS_ORIGINS']}},
        supports_credentials=True
    )
    
    # Configure sessions
    Session(app)

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app