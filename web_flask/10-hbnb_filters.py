#!/usr/bin/python3
"""
script that starts a Flask web application
Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /hbnb_filters
"""

from flask import Flask, render_template
from models import storage
from models import *

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filter():
    """Display a HTML page like 6-index.html"""
    st = storage.all("State")
    am = storage.all("Amenity")
    return render_template("10-hbnb_filters.html", st=st, am=am)


@app.teardown_appcontext
def teardown(exception):
    """Deletes SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
