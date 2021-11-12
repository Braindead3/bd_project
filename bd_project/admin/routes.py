from flask import Blueprint, render_template, redirect, url_for, request, flash
from bd_project.admin.user_forms import AddUserForm, UpdateUserForm, DeleteUserForm
from bd_project.models import User, Product, Courier, Order, OrderList
from bd_project import bcrypt
from bd_project.admin.utils import (set_update_form_fields_values, add_user, update_user, init_users_forms_and_users)

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def admin_page():
    return render_template('admin_pages/admin.html', title='admin')


@admin.route('/admin/users/', methods=['GET'])
def users_table():
    selected_username = 'None'
    users, add_form, delete_form, update_form = init_users_forms_and_users()
    delete_form.select_del_user.choices = [(g.id, g.username) for g in users]
    return render_template('admin_pages/table_users.html', title='users', users=users, add_form=add_form,
                           delete_form=delete_form, update_form=update_form, selected_username=selected_username)


@admin.route('/admin/users/add', methods=['POST'])
def user_creation():
    users, add_form, delete_form, update_form = init_users_forms_and_users()
    if add_form.add_submit.data and add_form.validate_on_submit():
        add_user(add_form)
        flash('Add successful', 'success')
        return redirect(url_for('admin.users_table'))
    return render_template('admin_pages/table_users.html', title='users', users=users, add_form=add_form,
                           delete_form=delete_form, update_form=update_form)


@admin.route('/admin/users/delete', methods=['POST'])
def user_removing():
    users, add_form, delete_form, update_form = init_users_forms_and_users()
    delete_form.select_del_user.choices = [(g.id, g.username) for g in users]
    if delete_form.del_submit.data and delete_form.validate_on_submit():
        user = User.get(
            User.username == dict(delete_form.select_del_user.choices).get(delete_form.select_del_user.data))
        user.delete_instance(recursive=True)
        flash('Delete successful', 'success')
        return redirect(url_for('admin.users_table'))
    return render_template('admin_pages/table_users.html', title='users', users=users, add_form=add_form,
                           delete_form=delete_form, update_form=update_form)


@admin.route('/admin/users/update?<int:user_id>', methods=['GET', 'POST'])
def user_updating(user_id):
    selected_username = 'None'
    users, add_form, delete_form, update_form = init_users_forms_and_users()
    upd_user = User.get_or_none(User.id == user_id)
    update_form.updated_user = upd_user
    if update_form.submit_update.data and update_form.validate_on_submit():
        update_user(user_id, update_form)
        flash('Update successful', 'success')
        return redirect(url_for('admin.users_table'))
    elif request.method == 'GET':
        selected_username = set_update_form_fields_values(update_form, user_id)
    return render_template('admin_pages/table_users.html', title='users', users=users, add_form=add_form,
                           delete_form=delete_form, update_form=update_form,
                           selected_username=selected_username)
