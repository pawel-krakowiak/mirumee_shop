import graphene

from ...checkout.models import Checkout, CheckoutLine
from .mutations import CheckoutCreate
from .types import CheckoutLineType, CheckoutType


class CheckoutQueries(graphene.ObjectType):
    checkout = graphene.Field(
        CheckoutType,
        id=graphene.Argument(graphene.ID, description="ID of checkout."),
    )
    checkouts = graphene.List(CheckoutType)
    checkout_line = graphene.Field(
        CheckoutType,
        id=graphene.Argument(graphene.ID, description="Id of checkout line."),
    )
    checkout_lines = graphene.List(CheckoutLineType)

    def resolve_checkout(self, info, token):
        checkout = Checkout.objects.filter(id=id).first()
        return checkout

    def resolve_checkouts(self, info):
        checkouts = Checkout.objects.all()
        return checkouts

    def resolve_checkout_line(self, info, id):
        checkout_line = CheckoutLine.objects.filter(id=id).first()
        return checkout_line

    def resolve_checkout_lines(self):
        checkout_lines = CheckoutLine.objects.all()
        return checkout_lines


class CheckoutMutations(graphene.ObjectType):
    checkout_create = CheckoutCreate.Field()
