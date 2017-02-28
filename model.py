"""Models and database functions for Kate's project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


##############################################################################
# Model definitions

class Species(db.Model):
    """Species of birds."""

    __tablename__ = "species"

    taxonomic_num = db.Column(db.Float, primary_key=True)
    # category = db.Column(db.String(50), nullable=False)
    common_name = db.Column(db.String(300), nullable=False)
    scientific_name = db.Column(db.String(300), nullable=False)

    def __repr__(self):

        return "<Common name=%s Taxanomic number=%s>" % (self.common_name,
                                                         self.taxonomic_num)


class SamplingEvent(db.Model):
    """Checklist of bird observation."""

    __tablename__ = "sampling_event"

    # sampling_event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    checklist = db.Column(db.String(100), primary_key=True, nullable=False)

    # Location of event
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    county = db.Column(db.String(50), nullable=False)

    # Date of sampling event
    observation_date = db.Column(db.DateTime, nullable=False)

    # Type of observation: (1) reporting all species or (2) only reporting a selection of species
    # Helps detection probabilities, and given a large enough sample serves as a surrogate for
    # absence data. (1 = yes; 0 = no).
    all_species = db.Column(db.Integer, nullable=False)

    def __repr__(self):

        return "<Checklist ID=%s County=%s>" % (self.checklist,
                                                self.county)


class Observation(db.Model):
    """Bird sighting observation."""

    __tablename__ = "observation"

    global_id = db.Column(db.String(300), primary_key=True)
    # sampling_event_id = db.Column(db.Integer, db.ForeignKey('sampling_event.sampling_event_id'), nullable=False)
    checklist = db.Column(db.String(100), db.ForeignKey('sampling_event.checklist'), nullable=False)

    # Which species and how many.
    taxonomic_num = db.Column(db.Float, db.ForeignKey('species.taxonomic_num'), nullable=False)
    observation_count = db.Column(db.String(20), nullable=False)

    # Create relationships with other tables
    species = db.relationship("Species")
    sampling_event = db.relationship("SamplingEvent")

    def __repr__(self):

        return "<Global id=%s Species ID=%s Observation count=%s>" % (self.global_id,
                                                                      self.taxonomic_num,
                                                                      self.observation_count)


class MonthlyAvg(db.Model):
    """Montly observations per month per species"""

    __tablename__ = "monthly_avg"

    sum_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    common_name = db.Column(db.String(300))
    taxonomic_num = db.Column(db.Float, db.ForeignKey('species.taxonomic_num'), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    janAvg = db.Column(db.Integer, nullable=False)
    febAvg = db.Column(db.Integer, nullable=False)
    marAvg = db.Column(db.Integer, nullable=False)
    aprilAvg = db.Column(db.Integer, nullable=False)
    mayAvg = db.Column(db.Integer, nullable=False)
    juneAvg = db.Column(db.Integer, nullable=False)
    julyAvg = db.Column(db.Integer, nullable=False)
    augAvg = db.Column(db.Integer, nullable=False)
    septAvg = db.Column(db.Integer, nullable=False)
    octAvg = db.Column(db.Integer, nullable=False)
    novAvg = db.Column(db.Integer, nullable=False)
    decAvg = db.Column(db.Integer, nullable=False)

    species_rel = db.relationship("Species")
    # sampling_rel = db.relationship("SamplingEvent")

    def __repr__(self):

        return "<Taxanomic Num=%s Species=%s County=%s>" % (self.taxonomic_num,
                                                            self.common_name,
                                                            self.county)


def example_data():
    """Create example data for the test database."""

    # bird1 = Species(taxonomic_num=27938, common_name="Yellow-rumped Warbler", scientific_name="Setophaga coronata")
    # bird2 = Species(taxonomic_num=29580, common_name="Spotted Towhee", scientific_name="Pipilo maculatus")
    bird3 = Species(taxonomic_num=29864, common_name="Song Sparrow", scientific_name="Melospiza melodia")
    # checklist1 = SamplingEvent(checklist="S17184369", latitude=36.2819875, longitude=-121.8595805, county="Monterey", observation_date=2/24/2014, all_species=1)
    # checklist2 = SamplingEvent(checklist="S17184369", latitude=36.2819875, longitude=-121.8595805, county="Monterey", observation_date=2/24/2014, all_species=1)
    checklist3 = SamplingEvent(checklist="S17184369", latitude=36.2819875, longitude=-121.8595805, county="Monterey", observation_date=datetime.strptime("2/24/2014", '%m/%d/%Y'), all_species=1)
    # obs1 = Observation(global_id="URN:CornellLabOfOrnithology:EBIRD:OBS236783548", checklist="S17184369", taxonomic_num=27938, observation_count="24")
    # obs2 = Observation(global_id="URN:CornellLabOfOrnithology:EBIRD:OBS236783543", checklist="S17184369", taxonomic_num=29580, observation_count="3")
    obs3 = Observation(global_id="URN:CornellLabOfOrnithology:EBIRD:OBS236783532", checklist="S17184369", taxonomic_num=29864, observation_count="2")

    # db.session.add_all([bird1, bird2, bird3, checklist1, checklist2, checklist3, obs1, obs2, obs3])
    db.session.add_all([bird3, checklist3, obs3])
    db.session.commit()

##############################################################################
# Helper functions


def connect_to_db(app, db_uri="postgresql:///ebird_CA_data"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ebird_data'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
