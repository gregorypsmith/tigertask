import os

def is_heroku():
    return os.environ.get("IS_HEROKU", None)