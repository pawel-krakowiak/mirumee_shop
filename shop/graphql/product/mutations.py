import graphene

from .types import ProductType, ProductVariantType
from ...product.models import Product, ProductVariant


class ProductCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    description = graphene.String(required=True)
    quantity = graphene.Int()


class ProductCreate(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        input = ProductCreateInput(required=True)

    @classmethod
    def clean_input(cls, input):
        # TODO price should be Decimal
        return input

    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)

        product = Product.objects.create(**cleaned_input)

        return ProductCreate(product=product)


class ProductVariantCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    sku = graphene.String(required=True)
    price = graphene.Decimal(required=True)


class ProductVariantCreate(graphene.Mutation):
    product_variant = graphene.Field(ProductVariantType)

    class Arguments:
        input = ProductVariantCreateInput(required=True)
        product_id = graphene.ID(required=True)

    @classmethod
    def clean_input(cls, data):
        return data

    @classmethod
    def mutate(cls, root, _info, input, product_id):
        cleaned_input = cls.clean_input(input)
        product_variant = ProductVariant.objects.create(product_id=product_id, **cleaned_input)

        return ProductVariantCreate(product_variant=product_variant)