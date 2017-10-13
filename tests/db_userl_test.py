import unittest
from hopkin.app import flask_app
from hopkin.models.users import User
import datetime


class TestDB(unittest.TestCase):
    def setUp(self):
        """
        Setup app for testing
        :return:
        """
        self.app = flask_app.test_client()
        self.app.testing = True

    def tearDown(self):
        self.app.delete()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_add_new_user(self):
        new_user = {
            'username': 'aaron',
            'password': 'password',
            'displayName': {
                'firstName': 'Aaron',
                'lastName': 'Smith'
            },
            'email': 'aaron@example.com',
            'adminRights': False,
            'paymentInfo': {
                'name': 'Aaron Smith',
                'cardType': 'VISA',
                'num': 451535486,
                'expiry': datetime.datetime(2017, 1, 1)
            },
            'address': {
                'number': 123,
                'name': 'Main',
                'streetType': 'Boulevard',
                'postalCode': 'M3E5R1'
            }
        }

        with flask_app.app_context():
            User.save(new_user)
            found_user = User.get_by_email(new_user['email'])
            self.assertEqual(new_user['email'], found_user['email'], "User emails not equal")
            User.remove(new_user)
