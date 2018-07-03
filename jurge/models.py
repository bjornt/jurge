import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .database import Base


class Language(Base):
    __tablename__ = 'language'

    id = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    currency = sa.Column(sa.String, nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)


class ProductInfo(Base):
    __tablename__ = 'product_info'

    language_id = sa.Column(
        sa.Integer, sa.ForeignKey('language.id'), primary_key=True)
    language = relationship('Language')
    product_id = sa.Column(
        sa.Integer, sa.ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')
    description = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Numeric(2), nullable=False)
