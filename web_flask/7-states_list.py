#!/usr/bin/python3
"""Starts a flask application, and defines a single route.

Listening on host 0.0.0.0, port 5000.
Routes:
    /states_list: displays a HTML page with all states listed
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """A route for viewing the current states in the database"""
    from models.state import State
    states = storage.all(State)
    state_map = []
    for k, state in states.items():
        value = {}
        value["id"] = state.id
        value["name"] = state.name
        state_map.append(value)
    return render_template("7-states_list.html", states=state_map)


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
