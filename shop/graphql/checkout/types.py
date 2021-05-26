import graphene
from django.db.models import Sum
from graphene_django import DjangoObjectType

from ...checkout.models import Checkout, CheckoutLine

class CheckoutType(DjangoObjectType):
    total_price = graphene.Decimal(description='Total price of checkout.')

    class Meta:
        model = Checkout
        fields = '__all__'

    def resolve_total_price(self, _info):
        checkout = self.lines.all().aggregate(total_variant_price=Sum('variant__price'))
        total_variant_price = checkout['total_variant_price']
        if not total_variant_price:
            return self.price

        return checkout['total_variant_price']

class CheckoutLineType(DjangoObjectType):
    class Meta:
        model = CheckoutLine
        fields = '__all__'
        