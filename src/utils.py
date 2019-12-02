from os import path, environ
import xlrd

def is_heroku():
    return environ.get("IS_HEROKU", None)





