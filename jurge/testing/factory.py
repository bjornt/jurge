import decimal
import random

from .. import database
from ..models import Category, Language, Product, ProductInfo


_name_counters = {}


def make_name(prefix):
    counter = _name_counters.setdefault(prefix, 0)
    counter += 1
    _name_counters[prefix] = counter
    return f'{prefix}-{counter}'


def make_price():
    return decimal.Decimal(random.randrange(155, 389))/10


def make_Category(name=None):
    if name is None:
        name = make_name('category')
    category = Category(name=name)
    database.session.add(category)
    return category


def make_Product(name=None, category=None):
    if name is None:
        name = make_name('product')
    if category is None:
        category = make_Category()

    product = Product(name=name, category=category)
    database.session.add(product)
    return product


def make_Language(code=None, name=None, currency=None):
    if code is None:
        code = make_name('code')
    if name is None:
        name = make_name('language')
    if currency is None:
        currency = make_name('currency')
    language = Language(code=code, name=name, currency=currency)
    database.session.add(language)
    return language


def make_ProductInfo(language=None, product=None, title=None,
                     description=None, price=None):
    if language is None:
        language = make_Language()
    if product is None:
        product = make_Product()
    if title is None:
        title = make_name('Product info')
    if description is None:
        description = make_name('Info about product')
    if price is None:
        price = make_price()
    product_info = ProductInfo(
        language=language, product=product, title=title,
        description=description, price=price)
    database.session.add(product_info)
    return product_info
