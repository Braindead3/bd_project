from flask import render_template, Blueprint

main = Blueprint('main', __name__)

products = [
    {
        'product_id': 1,
        'product_name': 'milk',
        'product_price': 12,
        'description': 'some milk',
        'weight': 2000,
    },
    {
        'product_id': 2,
        'product_name': 'meat',
        'product_price': 25,
        'description': 'some meat',
        'weight': 650,
    },
    {
        'product_id': 2,
        'product_name': 'meat',
        'product_price': 25,
        'description': 'some meat',
        'weight': 650,
    },
    {
        'product_id': 2,
        'product_name': 'meat',
        'product_price': 25,
        'description': 'some meat',
        'weight': 650,
    },
    {
        'product_id': 2,
        'product_name': 'meat',
        'product_price': 25,
        'description': 'some meat',
        'weight': 650,
    },
    {
        'product_id': 2,
        'product_name': 'meat',
        'product_price': 25,
        'description': 'some meat',
        'weight': 650,
    }
]


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home page', products=products)


@main.route('/admin_tables')
def admin_page():
    return render_template('admin_pages/admin.html', title='admin_users_table')
