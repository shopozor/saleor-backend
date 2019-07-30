from behave import then


@then(u'il n\'obtient aucun message d\'erreur')
def step_impl(context):
    user_mutation = next(iter(context.response['data']))
    context.test.assertEqual(
        0, len(context.response['data'][user_mutation]['errors']))


@then(u'il obtient un message d\'erreur stipulant que le lien a expiré')
def step_impl(context):
    # this retrieves the user mutation
    user_mutation = next(iter(context.response['data']))
    context.test.assertEqual(
        context.expired_link, context.response['data'][user_mutation])
