from hopkin.app import flask_db
from bson.objectid import ObjectId


class User:
    collection_name = 'users'

    @staticmethod
    def get_by_token(token):
        return flask_db.db[User.collection_name].find_one({'token': token})

    @staticmethod
    def get_by_username(username):
        return flask_db.db[User.collection_name].find_one({'username': username})

    @staticmethod
    def get_by_email(email):
        return flask_db.db[User.collection_name].find_one({'email': email})

    @staticmethod
    def get_by_id(id):
        return flask_db.db[User.collection_name].find_one({'_id': ObjectId(id)})

    @staticmethod
    def save(user):
        flask_db.db[User.collection_name].save(user)

    # Shouldn't be used in production. Only for testing purposes
    @staticmethod
    def remove(user_email):
        flask_db.db[User.collection_name].delete_one({'email': user_email})
