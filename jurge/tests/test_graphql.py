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
        product1 = factory.make_ProductInfo().product
        product2 = factory.make_ProductInfo().product
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

    def test_product_info_basics(self, session):
        info = factory.make_ProductInfo()
        session.flush()
        client = Client(graphql.schema)
        query = """
            query ProductQuery {
                products {
                    edges {
                        node {
                            info {
                                edges {
                                    node {
                                        title
                                        description
                                        price
                                    }
                                }
                            }
                        }
                    }
                }
            }"""
        result = client.execute(query)
        returned_products = [
            edge['node']
            for edge in result['data']['products']['edges']]
        returned_infos = [
            dict(edge['node'])
            for node in returned_products
            for edge in node['info']['edges']]
        assert returned_infos == [{
                'title': info.title,
                'description': info.description,
                'price': str(info.price),
        }]
