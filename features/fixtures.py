import os.path
from behave import fixture

from features.utils import *
from saleor.account.models import User


@fixture
def graphql_query(context, queryfile):
    context.query = get_query_from_file(queryfile)
    yield context.query
    del context.query


@fixture
def unknown(context):
    user_data = get_user_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Credentials', 'InvalidEmailAndPassword.json'))
    context.unknown = user_data
    yield context.unknown
    del context.unknown


@fixture
def consumer(context):
    user_data = get_user_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Credentials', 'Consommateur.json'))
    user = create_database_user(user_data)
    context.consumer = user_data
    yield context.consumer
    user.delete()
    del context.consumer


@fixture
def producer(context):
    user_data = get_user_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Credentials', 'Producteur.json'))
    user = create_database_user(user_data)
    context.producer = user_data
    yield context.producer
    user.delete()
    del context.producer


@fixture
def manager(context):
    user_data = get_user_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Credentials', 'Responsable.json'))
    user = create_database_user(user_data)
    context.manager = user_data
    yield context.manager
    user.delete()
    del context.manager


@fixture
def rex(context):
    user_data = get_user_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Credentials', 'Rex.json'))
    user = create_database_user(user_data)
    context.rex = user_data
    yield context.rex
    user.delete()
    del context.rex


@fixture
def softozor(context):
    user_data = get_user_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Credentials', 'Softozor.json'))
    user = User.objects.create_superuser(email=user_data['email'])
    user.set_password(user_data['password'])
    user.save()
    context.softozor = user_data
    yield context.softozor
    user.delete()
    del context.softozor
