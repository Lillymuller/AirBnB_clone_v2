#!/usr/bin/python3
"""
script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
Routes:
    /states: display a HTML page: (inside the tag BODY)
    /states/<id>: display a HTML page: (inside the tag BODY)
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Displays an HTML page with a list of all States"""
    state_lst = storage.all("State")
    return render_template("9-states.html", state_lst=state_lst)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Displays an HTML page state with ids"""
    store = storage.all("State").values()
    for state in store:
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exception):
    """Remove SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
