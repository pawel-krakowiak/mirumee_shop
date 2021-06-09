from graphene_django import DjangoObjectType
from django import forms

from shop.account.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

        widgets = {
            'password': forms.PasswordInput()
        }
