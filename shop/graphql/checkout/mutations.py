import graphene

from .types import CheckoutType, CheckoutLineType
from ...checkout.models import Checkout, CheckoutLine

class CheckoutLineCreateInput(graphene.InputObjectType):
    quantity = graphene.Int(required=True)
    variant_id = graphene.ID(required=True)
    checkout_id = graphene.ID(required=False)


class CheckoutCreateInput(graphene.InputObjectType):
    user_email = graphene.String(required=False)
    user = graphene.String(required=True)
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
            checkout_lines.append(CheckoutLine(checkout_id=checkout.id, **line))        
        
        checkout.lines.bulk_create(checkout_lines)
        return CheckoutCreate(checkout=checkout) 


class CheckoutLineCreate(graphene.Mutation):
    checkout_line = graphene.Field(CheckoutLineType)

    class Arguments:
        input = CheckoutLineCreateInput(required=True)

    @classmethod
    def clean_input(cls, input):
        return input

    @classmethod
    def mutate(cls, root, _info, input):
        cleaned_input = cls.clean_input(input)
        
        checkout_id = input.get('checkout_id')

        if checkout_id:
            variant_id = input.get('variant_id')
            quantity = input.get('quantity')
            checkout = Checkout.objects.get(id=input_checkout)

            try:
                line = checkout.lines.get(variant_id=variant_id)

            except CheckoutLine.DoesNotExist:
                checkout_line = CheckoutLine.objects.create(**cleaned_input)

            else:
                line.quantity += quantity
                line.save(updated_fields=['quantity'])
                return

        checkout_line = CheckoutLine.objects.create(**cleaned_input)