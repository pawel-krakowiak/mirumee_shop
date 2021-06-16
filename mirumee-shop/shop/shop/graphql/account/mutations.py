  
import graphene

from .types import UserType
from ...account.models import User
from ..core.utils.permissions import staff_member_required, superuser_required

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)

    @staticmethod
    def validate_input(input):
        def validate_email(email):
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    raise ValidationError(f"This email actually exists: {email}")
                
            except ValidationError:
                raise ValidationError("Email input corrupted")
                
            return email

        def validate_password(password):
            if len(password) < 8:
                raise ValidationError("A password must contain at least 8 characters.")
            return password

        input['email'] = validate_email(input.get('email'))
        input['password'] = validate_password(input.get('password'))


class UserCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserCreateInput(required=True)

    @classmethod
    def mutate(cls, root, _info, input):
        UserCreateInput.validate_input(input)
        user = User.objects.create_user(**input)
        return UserCreate(user=user)


class StaffCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserCreateInput(required=True)

    @classmethod
    @superuser_required
    def mutate(cls, root, _info, input):
        UserCreateInput.validate_input(input)
        staff = User.objects.create_user(**input, is_staff=True)
        return StaffCreate(user=staff)