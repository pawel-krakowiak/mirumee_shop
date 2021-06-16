import graphene

from .types import ProductType, ProductVariantType
from ...product.models import Product, ProductVariant
from ..core.utils.permissions import staff_member_required

from django.core.exceptions import ValidationError


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
    def validate_input(cls, input):

        def validate_quantity(quantity):
            if quantity <= 0:
                raise ValidationError("Quantity have to be a positive value.")
            return quantity

        def validate_price(price):
            if price <= 0:
                raise ValidationError("Price have to be a positive value.")
            return price

        input['price'] = validate_price(input.get('price'))
        input['quantity'] = validate_quantity(input.get('quantity'))

    @classmethod
    @staff_member_required
    def mutate(cls, root, _info, input):
        cls.validate_input(input)

        product = Product.objects.create(**input)

        return ProductCreate(product=product)


class ProductVariantCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    sku = graphene.String(required=True)
    price = graphene.Decimal(required=True)


class ProductVariantCreate(graphene.Mutation):
    productVariant = graphene.Field(ProductVariantType)

    class Arguments:
        input = ProductVariantCreateInput(required=True)
        product_id = graphene.ID(required=True)

    @classmethod
    def validate_input(cls, input, product_id):
        
        def validate_product(product_id):
            if not Product.objects.filter(id=product_id).exists():
                raise ValidationError(f"A product with this ID: {product_id} does not exists.")
            return product_id

        def validate_sku(sku):
            if ProductVariant.objects.filter(sku=sku).exists():
                raise ValidationError(f"A product with this SKU: {sku} already exists.")
            return sku
        
        input['product_id'] = validate_product(input.get('product_id'))
        input['sku'] = validate_sku(input.get('sku'))
        input['price'] = ProductCreate.validate_input.validate_price(input.get('price'))

    @classmethod
    @staff_member_required
    def mutate(cls, root, info, input, product_id):
        cls.validate_input(input, product_id)

        product_variant = ProductVariant.objects.create(**input, product_id=product_id)

        return ProductVariantCreate(productVariant=product_variant)
