import os
is_heroku = os.environ.get("IS_HEROKU", None)

if is_heroku:
    from src.app import app
else:
    from app import app

import routes

if __name__ == "__main__":
    print("Running app")
    app.run()