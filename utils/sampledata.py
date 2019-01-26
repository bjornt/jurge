from decimal import Decimal

import yaml

from jurge.database import session, transact
from jurge.models import Category, Language, Product, ProductInfo


def insert_products():
    with open('products.yaml', 'r') as f:
        products = yaml.safe_load(f.read())
    for name in products.keys():
        category_id = session.query(Category.id).filter(
            Category.name == name).one_or_none()
        if category_id is None:
            category = Category(name=name)
            session.add(category)
            session.flush()
            category_id = category.id
        for product_num, product_info in products[name].items():
            product = Product(name=product_num, category_id=category_id)
            session.add(product)
            for lang_code, lang_info in product_info.items():
                lang_id = session.query(Language.id).filter(
                    Language.code == lang_code).one_or_none()
                if lang_id is None:
                    language = Language(
                        name=lang_code, code=lang_code, currency='SEK')
                    session.add(language)
                    session.flush()
                    lang_id = language.id
                info = ProductInfo(
                    language_id=lang_id, product=product,
                    description=lang_info['description'],
                    title=lang_info['title'],
                    price=Decimal(lang_info['price']))
                session.add(info)


transact(insert_products)
