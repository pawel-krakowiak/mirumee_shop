import graphene
from django.db.models import Sum
from grapehene_django import DjangoObjectType

from ...checkout.models import Checkout, CheckoutLine

class CheckoutType(DjangoObjectType):
    total_price = graphene.Decimal(description='Total price of checkout.')

    class Meta:
        model = Checkout
        fields = '__all__'

    def resolve_total_price(self, _info):
        checkout = self.variants.all().aggregate(total_variant_price=Sum('price'))
        total_variant_price = product['total_variant_price']
        if not total_variant_Price:
            return self.price

        return product['total_variant_price']

class CheckoutLineType(DjangoObjectType):
    class Meta:
        model = CheckoutLine
        fields = '__all__'
        