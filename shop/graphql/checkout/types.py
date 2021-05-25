import graphene
from graphene_django import DjangoObjectType
from django.db.models import Sum

from ...checkout.models import Checkout, CheckoutLine

class CheckoutType(DjangoObjectType):
    total_price = graphene.Decimal(description="Total price of products in checkout.")

    class Meta:
        model = Checkout
        fields = '__all__'

    def resolve_total_price(self, _info):
        checkout = self.variants.all().aggregate(total_variant_price=Sum('price'))
        total_variant_price = checkout['total_variant_price']
        if not total_variant_price:
            return self.price

        return total_variant_price

class CheckoutLineType(DjangoObjectType):
    class Meta:
        model = CheckoutLine
        fields = '__all__'