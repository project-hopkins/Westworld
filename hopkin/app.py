#!/usr/bin/env python
import os
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_swagger import swagger

from flask_pymongo import PyMongo
from hopkin.routes.login import login_api
from hopkin.routes.items import item_api
from hopkin.routes.customer import customer_api
from hopkin.routes.orders import order_api
from hopkin.routes.restaurants import restaurant_api

flask_app = Flask(__name__)
flask_app.config['MONGO_URI'] = os.getenv('DBURI', 'mongodb://localhost/kanaoreeves')
flask_app.config['MONGO_DBNAME'] = 'kanaoreeves'
flask_db = PyMongo(flask_app)

CORS(flask_app)

flask_app.register_blueprint(login_api)
flask_app.register_blueprint(item_api)
flask_app.register_blueprint(order_api)
flask_app.register_blueprint(customer_api)
flask_app.register_blueprint(restaurant_api)


@flask_app.before_request
def before_request() -> tuple:
    """
    Checks if a token header in requests
    :return:
    """
    if request.method == 'GET' or request.method == 'POST':
        flask_app.logger.log(10, 'Headers: %s', request.headers)
        flask_app.logger.log(10, 'Body: %s', request.get_data())

        from hopkin.models.users import User
        no_auth_paths = ['/spec', '/favicon.ico', '/item', '/login']
        auth_required = True
        for path in no_auth_paths:
            if request.path.startswith(path):
                auth_required = False
        if '/' is request.path:
            auth_required = False
        if auth_required and 'token' in request.headers:
            token = request.headers['token']
            user = User.get_by_token(token)

            if user is None:
                return jsonify({'error': 'not a valid token'}), 403
            else:
                g.user_id = user['_id']
                g.is_admin = user['adminRights']
        elif auth_required and 'token' not in request.headers:
            return jsonify({'error': 'no token provided'}), 403


@flask_app.route('/', methods=['GET'])
def root():
    """
    Root api to test if its working
    :return:
    """
    return jsonify({'data': {'success': True}})


@flask_app.route('/spec')
def spec():
    swag = swagger(flask_app, from_file_keyword='swagger_from_file')
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Hopkins"
    return jsonify(swag)


@flask_app.errorhandler(404)
def handel404(error):
    """
    Method to handle 404 error
    :return:
    """
    err_string = 'Route not found: '+request.path
    flask_app.logger.error(err_string)
    return jsonify({'error': err_string+' '+error}), 404


@flask_app.errorhandler(400)
def handel400(error):
    err_string = str(error) + ' ' + request.path
    flask_app.logger.error(err_string)
    return jsonify({'error': err_string}), 400


@flask_app.errorhandler(500)
def handel500(error):
    flask_app.logger.error(error)
    return jsonify({'error': error}), 500


if __name__ == "__main__":
    flask_app.run(debug=True)
