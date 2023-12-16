from flask_testing import TestCase
from app import create_app
from app import db


class BaseTest(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)