
import graphene
from copy import copy
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from saleor.account.models import User

from saleor.graphql.core.mutations import CreateToken, ModelMutation, BaseMutation
from saleor.graphql.core.types import Error

from shopozor.emails import EmailSender
from shopozor.exceptions import HackerAbuseException
from shopozor.models import HackerAbuseEvents
from shopozor.tokens import activation_token_generator, INVALID_TOKEN


def to_node_global_id(**data):
    return graphene.Node.to_global_id(
        "User", force_text(urlsafe_base64_decode(data.get("id"))))


class Login(CreateToken):

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
            email_sender = EmailSender()
            email_sender.send_activate_account_email(instance.pk)
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
            data['input']['email'] = data['input']['email'].lower()
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
        email_sender = EmailSender()
        email_sender.send_hacker_abuse_email_notification(user.email)
        HackerAbuseEvents(user=user).save()


class ConsumerActivateInput(graphene.InputObjectType):
    token = graphene.String(
        description="A one-time token required to set the password.", required=True
    )


class ConsumerActivate(ModelMutation):
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
            raise ValidationError(INVALID_TOKEN)
        return cleaned_input

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.is_active = True
        instance.save()

    @classmethod
    def get_instance(cls, info, **data):
        data["id"] = to_node_global_id(**data)
        return super().get_instance(info, **data)


class PasswordReset(BaseMutation):
    class Arguments:
        email = graphene.String(description="Email", required=True)

    class Meta:
        description = "Sends password reset email"

    @classmethod
    def perform_mutation(cls, _root, info, email):
        try:
            user = User.objects.get(email=email)
            email_sender = EmailSender()
            email_sender.send_password_reset(user)
        except ObjectDoesNotExist:
            pass

        return PasswordReset()


class SetPasswordInput(graphene.InputObjectType):
    token = graphene.String(
        description="A one-time token required to set the password.", required=True
    )
    password = graphene.String(description="Password", required=True)


class SetPassword(ModelMutation):
    class Arguments:
        id = graphene.ID(
            description="ID of a user to set password whom.", required=True
        )
        input = SetPasswordInput(
            description="Fields required to set password.", required=True
        )

    class Meta:
        description = "Sets user password."
        model = User

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        token = cleaned_input.pop("token")
        if not default_token_generator.check_token(instance, token):
            raise ValidationError(INVALID_TOKEN)
        return cleaned_input

    @classmethod
    def save(cls, info, instance, cleaned_input):
        # the set_password actually encodes the password. The instance already contains
        # the correct password after: instance = cls.construct_instance(instance, cleaned_input)
        try:
            validate_password(cleaned_input["password"])
            instance.set_password(cleaned_input["password"])
            instance.save()
        except ValidationError as error:
            errors = error.error_list
            errors.insert(0, ValidationError("PASSWORD_NOT_COMPLIANT"))
            raise ValidationError(errors)

    @classmethod
    def get_instance(cls, info, **data):
        data["id"] = to_node_global_id(**data)
        return super().get_instance(info, **data)
