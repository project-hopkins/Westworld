import json
from datetime import datetime
from flask import Blueprint, jsonify, request, g

order_api = Blueprint('orderApi', __name__)


@order_api.route('/order', strict_slashes=False, methods=['GET'])
def get_user_orders() -> dict:
    """
    returns all the orders for user as a json array
    :return:
    """
    from hopkin.models.orders import Order

    # get all orders
    orders = Order.get_all(str(g.user_id))
    orders_list = []
    # create response
    for order in orders:
        items_list = []
        for item in order['items']:
            items_list.append({'itemId': item['itemId'], 'quantity': item['quantity']})
        orders_list.append({
            "_id": str(order['_id']),
            "items": items_list,
            "total": str(order['total']),
            "delivery": str(order['delivery']),
            "date": datetime.strptime(order['date'], '%d:%m:%Y')
        })

    orders_list.sort(key=lambda o: o['date'], reverse=True)
    return jsonify({'data': {'orders': orders_list}})


@order_api.route('/order/add', strict_slashes=False, methods=['POST'])
def add_order() -> tuple:
    """
    Adds a new order to the database 
    :return: 
    """
    from hopkin.models.orders import Order

    if request.json is not None:
        # find specific item
        items = []

        for item in request.json['items']:
            key, value = item.popitem()
            items.append({'itemId': key, 'quantity': value})

        new_order = {
            'items': items,
            'total': request.json['price'],
            'userId': str(g.user_id),
            'delivery': request.json['delivery'],
            'date': request.json['date']
        }
        new_order_id = Order.insert(new_order)

        # returns a message
        return jsonify({'data': {
            'message': 'order added with id ' + str(new_order_id),
            'orderId': str(new_order_id)
        }})
    else:
        return jsonify({'error': 'no order placed'}), 401

