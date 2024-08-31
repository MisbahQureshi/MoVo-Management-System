from dotenv import load_dotenv
from app import create_app
import os

load_dotenv()  # This loads the variables from .env
app = create_app()

print("MONGO_URI from env:", os.getenv('MONGO_URI'))
print("SECRET_KEY from env:", os.getenv('SECRET_KEY'))
print("FLASK_ENV from env:", os.getenv('FLASK_ENV'))



if __name__ == '__main__':
    app.run(port=5001)

#print("MONGO_URI from env:", os.environ.get('MONGO_URI'))
#print("\nAll environment variables:", os.environ)