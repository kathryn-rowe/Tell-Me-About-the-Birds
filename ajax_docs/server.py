"""Bird abundance by observation."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Species, SamplingEvent, Observation, connect_to_db, db
import secret_key

from geojson import Feature, Point, FeatureCollection

from datetime import datetime

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
    """Homepage, choose a county and species"""

    counties = []
    for county in county_location:
        counties.append(county)

    bird_species = db.session.query(Species).all()
    species_list = []
    for bird in bird_species:
        species_list.append(bird.common_name)

    return render_template("homepage.html",
                           counties=counties,
                           species_list=species_list)


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
        feature["properties"]["month"] = location['date']
        feature["properties"]["day"] = location['day']
        feature["properties"]["tax_num"] = location['species']
        feature["properties"]["obs_count"] = location['obs_count']
        lat_long_features.append(feature)

    # Geojson FeatureCollection object
    birding_locations = FeatureCollection(lat_long_features)

    return birding_locations


def query_species_county(county, species):
    """Query DB to get data list for specified county and bird species selected."""

    # county_info = db.session.query(SamplingEvent).filter_by(county=county_name).all()
    bird_info = db.session.query(Species).filter_by(common_name=species).first()
    bird_number = bird_info.taxonomic_num
    bird_county = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(SamplingEvent.county == county, Observation.taxonomic_num == bird_number).all()

    if bird_county == []:
        flash("There are no recording for that species in that county. Please choose another bird.")

    # Long, lat, date, day, species, and how many birds for each checklist
    sampling_points = []

    # Generate sampling_points list from database
    # for location in county_info:
    for bird_location in bird_county:
        location_dict = {}
        location_dict["long"] = bird_location[1].longitude
        location_dict["lat"] = bird_location[1].latitude
        location_dict["date"] = bird_location[1].observation_date.strftime('%B')
        location_dict["day"] = bird_location[1].observation_date.strftime('%d')
        location_dict["species"] = bird_location[0].taxonomic_num
        location_dict["obs_count"] = bird_location[0].observation_count
        sampling_points.append(location_dict)

    return sampling_points


@app.route("/get_api_key")
def get_API_key():

    return jsonify([mapbox_api_key])


@app.route("/render_map")
def render_map():
    """returns map with locations of eBird checklist submissions."""

    county_name = request.args.get("location")
    bird_name = request.args.get("bird-species")

    session["county_name"] = county_name
    session["bird_name"] = bird_name

    return render_template("map.html")


@app.route("/get_lat_long")
def get_lat_long():

    # CENTER map; get_county returns long, lat tuple.
    county_name = session["county_name"]
    long_lat = get_county(county_name)
    longitude, latitude = long_lat

    location_dict = {"longitude": longitude,
                     "latitude": latitude}

    return jsonify(location_dict)


@app.route("/get_data")
def get_data():

    bird_name = session["bird_name"]
    county_name = session["county_name"]

    #Query DB to get data list for specified county and bird species selected.
    sampling_points = query_species_county(county_name, bird_name)

    # Geojson of birding locations generated from eBird database
    birding_locations = create_geojson(sampling_points)

    data_dict = {"bird_loc": birding_locations}

    return jsonify(data_dict)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
