import graphene

from .types import CheckoutType, CheckoutLineType
from ...checkout.models import Checkout, CheckoutLine

class CheckoutLineCreateInput(graphene.InputObjectType):
    quantity = graphene.Int()
    variant_id = graphene.Int()

class CheckoutCreateInput(graphene.InputObjectType):
    user_email = graphene.String(required=True)
    user = graphene.String(required=False)
    lines = graphene.List(CheckoutLineCreateInput, required=True)
    # lines = graphene.List(graphene.String(), required=False)

class CheckoutCreate(graphene.Mutation):
    checkout = graphene.Field(CheckoutType)

    class Arguments:
        input = CheckoutCreateInput(required=True)

    @classmethod
    def clean_input(cls, input):
        # TODO: Validate e-mail
        return input

    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)
    
        # checkout = Checkout.objects.create(**cleaned_input)
        checkout = Checkout.objects.create(**input)
        
        return CheckoutCreate(checkout=checkout)


class CheckoutLineCreate(graphene.Mutation):
    
    checkout_line = graphene.Field(CheckoutLineType)

    class Arguments:
        input = CheckoutLineCreateInput(required=True)
        checkout_id = graphene.ID(required=True)

    @classmethod
    def clean_input(cls, input):
        # TODO: quantity can't be a negative number
        return input

    @classmethod
    def mutate(cls, root, _info, input, checkout_id):
        cleaned_input = cls.clean_input(input)
        checkout_line = CheckoutLine.objects.create(checkout_id=checkout_id, **cleaned_input)

        return CheckoutLineCreate(checkout_line=checkout_line)