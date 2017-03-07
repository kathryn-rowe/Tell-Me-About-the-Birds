"""Bird abundance by observation."""

from jinja2 import StrictUndefined

from flask import (Flask,
                   render_template,
                   request, session,
                   jsonify,
                   g)

from flask_debugtoolbar import DebugToolbarExtension

from model import (Species,
                   SamplingEvent,
                   Observation,
                   MonthlyAvg,
                   connect_to_db,
                   db)

import secret_key

from geojson import (Feature,
                     Point,
                     FeatureCollection)

# from datetime import datetime

app = Flask(__name__)

JS_TESTING_MODE = False

app.secret_key = secret_key.flask_secret_key
mapbox_api_key = secret_key.mapbox_api_key

# If you use an undefined variable in Jinja2, it raises an error.
app.jinja_env.undefined = StrictUndefined

county_location = {"Humboldt": [(-123.86, 40.74), 9],
                   "Monterey": [(-122.00, 36.6), 10],
                   "San Francisco": [(-122.44, 37.76), 11],
                   "Yuba": [(-121.40, 39.28), 10]}
                   # "Alameda": [(-122.884, 37.59), 9],
                   # "Alpine": [(-119.80, 38.59), 9],
                   # "Amador": [(-120.65, 38.44), 9],
                   # "Butte": [(-121.56, 39.64), 9],
                   # "Calaveras": [(-120.58, 38.16), 9],
                   # "Colusa": [(-122.26, 39.18), 9],
                   # "Contra Costa": [(-121.93, 37.93), 9],
                   # "Del Norte": [(-123.90, 41.69), 9],
                   # "El Dorado": [(-120.51, 38.76), 9],
                   # "Fresno": [(-119.83, 36.66), 9],
                   # "Glenn": [(-122.43, 39.59), 9],
                   # "Imperial": [(-115.41, 33.03), 9],
                   # "Inyo": [(-117.41, 36.58), 9],
                   # "Kern": [(-118.66, 35.29), 9],
                   # "Kings": [(-119.83, 36.03), 9],
                   # "Lake": [(-122.78, 39.09), 9],
                   # "Lassen": [(-120.58, 40.66), 9],
                   # "Los Angeles": [(-118.20, 34.36), 9],
                   # "Madera": [(-119.83, 37.16), 9],
                   # "Marin": [(-122.73, 38.06), 11],
                   # "Mariposa": [(-119.90, 37.54), 9],
                   # "Mendocino": [(-123.41, 39.41), 9],
                   # "Merced": [(-120.75, 37.16), 9],
                   # "Modoc": [(-120.73, 41.56), 9],
                   # "Mono": [(-118.86, 37.91), 9],
                   # "Napa": [(-122.33, 38.48), 9],
                   # "Nevada": [(-120.88, 39.34), 9],
                   # "Orange": [(-117.76, 33.70), 9],
                   # "Placer": [(-120.76, 39.06), 9],
                   # "Plumas": [(-120.86, 39.98), 9],
                   # "Riverside": [(-116.05, 33.73), 9],
                   # "Sacramento": [(-121.31, 38.46), 9],
                   # "San Benito": [(-121.08, 36.61), 9],
                   # "San Bernardino": [(-116.16, 34.66), 9],
                   # "San Diego": [(-116.80, 33.03), 9],
                   # "San Joaquin": [(-121.30, 37.93), 9],
                   # "San Luis Obispo": [(-120.53, 35.36), 9],
                   # "San Mateo": [(-122.35, 37.44), 9],
                   # "Santa Barbara": [(-120.03, 34.73), 9],
                   # "Santa Clara": [(-121.76, 37.23), 9],
                   # "Santa Cruz": [(-122.05, 37.06), 9],
                   # "Shasta": [(-122.03, 40.76), 9],
                   # "Sierra": [(-120.55, 39.58), 9],
                   # "Siskiyou": [(-122.51, 41.58), 9],
                   # "Solano": [(-121.95, 38.23), 9],
                   # "Sonoma": [(-122.90, 38.55), 9],
                   # "Stanislaus": [(-121.00, 37.54), 9],
                   # "Sutter": [(-121.70, 39.01), 9],
                   # "Tehama": [(-122.30, 40.13), 9],
                   # "Trinity": [(-123.16, 40.58), 9],
                   # "Tulare": [(-118.80, 36.26), 9],
                   # "Tuolumne": [(-119.90, 38.06), 9],
                   # "Ventura": [(-119.01, 34.46), 9],
                   # "Yolo": [(-121.88, 38.69), 9],


@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


@app.route('/')
def index():
    """Homepage, choose a county and species"""

    counties = []
    for county in county_location:
        counties.append(county)

    return render_template("homepage.html",
                           counties=counties)


@app.route('/get_species.json')
def get_species():

    county = request.args.get("county")

    session["county_name"] = county

    birds_in_county = db.session.query(MonthlyAvg).filter(MonthlyAvg.county == county).all()

    species_list = []
    for bird in birds_in_county:
        species_list.append(bird.common_name)

    return jsonify(species_list)


@app.route('/show_species')
def show_species():

    bird_name = request.args.get("bird")
    # print bird_name
    # print "*****************************"
    session["bird_name"] = bird_name

    return jsonify(bird_name)


def get_county(county_name):
    """ Return longitude and latitude of chosen county. Value used to center map.

    >>> get_county("Humboldt")
    (-123.86, 40.74)

    >>> get_county("Santa Monica")
    """
    return county_location[county_name][0]


def get_zoom(county_name):
    """Return zoom level for chosen county"""

    return county_location[county_name][1]

# @app.route("/filter_geojson", methods=['POST'])
# def filter_geojson():

#     data = request.get_json()

#     data_list = data['data']

#     # for data in data_list:
#     #     print data

#     bird_data = []

#     bird_data.append(data_list)
#     # print bird_data

#     birdDataMonth = FeatureCollection(bird_data)
#     # print bird_data_month

#     bird_json = {
#         'birdDataMonth': birdDataMonth
#     }

#     # return "string"
#     return jsonify(bird_json)


def create_geojson(sampling_points):
    """Create a geojson object for input list from in the choosen county"""

    lat_long_features = []

    # for each location object, use the data to populate a feature
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


@app.route("/render_map")
def render_map():
    """Receives user's choice of county and returns map with locations of eBird checklist submissions."""

    county_name = session["county_name"]
    bird_name = session["bird_name"]
    print bird_name

    # query for the taxonmic number of the chosen species
    bird_info = db.session.query(Species).filter_by(common_name=bird_name).first()
    bird_number = bird_info.taxonomic_num
    session["bird_num"] = bird_number

    counties = []
    for county in county_location:
        counties.append(county)

    return render_template("map.html",
                           county_name=county_name,
                           bird_name=bird_name,
                           counties=counties)


@app.route("/get_data.json")
def get_data():
    """ Return bird species, totals, location to map """

    county_name = session["county_name"]
    bird_name = session["bird_name"]
    bird_number = session["bird_num"]

    zoomLevel = get_zoom(county_name)
    session["zoom_level"] = zoomLevel

    # CENTER map; get_county returns long, lat tuple.
    long_lat = get_county(county_name)
    longitude, latitude = long_lat

    # find bird totals, location, species based on the chosen county
    bird_county = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(SamplingEvent.county == county_name,
                                                                                          Observation.taxonomic_num == bird_number).all()

    # Long, lat for each checklist
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

    # Geojson of birding locations generated from eBird database
    birding_locations = create_geojson(sampling_points)

    # send all this information to website using json
    bird_data = {
        "longitude": longitude,
        "latitude": latitude,
        "mapbox_api_key": mapbox_api_key,
        "birding_locations": birding_locations,
        "bird_name": bird_name,
        "county_name": county_name,
        "zoomLevel": zoomLevel}

    return jsonify(bird_data)


def create_geoFeature(bird_name, county_name):
    # query for the taxonmic number of the chosen species
    bird_info = db.session.query(Species).filter_by(common_name=bird_name).first()
    bird_number = bird_info.taxonomic_num
    session["bird_num"] = bird_number

    # find bird totals, location, species based on the chosen county
    bird_county = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(SamplingEvent.county == county_name,
                                                                                          Observation.taxonomic_num == bird_number).all()

    # Long, lat for each checklist
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

    # Geojson of birding locations generated from eBird database
    birding_locations = create_geojson(sampling_points)

    return birding_locations


@app.route("/reload_data.json")
def reload_data():
    """ Return bird species, totals, location to map """

    bird_name = request.args.get("bird")
    session["bird_name"] = bird_name
    county_name = session["county_name"]

    birding_locations = create_geoFeature(bird_name, county_name)

    # send all this information to website using json
    bird_data = {
        "mapbox_api_key": mapbox_api_key,
        "birding_locations": birding_locations,
        "bird_name": bird_name,
        "county_name": county_name}

    return jsonify(bird_data)


@app.route("/reload_county.json")
def reload_county():
    """ Return bird species, totals, location to map """

    # receive data from drop-down menu ajax request
    bird = request.args.get("bird")
    county = request.args.get("county")
    print bird
    print "***************************"
    # get  the zoom level of the new chosen county
    zoomLevel = get_zoom(county)

    # reset session data from the ajax request
    session["bird_name"] = bird
    session["county_name"] = county
    session["zoom_level"] = zoomLevel

    # CENTER map; get_county returns long, lat tuple.
    long_lat = get_county(county)
    longitude, latitude = long_lat

    birding_locations = create_geoFeature(bird, county)

    # send all this information to website using json
    bird_data = {
        "longitude": longitude,
        "latitude": latitude,
        "mapbox_api_key": mapbox_api_key,
        "birding_locations": birding_locations,
        "bird": bird,
        "county": county,
        "zoomLevel": zoomLevel}

    return jsonify(bird_data)


@app.route('/birds_per_month.json')
def bird_per_month_data():
    """Return how many total per species seen each month for D3 graph."""

    county_name = session["county_name"]

    bird_monthly_avgs = []
    # GOAL: [{id:"Robin",
            # "values": [{"month": "Jan", "total": 600}], [{"month": "Feb", "total": 40}]},
            # {id:"Jay",
            # "values": [{"month": "Jan", "total": 600}], [{"month": "Feb", "total": 40}]}
            # ]

    # Monthly totals are stored in MonthlyAvg table in database.
    monthly_avgs = db.session.query(MonthlyAvg).filter(MonthlyAvg.county == county_name, MonthlyAvg.augAvg < 900000, MonthlyAvg.janAvg < 80000).all()
    for avg in monthly_avgs:
        birds_in_graph = {}
        birds_in_graph["id"] = avg.common_name
        birds_in_graph["latin"] = avg.taxonomic_num
        birds_in_graph["values"] = []
        months = {1: avg.janAvg,
                  2: avg.febAvg,
                  3: avg.marAvg,
                  4: avg.aprilAvg,
                  5: avg.mayAvg,
                  6: avg.juneAvg,
                  7: avg.julyAvg,
                  8: avg.augAvg,
                  9: avg.septAvg,
                  10: avg.octAvg,
                  11: avg.novAvg,
                  12: avg.decAvg}
        for month in months:
            values = {}
            values["month"] = month
            values["total"] = months[month]
            birds_in_graph["values"].append(values)
        bird_monthly_avgs.append(birds_in_graph)

    return jsonify(bird_monthly_avgs)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True

    app.run(host='0.0.0.0')
