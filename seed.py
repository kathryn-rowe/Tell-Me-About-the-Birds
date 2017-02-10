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
    tax_number_set = set()

    # Read file and insert data
    for row in open("seed_data/ebd_US-CA_200601_201702_relNov-2016.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:5]

            # Get the values from the row
            taxonomic_num = row[1]
            category_type = row[2]
            common_name = row[3]
            scientific_name = row[4]

            # Using the set to store values; do not want to add multiple rows of each species
            # Category must be species, otherwise the column returns non-species info, ex gull sp.
            if taxonomic_num not in tax_number_set and category_type == 'species':
                tax_number_set.add(taxonomic_num)

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
    checklist_set = set()

    # Read file insert data

    for row in open("seed_data/ebd_US-CA_200601_201702_relNov-2016.txt"):
        if count > 50:
            break
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:37]

            # Get the values from the row
            county = row[14]
            latitude = row[22]
            longitude = row[23]

            # Set observation date to datetime
            observation_date = row[24]
            # print observation_date
            if observation_date:
                if "/" in observation_date:
                    observation_date = datetime.strptime(observation_date, '%m/%d/%Y')
                else:
                    observation_date = datetime.strptime(observation_date, '%Y-%m-%d')
            else:
                observation_date = None

            # not sure if I will use this information; reports on species occurence
            all_species = row[36]

            # Using the set to store values; do not want to add multiple rows of each checklist
            checklist = row[29]
            if checklist not in checklist_set:
                checklist_set.add(checklist)

                samplingEvent = SamplingEvent(county=county,
                                              latitude=latitude,
                                              longitude=longitude,
                                              observation_date=observation_date,
                                              checklist=checklist,
                                              all_species=all_species)

                # Add to the session or it won't ever be stored
                db.session.add(samplingEvent)
        count += 1
        if count % 1000 == 0:
            print count
    # Commit work
    db.session.commit()


def load_observation():
    """Load Observational data into database."""

    print "Bird Observation event"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Observation.query.delete()
    count = 0
    tax_number_set = set()

    # Read file and insert data
    for row in open("seed_data/ebd_US-CA_200601_201702_relNov-2016.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:30]

            # Get the values from the row
            global_id = row[0]
            taxonomic_num = row[1]
            category_type = row[2]
            observation_count = row[7]
            checklist = row[29]

            # Category must be species, otherwise the column returns non-species info, ex gull sp.
            if category_type == 'species':

                observation = Observation(global_id=global_id,
                                          taxonomic_num=taxonomic_num,
                                          observation_count=observation_count,
                                          checklist=checklist)

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