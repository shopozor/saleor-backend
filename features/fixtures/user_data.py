from behave import fixture

from saleor.account.models import User


@fixture
def customer(context):
    password = 'H7V6WfOgnkDf68BAR4MN'
    customer = User.objects.create(email='customer@shopozor.ch')
    customer.set_password(password)
    customer.save()
    context.customer = {
        'email': customer.email,
        'password': password
    }
    yield context.customer
    del context.customer


@fixture
def staff(context):
    password = 'ceOC6T5efnWRQqdequpN'
    staff = User.objects.create(email='staff@shopozor.ch', is_staff=True)
    staff.set_password(password)
    staff.save()
    context.staff = {
        'email': staff.email,
        'password': password
    }
    yield context.staff
    del context.staff


@fixture
def unknown(context):
    password = 'password'
    email = 'unknown@shopozor.ch'
    context.unknown = {
        'email': email,
        'password': password
    }
    yield context.unknown
    del context.unknown
