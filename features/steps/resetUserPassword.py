from behave import given, then, when
from datetime import datetime
from datetime import timedelta
from saleor.account.models import User


@given(u'un {persona:PersonaType} qui a reçu un lien de réinitialisation de mot de passe')
def step_impl(context, persona):
    raise NotImplementedError(
        u'STEP: Given un Consommateur qui a reçu un lien de réinitialisation de mot de passe')


@given(u'qui a déjà réinitialisé son mot de passe avec ce lien')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Given qui a déjà réinitialisé son mot de passe avec ce lien')


@when(u'un {persona:PersonaType} enregistré fait une demande de réinitialisation de mot de passe')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: When un Consommateur enregistré fait une demande de réinitialisation de mot de passe')


@when(u'un utilisateur inconnu fait une demande de réinitialisation de mot de passe')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: When un utilisateur inconnu fait une demande de réinitialisation de mot de passe')


@when(u'il définit un mot de passe conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: When il définit un mot de passe conforme au plus tard 1 jour après sa réception')


@when(u'il définit un mot de passe non conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context):
    # expiration_delta_in_seconds = amount * unit
    # elapsed_time_since_email_reception_in_seconds = (
    #     datetime.now() - context.email_reception_time).total_seconds()
    # context.test.assertTrue(
    #     elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)
    # uidb64 = context.credentials['uidb64']
    # token = context.credentials['token']
    # password = 'abdc'
    # activate_account(context, uidb64, token, password)
    raise NotImplementedError(
        u'STEP: When il définit un mot de passe non conforme au plus tard 1 jour après sa réception')


@when(u'il le réinitialise pour la deuxième fois')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: When il le réinitialise pour la deuxième fois')


@when(u'il définit un mot de passe conforme 2 jours après sa réception')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: When il définit un mot de passe conforme 2 jours après sa réception')


@then(u'il reçoit un e-mail de réinitialisation de mot de passe')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Then il reçoit un e-mail de réinitialisation de mot de passe')


@then(u'son mot de passe reste inchangé')
def step_impl(context):
    #     user = User.objects.filter(email=context.unknown['email'])
    #     context.test.assertEqual(user.password, context.current_encrypted_password)
    raise NotImplementedError(u'STEP: Then son mot de passe reste inchangé')


@then(u'il ne reçoit pas d\'e-mail de réinitialisation de compte')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Then il ne reçoit pas d\'e-mail de réinitialisation de compte')


@then(u'son nouveau mot de passe est sauvegardé')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Then son nouveau mot de passe est sauvegardé')


@then(u'son lien de réinitialisation est invalidé')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Then son lien de réinitialisation est invalidé')
