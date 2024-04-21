#!/usr/bin/python3
"""
script that starts a Flask web application
Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /hbnb
"""
from flask import Flask, render_template
from models import storage
from models import *

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def route_hbnb():
    """Displays the HTML page"""
    st = storage.all("State").value()
    am = storage.all("Amenity").value()
    pl = storage.all("Place").value()
    us = storage.all("User").value()
    return render_template("100-hbnb.html", st=st, am=am, pl=pl, us=us)


@app.teardown_appcontext
def teardown(exception):
    """Deletes the SQLAlchemy session"""
    storage.close()


if __name__ == ('__main__'):
    app.run(host='0.0.0.0', port='5000')
