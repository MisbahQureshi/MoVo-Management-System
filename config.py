import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # MongoDB connection URI
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://mongodbuser:AlphaBetaGamma1101@cluster0.v9psk.mongodb.net/movodb?retryWrites=true&w=majority'

    # Upload folder for handling file uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    # Allowed extensions for file uploads
    ALLOWED_EXTENSIONS = {'xlsx'}

    # Flask settings
    DEBUG = os.environ.get('FLASK_DEBUG') or False

    # Other configurations (e.g., for mail, logging, etc.) can be added here

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb+srv://mongodbuser:AlphaBetaGamma1101@cluster0.v9psk.mongodb.net/movodb?retryWrites=true&w=majority'

class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://mongodbuser:AlphaBetaGamma1101@cluster0.v9psk.mongodb.net/movodb?retryWrites=true&w=majority'

# Dictionary to easily switch configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}