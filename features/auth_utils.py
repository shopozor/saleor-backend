from behave import use_fixture
from features.fixtures import graphql_query
from tests.api.utils import get_graphql_content


class UserLogger:
    def __init__(self, context):
        self.context = context

    def login(self, **kwargs):
        compulsory_args = ('email', 'password')
        if not all(key in kwargs for key in compulsory_args):
            raise TypeError(
                'You need to provide at least an email and a password to login')

        use_fixture(graphql_query, self.context, 'login.graphql')
        response = self.context.test.client.post_graphql(
            self.context.query, kwargs)
        return get_graphql_content(response)

    def valid_mail_and_password(self, user_type, is_staff_user):
        switch = {
            'client': dict(
                email=self.context.consumer['email'],
                password=self.context.consumer['password'],
                isStaff=is_staff_user
            ),
            'administrateur': dict(
                email=self.context.producer['email'],
                password=self.context.producer['password'],
                isStaff=is_staff_user
            )
        }
        return switch[user_type]

    def invalid_mail_and_password(self, is_staff_user):
        return dict(
            email=self.context.unknown['email'],
            password=self.context.unknown['password'],
            isStaff=is_staff_user
        )

    def valid_mail_invalid_password(self, user_type, is_staff_user):
        switch = {
            'client': dict(email=self.context.consumer['email'], password=self.context.consumer['password'] + 'a',
                           isStaff=is_staff_user),
            'administrateur': dict(email=self.context.producer['email'], password=self.context.producer['password'] + 'a',
                                   isStaff=is_staff_user)
        }
        return switch[user_type]

    def valid_persona_credentials(self, persona):
        switch = {
            'Consommateur': dict(email=self.context.consumer['email'], password=self.context.consumer['password']),
            'Producteur': dict(email=self.context.producer['email'], password=self.context.producer['password']),
            'Responsable': dict(email=self.context.manager['email'], password=self.context.manager['password']),
            'Rex': dict(email=self.context.rex['email'], password=self.context.rex['password']),
            'Softozor': dict(email=self.context.softozor['email'], password=self.context.softozor['password']),
        }
        return switch[persona]


class UserRegistrar:
    def __init__(self, context):
        self.context = context

    def sign_user_up(self, email, password):
        use_fixture(graphql_query, self.context, 'signup.graphql')
        variables = {
            'email': email,
            'password': password
        }
        response = self.context.test.client.post_graphql(
            self.context.query, variables)
        return get_graphql_content(response)
