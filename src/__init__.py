import os
from utils import is_heroku

if is_heroku():
    from src.app import app
else:
    from app import app

import routes

if __name__ == "__main__":
    print("Running app")
    app.run()