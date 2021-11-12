from flask import Blueprint, render_template, redirect, url_for, request, flash
from bd_project.admin.forms import AddUserForm, UpdateUserForm, DeleteUserForm
from bd_project.models import User, Product, Courier, Order, OrderList
from bd_project import bcrypt

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def admin_page():
    return render_template('admin_pages/admin.html', title='admin')


@admin.route('/admin/users?<int:user_id>', methods=['GET', 'POST'])
def users_table(user_id):
    users = User.select()
    add_form = AddUserForm()
    delete_form = DeleteUserForm()
    delete_form.select_del_user.choices = [(g.id, g.username) for g in users]
    update_form = UpdateUserForm()
    selected_username = 'None'
    upd_user = User.get_or_none(User.id == user_id)
    update_form.updated_user = upd_user
    if add_form.add_submit.data and add_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(add_form.password.data).decode('utf-8')
        user = User(username=add_form.username_add_form.data, email=add_form.email.data, password=hashed_password,
                    phone=add_form.phone.data,
                    address=add_form.address.data)
        user.save()
        return redirect(url_for('admin.users_table', user_id=0))
    if delete_form.del_submit.data and delete_form.validate_on_submit():
        user = User.get(
            User.username == dict(delete_form.select_del_user.choices).get(delete_form.select_del_user.data))
        user.delete_instance(recursive=True)
        return redirect(url_for('admin.users_table', user_id=0))
    if update_form.submit_update.data and update_form.validate_on_submit():
        user = User.get(User.id == user_id)
        user.username = update_form.username_update.data
        user.email = update_form.email_update.data
        user.phone = update_form.phone_update.data
        user.address = update_form.address_update.data
        user.save()
        flash('Update successful', 'successful')
        return redirect(url_for('admin.users_table', user_id=0))
    elif request.method == 'GET':
        if upd_user:
            update_form.username_update.data = upd_user.username
            update_form.email_update.data = upd_user.email
            update_form.phone_update.data = upd_user.phone
            update_form.address_update.data = upd_user.address
            selected_username = upd_user.username
    return render_template('admin_pages/table_users.html', title='users', users=users, add_form=add_form,
                           delete_form=delete_form, update_form=update_form, selected_username=selected_username)
