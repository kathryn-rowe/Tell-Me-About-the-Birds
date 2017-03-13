from model import Species, SamplingEvent, Observation, MonthlyAvg
from datetime import datetime

from model import connect_to_db, db
from server import app

# KEY: eBird row ordering
# global_id, taxonomic_num, category, common_name, scientific_name = row[:5]
# __, __, observation_count = row[7]
# __, __, __, __, __, __, county = row[14]
# __, __, __, __, __, __, __, latitude, longitude, observation_date = row[22:24]
# __, __, __, __, __, __, sampling_event_id = row[29]
# __, __, __, __, __, __, all_species = row[36]


def load_species():
    """Load species data into database."""

    print "***Bird data***"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate data
    # Species.query.delete()
    count = 0
    tax_number_set = set()

    # Read file that contains 5 years of data and get all species.
    for row in open("example_data/ebd_US-CA-053_201401_201409_relAug-2014.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:5]

            # Get the values from the row
            taxonomic_num = row[1]
            category_type = row[2]

            # Using the set to store values; do not want to add multiple rows of each species
            # Category must be species, otherwise the column returns non-species info, ex gull sp.
            if taxonomic_num not in tax_number_set and category_type == 'species':
                tax_number_set.add(taxonomic_num)

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

    print "***Sampling event***"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate data
    count = 0
    checklist_set = set()

    # Read file insert data

    for row in open("example_data/ebd_US-CA-053_201401_201409_relAug-2014.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:37]

            # Set observation date to datetime
            observation_date = row[24]

             # print observation_date
            if observation_date:
                if "/" in observation_date:
                    observation_date = datetime.strptime(observation_date, '%m/%d/%Y')
                else:
                    observation_date = datetime.strptime(observation_date, '%Y-%m-%d')

            # if observation_date.year == 2014:

            checklist = row[29]

            # Using the set to store values; do not want to add multiple rows of each checklist
            if checklist not in checklist_set:
                checklist_set.add(checklist)

                # Get the values from the row
                county = row[14]
                latitude = row[22]
                longitude = row[23]

                # not sure if I will use this information; reports on species occurence
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
        # print count
        if count % 100000 == 0:
            print count
    # Commit work
    db.session.commit()


def load_observation():
    """Load Observational data into database."""

    print "***Bird Observation event***"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    # Observation.query.delete()
    count = 0
    # tax_number_set = set()

    # Read file and insert data
    for row in open("example_data/ebd_US-CA-053_201401_201409_relAug-2014.txt"):
        if count != 0:
            row = row.rstrip()
            row = row.split("\t")[:30]

            category_type = row[2]

            # Category must be species, otherwise the column returns non-species info, ex gull sp.
            if category_type == 'species':

                # Get the values from the row
                global_id = row[0]
                taxonomic_num = row[1]
                observation_count = row[7]
                checklist = row[29]

                observation = Observation(global_id=global_id,
                                          taxonomic_num=taxonomic_num,
                                          observation_count=observation_count,
                                          checklist=checklist)

                # Add to the session or it won't ever be stored
                db.session.add(observation)

        count += 1
        if count % 1000 == 0:
            print count
        # Commit work
        db.session.commit()


def get_month_avg(county, tax_num):
    """Find the monthly averages for the given county and bird species"""

    bird_date = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(Observation.taxonomic_num == tax_num,
                                                                                        Observation.observation_count != 'X',
                                                                                        SamplingEvent.county == county).all()

    sum_per_month = {"January": 2, "February": 2, "March": 2, "April": 2, "May": 2, "June": 2,
                     "July": 2, "August": 2, "September": 2, "October": 2, "November": 2, "December": 2}

    # gets total number of bird species seen per month
    for label in sum_per_month:
        for observation in bird_date:
            if observation[1].observation_date.strftime('%B') == label:
                sum_per_month[label] += int(observation[0].observation_count)

    return sum_per_month


def load_monthly_avgs():
    """Load monthly observations per species per month"""

    print "***Monthly Avgs.***"

    counties = ["Humboldt", "Yuba", "San Francisco", "Monterey"]

    for county in counties:
        birds_per_county = db.session.query(Observation, SamplingEvent).join(SamplingEvent).filter(SamplingEvent.county == county,
                                                                                                   Observation.observation_count != 'X').all()
        county = county
        birds_in_county = set()

        for bird in birds_per_county:
            bird_num = bird[0].taxonomic_num
            if bird_num not in birds_in_county:
                birds_in_county.add(bird_num)
                taxonomic_num = bird_num
                bird_name = db.session.query(Species).filter(Species.taxonomic_num == taxonomic_num).first()
                common_name = bird_name.common_name

                sum_per_month = get_month_avg(county, taxonomic_num)

                janAvg = sum_per_month["January"]
                febAvg = sum_per_month["February"]
                marAvg = sum_per_month["March"]
                aprilAvg = sum_per_month["April"]
                mayAvg = sum_per_month["May"]
                juneAvg = sum_per_month["June"]
                julyAvg = sum_per_month["July"]
                augAvg = sum_per_month["August"]
                septAvg = sum_per_month["September"]
                octAvg = sum_per_month["October"]
                novAvg = sum_per_month["November"]
                decAvg = sum_per_month["December"]

                monthlyAvg = MonthlyAvg(county=county,
                                        taxonomic_num=taxonomic_num,
                                        common_name=common_name,
                                        janAvg=janAvg,
                                        febAvg=febAvg,
                                        marAvg=marAvg,
                                        aprilAvg=aprilAvg,
                                        mayAvg=mayAvg,
                                        juneAvg=juneAvg,
                                        julyAvg=julyAvg,
                                        augAvg=augAvg,
                                        septAvg=septAvg,
                                        octAvg=octAvg,
                                        novAvg=novAvg,
                                        decAvg=decAvg)
                print "*****appending***"
                # Add to the session or it won't ever be stored
                db.session.add(monthlyAvg)

        # Commit work
        db.session.commit()
        print "*****appended*****"

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data. UNCOMMENT WHEN READY TO SEED FILE!!!!!!
    # load_species()
    # load_sampling_event()
    # load_observation()
    # load_monthly_avgs()
