from behave import then


@then(u'il n\'obtient aucun message d\'erreur')
def step_impl(context):
    context.test.assertEqual(0, len(context.response['data']['errors']))
