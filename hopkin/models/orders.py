from hopkin.app import flask_db
from bson.objectid import ObjectId


class Order:
    collection_name = 'orders'

    @staticmethod
    def get_all(user_id):
        return flask_db.db[Order.collection_name].find({'userId': user_id})

    @staticmethod
    def get_by_id(order_id):
        return flask_db.db[Order.collection_name].find_one({'_id': order_id})

    @staticmethod
    def insert(new_order):
        return flask_db.db[Order.collection_name].insert_one(new_order).inserted_id

    @staticmethod
    def remove(order_id):
        flask_db.db[Order.collection_name].delete_one({'_id': ObjectId(order_id)})
