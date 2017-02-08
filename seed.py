from sqlalchemy import func
from model import Species, SamplingEvent, Observation
from datetime import datetime

from model import connect_to_db, db
from server import app

# KEY: eBird row ordering
# global_id, taxonomic_num, category, common_name, scientific_name = row[:5]
# __, __, observation_count = row[7]
# __, __, __, __, __, __, county = row[14]
# __, __, __, __, __, latitude, longitude, observation_date = row[20:22]
# __, __, __, __, __, __, sampling_event_id = row[29]
# __, __, __, __, __, __, all_species = row[36]


def load_species():
    """Load species data into database."""

    print "Bird data"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate data
    Species.query.delete()
    count = 0

    # Read file and insert data
    for row in open("seed_data/ebd_US-CA-053_201401_201409_relAug-2014.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:5]
            taxonomic_num = row[1]
            category = row[2]
            common_name = row[3]
            scientific_name = row[4]

            species = Species(taxonomic_num=taxonomic_num,
                              common_name=common_name,
                              scientific_name=scientific_name)

        # Add to the session or it won't ever be stored
            db.session.add(species)
        count += 1

    # Commit work
    db.session.commit()


def load_sampling_event():
    """Load Sampling Event information into database."""

    print "Sampling event"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate data
    SamplingEvent.query.delete()
    count = 0

    # Read file insert data
    for row in open("seed_data/ebd_US-CA-053_201401_201409_relAug-2014.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:37]

            county = row[14]
            latitude = row[20]
            longitude = row[21]

            observation_date = row[22]
            if observation_date:
                observation_date = datetime.strptime(observation_date, '%m/%d/%Y')
            else:
                observation_date = None

            checklist = row[29]
            all_species = row[36]

            samplingEvent = SamplingEvent(county=county,
                                          latitude=latitude,
                                          longitude=longitude,
                                          observation_date=observation_date,
                                          checklist=checklist,
                                          all_species=all_species)

            # Add to the session or it won't ever be stored
            db.session.add(samplingEvent)

        count += 1

    # Commit work
    db.session.commit()


def load_observation():
    """Load Observational data into database."""

    print "Bird Observation event"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Observation.query.delete()
    count = 0

    # Read file and insert data
    for row in open("seed_data/ebd_US-CA-053_201401_201409_relAug-2014.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:30]
            global_id = row[0]
            species_id = row[1]
            observation_count = row[7]
            sampling_event_id = row[29]

            observation = Observation(global_id=global_id,
                                      species_id=species_id,
                                      observation_count=observation_count,
                                      sampling_event_id=sampling_event_id)

            # Add to the session or it won't ever be stored
            db.session.add(observation)

        count += 1

    # Commit work
    db.session.commit()

# taken from ratings exercise -- do I need this????
# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_species()
    # load_sampling_event()
    load_observation()
    # set_val_user_id()