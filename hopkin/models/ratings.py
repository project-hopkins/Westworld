import copy
import re
from hopkin.app import flask_db
from bson.objectid import ObjectId


class Rating:
    collection_name = 'ratings'

    @staticmethod
    def get_all():
        return flask_db.db[Rating.collection_name].find()

    @staticmethod
    def get_rating(item_id, user_id):
        return flask_db.db[Rating.collection_name].find_one({'item_id': item_id, 'user_id': str(user_id)})

    @staticmethod
    def insert(new_rating):
        return flask_db.db[Rating.collection_name].insert_one(new_rating).inserted_id

    @staticmethod
    def save(rating):
        item_to_save = copy.deepcopy(rating)
        flask_db.db[Rating.collection_name].save(item_to_save)

    @staticmethod
    def update(rating):
        return flask_db.db[Rating.collection_name].update_one({'_id': rating['_id']}, {"$set": rating}, upsert=True)

    @staticmethod
    def remove(item_id):
        flask_db.db[Rating.collection_name].delete_one({'_id': item_id})

    @staticmethod
    def remove_all_ratings():
        """
        Test only
        :return:
        """
        flask_db.db[Rating.collection_name].delete_many({})