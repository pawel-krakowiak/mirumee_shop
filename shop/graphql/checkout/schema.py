import graphene

from .types import CheckoutType, CheckoutLineType
from ...checkout.models import Checkout, CheckoutLine
from .mutation import CheckoutCreate, CheckoutLineCreate

class CheckoutQueries(graphene.ObjectType):
    checkout = graphene.Field(
        CheckoutType, id=graphene.Argument(graphene.ID, description="ID of checkout.")
    )
    checkouts = graphene.List(CheckoutType)
    checkout_line = graphene.FIeld(
        CheckoutLineType,
        id=graphene.Argument(graphene.ID, description="ID of checkout line.")
    )

    def resolve_checkout(self, _info, id):
        return Checkout.objects.filter(id=id).first()

    def resolve_checkouts(self, _info):
        return Checkout.objects.all()

    def resolve_checkout_line(self, _info, id):
        return CheckoutLine.objects.filter(id=id).first()

    def resolve_checkout_lines(self, _info, id):
        return CheckoutLine.objects.all()


class CheckoutMutations(graphene.ObjectType):
    checkout_create = CheckoutCreate.Field()
    checkout_variant_create = CheckoutLineCreate.Field()


