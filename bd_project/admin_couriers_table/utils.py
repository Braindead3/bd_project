from bd_project.admin_couriers_table.forms import AddCourierForm, UpdateCourierForm, DeleteCourierForm
from bd_project.models import Courier
from bd_project import bcrypt


def init_forms_and_couriers():
    add_form = AddCourierForm()
    delete_form = DeleteCourierForm()
    update_form = UpdateCourierForm()
    couriers = Courier.select()
    return add_form, delete_form, update_form, couriers


def add_courier(form):
    hashed_password = bcrypt.generate_password_hash(form.password_add.data).decode('utf-8')
    courier = Courier(name=form.name_add.data, phone=form.phone_add.data, address=form.address_add.data,
                      password=hashed_password)
    courier.save()


def update_courier(courier_id, form):
    courier = Courier.get_or_none(Courier.id == courier_id)
    if courier:
        courier.name = form.name_update.data
        courier.phone = form.phone_update.data
        courier.address = form.address_update.data
        courier.save()


def set_updating_form_fields(form):
    if form.updated_courier:
        form.name_update.data = form.updated_courier.name
        form.phone_update.data = form.updated_courier.phone
        form.address_update.data = form.updated_courier.address
        selected_courier = form.updated_courier.name
        return selected_courier
    return 'None'
