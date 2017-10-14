import unittest

from hopkin.app import flask_app
from hopkin.models.items import Item


class TestItems(unittest.TestCase):
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

    def test_add_new_item(self):
        new_item = {
            'name': 'Test Item',
            'description': 'This is just a test description',
            'imageURL': "http://i.imgur.com/1vLLI3A.png",
            'price': 9.99,
            'calories': 500,
            'category': 'Entrees',
            'tags': ['bread', 'healthy']
        }

        with flask_app.app_context():
            Item.save(new_item)
            found_item = Item.get_by_name(new_item['name'])
            self.assertEqual(new_item['name'], found_item['name'], "Items not equal")
            Item.remove(new_item)
