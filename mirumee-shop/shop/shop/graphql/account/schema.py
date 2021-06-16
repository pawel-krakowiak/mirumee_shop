import graphene

from .types import UserType
from .mutations import UserCreate, StaffCreate
from ...account.models import User
from ..core.utils.permissions import staff_member_required


class UserQueries(graphene.ObjectType):
    user = graphene.Field(UserType, email=graphene.Argument(graphene.String))
    users = graphene.List(UserType)

    def resolve_user(self, _info, email):
        user = User.objects.filter(email=email).first()
        return user

    @staff_member_required
    def resolve_users(self, _info):
        print(_info.context.user)
        users = User.objects.all()
        return users


class UserMutations(graphene.ObjectType):
    user_create = UserCreate.Field()
    staff_create = StaffCreate.Field()
