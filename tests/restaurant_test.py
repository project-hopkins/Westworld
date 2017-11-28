import unittest
import json
import copy
from hopkin.app import flask_app
from hopkin.models.restaurants import Restaurant
from hopkin.models.users import User


class TestRestaurantRoute(unittest.TestCase):
    __test_restaurant_data_1 = {
        'address':
            {
                'streetNumber': 9022,
                'streetName': 'Thraser Avenue',
                'city': 'Kelowna',
                'province': 'BC',
                'postalCode': 'V1W 3Y9'
            },
        'location':
            {
                'longitude': 49.7930404,
                'latitude': -119.5252368
            }
    }
    __test_restaurant_data_2 = {
        'address':
            {
                'streetNumber': 1280,
                'streetName': 'Main Street',
                'city': 'Hamliton',
                'province': 'ON',
                'postalCode': 'L8S 4L8'
            },
        'location':
            {
                'longitude': 43.260879,
                'latitude': -79.9192254
            }
    }
    __admin_user_data = '{"username": "aaron","password": "password","displayName": {"firstName": "Aaron",' \
                        '"lastName": "Fernandes"},"email": "aaron4@example.com","adminRights": true, ' \
                        '"paymentInfo": {"name": "Aaron Fernandes","cardType": "VISA","num": 451535486,' \
                        '"expiry": "1/1/17 12:00:00 AM UTC"},"address":{"number": 345,"name": "Fake","streetType": ' \
                        '"Street","postalCode": "M3H5R1"}}'

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

    def test_get_all_restaurants(self):
        restaurant_1 = self.__add_restaurant(self.__test_restaurant_data_1)
        restaurant_2 = self.__add_restaurant(self.__test_restaurant_data_2)

        result = self.app.get('/restaurant')
        json_data = json.loads(result.data)
        self.assertTrue(len(json_data['data']['restaurants']) >= 2, 'no items in db')

        with flask_app.app_context():
            Restaurant.remove(restaurant_1['_id'])
            Restaurant.remove(restaurant_2['_id'])

    def test_get_restaurant_by_id(self):
        restaurant = self.__add_restaurant(self.__test_restaurant_data_1)

        result = self.app.get('/restaurant/id/' + str(restaurant['_id']))
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['restaurant'] is not None and
                        json_data['data']['restaurant']['address']['streetName'] == self.__test_restaurant_data_1['address']['streetName'],
                        'no proper restaurant by id found')

        with flask_app.app_context():
            Restaurant.remove(restaurant['_id'])

    def test_admin_add_restaurant(self):
        json_response_reg = self.__register_user(self.__admin_user_data)
        admin_token = self.__login_user(json.loads(self.__admin_user_data))

        # add restaurant as admin
        result = self.app.post(
            '/admin/restaurant/add',
            headers={'Content-Type': 'application/json', 'token': admin_token},
            data=json.dumps(self.__test_restaurant_data_1)
        )

        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['restaurant'] is not None, 'restaurant not added')

        with flask_app.app_context():
            Restaurant.remove(json_data['data']['restaurantId'])
            User.remove(json_response_reg['data']['user']['email'])

        return {'id': json_data['data']['restaurantId'], 'token': admin_token, 'restaurant': json_data['data']['restaurant']}

    def test_admin_del_item(self):
        json_response_reg = self.__register_user(self.__admin_user_data)
        admin_token = self.__login_user(json.loads(self.__admin_user_data))

        # add an restaurant to delete
        restaurant = self.__add_restaurant(self.__test_restaurant_data_1)

        result = self.app.post(
            '/admin/restaurant/delete/' + str(restaurant['_id']),
            headers={'Content-Type': 'application/json', 'token': admin_token},
        )
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['success'] is not None, 'fail delete restaurant')

        with flask_app.app_context():
            Restaurant.remove(restaurant['_id'])
            User.remove(json_response_reg['data']['user']['email'])

    def __add_restaurant(self, data):
        with flask_app.app_context():
            Restaurant.save(data)
            return Restaurant.get_all()

    def __register_user(self, data):
        result = self.app.post('/login/register', data=data, content_type='application/json')
        return json.loads(result.data)

    def __login_user(self, data):
        login_result = self.app.post('/login', headers={'username': data['username'], 'password': data['password']})
        return json.loads(login_result.data)['data']['token']
