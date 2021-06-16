import graphene

from .types import CheckoutType, CheckoutLineType
from ...checkout.models import Checkout, CheckoutLine
from ...product.models import ProductVariant
from ...account.models import User

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CheckoutLineCreateInput(graphene.InputObjectType):
    variant_id = graphene.Int()
    quantity = graphene.Int()


class CheckoutCreateInput(graphene.InputObjectType):
    user_id = graphene.Int(required=False)
    user_email = graphene.String(required=True)
    lines = graphene.List(CheckoutLineCreateInput, required=True)


class CheckoutCreate(graphene.Mutation):
    checkout = graphene.Field(CheckoutType)

    class Arguments:
        input = CheckoutCreateInput(required=True)

    @classmethod
    def validate_input(cls, input):

        def validate_user(user_id):
            if not User.objects.filter(id=user_id).exists():
                raise ValidationError(f"This youser (ID: {user_id}) does not exists.")
            return user_id


        def validate_email(email):
            try:
                validate_email(email)
                
                if not User.objects.filter(email=email).exists():
                    raise ValidationError(f"This email does not exists {email}")
                
            except ValidationError:
                raise ValidationError("Email input corrupted.")
            return email


        def validate_variant(variant_id):
            if not ProductVariant.objects.filter(id=variant_id).exists():
                raise ValidationError(f"This variant (ID: {variant_id}) does not exists.")
            return variant_id


        def validate_quantity(quantity):
            if quantity <= 0:
                raise ValidationError("Quantity have to be a positive value,")
            return quantity
        
        
        for line in input.get('lines'):
            line['variant_id'] = validate_variant(line.get('variant_id'))
            line['quantity'] = validate_quantity(line.get('quantity'))

        input['user_email'] = validate_email(input.get('user_email'))
        
        if input.get('user_id'):
            input['user_id'] = validate_user(input.get('user_id'))
            

    @classmethod
    def mutate(cls, root, _info, input):
        cls.validate_input(input)

        checkout_lines_input = input.pop('lines')
        checkout = Checkout.objects.create(**input)

        checkout_lines = []
        for line in checkout_lines_input:
            checkout_lines.append(CheckoutLine(**line, checkout=checkout))
        checkout.lines.bulk_create(checkout_lines)

        return CheckoutCreate(checkout=checkout)


class CheckoutLineCreate(graphene.Mutation):
    checkout_line = graphene.Field(CheckoutLineType)

    class Arguments:
        input = CheckoutLineCreateInput(required=True)
        checkout_id = graphene.ID(required=True)

    @classmethod
    def validate_input(cls, input, checkout_id):
        
        def validate_checkout(checkout_id):
            if not Checkout.objects.filter(id=checkout_id).exists():
                raise ValidationError(f"This checkout (ID: {checkout_id}) does not exist.")

        input['checkout_id'] = validate_checkout(input.get('checkout_id'))
        input['variant_id'] = CheckoutCreate.validate_input.validate_variant(input.get('variant_id'))
        input['quantity'] = CheckoutCreate.validate_input.validate_quantity(input.get('quantity'))

    @classmethod
    def mutate(cls, root, _info, input, checkout_id):
        cls.validate_input(input, checkout_id)

        variant_id = input.pop('variant_id')
        line, created = CheckoutLine.objects.get_or_create(
            checkout_id=checkout_id,
            variant_id=variant_id,
            defaults=input
        )
        if not created:
            line.quantity += input['quantity']
            line.save()
        return CheckoutLineCreate(checkout_line=line)
