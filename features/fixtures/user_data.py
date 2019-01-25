from behave import fixture

from saleor.account.models import User


@fixture
def customer(context):
    password = 'H7V6WfOgnkDf68BAR4MN'
    user = User.objects.create(email='customer@shopozor.ch')
    user.set_password(password)
    user.save()
    context.customer = {
        'email': user.email,
        'password': password
    }
    yield context.customer
    del context.customer


@fixture
def staff(context):
    password = 'ceOC6T5efnWRQqdequpN'
    user = User.objects.create(email='staff@shopozor.ch', is_staff=True)
    user.set_password(password)
    user.save()
    context.staff = {
        'email': user.email,
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


@fixture
def consumer(context):
    password = 'zzc0udkZBOK5vYerv51J'
    user = User.objects.create(email='consumer@shopozor.ch')
    user.set_password(password)
    user.save()
    context.consumer = {
        'email': user.email,
        'password': password
    }
    yield context.consumer
    del context.consumer


@fixture
def producer(context):
    password = 'NM34bo7yvVMy29gjzPTs'
    user = User.objects.create(email='producer@shopozor.ch', is_staff=True)
    user.set_password(password)
    user.save()
    context.producer = {
        'email': user.email,
        'password': password
    }
    yield context.producer
    del context.producer


@fixture
def manager(context):
    password = 'Lw5wuSo9Tc8XVI6pi5NY'
    user = User.objects.create(email='manager@shopozor.ch', is_staff=True)
    user.user_permissions.add('account.manage_producers')
    user.set_password(password)
    user.save()
    context.manager = {
        'email': user.email,
        'password': password
    }
    yield context.manager
    del context.manager


@fixture
def rex(context):
    password = 'bQsW6Tn7rqf6tGkCjnI0'
    user = User.objects.create(email='rex@shopozor.ch', is_staff=True)
    user.user_permissions.add('account.manage_producers')
    user.user_permissions.add('account.manage_managers')
    user.user_permissions.add('account.manage_users')
    user.user_permissions.add('account.manage_staff')
    user.set_password(password)
    user.save()
    context.rex = {
        'email': user.email,
        'password': password
    }
    yield context.rex
    del context.rex


@fixture
def softozor(context):
    password = 'hPDo8GU4vfZkPwaDvM9i'
    user = User.objects.create_superuser(email='softozor@shopozor.ch')
    user.set_password(password)
    user.save()
    context.softozor = {
        'email': user.email,
        'password': password
    }
    yield context.softozor
    del context.softozor
