import unittest
import json
from hopkin.app import flask_app
from hopkin.models.users import User


class TestCustomerInfo(unittest.TestCase):
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

    def test_get_customer_payment_info(self):
        json_response_reg = self.__register_user()

        token = self.__login()
        result = self.app.get('/customer/payment', headers={'token': token})
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['paymentInfo'] is not None, 'no payment info')

        with flask_app.app_context():
            User.remove(json_response_reg['data']['user']['email'])

    def test_get_customer_info(self):
        json_response_reg = self.__register_user()

        token = self.__login()
        result = self.app.get('/customer/profile', headers={'token': token})
        self.assertIsNotNone(result, 'No user info')

        with flask_app.app_context():
            User.remove(json_response_reg['data']['user']['email'])

    def test_customer_profile_update(self):
        from hopkin.models.users import User

        # creating new user
        data = '{"address": {"name": "Queen", "number": 155, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
               '"adminRights": false, "displayName": {"firstName": "Jane", "lastName": "Doe"}, ' \
               '"email": "example69@example.com", "password": "password", "paymentInfo": {"cardType": "VISA", ' \
               '"expiry": "1/1/17 12:00:00 AM UTC", "name": "Jane Doe", "num": 451535486}, "username": "Jane"}'
        self.app.post('/login/register', data=data, content_type='application/json')

        # login to get token
        login_result = self.app.post('/login', headers={'username': 'Jane', 'password': 'password'})
        json_response = json.loads(login_result.data)['data']['token']
        self.assertIsNotNone(json_response)

        # update user info
        updated_data = '{"address": {"name": "Baker", "number": 221, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
                       '"adminRights": false, "displayName": {"firstName": "Jane", "lastName": "Doe"}, ' \
                       '"email": "example@example.com", "paymentInfo": {"cardType": "VISA", ' \
                       '"expiry": "1/1/17 12:00:00 AM UTC", "name": "Jane Doe", "num": 451535486}, "username": "Jane"}'

        result = self.app.post('/customer/profile/edit', data=updated_data, headers={'token': json_response})
        json_data = json.loads(result.data)
        self.assertIsNotNone(len(json_data))

        with flask_app.app_context():
            user = User.get_by_token(json_response)
            User.remove(user['email'])

    def test_customer_password_update(self):
        json_response_reg = self.__register_user()
        token = self.__login()

        # password to reset
        password_data = '{"oldpass": "smith", "newpass": "smith123"}'

        result = self.app.post('/customer/password/edit', data=password_data, headers={'token': token}, content_type='application/json')
        json_result = json.loads(result.data)
        self.assertTrue(json_result['success'], True)

        with flask_app.app_context():
            user = User.get_by_token(token)
            User.remove(user['email'])


    def __login(self):
        login_result = self.app.post('/login', headers={'username': 'steve', 'password': 'smith'})
        return json.loads(login_result.data)['data']['token']

    def __register_user(self):
        data = '{"address": {"name": "Main", "number": 123, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
               '"adminRights": false, "displayName": {"firstName": "Aaron", "lastName": "Smith"}, ' \
               '"email": "example@example.com", "password": "smith", "paymentInfo": {"cardType": "VISA", ' \
               '"expiry": "1/1/17 12:00:00 AM UTC", "name": "steve Smith", "num": 1234567890123456}, "username": "steve"}'
        result = self.app.post('/login/register', data=data, content_type='application/json')
        return json.loads(result.data)
