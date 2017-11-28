from hopkin.app import flask_db
from bson.objectid import ObjectId

class Restaurant:
    collection_name = 'restaurants'

    @staticmethod
    def get_all():
        return flask_db.db[Restaurant.collection_name]

    @staticmethod
    def get_by_id(restaurant_id):
        return flask_db.db[Restaurant.collection_name].find_one({'_id': ObjectId(restaurant_id)})

    @staticmethod
    def insert(new_restaurant):
        return flask_db.db[Restaurant.collection_name].insert_one(new_restaurant).inserted_id

    @staticmethod
    def remove(restaurant_id):
        flask_db.db[Restaurant.collection_name].delete_one({'_id': ObjectId(restaurant_id)})
