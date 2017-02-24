"""Bird abundance by observation."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request,
                   session, jsonify, g)

from flask_debugtoolbar import DebugToolbarExtension

from model import Species, SamplingEvent, Observation, connect_to_db, db
import secret_key

from geojson import Feature, Point, FeatureCollection

# from datetime import datetime

app = Flask(__name__)

JS_TESTING_MODE = False

# Change this!
app.secret_key = secret_key.flask_secret_key
mapbox_api_key = secret_key.mapbox_api_key

# If you use an undefined variable in Jinja2, it raises an error.
app.jinja_env.undefined = StrictUndefined

county_location = {"Humboldt": (-123.86, 40.74),
                   "Yuba": (-121.40, 39.28),
                   "San Francisco": (-122.44, 37.76),
                   "Monterey": (-121.89, 36.6)}


@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


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
    """ Return longitude and latitude of chosen county. Value used to center map.

    >>> get_county("Humboldt")
    (-123.86, 40.74)

    >>> get_county("Santa Monica")
    """

    for county in county_location:
        if county == county_name:
            return county_location[county]


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

    county_name = request.args.get("location")
    bird_name = request.args.get("bird-species")

    session["county_name"] = county_name
    session["bird_name"] = bird_name

    return render_template("map.html")


@app.route("/get_data.json")
def get_data():
    """ Return bird species, totals, location to map """

    county_name = session["county_name"]
    bird_name = session["bird_name"]

    # CENTER map; get_county returns long, lat tuple.
    long_lat = get_county(county_name)
    longitude, latitude = long_lat

    # query for the taxonmic number of the chosen species
    bird_info = db.session.query(Species).filter_by(common_name=bird_name).first()
    bird_number = bird_info.taxonomic_num
    session["bird_num"] = bird_number

    # find bird totals, location, species based on the chosen county
    bird_county = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(SamplingEvent.county == county_name,
                                                                                          Observation.taxonomic_num == bird_number).all()

    # not all birds are seen at each location
    # if bird_county == []:
    #     flash("There are no recording for that species in that county. Please choose another bird.")
    #     return redirect('/')

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
        "county_name": county_name}

    return jsonify(bird_data)


@app.route('/bird_per_month.json')
def bird_per_month():
    """Return how many total per species seen each month for graph."""

    county_name = session["county_name"]
    taxonomic_num = session["bird_num"]
    bird_name = session["bird_name"]
    # print bird_name + "****************************"

    # returns total amount of specified species seen per checklist, where total is not indicated by present, or 'x'
    bird_date = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(Observation.taxonomic_num == taxonomic_num,
                                                                                        Observation.observation_count != 'X',
                                                                                        SamplingEvent.county == county_name).all()

    # X-axis labels
    sum_per_month = {"July": 0, "August": 0, "September": 0, "October": 0, "November": 0, "December": 0}

    # gets total number of bird species seen per month
    for label in sum_per_month:
        for observation in bird_date:
            if observation[1].observation_date.strftime('%B') == label:
                sum_per_month[label] += int(observation[0].observation_count)

    # returned totals have to be ordered by month
    month_totals = [sum_per_month["July"],
                    sum_per_month["August"],
                    sum_per_month["September"],
                    sum_per_month["October"],
                    sum_per_month["November"],
                    sum_per_month["December"]]

    # create chart/graph showing total species per month
    data_dict = {
        "labels": ["July", "Aug", "Sept", "Oct", "Nov", "Dec"],
        "datasets": [
            {
                "label": bird_name,
                "fill": False,
                "lineTension": 0.5,
                "backgroundColor": "rgba(220,220,220,0.2)",
                "borderColor": "rgba(220,220,220,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(220,220,220,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": month_totals,
                "spanGaps": False,
                }
        ]
    }

    return jsonify(data_dict)


@app.route('/birds_per_month.json')
def bird_per_month_data():
    """Return how many total per species seen each month for graph."""

    county_name = session["county_name"]

    birds_per_county = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(SamplingEvent.county == county_name,
                                                                                               Observation.observation_count != 'X').all()

    birds_in_county = []

    for bird in birds_per_county:
        bird_num = bird[0].taxonomic_num
        if bird_num not in birds_in_county:
            birds_in_county.append(bird_num)

    birds_in_graph = []
    # GOAL: [{id:"Robin", 
            # "values": [{"month": "Jan", "total": 600}], [{"month": "Feb", "total": 40}]},
            # {id:"Jay", 
            # "values": [{"month": "Jan", "total": 600}], [{"month": "Feb", "total": 40}]}
            # ]

    months = ["July", "August", "September", "October", "November", "December"]
    for number in birds_in_county:
        bird_dict = {}
        bird_name = db.session.query(Species).filter(Species.taxonomic_num == number).first()
        bird_name = bird_name.common_name
        bird_dict["id"] = bird_name
        values = []
        for month in months:
            value_dict = {}
            value_dict["month"] = month
            value_dict["total"] = 0
            for observation in birds_per_county:
                if observation[1].observation_date.strftime('%B') == month and observation[0].taxonomic_num == number:
                    value_dict["total"] += int(observation[0].observation_count)
            values.append(value_dict)
        bird_dict["values"] = values
        birds_in_graph.append(bird_dict)

    return jsonify(birds_in_graph)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True

    app.run(host='0.0.0.0')
