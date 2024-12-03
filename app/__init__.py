from flask import Flask
from .extensions import mongo
from .routes.admin import admin_bp
from .routes.volunteer import volunteer_bp
from .routes.event import event_bp
from .routes.task import task_bp  # Import the task blueprint
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure MONGO_URI is correctly set in app config
    app.config['MONGO_URI'] = Config.MONGO_URI

    # Initialize MongoDB with Flask app
    mongo.init_app(app)

    # Print configuration to verify
    print("MONGO_URI in app config:", app.config.get('MONGO_URI'))

    # Register blueprints for different modules
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
    app.register_blueprint(event_bp, url_prefix='/event')
    app.register_blueprint(task_bp, url_prefix='/admin')  

    return app
