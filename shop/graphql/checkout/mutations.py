import graphene

from .types import CheckoutType, CheckoutLineType
from ...checkout.models import Checkout, CheckoutLine

class CheckoutLineCreateInput(graphene.InputObjectType):
    quantity = graphene.Int(required=True)
    variant_id = graphene.Int(required=True)
    checkout_id = graphene.Int(required=False)


class CheckoutCreateInput(graphene.InputObjectType):
    user_email = graphene.String(required=False)
    user = graphene.String(required=False)
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

        if 'checkout_id' in cleaned_input:
            input_checkout = input.get('checkout_id')
            input_variant = input.get('variant_id')
            input_quantity = input.get('quantity')
            checkout = Checkout.objects.get(id=input_checkout)

            if checkout.lines.filter(variant_id=input_variant).count():
                line = checkout.lines.get(variant_id=input_variant)
                line.quantity += input_quantity
                checkout.lines.filter(variant_id=input_variant).update(quantity=line.quantity)
                return

        checkout_line = CheckoutLine.objects.create(**cleaned_input)