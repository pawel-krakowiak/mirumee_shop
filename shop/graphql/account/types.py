import graphene

from graphene_django import DjangoObjectType
from ...account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'
