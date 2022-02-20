from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from bd_project.models import Courier
import phonenumbers


class AddCourierForm(FlaskForm):
    name_add = StringField('Имя курьера',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone_add = StringField('Телефон',
                            validators=[DataRequired()])
    address_add = StringField('Адрес проживания',
                              validators=[DataRequired()])
    password_add = StringField('Пароль', validators=[DataRequired()])
    submit_add = SubmitField('Добавить')

    @staticmethod
    def validate_username_add_form(self, name_add_form):
        user = Courier.get_or_none(Courier.name == name_add_form.data)
        if user:
            raise ValidationError('Такой курьер уже существует. Введите другое имя.')

    @staticmethod
    def validate_phone(self, phone):
        if len(phone.data) > 16:
            raise ValidationError('Неправельный номер телефона.')
        try:
            input_number = phonenumbers.parse(phone.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Неправельный номер телефона.')
        except:
            raise ValidationError('Неправельный номер телефона.')


class DeleteCourierForm(FlaskForm):
    select_del = SelectField('Выберите курьера', coerce=int)
    del_submit = SubmitField('Удалить')


class UpdateCourierForm(FlaskForm):
    name_update = StringField('Имя курьера',
                              validators=[DataRequired(), Length(min=2, max=20)])
    phone_update = StringField('Телефон',
                               validators=[DataRequired()])
    address_update = StringField('Адрес',
                                 validators=[DataRequired()])
    submit_update = SubmitField('Изменить')
    updated_courier = None

    @staticmethod
    def validate_username_add_form(self, name_add_form):
        if self.updated_courier:
            if self.updated_courier.name != name_add_form.data:
                user = Courier.get_or_none(Courier.name == name_add_form.data)
                if user:
                    raise ValidationError('Такой курьер уже существует. Введите другое имя.')

    @staticmethod
    def validate_phone(self, phone):
        if self.updated_courier:
            if self.updated_courier.phone != phone.data:
                if len(phone.data) > 16:
                    raise ValidationError('Неправельный номер телефона.')
                try:
                    input_number = phonenumbers.parse(phone.data)
                    if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError('Неправельный номер телефона.')
                except:
                    raise ValidationError('Неправельный номер телефона.')
