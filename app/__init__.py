from flask import Flask, session
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure session management
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = app.config.get('SECRET_KEY', 'default_secret_key')  
    Session(app)

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Create tables and register blueprints
    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)
        db.create_all()

    return app
