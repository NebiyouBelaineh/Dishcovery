from flask import render_template
from  dishcovery import app

@app.route("/login", strict_slashes=False)
def login_route():
    """ Print Hello HBNB! on the browser """
    return render_template('login.html')


@app.route("/register", strict_slashes=False)
def register_route():
    """ Print Hello HBNB! on the browser """
    return render_template('register.html')

@app.route("/home", strict_slashes=False)
def home_route():
    """ Print Hello HBNB! on the browser """
    return render_template('home.html')

