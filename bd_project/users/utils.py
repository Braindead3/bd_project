import json

from flask import url_for
from flask_login import current_user
from flask_mail import Message
from bd_project import mail
from bd_project.models import OrderList, Product


def add_current_ordered_products(order_products_by_current_user, order_id):
    for products in order_products_by_current_user:
        for pr_id, product in products.items():
            order_product = OrderList(order_id=order_id, product_id=Product.get(Product.id == pr_id),
                                      amount=product.get('amount'))
            order_product.save()


def get_current_order_products(user_id):
    with open('ordered_products.json', 'r') as f:
        order_products_by_users = json.load(f)
        order_products_by_current_user = order_products_by_users.get(f'{user_id}')
    return order_products_by_current_user if order_products_by_current_user else None


def clear_current_user_ordered_products(order_products_by_users):
    order_products_by_users[f'{current_user.id}'] = []
    with open('ordered_products.json', 'w') as f:
        json.dump(order_products_by_users, f, indent=2)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Сброс пароля', sender='vladislavBlog@gmail.com', recipients=[user.email])
    msg.body = f'''
Что бы сбросить пароль перейдите по ссылке:
{url_for('users.reset_token', token=token, _external=True)}
Если вы не делали этого запроса проигнорируйте сообщение.
'''
    mail.send(msg)
