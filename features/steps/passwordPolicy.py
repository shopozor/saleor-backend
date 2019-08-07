from behave import given, then
from django.contrib.auth.password_validation import validate_password, ValidationError


@given(u'le mot de passe {password}')
def step_impl(context, password):
    context.password = password


@then(u'il est non conforme')
def step_impl(context):
    with context.test.assertRaises(ValidationError):
        validate_password(context.password)
