import json
from playhouse.flask_utils import object_list
from flask import render_template, Blueprint

from flask import render_template, Blueprint, flash
from flask_login import current_user
from bd_project.models import Product
from bd_project.main.forms import SearchForm

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    order_products_by_current_user = None
    form = SearchForm()
    if current_user.is_authenticated:
        with open('ordered_products.json', 'r') as f:
            order_products_by_users = json.load(f)
            order_products_by_current_user = order_products_by_users.get(f'{current_user.id}')
    products = Product.select()
    if form.validate_on_submit():
        products = Product.select().where(Product.name.startswith(f'{form.search_product_name.data}'))
        if not products:
            flash('Nothing found', 'success')
    else:
        products = Product.select()
    return object_list('home.html', title='Home page', query=products, context_variable='products', paginate_by=2,
                       order_products=order_products_by_current_user, form=form)


@main.route('/admin_tables')
def admin_page():
    return render_template('admin_pages/admin.html', title='admin_users_table')
