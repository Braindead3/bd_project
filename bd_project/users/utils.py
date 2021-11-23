import json


def get_current_order_products(user_id):
    with open('ordered_products.json', 'r') as f:
        order_products_by_users = json.load(f)
        order_products_by_current_user = order_products_by_users.get(f'{user_id}')
    return order_products_by_current_user if order_products_by_current_user else None
