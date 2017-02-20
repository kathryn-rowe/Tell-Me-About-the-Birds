import unittest

from server import app
from test_model import db, connect_to_db, example_data


class BirdDataTests(unittest.TestCase):
    """Tests for my eBird data site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("species", result.data)
        self.assertEqual(result.status_code, 200)

    def test_map_page(self):
        result = self.client.get("/render_map")
        self.assertIn("Observations", result.data)
        self.assertEqual(result.status_code, 200)


class eBirdTestsDatabase(unittest.TestCase):
    """Flask tests that use the test database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def test_ebird_data(self):

        result = self.client.get("/render_map")
        self.assertIn("Song Sparrow", result.data)

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    # def test_games(self):
    #     #FIXME: test that the games page displays the game from example_data()
    #     result = self.client.get("/games")
    #     self.assertIn("Duck Duck Goose", result.data)

if __name__ == "__main__":
    unittest.main()
