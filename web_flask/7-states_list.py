#!/usr/bin/python3
"""
script that starts a Flask web application
Your web application must be listening on 0.0.0.0, port 5000
must remove the current SQLAlchemy Session:
    Declare a method to handle @app.teardown_appcontext
    Call in this method storage.close()
Route:
    /states_list
"""

from flask import Flask, render_template
from models import storage
from models import *

app = Flask(__name__)


@app.route("/states_list",  strict_slashes=False)
def states_cities():
    """Displays an HTML page with list of all State in DBStorage"""
    state_list = storage.all("State").values()
    return render_template("7-states_list.html", state_list=state_list)


@app.teardown_appcontext
def teardown(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
