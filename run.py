import os

is_heroku = os.environ.get("IS_HEROKU", None)

from app import app

if __name__ == "__main__":
    app.run(debug=True)

import routes