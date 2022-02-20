import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bd_project.models import User


class AddUserForm(FlaskForm):
    username_add_form = StringField('Имя пользователя',
                                    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])
    phone = StringField('Телефон',
                        validators=[DataRequired()])
    address = StringField('Адрес',
                          validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    add_submit = SubmitField('Добавить пользователя')

    @staticmethod
    def validate_username_add_form(self, username_add_form):
        user = User.get_or_none(User.username == username_add_form.data)
        if user:
            raise ValidationError('Такое имя пользователя уже существует. Выберите другое пожалуйста.')

    @staticmethod
    def validate_email(self, email):
        user = User.get_or_none(User.email == email.data)
        if user:
            raise ValidationError('Такая почта уже существует. Выберите другую пожалуйста.')

    @staticmethod
    def validate_phone(self, phone):
        if len(phone.data) > 16:
            raise ValidationError('Неправильный номер телефона.')
        try:
            input_number = phonenumbers.parse(phone.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Неправильный номер телефона.')
        except:
            raise ValidationError('Неправильный номер телефона.')


class DeleteUserForm(FlaskForm):
    select_del_user = SelectField('Выбирите пользователя', coerce=int)
    del_submit = SubmitField('Удалить пользователя')


class UpdateUserForm(FlaskForm):
    username_update = StringField('Имя пользователя',
                                  validators=[DataRequired(), Length(min=2, max=20)])
    email_update = StringField('Почта',
                               validators=[DataRequired(), Email()])
    phone_update = StringField('Телефон',
                               validators=[DataRequired()])
    address_update = StringField('Домашний адрес',
                                 validators=[DataRequired()])
    submit_update = SubmitField('Изменить пользователя')
    updated_user = None

    @staticmethod
    def validate_username_update(self, username_update):
        if self.updated_user:
            if self.updated_user.username != username_update.data:
                user = User.get_or_none(User.username == username_update.data)
                if user:
                    raise ValidationError('Такое имя пользователя уже существует. Выберите другое пожалуйста.')

    @staticmethod
    def validate_email_update(self, email_update):
        if self.updated_user:
            if self.updated_user.email != email_update.data:
                user = User.get_or_none(User.email == email_update.data)
                if user:
                    raise ValidationError('Такая почта уже существует. Выберите другую пожалуйста.')

    @staticmethod
    def validate_phone_update(self, phone_update):
        if self.updated_user:
            if self.updated_user.phone != phone_update.data:
                if len(phone_update.data) > 16:
                    raise ValidationError('Неправильный номер телефона.')
                try:
                    input_number = phonenumbers.parse(phone_update.data)
                    if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError('Неправильный номер телефона.')
                except:
                    raise ValidationError('Неправильный номер телефона.')
