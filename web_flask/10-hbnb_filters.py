#!/usr/bin/python3
"""Starts a flask application, and defines 3 routes.

Listening on host 0.0.0.0, port 5000.
Routes:
    /states<id>: displayes all cities in a state
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays the main HBNB filters HTML page."""
    from models.state import State
    from models.amenity import Amenity
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


@app.teardown_appcontext
def cleanup(f):
    """cleanup session objects after a request is completed"""
    try:
        storage.close()
    except Exception as err:
        print("err: ", err)

    return f


if __name__ == "__main__":
    app.run("0.0.0.0")
