#!/usr/bin/python3
"""Starts a flask application, and defines 3 routes.

Listening on host 0.0.0.0, port 5000.
Routes:
    /states_list: displays a HTML page with all states listed
    /cities_by_states: displays a HTML page with all states and cities listed
    /states: displayes all cities in a state
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
    for _, state in states.items():
        value = {}
        value["id"] = state.id
        value["name"] = state.name
        state_map.append(value)
    return render_template("7-states_list.html", states=state_map)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """A route for viewing the current states and cities in the database"""
    from models.state import State
    states = storage.all(State)
    state_map = []
    for _, state in states.items():
        value = {}
        value["id"] = state.id
        value["name"] = state.name
        value["cities"] = state.cities
        state_map.append(value)
    return render_template("8-cities_by_states.html", states=state_map)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    """A route for viewing the current states and cities in the database"""
    from models.state import State
    if id:
        for state in storage.all(State).values():
            if state.id == id:
                return render_template("9-states.html", state=state)
        return render_template("9-states.html")
    else:
        states = storage.all(State)
        return render_template("9-states.html", state=states)


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
