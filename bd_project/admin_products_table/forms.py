from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from bd_project.models import Product


class AddProductForm(FlaskForm):
    name_add = StringField('Product name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    price_add = FloatField('Product price', validators=[DataRequired()])
    description_add = StringField('Product description', validators=[DataRequired()])
    weight_add = IntegerField('Product weight', validators=[DataRequired()])
    image_add = FileField('Product picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp'])])
    submit_add = SubmitField('Add')

    @staticmethod
    def validate_name_add(self, name_add):
        product = Product.get_or_none(Product.name == name_add.data)
        if product:
            raise ValidationError('That product name is taken. Please choose a different one.')


class UpdateProductForm(FlaskForm):
    name_update = StringField('Product name',
                              validators=[DataRequired(), Length(min=2, max=20)])
    price_update = FloatField('Product price', validators=[DataRequired()])
    description_update = StringField('Product description', validators=[DataRequired()])
    weight_update = IntegerField('Product weight', validators=[DataRequired()])
    image_update = FileField('Update product picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp'])])
    submit_update = SubmitField('Update')
    updated_product = None

    @staticmethod
    def validate_name_add(self, name_add):
        if self.updated_product:
            if self.updated_product.name != name_add.data:
                product = Product.get(Product.name == name_add.data)
                if product:
                    raise ValidationError('That product name is taken. Please choose a different one.')


class DeleteProductForm(FlaskForm):
    select_delete = SelectField('Select product', coerce=int)
    submit_delete = SubmitField('Delete')
