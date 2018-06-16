from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from .server import app

__all__ = ['db']


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///jurge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Language(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class ProductInfo(db.Model):

    language_id = db.Column(
        db.Integer, db.ForeignKey('language.id'), primary_key=True)
    language = relationship('language')
    product_id = db.Column(
        db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product = relationship('product')
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(2), nullable=False)
