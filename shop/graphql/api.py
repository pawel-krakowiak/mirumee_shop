import graphene

from ..graphql.product.schema import ProductQueries, ProductMutations


class Query(ProductQueries):
    pass


class Mutations(ProductMutations):
    pass


schema = graphene.Schema(query=Query,mutation=Mutations)
