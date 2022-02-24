from flask_login import current_user
import json


class UserHelper:

    @staticmethod
    def order_price(order_products_by_current_user):
        order_price = 0
        if order_products_by_current_user:
            for products in order_products_by_current_user:
                for pr_id, product in products.items():
                    order_price += product.get("price") * product.get('amount')
        return round(order_price, 2)

    @staticmethod
    def current_user_ordered_products():
        order_products_by_current_user = None
        if current_user.is_authenticated:
            with open('ordered_products.json', 'r') as f:
                order_products_by_users = json.load(f)
                order_products_by_current_user = order_products_by_users.get(f'{current_user.id}')
        return order_products_by_current_user

    @staticmethod
    def users_ordered_products():
        order_products_by_current_user = None
        if current_user.is_authenticated:
            with open('ordered_products.json', 'r') as f:
                order_products_by_users = json.load(f)
        return order_products_by_users
