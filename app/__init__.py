# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        db.create_all()

    return app
