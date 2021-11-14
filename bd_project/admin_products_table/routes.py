from flask import Blueprint, render_template, redirect, url_for, flash, request
from bd_project.admin_products_table.forms import AddProductForm, DeleteProductForm, UpdateProductForm
from bd_project.models import Product
from bd_project.admin_products_table.utils import (save_picture, init_forms, add_product, set_updated_form_fields,
                                                   update_product)

admin_products_table = Blueprint('admin_products_table', __name__)


@admin_products_table.route('/admin_tables/products/', methods=['GET'])
def products_table():
    selected_product = 'None'
    add_form, delete_form, update_form, products = init_forms()
    delete_form.select_delete.choices = [(product.id, product.name) for product in products]
    return render_template('admin_pages/table_products.html', add_form=add_form, delete_form=delete_form,
                           update_form=update_form, products=products, selected_product=selected_product)


@admin_products_table.route('/admin_tables/products/add', methods=['POST'])
def product_creation():
    add_form, delete_form, update_form, products = init_forms()
    if add_form.submit_add.data and add_form.validate_on_submit():
        add_product(add_form)
        flash('Add successful', 'success')
        return redirect(url_for('admin_products_table.products_table'))
    return render_template('admin_pages/table_products.html', add_form=add_form, delete_form=delete_form,
                           update_form=update_form, products=products)


@admin_products_table.route('/admin_tables/products/delete', methods=['POST'])
def product_removing():
    add_form, delete_form, update_form, products = init_forms()
    delete_form.select_delete.choices = [(product.id, product.name) for product in products]
    if delete_form.submit_delete.data and delete_form.validate_on_submit():
        product = Product.get(Product.id == delete_form.select_delete.data)
        product.delete_instance(recursive=True)
        flash('Delete successful', 'success')
        return redirect(url_for('admin_products_table.products_table'))
    return render_template('admin_pages/table_products.html', add_form=add_form, delete_form=delete_form,
                           update_form=update_form, products=products)


@admin_products_table.route('/admin_tables/products/update?<int:product_id>', methods=['GET', 'POST'])
def product_updating(product_id):
    selected_product = 'None'
    add_form, delete_form, update_form, products = init_forms()
    delete_form.select_delete.choices = [(product.id, product.name) for product in products]
    update_form.updated_product = Product.get(Product.id == product_id)
    if update_form.submit_update.data and update_form.validate_on_submit():
        update_product(update_form)
        flash('Update successful', 'success')
        return redirect(url_for('admin_products_table.products_table'))
    elif request.method == 'GET':
        selected_product = set_updated_form_fields(update_form)
    return render_template('admin_pages/table_products.html', add_form=add_form, delete_form=delete_form,
                           update_form=update_form, products=products, selected_product=selected_product)
