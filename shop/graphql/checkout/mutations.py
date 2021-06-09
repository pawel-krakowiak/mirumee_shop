import graphene
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from ...checkout.models import Checkout, CheckoutLine
from ...product.models import ProductVariant
from .types import CheckoutLineType, CheckoutType


class CheckoutLineCreateInput(graphene.InputObjectType):
    quantity = graphene.Int(required=True, description="The number of items purchased.")
    variant_id = graphene.ID(required=True, description="ID of the product variant.")


class CheckoutCreateInput(graphene.InputObjectType):
    user_email = graphene.String()
    lines = graphene.List(CheckoutLineCreateInput, required=True)


class CheckoutCreate(graphene.Mutation):
    checkout = graphene.Field(CheckoutType)

    class Arguments:
        input = CheckoutCreateInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        lines = input.pop('lines')
        checkout = Checkout.objects.create(**input)

        checkout_lines = []
        for line in lines:
            checkout_lines.append(
                CheckoutLine(checkout_id=checkout.id, **line)
            )
        checkout.lines.bulk_create(checkout_lines)
        return CheckoutCreate(checkout=checkout)


class CheckoutLineCreate(graphene.Mutation):
    checkout_line = graphene.Field(CheckoutLineType)

    class Arguments:
        input = CheckoutLineCreateInput(required=True)
        checkout_id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, input, checkout_id):

        variant_id = input.pop('variant_id')
        input_quantity = input.pop('quantity')

        try:
            checkout_line = CheckoutLine.objects.get(checkout_id=checkout_id, variant=variant_id)
        except ObjectDoesNotExist():
            checkout_line = CheckoutLine.objects.create(
                checkout_id=checkout_id,
                variant_id=variant_id,
                quantity=input_quantity)

            return CheckoutLineCreate(checkout_line=checkout_line)

        quantity = checkout_line.quantity + input_quantity

        checkout_line.quantity = quantity
        checkout_line.save()

        return CheckoutLineCreate(checkout_line=checkout_line)