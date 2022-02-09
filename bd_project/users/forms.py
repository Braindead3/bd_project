import phonenumbers
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bd_project.models import User
import phonenumbers


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone',
                        validators=[DataRequired()])
    address = StringField('Address',
                          validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_username(self, username):
        user = User.get_or_none(User.username == username.data)
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    @staticmethod
    def validate_email(self, email):
        user = User.get_or_none(User.email == email.data)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    @staticmethod
    def validate_phone(self, phone):
        user = User.get_or_none(User.phone == phone.data)
        if user:
            raise ValidationError('That phone is taken. Please choose a different one.')
        else:
            if len(phone.data) > 16:
                raise ValidationError('Invalid phone number.')
            try:
                input_number = phonenumbers.parse(phone.data)
                if not (phonenumbers.is_valid_number(input_number)):
                    raise ValidationError('Invalid phone number.')
            except:
                raise ValidationError('Invalid phone number.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone',
                        validators=[DataRequired()])
    address = StringField('Address',
                          validators=[DataRequired()])
    submit = SubmitField('Update')

    @staticmethod
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.get_or_none(User.username == username.data)
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    @staticmethod
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.get_or_none(User.email == email.data)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

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


class OrderForm(FlaskForm):
    address = StringField('Адресс', validators=[DataRequired()])
    order_date = DateField('Время и дата заказа', format='%Y-%m-%d',
                           render_kw={'placeholder': '6/20/15 for June 20, 2015'})
    submit = SubmitField('Заказать')


class RequestResetForm(FlaskForm):
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Сброс пароля')

    @staticmethod
    def validate_email(self, email):
        user = User.get_or_none(User.email == email.data)
        if user is None:
            raise ValidationError('Такого аккаунта не существует')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Потдвердите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')
