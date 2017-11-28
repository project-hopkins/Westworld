import json
from flask import Blueprint, jsonify, request, g

restaurant_api = Blueprint('restaurant_Api', __name__)


def get_restaurant_as_object(restaurant):
    return {
        "_id": str(restaurant['_id']),
        "address":
            {
                'streetNumber': restaurant['streetNum'],
                'streetName': restaurant['streetName'],
                'city': restaurant['city'],
                'province': restaurant['province'],
                'postalCode': restaurant['postalCode']

            },
        'location':
            {
                'longitude': restaurant['longitude'],
                'latitude': restaurant['latitude']
            }

    }


@restaurant_api.route('/restaurant', strict_slashes=False, methods=['GET'])
def get_all_restaurants() -> tuple:
    """
    swagger_from_file: ../swagger/restaurant/getRestaurants.yml

    returns all the restaurant as a json array
    :return:
    """
    from hopkin.models.restaurants import Restaurant
    # get all restaurant
    restaurants = Restaurant.get_all()
    # create restaurant list
    restaurants_list = []
    # create response
    for restaurant in restaurants:
        restaurants_list.append(get_restaurant_as_object(restaurant))
    return jsonify({'data': {'restaurant': restaurants_list}})


@restaurant_api.route('/restaurant/id/<restaurant_id>', strict_slashes=False, methods=['GET'])
def get_restaurant_by_id(restaurant_id) -> tuple:
    """
    swagger_from_file: ../swagger/restaurant/getRestaurantbyId.yml

    returns one restaurant as a json array
    :return:
    """
    from hopkin.models.restaurants import Restaurant
    # find specific restaurant
    restaurant = Restaurant.get_by_id(restaurant_id)

    return jsonify({'data': {'restaurant': get_restaurant_as_object(restaurant)}})


@restaurant_api.route('/admin/restaurant/add', strict_slashes=False, methods=['POST'])
def add_new_restaurant() -> tuple:
    """
    swagger_from_file: ../swagger/restaurant/addRestaurant.yml
    adds an restaurant to the database and returns it in a JSON object
    :return:
    """
    from hopkin.models.restaurants import Restaurant
    if request.json is not None and g.is_admin:
        new_restaurant = {
                "address":
                    {
                        'streetNumber': request.json['streetNum'],
                        'streetName': request.json['streetName'],
                        'city': request.json['city'],
                        'province': request.json['province'],
                        'postalCode': request.json['postalCode']

                    },
                'location':
                    {
                        'longitude': request.json['longitude'],
                        'latitude': request.json['latitude']
                    }


        }

        new_restaurant_id = Restaurant.insert(new_restaurant)

        return jsonify({'data': {'restaurant': request.json, 'restaurantId': str(new_restaurant_id)}})
    else:
        return jsonify({'error': 'invalid restaurant' + request.json}), 403


@restaurant_api.route('/admin/restaurant/delete/<restaurant_id>', strict_slashes=False, methods=['POST'])
def delete_restaurant(restaurant_id):
    """
    swagger_from_file: ../swagger/restaurant/deleteRestaurant.yml
    deletes the selected restaurant from the database
    :return:
    """
    from hopkin.models.restaurants import Restaurant
    # search for restaurant by id
    restaurant = Restaurant.get_by_id(str(restaurant_id))
    if restaurant is not None and g.is_admin:
        # remove restaurant
        Restaurant.remove(restaurant_id)
        return jsonify({'data': {'success': True}})
    else:
        return jsonify({'error': 'No restaurant found with id ' + restaurant_id})
