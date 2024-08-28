from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from app.models import init_db
from app.views import main_blueprint

# Initialize Flask extensions
mongo = PyMongo()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Corrected dynamic configuration loading
    config_class = {
        'default': 'config.DevelopmentConfig',
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig'
    }.get(config_name.lower(), 'config.DevelopmentConfig')

    app.config.from_object(config_class)
    
    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)

    # Initialize the database (create collections, indexes, etc.)
    with app.app_context():
        init_db(mongo)
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    
<<<<<<< HEAD
    return app
=======
    return app

>>>>>>> upstream/main
