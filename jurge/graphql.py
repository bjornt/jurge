import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from . import models


class Product(SQLAlchemyObjectType):

    class Meta:
        model = models.Product
        interfaces = (relay.Node, )


class ProductInfo(SQLAlchemyObjectType):

    class Meta:
        model = models.ProductInfo
        interfaces = (relay.Node, )


class Language(SQLAlchemyObjectType):

    class Meta:
        model = models.Language
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_products = SQLAlchemyConnectionField(Product)
    all_languages = SQLAlchemyConnectionField(Language)


schema = graphene.Schema(query=Query, types=[Product, ProductInfo, Language])
