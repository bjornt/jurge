from graphene.test import Client

from .. import graphql
from ..testing import factory


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
        product1 = factory.make_Product()
        product2 = factory.make_Product()
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
        returned_names = [
            edge['node']['name']
            for edge in result['data']['products']['edges']]
        assert returned_names == [product1.name, product2.name]
