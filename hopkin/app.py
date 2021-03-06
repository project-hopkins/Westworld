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
flask_app.url_map.strict_slashes = False
flask_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
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
        no_auth_paths = ['/spec', '/favicon.ico', '/item', '/login', '/restaurant']
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


############### Error Handling #########################

def generate_error_response(error):
    err_string = str(error.code) + '' + request.path + ' ' + error.description
    flask_app.logger.error(err_string)
    return jsonify({'error': err_string}), error.code


@flask_app.errorhandler(404)
def handel404(error):
    """
    Method to handle 404 error
    :return:
    """
    return generate_error_response(error)


@flask_app.errorhandler(400)
def handel400(error):
    return generate_error_response(error)


@flask_app.errorhandler(500)
def handel500(error):
    flask_app.logger.error(str(error.args[0]))
    return jsonify({'error': str(error.args[0])}), 500


if __name__ == "__main__":
    flask_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    flask_app.run(debug=False)
