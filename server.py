"""Bird abundance by observation."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Species, SamplingEvent, Observation, connect_to_db, db
import secret_key

from geojson import Feature, Point, FeatureCollection

app = Flask(__name__)

# Change this!
app.secret_key = secret_key.flask_secret_key
mapbox_api_key = secret_key.mapbox_api_key

# If you use an undefined variable in Jinja2, it raises an error.
app.jinja_env.undefined = StrictUndefined

county_location = {"Humboldt": (-123.86, 40.74),
                   "Yuba": (-121.40, 39.28),
                   "San Francisco": (-122.44, 37.76),
                   "Monterey": (-121.89, 36.6)}


@app.route('/')
def index():
    """Homepage, choose a county."""

    counties = []
    for county in county_location:
        counties.append(county)

    return render_template("homepage.html",
                           counties=counties)


def get_county(county_name):
    """ Return longitude and latitude of chosen county. Value used to center map """

    for county in county_location:
        if county == county_name:
            return county_location[county]


def create_geojson(sampling_points):
    """Create a geojson object for input list from in the choosen county"""

    lat_long_features = []

    for location in sampling_points:
        point = Point([location['long'], location['lat']])
        feature = Feature(geometry=point, properties={})
        lat_long_features.append(feature)

    # Geojson FeatureCollection object
    birding_locations = FeatureCollection(lat_long_features)

    return birding_locations


@app.route("/render_map")
def render_map():
    """Receives user's choice of county and returns map with locations of eBird checklist submissions."""

    county_name = request.args.get("location")
    # print "*********" + county_name

    # CENTER map; get_county returns long, lat tuple.
    long_lat = get_county(county_name)
    longitude, latitude = long_lat

    # get long, lat, date information associated with the chosen county
    county_info = db.session.query(SamplingEvent).filter_by(county=county_name).all()

    # Long, lat for each checklist
    sampling_points = []

    # Generate sampling_points list from database
    for location in county_info:
        location_dict = {}
        location_dict["long"] = location.longitude
        location_dict["lat"] = location.latitude
        sampling_points.append(location_dict)

    # Geojson of birding locations generated from eBird database
    birding_locations = create_geojson(sampling_points)

    return render_template("mapbox_example.html",
                           longitude=longitude,
                           latitude=latitude,
                           mapbox_api_key=mapbox_api_key,
                           birding_locations=birding_locations)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
