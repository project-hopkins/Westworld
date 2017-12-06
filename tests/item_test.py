import unittest
import json
import copy
from hopkin.app import flask_app
from hopkin.models.items import Item
from hopkin.models.users import User


class TestItemRoute(unittest.TestCase):
    __test_item_data_1 = {
        'name': 'Test Item',
        'description': 'This is just a test description',
        'imageURL': "http://i.imgur.com/1vLLI3A.png",
        'price': 9.99,
        'calories': 500,
        'category': 'Starter',
        'tags': ['bread', 'healthy']
    }
    __test_item_data_2 = {
        'name': 'Test Item 2',
        'description': 'This is just a test description 2',
        'imageURL': "http://i.imgur.com/1vLLI3A.png",
        'price': 9.992,
        'calories': 5002,
        'category': 'Entrees',
        'tags': ['healthy']
    }
    __admin_user_data = '{"username": "aaron","password": "password","displayName": {"firstName": "Aaron",' \
                        '"lastName": "Fernandes"},"email": "aaron@example.com","adminRights": true, ' \
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

    def test_get_all_items(self):
        item_1 = self.__add_item(self.__test_item_data_1)
        item_2 = self.__add_item(self.__test_item_data_2)

        result = self.app.get('/item')
        json_data = json.loads(result.data)
        self.assertTrue(len(json_data['data']['items']) >= 2, 'no items in db')

        with flask_app.app_context():
            Item.remove(item_1['_id'])
            Item.remove(item_2['_id'])

    def test_get_item_by_id(self):
        item = self.__add_item(self.__test_item_data_1)

        result = self.app.get('/item/id/' + str(item['_id']))
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['item'] is not None and
                        json_data['data']['item']['name'] == self.__test_item_data_1['name'],
                        'no proper item by id found')

        with flask_app.app_context():
            Item.remove(item['_id'])

    def test_get_item_by_category(self):
        item = self.__add_item(self.__test_item_data_1)

        result = self.app.get('/item/category/' + str(self.__test_item_data_1['category']))
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['items'] is not None and
                        len(json_data['data']['items']) >= 1,
                        'no item by category found')

        with flask_app.app_context():
            Item.remove(item['_id'])

    def test_admin_add_item(self):
        json_response_reg = self.__register_user(self.__admin_user_data)
        admin_token = self.__login_user(json.loads(self.__admin_user_data))

        # add item as admin
        result = self.app.post(
            '/admin/item/add',
            headers={'Content-Type': 'application/json', 'token': admin_token},
            data=json.dumps(self.__test_item_data_1)
        )

        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['item'] is not None, 'item not added')

        with flask_app.app_context():
            Item.remove(json_data['data']['itemId'])
            User.remove(json_response_reg['data']['user']['email'])

        return {'id': json_data['data']['itemId'], 'token': admin_token, 'item': json_data['data']['item']}

    def test_admin_del_item(self):
        json_response_reg = self.__register_user(self.__admin_user_data)
        admin_token = self.__login_user(json.loads(self.__admin_user_data))

        # add an item to delete
        item = self.__add_item(self.__test_item_data_1)

        result = self.app.post(
            '/admin/item/delete/' + str(item['_id']),
            headers={'Content-Type': 'application/json', 'token': admin_token},
        )
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['success'] is not None, 'fail delete item')

        with flask_app.app_context():
            Item.remove(item['_id'])
            User.remove(json_response_reg['data']['user']['email'])

    def test_admin_update_item(self):
        json_response_reg = self.__register_user(self.__admin_user_data)
        admin_token = self.__login_user(json.loads(self.__admin_user_data))

        # add an item to update
        item = self.__add_item(self.__test_item_data_1)

        updated_name = 'updated name'
        updated_item = copy.deepcopy(self.__test_item_data_1)
        updated_item['name'] = updated_name
        updated_item['_id'] = str(item['_id'])

        result = self.app.post('/admin/item/update',
                               headers={'Content-Type': 'application/json', 'token': admin_token},
                               data=json.dumps(updated_item)
                               )
        self.assertIsNotNone(json.loads(result.data)['data'] is not None, 'no data from admin item update')

        with flask_app.app_context():
            Item.remove(item['_id'])
            User.remove(json_response_reg['data']['user']['email'])

    def __add_item(self, data):
        with flask_app.app_context():
            Item.save(data)
            return Item.get_by_name(data['name'])

    def __register_user(self, data):
        result = self.app.post('/login/register', data=data, content_type='application/json')
        return json.loads(result.data)

    def __login_user(self, data):
        login_result = self.app.post('/login', headers={'username': data['username'], 'password': data['password']})
        return json.loads(login_result.data)['data']['token']
