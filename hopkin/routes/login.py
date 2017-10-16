import jwt
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, jsonify, request

login_api = Blueprint('loginApi', __name__)


@login_api.route('/login/register', strict_slashes=False, methods=['POST'])
def register() -> tuple:
    """

    swagger_from_file: ../swagger/login/register.yml

    Register a new user
    :return:
    """
    # import here because of circular reference
    from hopkin.models.users import User
    if request.json is not None:
        new_user = {
            'username': request.json['username'],
            'password': generate_password_hash(request.json['password']),
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
        User.save(new_user)
        return jsonify({'data': {'user': request.json}})
    else:
        return jsonify({'error': 'no username or password provided'}), 401


@login_api.route('/login', strict_slashes=False, methods=['POST'])
def login() -> tuple:
    """

    swagger_from_file: ../swagger/login/login.yml

    Login to the api
    Pass in the username and password in the header
    A token is returned
    {"data": {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE0ODkxODUyMjAsInNvbWVQY"}}
    :return: token
    """
    # import here because of circular reference
    from hopkin.models.users import User

    if ('username' in request.headers) and ('password' in request.headers):
        username = request.headers['username']
        password = request.headers['password']
    else:
        return jsonify({'error': 'no username or password provided'}), 403

    # find user from database
    user = User.get_by_username(username)
    if user is None:
        return jsonify({'error': 'wrong username or password'}), 403
    else:
        # verify password
        if not check_password_hash(user['password'], password):
            return jsonify({'error': 'wrong username or password'}), 403

    # TODO check if user has token
    # if token return token
    # else gen new token

    if hasattr(user, 'token'):
        jwt_token = user['token']
    else:
        # generate a new token for the user for 1 week
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
            'user_id': str(user['_id'])},
            'secret', algorithm='HS512')
        jwt_token = token.decode("utf-8")
        user['token'] = jwt_token
        User.save(user)

    return jsonify({
        'data': {
            'token': jwt_token,
            'adminRights': user['adminRights']
        }
    })
