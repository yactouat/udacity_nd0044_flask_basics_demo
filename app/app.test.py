from sqlalchemy import create_engine
import unittest

from init import create_app
from models import db


class AppTest(unittest.TestCase):
    """This class represents the app's test case"""

    def setUp(self):
        """Initialize the app with
           - test DB
           - setting up a web client
        """
        self.app = create_app("test")
        # context for SQLAlchemy to be aware of the Flask app' we're using
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
        self.app.app_context().push()
        # bootstrap database, here we conveniently dont use db migrations
        db.init_app(self.app)
        db.create_all()
        # defining the web client
        self.client = self.app.test_client

    # tearing down logic helps guarantee that code runs in isolation
    # although, keep in mind that sometimes
    # it's better to put tear down logic in the setup
    # because an error may crash your whole test suite without your intended
    # teardown logic being executed
    def tearDown(self):
        """Reset logic:
           - reset DB after each test is run
        """
        engine = create_engine("postgresql://usr:pwd@pgsql-test:5433/todos")
        connection = engine.raw_connection()
        cursor = connection.cursor()
        command = "DROP TABLE todos, todos_lists;"
        cursor.execute(command)
        connection.commit()
        cursor.close()

    def test_get_unknown_url_returns_formatted_404(self):
        """Given a web user, when he hits /api/unknown with a GET request,
        then the response should have a status code of 404
        and the response body should contain the expected payload"""
        res = self.client().get('/api/unknown')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json["msg"], "resource not found, aborting...")
        self.assertEqual(res.json["data"], None)
        self.assertFalse(res.json["success"])

    def test_get_base_url_expected_payload(self):
        """Given a web user, when he hits /api with a get request,
           then the response should have a status code of 200"""
        res = self.client().get('/api')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["msg"], "todos api is up")
        self.assertEqual(res.json["data"], None)
        self.assertTrue(res.json["success"])


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
