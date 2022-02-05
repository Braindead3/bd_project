import json

from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user
from playhouse.flask_utils import object_list
from bd_project.classes import UserHelper

from bd_project.main.forms import SearchForm
from bd_project.models import Product

main = Blueprint('main', __name__)

sel_category = None


def choose_categories():
    all_products = Product.select()
    product_categories = set()
    for product in all_products:
        product_categories.add(product.category)
    return list(product_categories)


def current_user_ordered_products():
    order_products_by_current_user = None
    if current_user.is_authenticated:
        with open('ordered_products.json', 'r') as f:
            order_products_by_users = json.load(f)
            order_products_by_current_user = order_products_by_users.get(f'{current_user.id}')
    return order_products_by_current_user


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    global sel_category
    sel_category = None
    product_categories = choose_categories()
    form = SearchForm()
    order_products_by_current_user = current_user_ordered_products()
    order_price = UserHelper.order_price(order_products_by_current_user)
    if form.validate_on_submit():
        products = Product.select().where(Product.name.contains(f'{form.search_product_name.data.capitalize()}'))
        if not products:
            flash('Nothing found', 'danger')
            products = Product.select()
    else:
        products = Product.select()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=9,
                       order_products=order_products_by_current_user, form=form, categories=product_categories,
                       order_price=order_price)


@main.route('/admin_tables')
def admin_page():
    return render_template('admin_pages/admin.html', title='admin_users_table')


@main.route('/filtered_products/<category>')
def filter_products_by_category(category):
    global sel_category
    sel_category = category
    product_categories = choose_categories()
    form = SearchForm()
    products = Product.select().where(Product.category == sel_category)
    order_products_by_current_user = current_user_ordered_products()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=10,
                       order_products=order_products_by_current_user, form=form, categories=product_categories)


@main.route('/filtered_products/price')
def filter_products_by_cost():
    product_categories = choose_categories()
    form = SearchForm()
    if sel_category:
        products = Product.select().where(Product.category == sel_category).order_by(Product.price)
    else:
        products = Product.select().order_by(Product.price)
    order_products_by_current_user = current_user_ordered_products()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=10,
                       order_products=order_products_by_current_user, form=form, categories=product_categories)


@main.route('/filtered_products/price_desc')
def filter_products_by_cost_desc():
    product_categories = choose_categories()
    form = SearchForm()
    if sel_category:
        products = Product.select().where(Product.category == sel_category).order_by(Product.price.desc())
    else:
        products = Product.select().order_by(Product.price.desc())
    order_products_by_current_user = current_user_ordered_products()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=10,
                       order_products=order_products_by_current_user, form=form, categories=product_categories)
