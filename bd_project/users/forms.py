import phonenumbers
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bd_project.models import User
import phonenumbers


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])
    phone = StringField('Телефон',
                        validators=[DataRequired()])
    address = StringField('Адрес',
                          validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    @staticmethod
    def validate_username(self, username):
        user = User.get_or_none(User.username == username.data)
        if user:
            raise ValidationError('Такое имя пользователя уже существует. Выберите другое пожалуйста.')

    @staticmethod
    def validate_email(self, email):
        user = User.get_or_none(User.email == email.data)
        if user:
            raise ValidationError('Такая почта уже существует. Выберите другую пожалуйста.')

    @staticmethod
    def validate_phone(self, phone):
        user = User.get_or_none(User.phone == phone.data)
        if user:
            raise ValidationError('Такой номер телефона уже существует. Введите другой.')
        else:
            if len(phone.data) > 16:
                raise ValidationError('Неправильный номер телефона.')
            try:
                input_number = phonenumbers.parse(phone.data)
                if not (phonenumbers.is_valid_number(input_number)):
                    raise ValidationError('Неправильный номер телефона.')
            except:
                raise ValidationError('Неправильный номер телефона.')


class LoginForm(FlaskForm):
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])
    phone = StringField('Телефон',
                        validators=[DataRequired()])
    address = StringField('Адрес',
                          validators=[DataRequired()])
    submit = SubmitField('Изменить')

    @staticmethod
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.get_or_none(User.username == username.data)
            if user:
                raise ValidationError('Такое имя пользователя уже существует. Выберите другое пожалуйста.')

    @staticmethod
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.get_or_none(User.email == email.data)
            if user:
                raise ValidationError('Такая почта уже существует. Выберите другую пожалуйста.')

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

