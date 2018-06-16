import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker


__all__ = ['db_session', 'Base']


engine = sa.create_engine('postgres:///jurge', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


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
    language = relationship('language')
    product_id = sa.Column(
        sa.Integer, sa.ForeignKey('product.id'), primary_key=True)
    product = relationship('product')
    description = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Numeric(2), nullable=False)
