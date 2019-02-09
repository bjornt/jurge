from graphene.test import Client

import pytest
from pytest_postgresql import factories as pg_factory

from .. import database, graphql
from ..models import Category, Product


@pytest.fixture
def session(postgresql_proc):
    db_name = 'unittests'
    port = postgresql_proc.port
    user = postgresql_proc.user
    socketdir = postgresql_proc.unixsocketdir
    pg_factory.init_postgresql_database(user, socketdir, port, db_name)
    db_url = (
        f'postgresql:///{db_name}?'
        f'user={user}&host={socketdir}&port={port}')
    database.init(db_url)
    database.migrate()
    yield database.session
    pg_factory.drop_postgresql_database(
        user, socketdir, port, db_name, postgresql_proc.version)


class TestSchema:

    def test_empty(self, session):
        client = Client(graphql.schema)
        query = """
            query ProductQuery {
                products {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }"""
        result = client.execute(query)
        assert result['data']['products']['edges'] == []

    def test_product_names(self, session):
        category = Category(name='my-category')
        product1 = Product(name='product-1', category=category)
        product2 = Product(name='product-2', category=category)
        session.add(product1)
        session.add(product2)
        session.flush()
        client = Client(graphql.schema)
        query = """
            query ProductQuery {
                products {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }"""
        result = client.execute(query)
        expected = [
            {'node': {'name': 'product-1'}}, {'node': {'name': 'product-2'}}]
        assert result['data']['products']['edges'] == expected
