import json
from flask import Blueprint, jsonify, request, g

item_api = Blueprint('itemApi', __name__)


def get_item_as_object(item):
    return {
        "_id": str(item['_id']),
        "name": item['name'],
        "description": item['description'],
        "imageURL": item['imageURL'],
        "price": item['price'],
        "calories": item['calories'],
        "category": item['category'],
        "tags": item['tags'],
        "isRecommended": item['isRecommended']
    }


@item_api.route('/item', methods=['GET'])
def get_all_items() -> tuple:
    """
    swagger_from_file: ../swagger/item/getItems.yml

    returns all the items as a json array
    :return:
    """
    from hopkin.models.items import Item
    # get all items
    items = Item.get_all()
    # create items list
    items_list = []
    # create response
    for item in items:
        items_list.append(get_item_as_object(item))
    return jsonify({'data': {'items': items_list}})


@item_api.route('/item/id/<item_id>', methods=['GET'])
def get_item_by_id(item_id) -> tuple:
    """
    swagger_from_file: ../swagger/item/getItem.yml

    returns one item as a json array
    :return:
    """
    from hopkin.models.items import Item
    # find specific item
    item = Item.get_by_id(item_id)

    return jsonify({'data': {'item': get_item_as_object(item)}})


@item_api.route('/item/category/<category>', methods=['GET'])
def get_item_by_category(category) -> tuple:
    """
    swagger_from_file: ../swagger/item/getItemsByCategory.yml

    returns all the items in a category as a json array
    :return:
    """
    from hopkin.models.items import Item
    # find items by category
    items = Item.get_by_category(category)
    # create items list
    items_list = []
    # create response
    for item in items:
        items_list.append(get_item_as_object(item))
    return jsonify({'data': {'items': items_list}})


@item_api.route('/item/category/<category>/count', methods=['GET'])
def get_category_count(category) -> tuple:
    """
    swagger_from_file: ../swagger/item/getNumItemsInCat.yml
    Returns the number items in that category

    :param category: 
    :return: 
    """
    json_response = get_item_by_category(category)
    return jsonify({'data': {'count': len(json.loads(json_response.data)['data']['items'])}})


@item_api.route('/item/search', methods=['GET'])
def search_item() -> tuple:
    """
    swagger_from_file: ../swagger/item/searchItem.yml
    Searches items if query less that 3 
    it only searches the name else it will
    search the names and tags
    :return: 
    """
    from hopkin.models.items import Item
    items_list = []
    query: str = request.args['q']

    if not len(query) > 0:
        return jsonify({'error': 'no search results provided'})

    query = query.title()
    items = list(Item.get_by_name_search(query.lower()))
    if len(query) > 3:
        items = items + list(Item.get_by_tag_starts_with(query.lower()))

    unique_ids = []

    for item in items:
        if str(item['_id']) not in unique_ids:
            items_list.append({
                "_id": str(item['_id']),
                "name": item['name'],
                "description": item['description'],
                "imageURL": item['imageURL'],
                "price": item['price'],
                "calories": item['calories'],
                "category": item['category'],
                "tags": item['tags'],
                "isRecommended": item['isRecommended']
            })
            unique_ids.append(str(item['_id']))

    return jsonify({'data': {'items': items_list}})


@item_api.route('/admin/item/add', methods=['POST'])
def add_new_item() -> tuple:
    """
    swagger_from_file: ../swagger/item/itemAdd.yml
    adds an item to the database and returns it in a JSON object
    :return:
    """
    from hopkin.models.items import Item
    if request.json is not None and g.is_admin:
        new_item = {
            'name': request.json['name'],
            'description': request.json['description'],
            'imageURL': request.json['imageURL'],
            'price': request.json['price'],
            'calories': request.json['calories'],
            'category': request.json['category'],
            'tags': request.json['tags'],
            "isRecommended": request.json['isRecommended']
        }

        new_item_id = Item.insert(new_item)

        return jsonify({'data': {'item': request.json, 'itemId': str(new_item_id)}})
    return jsonify({'error': 'invalid item' + request.json}), 403


@item_api.route('/admin/item/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
    """
    swagger_from_file: ../swagger/item/deleteItem.yml
    deletes the selected item from the database
    :return:
    """
    from hopkin.models.items import Item
    # search for item by id
    item = Item.get_by_id(str(item_id))
    if item is not None and g.is_admin:
        # remove item
        Item.remove(item_id)
        return jsonify({'data': {'success': True}})
    return jsonify({'error': 'No item found with id ' + item_id})


@item_api.route('/admin/item/update', methods=['POST'])
def update_item():
    """
    swagger_from_file: ../swagger/item/updateItem.yml
    updated the selected item in the database
    :return:
    """
    from hopkin.models.items import Item

    if request.json is not None:
        item_update = Item.get_by_id(request.json['_id'])
        item_update['calories'] = request.json['calories']
        item_update['category'] = request.json['category']
        item_update['description'] = request.json['description']
        item_update['imageURL'] = request.json['imageURL']
        item_update['name'] = request.json['name']
        item_update['price'] = request.json['price']
        item_update['tags'] = request.json['tags']
        item_update['isRecommended'] = request.json['isRecommended']

        Item.save(item_update)

        return jsonify({'data': {'message': 'Updated with item id: ' + str(item_update['_id']),
                                 'mongo_id': str(item_update['_id'])}
                        })
    return jsonify({'error': 'item not updated'})

@item_api.route('/item/recommendations', methods=['GET'])
def get_recommendations() -> tuple:
    """
    swagger_from_file: ../swagger/item/getRecommended.yml

    returns all the items as a json array
    :return:
    """
    from hopkin.models.items import Item
    # get all items
    items = Item.get_recommended()
    # create items list
    items_list = []
    # create response
    for item in items:
        items_list.append(get_item_as_object(item))
    return jsonify({'data': {'items': items_list}})