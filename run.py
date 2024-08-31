from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env

import os
print("MONGO_URI from env:", os.environ.get('MONGO_URI'))

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5001)