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

    county_name = session["county_name"]
    bird_name = session["bird_name"]

    # query for the taxonmic number of the chosen species
    bird_info = db.session.query(Species).filter_by(common_name=bird_name).first()
    bird_number = bird_info.taxonomic_num
    session["bird_num"] = bird_number

    # print county_name
    # print bird_name
    # print "*****************************"
    return render_template("map.html",
                           county_name=county_name,
                           bird_name=bird_name)


@app.route("/get_data.json")
def get_data():
    """ Return bird species, totals, location to map """

    county_name = session["county_name"]
    bird_name = session["bird_name"]
    bird_number = session["bird_num"]
    print county_name
    print bird_name
    print "*****************************"

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
        "county_name": county_name}

    return jsonify(bird_data)



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

    bird_monthly_avgs = []
    # GOAL: [{id:"Robin",
            # "values": [{"month": "Jan", "total": 600}], [{"month": "Feb", "total": 40}]},
            # {id:"Jay",
            # "values": [{"month": "Jan", "total": 600}], [{"month": "Feb", "total": 40}]}
            # ]

    monthly_avgs = db.session.query(MonthlyAvg).filter(MonthlyAvg.county == county_name, MonthlyAvg.augAvg < 900000, MonthlyAvg.janAvg < 80000).all()
    for avg in monthly_avgs:
        birds_in_graph = {}
        birds_in_graph["id"] = avg.common_name
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
    DebugToolbarExtension(app)

    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True

    app.run(host='0.0.0.0')
