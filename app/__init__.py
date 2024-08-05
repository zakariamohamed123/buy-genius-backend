from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        db.create_all()

    return app
