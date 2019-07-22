from graphql_jwt import Refresh
from graphql_jwt.decorators import login_required, permission_required
from saleor.graphql.core.fields import FilterInputConnectionField
from saleor.graphql.core.types import FilterInputObjectType
from saleor.graphql.descriptions import DESCRIPTIONS
# from saleor.graphql.account.mutations import (
#     AddressCreate,
#     AddressDelete,
#     AddressSetDefault,
#     AddressUpdate,
#     CustomerAddressCreate,
#     CustomerCreate,
#     CustomerDelete,
#     CustomerPasswordReset,
#     CustomerRegister,
#     CustomerSetDefaultAddress,
#     CustomerUpdate,
#     LoggedUserUpdate,
#     PasswordReset,
#     SetPassword,
#     StaffCreate,
#     StaffDelete,
#     StaffUpdate,
#     UserAvatarDelete,
#     UserAvatarUpdate,
# )
from saleor.graphql.account.enums import CountryCodeEnum
from saleor.graphql.account.resolvers import resolve_address_validator, resolve_customers, resolve_staff_users
from saleor.graphql.account.types import AddressValidationData, User
from saleor.graphql.account.schema import CustomerFilterInput, StaffUserInput
from saleor.graphql.core.mutations import VerifyToken
from shopozor.graphql.auth.mutations import Login, ConsumerCreate, ConsumerActivate, PasswordReset

import graphene


class AuthQueries(graphene.ObjectType):
    # address_validation_rules = graphene.Field(
    #     AddressValidationData,
    #     country_code=graphene.Argument(CountryCodeEnum, required=False),
    #     country_area=graphene.String(required=False),
    #     city_area=graphene.String(required=False),
    # )
    # customers = FilterInputConnectionField(
    #     User,
    #     filter=CustomerFilterInput(),
    #     description="List of the shop's customers.",
    #     query=graphene.String(description=DESCRIPTIONS["user"]),
    # )
    me = graphene.Field(User, description="Logged in user data.")
    # staff_users = FilterInputConnectionField(
    #     User,
    #     filter=StaffUserInput(),
    #     description="List of the shop's staff users.",
    #     query=graphene.String(description=DESCRIPTIONS["user"]),
    # )
    user = graphene.Field(
        User,
        id=graphene.Argument(graphene.ID, required=True),
        description="Lookup a user by ID.",
    )

    # def resolve_address_validation_rules(
    #     self, info, country_code=None, country_area=None, city_area=None
    # ):
    #     return resolve_address_validator(
    #         info,
    #         country_code=country_code,
    #         country_area=country_area,
    #         city_area=city_area,
    #     )

    # @permission_required("account.manage_users")
    # def resolve_customers(self, info, query=None, **_kwargs):
    #     return resolve_customers(info, query=query)

    @login_required
    def resolve_me(self, info):
        return info.context.user

    # @permission_required("account.manage_staff")
    # def resolve_staff_users(self, info, query=None, **_kwargs):
    #     return resolve_staff_users(info, query=query)

    # @permission_required("account.manage_users")
    # def resolve_user(self, info, id):
    #     return graphene.Node.get_node_from_global_id(info, id, User)


class AuthMutations(graphene.ObjectType):
    login = Login.Field(description="Identifies a registered user.")
    token_refresh = Refresh.Field(
        description="""Authentication tokens need to be refreshed regularly.
            If a token has not been refreshed with some time, it is invalidated.
            For example, it can be that such a token would expire in one year but needs
            to be refreshed every month. If it hasn't been refreshed within a month,
            then it is invalidated.""")
    token_verify = VerifyToken.Field(
        description="Verifies if an authentication token is valid.")
    consumer_create = ConsumerCreate.Field(
        description="Creates a new consumer.")
    consumer_activate = ConsumerActivate.Field(
        description="Activates a user account.")
    password_reset = PasswordReset.Field(
        description="Resets a user password.")

    # password_reset = PasswordReset.Field()
    # set_password = SetPassword.Field()
