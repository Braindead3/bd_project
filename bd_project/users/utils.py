import json

from flask import url_for
from flask_login import current_user
from flask_mail import Message
from bd_project import mail
from bd_project.models import OrderList, Product
from bd_project.classes import UserHelper
from bd_project.models import Order


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


def clear_current_user_ordered_products():
    with open('ordered_products.json', 'r') as f:
        order_products = json.load(f)
    order_products[f'{current_user.id}'] = []
    with open('ordered_products.json', 'w') as f:
        json.dump(order_products, f, indent=2)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Сброс пароля', sender='vladislavBlog@gmail.com', recipients=[user.email])
    msg.body = f'''
Что бы сбросить пароль перейдите по ссылке:
{url_for('users.reset_token', token=token, _external=True)}
Если вы не делали этого запроса проигнорируйте сообщение.
'''
    mail.send(msg)


def send_sales_receipt(user, ordered_products):
    last_order = Order.select().order_by(Order.id.desc()).get()
    msg = Message(f'Чек для заказа из магазина зефира "Влад магазин"', sender='vladislavBlog@gmail.com',
                  recipients=[user.email])
    order_sum = UserHelper.order_price(ordered_products)
    receipt = f'Ваш заказ номер:{last_order.id}\n'
    for products in ordered_products:
        for pr_id, product in products.items():
            receipt += f'Продукт: {product.get("product")} - {product.get("amount")}\n'
    receipt += f'Сумма заказа: {order_sum}.'
    print(receipt)
    msg.body = receipt
    mail.send(msg)
