

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

is_heroku = os.environ.get("IS-HEROKU", None)

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
