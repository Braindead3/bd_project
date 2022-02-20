from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from bd_project.models import Product


class AddProductForm(FlaskForm):
    name_add = StringField('Название продукта',
                           validators=[DataRequired(), Length(min=2, max=20)])
    price_add = FloatField('Цена', validators=[DataRequired()])
    description_add = StringField('Описание', validators=[DataRequired()])
    weight_add = IntegerField('Вес', validators=[DataRequired()])
    category_add = SelectField('Категория', coerce=int)
    image_add = FileField('Картинка')
    submit_add = SubmitField('Добавить')

    @staticmethod
    def validate_name_add(self, name_add):
        product = Product.get_or_none(Product.name == name_add.data)
        if product:
            raise ValidationError('Такой продукт уже существует. Введите другое название.')


class UpdateProductForm(FlaskForm):
    name_update = StringField('Название',
                              validators=[DataRequired(), Length(min=2, max=20)])
    price_update = FloatField('Цена', validators=[DataRequired()])
    description_update = StringField('Описание', validators=[DataRequired()])
    weight_update = IntegerField('Вес', validators=[DataRequired()])
    category_update = SelectField('Выберите категорию', coerce=int)
    image_update = FileField('Картинка')
    submit_update = SubmitField('Обновить')
    updated_product = None

    @staticmethod
    def validate_name_add(self, name_add):
        if self.updated_product:
            if self.updated_product.name != name_add.data:
                product = Product.get(Product.name == name_add.data)
                if product:
                    raise ValidationError('Такой продукт уже существует. Введите другое название.')


class DeleteProductForm(FlaskForm):
    select_delete = SelectField('Выбирите продукт', coerce=int)
    submit_delete = SubmitField('Удалить')
