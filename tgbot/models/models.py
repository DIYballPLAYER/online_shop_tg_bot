from gino import Gino
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger

db = Gino()


class Users(db.Model):

    __tablename__ = 'users'

    tg_id = Column(Integer(), primary_key=True)


class Products(db.Model):

    __tablename__ = 'products'

    Id = Column(Integer(), primary_key=True)
    name = Column(String(60))
    photo_url = Column(String(150), unique=True)
    description = Column(String(600))
    price = Column(Integer())
    category = Column(ForeignKey('category.Id'))


class Category(db.Model):

    __tablename__ = 'category'

    Id = Column(Integer(), primary_key=True)
    name = Column(String(150))


class Cart(db.Model):

    __tablename__ = "cart"

    Id = Column(Integer(), primary_key=True)
    user_id = Column(ForeignKey("users.tg_id"))


class CartProducts(db.Model):

    __tablename__ = "cart products"

    Id = Column(Integer(), primary_key=True)
    cart_id = Column(ForeignKey("cart.Id"))
    products_id = Column(ForeignKey("products.Id"))
    amount = Column(BigInteger(), default=0)
