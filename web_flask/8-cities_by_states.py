#!/usr/bin/python3
"""
script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
Routes:
    /cities_by_states
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route("/cities_by_states",  strict_slashes=False)
def cities_states():
    """Displays an HTML page with list of all State in DBStorage"""
    slist = storage.all("State").values()
    return render_template("8-cities_by_states.html", slist=slist)


@app.teardown_appcontext
def teardown(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
