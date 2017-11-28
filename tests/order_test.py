import unittest
import json

from hopkin.app import flask_app
from hopkin.models.orders import Order
from hopkin.models.users import User


class TestOrderRoute(unittest.TestCase):
    def setUp(self):
        """
        Setup app for testing
        :return:
        """
        self.app = flask_app.test_client()
        self.app.testing = True

    def tearDown(self):
        """
        Remove app after testing
        :return:
        """
        self.app.delete()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_add_new_order(self):
        json_response_reg = self.__register_user()

        login = self.app.post('/login', headers={'username': 'steve', 'password': 'smith'})
        json_login = json.loads(login.data)
        data = '{"date": "12:05:2017","delivery": true,"items": [' \
               '{"58cb056f98717507c730d78b": 5},{"58cb0577630cc007c7870772": 2},' \
               '{"58d13f3e63ae2507c70a7d5e": 1}' \
               '],"price": 25.06}'

        result = self.app.post('/order/add/', headers={'token': json_login['data']['token']}, data=data, content_type='application/json')
        json_response = json.loads(result.data)
        self.assertIsNotNone(json_response['data']['orderId'], 'error in response')

        with flask_app.app_context():
            Order.remove(json_response['data']['orderId'])
            User.remove(json_response_reg['data']['user']['email'])

    def test_get_user_orders(self):
        json_response_reg = self.__register_user()

        login = self.app.post('/login', headers={'username': 'steve', 'password': 'smith'})
        json_response = json.loads(login.data)['data']['token']
        self.assertIsNotNone(json_response)
        result = self.app.get('/order', headers={'token': json_response})
        json_data = json.loads(result.data)
        self.assertIsNotNone(len(json_data), 'no orders in db')

        with flask_app.app_context():
            User.remove(json_response_reg['data']['user']['email'])

    def __register_user(self):
        data = '{"address": {"name": "Main", "number": 123, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
               '"adminRights": false, "displayName": {"firstName": "Aaron", "lastName": "Smith"}, ' \
               '"email": "example@example.com", "password": "smith", "paymentInfo": {"cardType": "VISA", ' \
               '"expiry": "1/1/17 12:00:00 AM UTC", "name": "steve Smith", "num": 451535486}, "username": "steve"}'
        result = self.app.post('/login/register', data=data, content_type='application/json')
        return json.loads(result.data)
