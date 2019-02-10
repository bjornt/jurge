from .. import database
from ..models import Category, Product


_name_counters = {}


def make_name(prefix):
    counter = _name_counters.setdefault(prefix, 0)
    counter += 1
    _name_counters[prefix] = counter
    return f'{prefix}-{counter}'


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
