
import graphene
import graphql_jwt

from saleor.graphql.core.mutations import VerifyToken

from shopozor.graphql.auth.mutations import Login


class AuthMutations(graphene.ObjectType):
    login = Login.Field()
    token_refresh = graphql_jwt.Refresh.Field()
    token_verify = VerifyToken.Field()
