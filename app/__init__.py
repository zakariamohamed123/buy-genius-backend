from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")

    with app.app_context():
        # Register Blueprints
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Create all database tables (if needed)
        db.create_all()

    return app, socketio
