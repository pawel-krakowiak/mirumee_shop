import graphene
import graphql_jwt

from .product.schema import ProductQueries, ProductMutations
from .checkout.schema import CheckoutMutations, CheckoutQueries
from .account.schema import UserQueries, UserMutations


class Query(ProductQueries, CheckoutQueries, UserQueries):
    pass


class Mutations(ProductMutations,
                CheckoutMutations,
                UserMutations
    ):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query,mutation=Mutations)
