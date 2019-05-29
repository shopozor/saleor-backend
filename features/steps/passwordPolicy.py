from behave import given, then
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


@given(u'le mot de passe {password}')
def step_impl(context, password):
    context.password_error = None
    try:
        validate_password(password)
    except Exception as e:
        context.password_error = e


@then(u'il est non conforme')
def step_impl(context):
    assert isinstance(context.password_error, ValidationError)
