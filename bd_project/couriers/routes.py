from flask import Blueprint, redirect, url_for, request, flash, render_template, session
from flask_login import login_user
from bd_project.models import Courier, Order
from bd_project.couriers.forms import LoginForm
from bd_project import bcrypt
from flask_login import current_user

couriers = Blueprint('couriers', __name__)


@couriers.route('/login_courier', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        courier = Courier.get_or_none(Courier.phone == form.phone.data)
        if courier and bcrypt.check_password_hash(courier.password, form.password.data):
            next_page = request.args.get('next')
            flash('You have successfully signed in to your account!', 'success')
            session['courier'] = courier.id
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Log In unsuccessful. Please check phone and password.', 'danger')
    return render_template('login_courier.html', title='Login', form=form)


@couriers.route('/logout_courier')
def logout():
    session.pop('courier', None)
    return redirect(url_for('main.home'))


@couriers.route('/orders')
def current_courier_orders():
    courier = Courier.get(session['courier'])
    return render_template('current_orders.html', orders=courier.orders)


@couriers.route('/complete_order/<int:order_id>')
def complete_order(order_id):
    order = Order.get_by_id(order_id)
    order.status = 'done'
    order.save()
    return redirect(url_for('couriers.current_courier_orders'))
