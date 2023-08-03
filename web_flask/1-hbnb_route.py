#!/usr/bin/python3
"""Starts a flask application"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb")
def main_hbnb():
    return "HBNB"


app.run("0.0.0.0", 5000)
