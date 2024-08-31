from dotenv import load_dotenv
from app import create_app
import os

load_dotenv()  # This loads the variables from .env
print("MONGO_URI from env:", os.environ.get('MONGO_URI'))
print("All environment variables:", os.environ)
app = create_app()

if __name__ == '__main__':
    app.run(port=5001)