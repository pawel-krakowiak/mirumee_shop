from graphene_django import DjangoObjectType

from ...checkout.models import Checkout, CheckoutLine


class CheckoutType(DjangoObjectType):
    class Meta:
        model = Checkout
        fields = "__all__"


class CheckoutLineType(DjangoObjectType):
    class Meta:
        model = CheckoutLine
        fields = "__all__"
