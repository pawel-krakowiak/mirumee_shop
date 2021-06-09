import graphene

from ...account.models import User, UserManager
from .mutations import UserCreate, StaffUserCreate
from .types import UserType

class UserQueries(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.Argument(graphene.ID, description="ID of user."),
        mail=graphene.Argument(graphene.String, description="Mail of user.")
    )
    users = graphene.List(UserType)

    def resolve_user(self, info):
        user = User.objects.filter(id=id).first()
        return user
    
    def resolve_users(self, info, token):
        users = User.objects.all()

    def resolve_users_by_mail(self, info):
        user = User.objects.filter(mail=mail).first()
        return user

class UserMutations(graphene.ObjectType):
    user_create = UserCreate.Field()
    staff_user_create = StaffUserCreate.Field()
    