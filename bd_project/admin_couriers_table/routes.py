from flask import Blueprint, render_template, flash, redirect, request, url_for
from bd_project.models import Courier
from bd_project.admin_couriers_table.utils import (init_forms_and_couriers, add_courier, update_courier,
                                                   set_updating_form_fields)

admin_couriers_table = Blueprint('admin_couriers_table', __name__)


@admin_couriers_table.route('/admin_tables/couriers/', methods=['GET'])
def couriers_table():
    add_form, delete_form, update_form, couriers = init_forms_and_couriers()
    delete_form.select_del.choices = [(g.id, g.name) for g in couriers]
    return render_template('admin_pages/table_couriers.html', couriers=couriers, add_form=add_form,
                           delete_form=delete_form, update_form=update_form)


@admin_couriers_table.route('/admin_tables/couriers/add', methods=['POST'])
def courier_creation():
    add_form, delete_form, update_form, couriers = init_forms_and_couriers()
    if add_form.submit_add.data and add_form.validate_on_submit():
        add_courier(add_form)
        flash('Add successful', 'success')
        return redirect(url_for('admin_couriers_table.couriers_table'))
    return render_template('admin_pages/table_couriers.html', couriers=couriers, add_form=add_form,
                           delete_form=delete_form, update_form=update_form)


@admin_couriers_table.route('/admin_tables/couriers/delete', methods=['POST'])
def courier_removing():
    add_form, delete_form, update_form, couriers = init_forms_and_couriers()
    delete_form.select_del.choices = [(g.id, g.name) for g in couriers]
    if delete_form.del_submit.data and delete_form.validate_on_submit():
        courier = Courier.get(Courier.id == delete_form.select_del.data)
        courier.delete_instance()
        flash('Delete successful', 'success')
        return redirect(url_for('admin_couriers_table.couriers_table'))
    return render_template('admin_pages/table_couriers.html', couriers=couriers, add_form=add_form,
                           delete_form=delete_form, update_form=update_form)


@admin_couriers_table.route('/admin_tables/couriers/update/<int:courier_id>', methods=['GET', 'POST'])
def courier_updating(courier_id):
    add_form, delete_form, update_form, couriers = init_forms_and_couriers()
    update_form.updated_courier = Courier.get(Courier.id == courier_id)
    select_courier = 'None'
    if update_form.submit_update.data and update_form.validate_on_submit():
        update_courier(courier_id, update_form)
        flash('Update successful', 'success')
        return redirect(url_for('admin_couriers_table.couriers_table'))
    elif request.method == 'GET':
        select_courier = set_updating_form_fields(update_form)
    return render_template('admin_pages/table_couriers.html', couriers=couriers, add_form=add_form,
                           delete_form=delete_form, update_form=update_form, select_courier=select_courier)
