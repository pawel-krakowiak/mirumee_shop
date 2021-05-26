import graphene

from ..graphql.product.schema import ProductQueries, ProductMutations
from ..graphql.checkout.schema import CheckoutQueries, CheckoutMutations


class Query(ProductQueries, CheckoutQueries):
    pass


class Mutations(ProductMutations, CheckoutMutations):
    pass


schema = graphene.Schema(query=Query,mutation=Mutations)
