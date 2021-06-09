import graphene
import graphql_jwt

from ...account.models import User, UserManager
from .mutations import UserCreate, StaffUserCreate
from .types import UserType

class UserQueries(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.Argument(graphene.ID, description="ID of user."),
        
    )

    user_by_email = graphene.Field(
        UserType,
        email=graphene.Argument(graphene.String, description="E-mail of user.")
    )

    users = graphene.List(UserType)

    graphene.String(description="Mail of user.")

    def resolve_user(self, info, id):
        user = User.objects.filter(id=id).first()
        return user
    
    def resolve_users(self, info):
        # users = User.objects.all()
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Auth Error: Your must be signed in')
        if not user.is_staff:
            raise Exception('Auth Error: You must be staff to resolve users')
        return get_user_model().objects.all()

    def resolve_user_by_email(self, info, email):
        user = User.objects.filter(email=email).first()
        return user

class UserMutations(graphene.ObjectType):
    user_create = UserCreate.Field()
    staff_user_create = StaffUserCreate.Field()
    