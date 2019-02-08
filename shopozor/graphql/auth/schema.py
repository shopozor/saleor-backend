import graphene
import graphql_jwt

from saleor.graphql.core.mutations import VerifyToken, CreateToken
from saleor.graphql.core.types import Error


class Login(CreateToken):

    class Arguments:
        is_staff = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        result = super().mutate(root, info, **kwargs)
        for error in result.errors or []:
            if 'Please, enter valid credentials' in error.message:
                error.message = 'WRONG_CREDENTIALS'
        return result



class AuthMutations(graphene.ObjectType):
    login = Login.Field()
    token_refresh = graphql_jwt.Refresh.Field()
    token_verify = VerifyToken.Field()
