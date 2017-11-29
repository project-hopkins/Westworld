import copy
from hopkin.app import flask_db
from bson.objectid import ObjectId


class Restaurant:
    collection_name = 'restaurant'

    @staticmethod
    def get_all():
        return flask_db.db[Restaurant.collection_name]

    @staticmethod
    def get_by_id(restaurant_id):
        return flask_db.db[Restaurant.collection_name].find_one({'_id': ObjectId(str(restaurant_id))})

    @staticmethod
    def insert(new_restaurant):
        return flask_db.db[Restaurant.collection_name].insert_one(new_restaurant).inserted_id

    @staticmethod
    def save(restaurant):
        restaurant_to_save = copy.deepcopy(restaurant)
        flask_db.db[Restaurant.collection_name].save(restaurant_to_save)

    @staticmethod
    def remove(restaurant_id):
        flask_db.db[Restaurant.collection_name].delete_one({'_id': ObjectId(str(restaurant_id))})
