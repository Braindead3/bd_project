import time

from flask import (Blueprint, url_for, redirect, flash, render_template, request)
from flask_login import current_user, login_user, logout_user, login_required
from bd_project import bcrypt
from bd_project.models import User, Product
from bd_project.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
import json

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, phone=form.phone.data,
                    address=form.address.data)
        user.save()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_or_none(User.email == form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have successfully signed in to your account!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Log In unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        updated_user = User.get_by_id(current_user.id)
        updated_user.username = form.username.data
        updated_user.email = form.email.data
        updated_user.phone = form.phone.data
        updated_user.address = form.address.data
        updated_user.save()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.address.data = current_user.address
    return render_template('account.html', title='Account', form=form)


@users.route('/add_to_cart?<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.get(Product.id == product_id)
    with open('ordered_products.json') as f:
        order_products_by_users = json.load(f)
    if f'{current_user.id}' in order_products_by_users:
        for product_or in order_products_by_users.get(f'{current_user.id}'):
            if f'{product_id}' in product_or:
                product_or.get(f'{product_id}')['amount'] = product_or.get(f'{product_id}').get('amount') + 1
                with open('ordered_products.json', 'w') as f:
                    json.dump(order_products_by_users, f, indent=2)
                return redirect(url_for('main.home'))
        order_products_by_users[f'{current_user.id}'].append({
            product_id:
                {
                    'product': product.name,
                    'amount': 1,
                    'price': product.price
                }
        })
    else:
        order_products_by_users[current_user.id] = [{
            product_id:
                {
                    'product': product.name,
                    'amount': 1,
                    'price': product.price
                }
        }]
    with open('ordered_products.json', 'w') as f:
        json.dump(order_products_by_users, f, indent=2)
    return redirect(url_for('main.home'))
