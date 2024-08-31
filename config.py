import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # MongoDB connection URI
    MONGO_URI = os.environ.get('MONGO_URI')

    # Upload folder for handling file uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    # Allowed extensions for file uploads
    ALLOWED_EXTENSIONS = {'csv'}

class DevelopmentConfig(Config):
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

class ProductionConfig(Config):
    DEBUG = False

# Dictionary to easily switch configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig if os.environ.get('FLASK_ENV') != 'production' else ProductionConfig
}