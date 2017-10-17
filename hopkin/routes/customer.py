from flask import Blueprint, jsonify, g, request
import datetime

customer_api = Blueprint('customer_api', __name__)


@customer_api.route('/customer/payment', strict_slashes=False, methods=['GET'])
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
                    'num': payment_info['num'],
                    'expiry': payment_info['expiry']
                }
        }
    })


@customer_api.route('/customer/profile', strict_slashes=False, methods=['GET'])
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
            'num': request['paymentInfo']['num'],
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


@customer_api.route('/customer/profile/edit', strict_slashes=False, methods=['POST'])
def customer_profile_update() -> tuple:
    """

    swagger_from_file: ../swagger/customer/profile.yml

    Gets a customers profile info
    :return:
    """
    if request.json is not None:

        from hopkin.models.users import User
        # read the the user to the db
        if request.json is not None:
            user_update = {
                'username': request.json['username'],
                'password': request.json['password'],
                'displayName': {
                    'firstName': request.json['displayName']['firstName'],
                    'lastName': request.json['displayName']['lastName']
                },
                'email': request.json['email'],
                'adminRights': request.json['adminRights'],
                'paymentInfo': {
                    'name': request.json['paymentInfo']['name'],
                    'cardType': request.json['paymentInfo']['cardType'],
                    'num': int(request.json['paymentInfo']['num']),
                    'expiry': datetime.datetime.strptime(request.json['paymentInfo']['expiry'],
                                                         "%w/%m/%y %I:%M:%S %p UTC")
                },
                'address': {
                    'number': int(request.json['address']['number']),
                    'name': request.json['address']['name'],
                    'streetType': request.json['address']['streetType'],
                    'postalCode': request.json['address']['postalCode']
                }
            }

            User.save(user_update)

        return jsonify({'data': {'user': user_update}})
    else:
        return jsonify({'error': 'user not updated'}), 400
