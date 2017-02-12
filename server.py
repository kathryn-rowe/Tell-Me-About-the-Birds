"""Bird abundance by observation."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Species, SamplingEvent, Observation, connect_to_db, db


app = Flask(__name__)

# Change this!
app.secret_key = "ABC"

# If you use an undefined variable in Jinja2, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    location = ["Humboldt", "San Francisco", "Yuba"]

    return render_template("homepage.html", location=location)


@app.route("/render_map")
def render_map():

    county_name = request.args.get("location")
    print "*********" + county_name

    if county_name == "Yuba":
        longitude = -121.40
        latitude = 39.28

    if county_name == "Humboldt":
        longitude = -123.86
        latitude = 40.74

    if county_name == "San Francisco":
        longitude = -122.44
        latitude = 37.76

    return render_template("mapbox_example.html", longitude=longitude, latitude=latitude)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
