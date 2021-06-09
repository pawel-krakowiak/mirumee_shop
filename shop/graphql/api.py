import graphene

from .product.schema import ProductQueries, ProductMutations
from .checkout.schema import CheckoutMutations, CheckoutQueries
from .account.authenticate import AuthenticateMutations
from .account.schema import UserQueries, UserMutations


class Query(ProductQueries, CheckoutQueries):
    pass


class Mutations(ProductMutations, CheckoutMutations, AuthenticateMutations):
    pass


schema = graphene.Schema(query=Query,mutation=Mutations)
