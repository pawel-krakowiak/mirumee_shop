import graphene

from graphene_django import DjangoObjectType
from ...checkout.models import Checkout, CheckoutLine


class CheckoutType(DjangoObjectType):
    total_price = graphene.Decimal(description='total price of the checkout')

    class Meta:
        model = Checkout
        fields = '__all__'

    def resolve_total_price(self, _info):
        checkout_lines = list(self.lines.all())
        total_price = sum(line.variant.price * line.quantity for line in checkout_lines)
        return total_price


class CheckoutLineType(DjangoObjectType):
    total_price = graphene.Decimal(description='total price of the item')

    class Meta:
        model = CheckoutLine
        fields = '__all__'

    def resolve_total_price(self, _info):
        total_line_price = self.variant.price * self.quantity
        return total_line_price
