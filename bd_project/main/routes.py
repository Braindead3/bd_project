import json

from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user
from playhouse.flask_utils import object_list
from bd_project.classes import UserHelper

from bd_project.main.forms import SearchForm, ReviveForm
from bd_project.models import Product, Categories, ProductReviews

main = Blueprint('main', __name__)

sel_category = None


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
    product_categories = Categories.select()
    form = SearchForm()
    try:
        order_products_by_current_user = current_user_ordered_products()
    except json.decoder.JSONDecodeError:
        order_products_by_current_user = None
    order_price = UserHelper.order_price(order_products_by_current_user)
    if form.validate_on_submit():
        products = Product.select().where(Product.name.contains(f'{form.search_product_name.data.capitalize()}'))
        if not products:
            flash('Ничего не найдено', 'danger')
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
    product_categories = Categories.select()
    form = SearchForm()
    products = Product.select().where(Product.category == sel_category)
    order_products_by_current_user = current_user_ordered_products()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=9,
                       order_products=order_products_by_current_user, form=form, categories=product_categories)


@main.route('/filtered_products/price')
def filter_products_by_cost():
    product_categories = Categories.select()
    form = SearchForm()
    if sel_category:
        products = Product.select().where(Product.category == sel_category).order_by(Product.price)
    else:
        products = Product.select().order_by(Product.price)
    order_products_by_current_user = current_user_ordered_products()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=9,
                       order_products=order_products_by_current_user, form=form, categories=product_categories)


@main.route('/filtered_products/price_desc')
def filter_products_by_cost_desc():
    product_categories = Categories.select()
    form = SearchForm()
    if sel_category:
        products = Product.select().where(Product.category == sel_category).order_by(Product.price.desc())
    else:
        products = Product.select().order_by(Product.price.desc())
    order_products_by_current_user = current_user_ordered_products()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=9,
                       order_products=order_products_by_current_user, form=form, categories=product_categories)


@main.route('/product/<product_id>', methods=['GET', 'POST'])
def product_revive(product_id):
    form = ReviveForm()
    product = Product.get(Product.id == product_id)
    revives = product.revives
    if form.validate_on_submit():
        revive = ProductReviews(review=form.revive.data, user_id=current_user.id, product_id=product_id)
        revive.save()
        form.revive.data = ''
        return redirect(url_for('main.product_revive', product_id=product_id))
    return render_template('product_revives.html', product=product, revives=revives, form=form)
