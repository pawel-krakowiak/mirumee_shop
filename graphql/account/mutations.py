import graphene
import re

import graphql_jwt
from graphql_jwt.decorators import staff_member_required, superuser_required
from graphql_jwt.shortcuts import create_refresh_token, get_token
from graphql import GraphQLError

from django.core.exceptions import ObjectDoesNotExist

from ...account.models import User, UserManager
from .types import UserType


class UserCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="User e-mail (username field)")
    password = graphene.String(required=True, description="User password")
    first_name = graphene.String(required=False, description="First name of user")
    last_name = graphene.String(required=False, description="Last name of user")
    is_active = graphene.Boolean(required=False, default=True, description="Optionally create an unactive user")


class UserCreate(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        input = UserCreateInput(required=True)

    @classmethod
    def make_email(cls, email):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return email
        else:
            raise GraphQLError("Email is invalid.")

    @classmethod
    def make_name(cls, name):
        regex = '/^[A-Za-z]+$/'
        if(re.search(regex, name)):
            return str(name).capitalize()
        else:
            raise GraphQLError(f"Name '{name}' is invalid, please enter correct name.")


    @classmethod
    def clean_input(cls, input):
        email = input.get('email')
        input['email'] = cls.make_email(email)

        fname = input.get('first_name')
        input['first_name'] = cls.make_name(fname)

        lname = input.get('last_name')
        input['last_name'] = cls.make_name(lname)
        
        return input
    
    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)
        password = cleaned_input.pop("password")

        if not User.objects.filter(email=input.get('email')):
            user = User.objects.create(
                is_staff=False,
                is_superuser=False,
                **cleaned_input
                )
            user.set_password(password)
            user.save()

            token = get_token(user)
            refresh_token = create_refresh_token(user)

            return UserCreate(user=user, token=token, refresh_token=refresh_token)

        else:
            raise GraphQLError(f'{cls.__name__} Error: That email already exists!')


class StaffUserCreate(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        input = UserCreateInput(required=True)
     
    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = UserCreate.clean_input(input)
        password = cleaned_input.pop("password")

        if not User.objects.filter(email=input.get('email')):
            user = User.objects.create(
                is_staff=True,
                is_superuser=False,
                **cleaned_input
                )
            user.set_password(password)
            user.save()

            token = get_token(user)
            refresh_token = create_refresh_token(user)
            
            return StaffUserCreate(user=user, token=token, refresh_token=refresh_token)

        else:
            raise GraphQLError(f'{cls.__name__} Error: That email already exists!')

