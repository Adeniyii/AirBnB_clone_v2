#!/usr/bin/python3
"""Starts a flask application, and defines a single route.

Listening on host 0.0.0.0, port 5000.
Routes:
    /: Displays 'Hello HBNB!'
    /hbnb: Displays 'HBNB'.
    /c/<text>: Displays 'C <text>'
    /python/<text>: Displays 'Python <text>'
    /number/<n>: Displays 'Python <text>'
    /number_template/<n>: Renders an html template if n is Int
    /number_odd_or_even/<n>: Renders an html template if n Int
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """handle requests for the root route"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def main_hbnb():
    """handle requests for the hbnb route"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_hbnb(text: str):
    """handle requests for route: c with query param: text"""
    return "C {}".format(text.replace("_", " "))


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_hbnb(text="is cool"):
    """handle requests for route: python with query param: text"""
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number_hbnb(n):
    """handle requests for route: number with query param: n"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_hbnb_template(n):
    """handle requests for route: number with query param: n"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_hbnb_even_or_odd(n):
    """handle requests for route: number with query param: n"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
