

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/homecustomer")
def homecustomer():
    return render_template('homecustomer.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
