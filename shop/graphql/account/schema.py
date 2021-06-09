import graphene
import graphql_jwt
from graphql_jwt.decorators import staff_member_required, login_required

from django.contrib.auth import get_user_model
from ...account.models import User, UserManager
from .mutations import UserCreate, StaffUserCreate
from .types import UserType

class UserQueries(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.Argument(graphene.ID, description="ID of user."),
        token=graphene.String(required=True)
    )

    user_by_email = graphene.Field(
        UserType,
        email=graphene.Argument(graphene.String, description="E-mail of user."),
        token=graphene.String(required=True)
    )

    users = graphene.List(UserType)

    graphene.String(description="Mail of user.")

    @login_required
    def resolve_user(self, info, id, token):
        user = User.objects.filter(id=id).first()
        return user
    
    @staff_member_required
    def resolve_users(self, info, token):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Auth Error: Your must be signed in')
        if not user.is_staff:
            raise Exception('Auth Error: You must be staff to resolve users')
        return get_user_model().objects.all()

    @login_required
    def resolve_user_by_email(self, info, email, token):
        user = User.objects.filter(email=email).first()
        return user

class UserMutations(graphene.ObjectType):
    user_create = UserCreate.Field()
    staff_user_create = StaffUserCreate.Field()
    