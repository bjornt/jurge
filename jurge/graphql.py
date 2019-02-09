import graphene
from graphene import relay

from . import models


class Product(graphene.ObjectType):

    class Meta:
        interfaces = (relay.Node, )

    name = graphene.String()

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
