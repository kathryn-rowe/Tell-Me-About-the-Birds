from sqlalchemy import func
from model import Species, SamplingEvent, Observation
import datetime

from model import connect_to_db, db
from server import app


def load_species():
    """Load species data into database."""

    print "Bird data"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate data
    Species.query.delete()

    # Read file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # Add to the session or it won't ever be stored
        db.session.add(user)

    # Commit work
    db.session.commit()


def load_sampling_event():
    """Load Sampling Event information into database."""

    print "Sampling event"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate data
    SamplingEvent.query.delete()

    # Read file insert data
    for i, row in enumerate(open("seed_data/u.item")):
        row = row.rstrip()
        row = row.split("|")[:-19]
        movie_id, movie, release_date, __, imdb_url = row
        title = movie.split("(")
        title = title[0].rstrip()
        title = title.decode("latin-1")
        if release_date:
            released_at = datetime.datetime.strptime(release_date, "%d-%b-%Y")
        else:
            released_at = None

        movie = Movies(title=title,
                       released_at=released_at,
                       imdb_url=imdb_url)

        # Add to the session or it won't ever be stored
        db.session.add(movie)

        if i % 100 == 0:
            print i

    # Commit work
    db.session.commit()


def load_observation():
    """Load Observational data into database."""

    print "Bird Observation event"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Observation.query.delete()

    # Read file and insert data
    for i, row in enumerate(open("seed_data/u.data")):
        row = row.rstrip()
        user_id, movie_id, score, __ = row.split("\t")
        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        rating = Ratings(user_id=user_id,
                         movie_id=movie_id,
                         score=score)

        # Add to the session or it won't ever be stored
        db.session.add(rating)

        if i % 100 == 0:
            print i

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
    load_species()
    load_sampling_event()
    load_observation()
    set_val_user_id()