import copy
import re
from hopkin.app import flask_db
from bson.objectid import ObjectId


class Item:
    collection_name = 'items'

    # name = db.StringField(required=True)
    # description = db.StringField(max_length=256, required=True)
    # imageURL = db.StringField(required=True)
    # price = db.FloatField(required=True)
    # calories = db.IntField(required=True)
    # category = db.StringField(required=True)
    # tags = db.ListField(db.StringField(), required=True)

    @staticmethod
    def get_all():
        return flask_db.db[Item.collection_name].find()

    @staticmethod
    def get_by_id(item_id):
        return flask_db.db[Item.collection_name].find_one({'_id': ObjectId(item_id)})

    @staticmethod
    def get_by_category(category):
        return flask_db.db[Item.collection_name].find({'category': category})

    @staticmethod
    def get_by_name(name):
        return flask_db.db[Item.collection_name].find_one({'name': name})

    @staticmethod
    def get_by_name_search(search_string):
        return flask_db.db[Item.collection_name].find({'name': re.compile(search_string, re.IGNORECASE)})

    @staticmethod
    def get_by_tag_starts_with(search_string):
        return flask_db.db[Item.collection_name].find({'tags': {'$regex': '^' + search_string}})

    @staticmethod
    def get_recommended():
        return flask_db.db[Item.collection_name].find({'isRecommended': 'true'})

    @staticmethod
    def insert(new_item):
        return flask_db.db[Item.collection_name].insert_one(new_item).inserted_id

    @staticmethod
    def save(item):
        item_to_save = copy.deepcopy(item)
        flask_db.db[Item.collection_name].save(item_to_save)

    @staticmethod
    def remove(item_id):
        flask_db.db[Item.collection_name].delete_one({'_id': item_id})