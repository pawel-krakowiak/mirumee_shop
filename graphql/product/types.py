import graphene
from django.db.models import Avg
from graphene_django import DjangoObjectType

from ...product.models import Product, ProductVariant


class ProductType(DjangoObjectType):
    average_price = graphene.Decimal(description='Average price of product.')

    class Meta:
        model = Product
        fields = '__all__'

    def resolve_average_price(self, _info):
        product = self.variants.all().aggregate(average_variant_price=Avg('price'))
        average_variant_price = product['average_variant_price']
        if not average_variant_price:
            return self.price

        return product['average_variant_price']


class ProductVariantType(DjangoObjectType):
    class Meta:
        model = ProductVariant
        fields = '__all__'
