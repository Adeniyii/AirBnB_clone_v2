#!/usr/bin/python3
"""Starts a flask application, and defines a single route
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """handle requests for the root route"""
    return "Hello HBNB!"


app.run("0.0.0.0", 5000)
