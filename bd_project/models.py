from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from peewee import *
from datetime import datetime
from bd_project import login_manager, db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class User(BaseModel, UserMixin):
    username = CharField(max_length=20, unique=True, null=False)
    email = CharField(max_length=20, unique=True, null=False)
    phone = CharField(max_length=15, unique=True, null=False)
    address = CharField(max_length=20, null=False)
    password = CharField(max_length=60, null=False)

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        user_id = s.loads(token).get('user_id')
        if user_id is None:
            return None
        return User.get_by_id(user_id)

    def __repr__(self):
        return f'User("{self.username}","{self.email},"{self.phone},"{self.address}")'

    class Meta:
        db_table = 'Users'


class Courier(BaseModel):
    name = CharField(max_length=20, unique=True, null=False)
    phone = CharField(max_length=15, unique=True, null=False)
    address = CharField(max_length=20, null=False)
    password = CharField(null=False)

    def __repr__(self):
        return f'Courier("{self.name}","{self.phone}","{self.address}")'

    class Meta:
        db_table = 'Couriers'


class Categories(BaseModel):
    category = CharField(max_length=20, null=False)

    def __repr__(self):
        return f'Product("{self.category}")'

    class Meta:
        db_table = 'Categories'


class Product(BaseModel):
    name = CharField(unique=True, null=False)
    price = DoubleField(null=False)
    description = TextField(null=False)
    weight = IntegerField(null=False)
    image = CharField(null=False)
    category = ForeignKeyField(Categories, backref='category')

    def __repr__(self):
        return f'Product("{self.name}","{self.price}","{self.description},{self.weight},{self.image}")'

    class Meta:
        db_table = 'Products'


class Order(BaseModel):
    user_id = ForeignKeyField(User, backref='orders', null=False)
    courier_id = ForeignKeyField(Courier, backref='orders', null=True)
    address = CharField(max_length=20, null=False)
    time_creation = DateTimeField(default=datetime.utcnow(), null=False)
    time_of_delivery = DateTimeField(null=False)
    status = CharField(max_length=10, default='not done')

    def __repr__(self):
        return f'OrderList("{self.order_id}","{self.product_id},{self.amount}")'

    class Meta:
        db_table = 'Orders'


class OrderList(BaseModel):
    order_id = ForeignKeyField(Order, backref='products')
    product_id = ForeignKeyField(Product, backref='orders', null=False)
    amount = IntegerField(null=False)

    def __repr__(self):
        return f'OrderList("{self.order_id}","{self.product_id},{self.amount}")'

    class Meta:
        db_table = 'OrderList'


class ProductReviews(BaseModel):
    review = TextField()
    user_id = ForeignKeyField(User, backref='revives')
    product_id = ForeignKeyField(Product, backref='revives')

    def __repr__(self):
        return f'Product("{self.review},"{self.user_id}")'

    class Meta:
        db_table = 'ProductReviews'


def create_db():
    with db:
        db.create_tables([ProductReviews])
