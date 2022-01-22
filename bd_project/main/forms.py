from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_product_name = StringField('Product',
                                      validators=[DataRequired()])
    search_submit = SubmitField('Search')
