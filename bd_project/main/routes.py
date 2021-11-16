from flask import render_template, Blueprint
from bd_project.models import Product

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    products = Product.select()
    return render_template('home.html', title='Home page', products=products)


@main.route('/admin_tables')
def admin_page():
    return render_template('admin_pages/admin.html', title='admin_users_table')

