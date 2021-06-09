import graphene
from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist

from ...account.models import User, UserManager
from .types import UserType


class UserCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="User e-mail (username field)")
    first_name = graphene.String(required=False, description="First name of user")
    last_name = graphene.String(required=False, description="Last name of user")
    is_active = graphene.Boolean(required=False, default=True, description="Optionally create an unactive user")


class UserCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserCreateInput(required=True)

    def clean_input(input):
        # TODO: Validate email
        return input

            
    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)

        if not User.objects.get(email=input.get('email')):
            user = User.objects.create(
                is_staff=False,
                is_superuser=False,
                **cleaned_input
                )
            user.save()
            return UserCreate(user=user)

        else:
            raise GraphQLError(f'{cls.__name__} Error: That email already exists!')
            return None
        
        
class StaffUserCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserCreateInput(required=True)
     
    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = UserCreate.clean_input(input)

        if not User.objects.get(email=input.get('email')):
            user = User.objects.create(
                is_staff=True,
                is_superuser=False,
                **cleaned_input
                )
            user.save()
            return StaffUserCreate(user=user)

        else:
            raise GraphQLError(f'{cls.__name__} Error: That email already exists!')
            return None

