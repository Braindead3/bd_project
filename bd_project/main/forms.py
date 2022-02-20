from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_product_name = StringField('Product',
                                      validators=[DataRequired()])
    search_submit = SubmitField('Search')


class ReviveForm(FlaskForm):
    revive = TextAreaField('Отзыв', validators=[DataRequired()])
    submit = SubmitField('Отправить')
