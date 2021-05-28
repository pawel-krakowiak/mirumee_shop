import graphene
import logging
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from graphql.error.located_error import GraphQLLocatedError

from .types import CheckoutType, CheckoutLineType
from ...checkout.models import Checkout, CheckoutLine


class CheckoutLineCreateInput(graphene.InputObjectType):
    quantity = graphene.Int(required=True)
    variant_id = graphene.ID(required=True)
    checkout_id = graphene.ID(required=False)

class CheckoutCreateInput(graphene.InputObjectType):
    user_email = graphene.String(required=False)
    user_id = graphene.ID(required=True)
    lines = graphene.List(CheckoutLineCreateInput, required=True)


class CheckoutCreate(graphene.Mutation):
    checkout = graphene.Field(CheckoutType)

    class Arguments:
        input = CheckoutCreateInput(required=True)

    @classmethod
    def clean_input(cls, input):
        # TODO: VALIDATION
        # class UserDoesNotExistError(Exception):
        #     # TODO: Improve logging
        #     logging.error("ERROR: ", Exception)

        # class UserEmailInvalidError(Exception):
        #     # TODO: Improve logging
        #     logging.error("ERROR: ", Exception)

        # def clean_email(email):
        #     validator = EmailValidator
        #     try:
        #         validator(email)
        #     except ValidationError:
        #         raise UserEmailInvalidError(ValidError)
        #         return
            
        #     return email

        # def clean_user(user):
        #     try:
        #         breakpoint()
        #         user = User.objects.get(id=user)
        #         return user.id

        #     except GraphQLLocatedError as LocatedError: 
        #         raise UserDoesNotExistError(LocatedError)

        #     return None
        return input

        email = input.get('user_email')
        if email:
            input['user_email'] = clean_email(email)

        user = input.get('user_id')
        if user:
            input['user_id'] = clean_user(user)

        return input


    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)

        lines = cleaned_input.pop('lines')
        checkout = Checkout.objects.create(**cleaned_input)
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