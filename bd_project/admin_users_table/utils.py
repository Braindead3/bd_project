from bd_project.admin_users_table.forms import AddUserForm, DeleteUserForm, UpdateUserForm
from bd_project.models import User
from bd_project import bcrypt


def update_user(user_id, form):
    user = User.get_or_none(User.id == user_id)
    if user:
        user.username = form.username_update.data
        user.email = form.email_update.data
        user.phone = form.phone_update.data
        user.address = form.address_update.data
        user.save()


def set_update_form_fields_values(form, user_id):
    user = User.get_or_none(User.id == user_id)
    if user:
        form.username_update.data = user.username
        form.email_update.data = user.email
        form.phone_update.data = user.phone
        form.address_update.data = user.address
        selected_username = user.username
        return selected_username
    return 'None'


def add_user(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username_add_form.data, email=form.email.data, password=hashed_password,
                phone=form.phone.data,
                address=form.address.data)
    user.save()


def init_users_forms_and_users():
    users = User.select()
    add_form = AddUserForm()
    delete_form = DeleteUserForm()
    update_form = UpdateUserForm()
    return users, add_form, delete_form, update_form
