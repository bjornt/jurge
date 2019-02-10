import decimal

import graphene
from graphene import relay

from . import models


from graphene.types.scalars import Scalar
from graphql.language import ast


class Decimal(Scalar):
    """
    The `Decimal` scalar type represents a python Decimal.
    """

    @staticmethod
    def serialize(dec):
        if isinstance(dec, str):
            dec = decimal.Decimal(dec)
        assert isinstance(dec, decimal.Decimal), (
            'Received not compatible Decimal "{}"'.format(repr(dec)))
        return str(dec)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.parse_value(node.value)

    @staticmethod
    def parse_value(value):
        try:
            return decimal.Decimal(value)
        except ValueError:
            return None


class ProductInfo(graphene.ObjectType):

    class Meta:
        interfaces = (relay.Node, )

    title = graphene.String()
    description = graphene.String()
    price = Decimal()

    @classmethod
    def get_node(self, info, id):
        return models.ProductInfo.query.get(id)


class ProductInfoConnection(graphene.Connection):

    class Meta:
        node = ProductInfo


class Product(graphene.ObjectType):

    class Meta:
        interfaces = (relay.Node, )

    name = graphene.String()
    info = graphene.ConnectionField(ProductInfoConnection)

    def resolve_info(self, info):
        return list(models.ProductInfo.query.filter(
            models.ProductInfo.product == self))

    @classmethod
    def get_node(self, info, id):
        return models.Product.query.get(id)


class ProductConnection(graphene.Connection):

    class Meta:
        node = Product


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    products = graphene.ConnectionField(ProductConnection)

    def resolve_products(self, info):
        return models.Product.query.all()


schema = graphene.Schema(query=Query, types=[Product])
