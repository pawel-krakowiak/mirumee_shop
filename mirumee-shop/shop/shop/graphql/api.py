import graphene
from .product.schema import ProductQueries, ProductMutations
from .checkout.schema import CheckoutQueries, CheckoutMutations
from .account.schema import UserQueries, UserMutations
from .account.authenticate import AuthenticateMutations


class Query(ProductQueries, CheckoutQueries, UserQueries):
    pass


class Mutations(ProductMutations, CheckoutMutations, UserMutations, AuthenticateMutations):
    pass

schema = graphene.Schema(query=Query, mutation=Mutations)
