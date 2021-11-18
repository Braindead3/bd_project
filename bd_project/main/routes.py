import json

from flask import render_template, Blueprint
from flask_login import current_user
from bd_project.models import Product

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    order_products_by_current_user = None
    if current_user.is_authenticated:
        with open('ordered_products.json', 'r') as f:
            order_products_by_users = json.load(f)
            order_products_by_current_user = order_products_by_users.get(f'{current_user.id}')
    products = Product.select()
    return render_template('home.html', title='Home page', products=products,
                           order_products=order_products_by_current_user)


@main.route('/admin_tables')
def admin_page():
    return render_template('admin_pages/admin.html', title='admin_users_table')
