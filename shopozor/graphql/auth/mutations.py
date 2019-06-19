
import graphene

from saleor.account.models import User

from saleor.graphql.core.mutations import CreateToken
from saleor.graphql.core.types import Error


class Login(CreateToken):

    class Arguments:
        is_staff = graphene.Boolean(
            description="""Set this field to true if you want to authenticate as a staff member.
                This field is used to access administration-relevant functionality. Users with insufficient
                credentials cannot access admin functionality. For example, a Consumer who's not
                a staff member and tries to access admin functionality by setting that field to true
                will get ungranted access. That prevents e.g. a Consumer from accessing the administration panels.
                Such panels log users in by setting that field to true. If the users are not staff members,
                their access is not granted.""")

    @classmethod
    def mutate(cls, root, info, **kwargs):

        # Reuse CreateToken mutation logic
        result = super().mutate(root, info, **kwargs)

        # Intercept errors included in graphql response returned by base
        # mutation CreateToken and add our own corresponding message code. Error
        # message is originaly defined in graphql-jwt
        # https://github.com/flavors/django-graphql-jwt/blob/ccea207e4fe9ab92359967426b9cd25b69bacb4a/graphql_jwt/decorators.py#L88
        # and most certainly won't change any time soon.
        for error in result.errors or []:
            if 'Please, enter valid credentials' in error.message:
                error.message = 'WRONG_CREDENTIALS'
                return result

        # make sure the password is not empty
        password = kwargs['password']
        if not password:
            return Login(errors=[Error(message='WRONG_CREDENTIALS')])

        # make the is_staff check
        wants_to_login_as_staff = kwargs.get('is_staff', False)
        email = kwargs['email']
        if wants_to_login_as_staff and User.objects.filter(email=email, is_staff=True).first() is None:
            return Login(errors=[Error(message='USER_NOT_ADMIN')])
        else:
            return result
