
import graphene
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from saleor.account.models import User

from saleor.graphql.core.mutations import CreateToken, ModelMutation
from saleor.graphql.core.types import Error

from shopozor.emails import send_activate_account_email, send_hacker_abuse_email_notification
from shopozor.exceptions import HackerAbuseException
from shopozor.models import HackerAbuseEvents
from shopozor.tokens import activation_token_generator


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


class ConsumerCreateInput(graphene.InputObjectType):
    email = graphene.String(
        description="The unique email address of the user.")
    password = graphene.String(description="The user password.")


class ConsumerCreate(ModelMutation):
    class Arguments:
        input = ConsumerCreateInput(
            description="Fields required to create a customer.", required=True
        )

    class Meta:
        description = "Register a new consumer."
        model = User

    @classmethod
    def save(cls, info, instance, cleaned_input):
        try:
            validate_password(instance.password)
            instance.is_active = False
            super().save(info, instance, cleaned_input)
            send_activate_account_email(instance.pk)
        except ValidationError as error:
            errors = error.error_list
            errors.insert(0, ValidationError("PASSWORD_NOT_COMPLIANT"))
            raise ValidationError(errors)

    @classmethod
    def get_instance(cls, info, **data):
        current_user = User.objects.filter(email=data.get("input")["email"])
        if current_user:
            current_user = current_user.get()
            cls.hacker_abuse_filter(current_user)
            object_id = graphene.Node.to_global_id(
                "User", current_user.pk)
            data["id"] = object_id

        return super().get_instance(info, **data)

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        try:
            return super().perform_mutation(_root, info, **data)
        except HackerAbuseException as error:
            cls.report_hacker_abuse(error.user)
            return cls.success_response(error.model)

    @classmethod
    def hacker_abuse_filter(cls, current_user):
        if current_user.is_active:
            raise HackerAbuseException(current_user, cls._meta.model())

    @staticmethod
    def report_hacker_abuse(user):
        send_hacker_abuse_email_notification(user.email)
        HackerAbuseEvents(user=user).save()


class ConsumerActivateInput(graphene.InputObjectType):
    token = graphene.String(
        description="A one-time token required to set the password.", required=True
    )


class ConsumerActivate(ModelMutation):
    INVALID_TOKEN = "ACCOUNT_CONFIRMATION_LINK_EXPIRED"

    class Arguments:
        id = graphene.ID(
            description="ID of a user to activate account whom.", required=True
        )
        input = ConsumerActivateInput(
            description="Fields required to activate account.", required=True
        )

    class Meta:
        description = "Activates user account."
        model = User

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        token = cleaned_input.pop("token")
        if not activation_token_generator.check_token(instance, token):
            raise ValidationError(ConsumerActivate.INVALID_TOKEN)
        return cleaned_input

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.is_active = True
        instance.save()

    @classmethod
    def get_instance(cls, info, **data):
        data["id"] = graphene.Node.to_global_id(
            "User", force_text(urlsafe_base64_decode(data.get("id"))))
        return super().get_instance(info, **data)
