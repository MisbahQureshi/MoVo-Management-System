from flask import Flask
from .extensions import mongo
from .routes.admin import admin_bp
from .routes.volunteer import volunteer_bp
from .routes.event import event_bp
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB with Flask app
    mongo.init_app(app)

    # Register blueprints for different modules
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
    app.register_blueprint(event_bp, url_prefix='/event')

    return app
