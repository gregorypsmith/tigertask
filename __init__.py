import os

is_heroku = os.environ.get("IS_HEROKU", None)

from app import app
import routes

if __name__ == "__main__":
    if is_heroku:
        app.run(debug=False)
    else: 
        app.run(debug=True)