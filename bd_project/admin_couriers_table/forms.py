from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from bd_project.models import Courier
import phonenumbers


class AddCourierForm(FlaskForm):
    name_add = StringField('Courier name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone_add = StringField('Phone',
                            validators=[DataRequired()])
    address_add = StringField('Address',
                              validators=[DataRequired()])
    submit_add = SubmitField('Add Courier')

    @staticmethod
    def validate_username_add_form(self, name_add_form):
        user = Courier.get_or_none(Courier.name == name_add_form.data)
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    @staticmethod
    def validate_phone(self, phone):
        if len(phone.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(phone.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            raise ValidationError('Invalid phone number.')


class DeleteCourierForm(FlaskForm):
    select_del = SelectField('Select Courier', coerce=int)
    del_submit = SubmitField('Delete Courier')


class UpdateCourierForm(FlaskForm):
    name_update = StringField('Username',
                              validators=[DataRequired(), Length(min=2, max=20)])
    phone_update = StringField('Phone',
                               validators=[DataRequired()])
    address_update = StringField('Address',
                                 validators=[DataRequired()])
    submit_update = SubmitField('Update Courier')
    updated_courier = None

    @staticmethod
    def validate_username_add_form(self, name_add_form):
        if self.updated_courier:
            if self.updated_courier.name != name_add_form.data:
                user = Courier.get_or_none(Courier.name == name_add_form.data)
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')

    @staticmethod
    def validate_phone(self, phone):
        if self.updated_courier:
            if self.updated_courier.phone != phone.data:
                if len(phone.data) > 16:
                    raise ValidationError('Invalid phone number.')
                try:
                    input_number = phonenumbers.parse(phone.data)
                    if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError('Invalid phone number.')
                except:
                    raise ValidationError('Invalid phone number.')
