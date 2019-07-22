from behave import then


@then(u'il n\'obtient aucun message d\'erreur')
def step_impl(context):
    user_mutation = next(iter(context.response['data']))
    context.test.assertEqual(
        0, len(context.response['data'][user_mutation]['errors']))
