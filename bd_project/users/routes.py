import flask_bcrypt
from flask import (Blueprint, url_for, redirect, flash, render_template, request)
from flask_login import current_user, login_user, logout_user, login_required
from bd_project import bcrypt
from bd_project.models import User, Product, Order, OrderList, Courier
from bd_project.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, OrderForm, RequestResetForm, \
    ResetPasswordForm
import json
from datetime import datetime
from bd_project.users.utils import (get_current_order_products, add_current_ordered_products,
                                    clear_current_user_ordered_products, send_reset_email, send_sales_receipt)
from random import choice
from bd_project.classes import UserHelper

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
    try:
        with open('ordered_products.json') as f:
            order_products_by_users = json.load(f)
    except json.decoder.JSONDecodeError:
        order_products_by_users = {}
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


@users.route('/remove_from_cart?<int:product_id>')
@login_required
def remove_from_cart(product_id):
    with open('ordered_products.json') as f:
        order_products_by_users = json.load(f)
    for product_or in order_products_by_users.get(f'{current_user.id}'):
        if f'{product_id}' in product_or:
            product_or.get(f'{product_id}')['amount'] = product_or.get(f'{product_id}').get('amount') - 1
            if product_or.get(f'{product_id}')['amount'] == 0:
                product_or.pop(f'{product_id}')
    with open('ordered_products.json', 'w') as f:
        json.dump(order_products_by_users, f, indent=2)
    return redirect(url_for('main.home'))


@users.route('/clear_cart')
@login_required
def clear_cart():
    with open('ordered_products.json') as f:
        order_products_by_users = json.load(f)
    clear_current_user_ordered_products()
    return redirect(url_for('main.home'))


@users.route('/order', methods=['GET', 'POST'])
@login_required
def add_order():
    form = OrderForm()
    order_products_by_current_user = UserHelper.current_user_ordered_products()
    order_price = UserHelper.order_price(order_products_by_current_user)
    if form.validate_on_submit():
        order = Order(user_id=current_user, address=form.address.data,
                      time_creation=datetime.utcnow(),
                      time_of_delivery=form.order_date.data)
        order.save()
        add_current_ordered_products(order_products_by_current_user, order.id)
        clear_current_user_ordered_products()
        flash('Ваp заказ принят и чек вышлен на почту.', 'success')
        send_sales_receipt(current_user, order_products_by_current_user)
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.address.data = current_user.address
    return render_template('order.html', order_products=order_products_by_current_user, form=form,
                           order_price=order_price)


@users.route('/current_orders', methods=['GET'])
@login_required
def current_orders():
    orders = current_user.orders
    order_products_by_current_user = get_current_order_products(current_user.id)
    return render_template('current_orders.html', order_products=order_products_by_current_user, orders=orders)


@users.route('/reset_password', methods=['GET', 'POST'])
def send_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.get(User.email == form.email.data)
        send_reset_email(user)
        flash('Письмо было отправлено. Следуйте инструцкиям из письма.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user: User = User.verify_reset_token(token)
    if user is None:
        flash('This is invalid token or expired token', 'warning')
        return redirect(url_for('users.send_reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        user.save()
        flash(f'Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset password', form=form)
