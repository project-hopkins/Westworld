from hopkin.app import flask_db


# class PaymentInfo(db.Document):
#     name = db.StringField(required=True)  # Name on Credit Card
#     cardType = db.EnumField(db.StringField(), 'VISA', 'MASTERCARD', 'AMEX')
#     num = db.IntField(required=True)  # Credit Card Number
#     cvNum = db.IntField(required=False)  # CVV Number on back of credit card
#     expiry = db.DateTimeField(required=False)
#
#
# class UserFullName(db.Document):
#     firstName = db.StringField(required=True)
#     lastName = db.StringField(required=True)
#
#
# class Address(db.Document):
#     number = db.IntField(required=True)
#     name = db.StringField(required=True)
#     streetType = db.StringField(required=True)
#     postalCode = db.StringField(required=True)


class User:
    collection_name = 'users'
    #
    # username = db.StringField(required=True)
    # username_index = Index().ascending('username').unique()
    # password = db.StringField(required=True)
    # token = db.StringField(required=False)
    # displayName = db.DocumentField(UserFullName)
    # email = db.StringField(required=True)
    # email_index = Index().ascending('email').unique()
    # adminRights = db.BoolField(required=True)
    # paymentInfo = db.DocumentField(PaymentInfo)
    # address = db.DocumentField(Address)

    @staticmethod
    def get_by_token(token):
        return flask_db.db[User.collection_name].find_one({'token': token})

    @staticmethod
    def get_by_username(username):
        return flask_db.db[User.collection_name].find_one({'username': username})

    @staticmethod
    def save(user):
        flask_db.db[User.collection_name].save(user)
