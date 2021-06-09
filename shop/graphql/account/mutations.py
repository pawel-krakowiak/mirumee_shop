import graphene
from graphql import GraphQLError
from ...account.models import User, UserManager
from .types import UserType


class UserCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="User e-mail (username field)")
    first_name = graphene.String(required=False, description="First name of user")
    last_name = graphene.String(required=False, description="Last name of user")
    is_active = graphene.BooleanField(required=False, default=True, description="Optionally create an unactive user")


class UserCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserCreateInput(required=True)

    def clean_input(input):
        # TODO: Validate email
        return input

    def check_user_exist(cls, email):
        try:
            Users.objects.get(email=email)
        except ObjectDoesNotExists():
            return False
        else:
            return True
            
    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)
        is_exist = cls.check_user_exist(input.get("email"))

        if not is_exist:
            user = User.objects.create(
                is_staff=False,
                is_superuser=False,
                **cleaned_input
                )
            user.save()
            return UserCreate(user=user)

        else:
            raise GraphQLError('That email already exists!')
            return
        
        
class StaffUserCreate(graphene.Mutation, UserCreate):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserCreateInput(required=True)
     
    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = UserCreate.clean_input(input)
        is_exist = UserCreate.check_user_exist(input.get("email"))

        if not is_exist:
            user = User.objects.create(
                is_staff=True,
                is_superuser=False,
                **cleaned_input
                )
            user.save()
            return StaffUserCreate(user=user)

        else:
            raise GraphQLError('That email already exists!')
            return

