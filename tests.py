import unittest

from server import app
from model import connect_to_db, db, example_data
from flask import session


class BirdDataTests(unittest.TestCase):
    """Tests for my eBird data site."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        with self.client as c:
            with c.session_transaction() as sess:
                sess['bird_name'] = "Song Sparrow"

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("species", result.data)
        self.assertEqual(result.status_code, 200)

    def test_map_page(self):
        result = self.client.get("/render_map")
        self.assertIn("Observations", result.data)
        self.assertEqual(result.status_code, 200)

    def test_ebird_data(self):

        result = self.client.get("/render_map")
        self.assertIn("County", result.data)


if __name__ == "__main__":
    unittest.main()
