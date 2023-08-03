#!/usr/bin/python3
"""Starts a flask application, and defines 2 routes
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_hbnb():
    """handle requests for the root route"""
    return "Hello HBNB!"


@app.route("/hbnb")
def main_hbnb():
    """handle requests for the hbnb route"""
    return "HBNB"


app.run("0.0.0.0", 5000)
