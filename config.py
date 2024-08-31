import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
   # MONGO_URI = os.environ.get('MONGO_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.getenv('MONGO_URI')
    FLASK_ENV = os.getenv('FLASK_ENV')
