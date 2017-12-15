from flask import Blueprint, jsonify, g, request
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

customer_api = Blueprint('customer_api', __name__)


def get_cc_number(cc_number: int):
    return '*'*12 + str(cc_number)[12:]


@customer_api.route('/customer/payment', methods=['GET'])
def customer_payment_info() -> dict:
    """

    swagger_from_file: ../swagger/customer/paymentInfo.yml

    Gets a customers payment info
    """
    from hopkin.models.users import User
    user = User.get_by_id(g.user_id)
    payment_info = user['paymentInfo']

    return jsonify({
        'data': {
            'paymentInfo':
                {
                    'name': payment_info['name'],
                    'cardType': payment_info['cardType'],
                    'num': get_cc_number(payment_info['num']),
                    'expiry': payment_info['expiry']
                }
        }
    })


@customer_api.route('/customer/profile', methods=['GET'])
def customer_profile_info() -> dict:
    """

    swagger_from_file: ../swagger/customer/profile.yml

    Gets a customers profile info
    :return:
    """
    from hopkin.models.users import User
    request = User.get_by_id(g.user_id)

    user_info = {
        'username': request['username'],
        'displayName': {
            'firstName': request['displayName']['firstName'],
            'lastName': request['displayName']['lastName']
        },
        'email': request['email'],
        'paymentInfo': {
            'name': request['paymentInfo']['name'],
            'cardType': request['paymentInfo']['cardType'],
            'num': get_cc_number(request['paymentInfo']['num']),
            'expiry': request['paymentInfo']['expiry']
        },
        'address': {
            'number': int(request['address']['number']),
            'name': request['address']['name'],
            'streetType': request['address']['streetType'],
            'postalCode': request['address']['postalCode']
        }
    }

    return jsonify({'data': {
        'user': user_info
    }
    })


@customer_api.route('/customer/profile/edit', methods=['POST'])
def customer_profile_update() -> tuple:
    """

    swagger_from_file: ../swagger/customer/profile.yml

    Gets a customers profile info
    :return:
    """
    if request.json is not None:

        from hopkin.models.users import User
        # read the the user to the db
        if request.json is None:
            return jsonify({'error': 'user not updated'}), 400

        user_update = User.get_by_id(g.user_id)

        user_update['username'] = request.json['username']
        user_update['displayName'] = {
                'firstName': request.json['displayName']['firstName'],
                'lastName': request.json['displayName']['lastName']
        }
        user_update['email'] = request.json['email']
        user_update['adminRights'] = request.json['adminRights']
        user_update['address'] = {
                'number': int(request.json['address']['number']),
                'name': request.json['address']['name'],
                'streetType': request.json['address']['streetType'],
                'postalCode': request.json['address']['postalCode']
        }

        if request.json.get('paymentInfo') is not None:
            user_update['paymentInfo'] = {
                'name': request.json['paymentInfo']['name'],
                'cardType': request.json['paymentInfo']['cardType'],
                'num': int(request.json['paymentInfo']['num']),
                'expiry': datetime.datetime.strptime(request.json['paymentInfo']['expiry'],
                                                     "%w/%m/%y %I:%M:%S %p UTC")
            }

        User.save(user_update)

    return jsonify({'data': {'user': user_update}})


@customer_api.route('/customer/password/edit', methods=['POST'])
def customer_password_update() -> tuple:
    """

    Allows a user to change password
    :return:
    """
    from hopkin.models.users import User

    if request.json is None:
        return jsonify({'error': 'password not changed'}), 400

    # get user from db
    user = User.get_by_id(g.user_id)

    # check if given password matches password in db
    if not check_password_hash(user['password'], request.json['oldpass']):
        return jsonify({'error': 'old passwords don\'t match'}), 400

    user['password'] = generate_password_hash(request.json['newpass'])

    User.save(user)

    return jsonify({'success': True})
