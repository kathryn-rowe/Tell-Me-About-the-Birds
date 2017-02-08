"""Models and database functions for Kate's project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class Species(db.Model):
    """Species of birds."""

    __tablename__ = "species"

    species_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    taxonomic_num = db.Column(db.Float)
    # category = db.Column(db.String(50), nullable=False)
    common_name = db.Column(db.String(500), nullable=False)
    scientific_name = db.Column(db.String(500), nullable=False)

    def __repr__(self):

        return "<Common name=%s Taxanomic number=%s>" % (self.common_name,
                                                         self.taxonomic_num)


class SamplingEvent(db.Model):
    """Checklist of bird observation."""

    __tablename__ = "sampling_event"

    sampling_event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    checklist = db.Column(db.String(100), nullable=False)

    # Location of event
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    county = db.Column(db.String(50), nullable=False)

    # Date of sampling event
    observation_date = db.Column(db.DateTime)

    # Type of observation: (1) reporting all species or (2) only reporting a selection of species
    # Helps detection probabilities, and given a large enough sample serves as a surrogate for
    # absence data. (1 = yes; 0 = no).
    all_species = db.Column(db.Integer, nullable=False)

    def __repr__(self):

        return "<Checklist ID=%s County=%s>" % (self.checklist,
                                                self.count)


class Observation(db.Model):
    """Bird sighting observation."""

    __tablename__ = "observation"

    global_id = db.Column(db.String(300), primary_key=True)
    sampling_event_id = db.Column(db.Integer, db.ForeignKey('sampling_event.sampling_event_id'), nullable=False)
    ***CHECK THIS***checklist = db.Column(db.String(100), nullable=False)

    # Which species and how many.
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'), nullable=False)
    observation_count = db.Column(db.Integer, nullable=False)

    # Create relationships with other tables
    species = db.relationship("Species")
    sampling_event = db.relationship("SamplingEvent")

    def __repr__(self):

        return "<Global id=%s Species ID=%s Observation count=%s>" % (self.global_id,
                                                                      self.species_id,
                                                                      self.observation_count)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ebird_data'
    # app.donfig['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
