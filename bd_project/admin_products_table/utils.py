import os
import secrets
from PIL import Image
from flask import current_app
from bd_project.admin_products_table.forms import AddProductForm, DeleteProductForm, UpdateProductForm
from bd_project.models import Product


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/food_pics', picture_file_name)

    output_size = (268, 180)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_file_name


def init_forms():
    add_form = AddProductForm()
    delete_form = DeleteProductForm()
    update_form = UpdateProductForm()
    products = Product.select()
    return add_form, delete_form, update_form, products


def add_product(add_form):
    picture_file = save_picture(add_form.image_add.data)
    product = Product(name=add_form.name_add.data, price=add_form.price_add.data,
                      description=add_form.description_add.data,
                      weight=add_form.weight_add.data, image=picture_file)
    product.save()


def set_updated_form_fields(update_form):
    update_form.name_update.data = update_form.updated_product.name
    update_form.price_update.data = update_form.updated_product.price
    update_form.description_update.data = update_form.updated_product.description
    update_form.weight_update.data = update_form.updated_product.weight
    return update_form.name_update.data


def update_product(update_form):
    if update_form.image_update.data:
        picture_file = save_picture(update_form.image_update.data)
        update_form.updated_product.image = picture_file
    update_form.updated_product.name = update_form.name_update.data
    update_form.updated_product.price = update_form.price_update.data
    update_form.updated_product.description = update_form.description_update.data
    update_form.updated_product.weight = update_form.weight_update.data
    update_form.updated_product.save()
