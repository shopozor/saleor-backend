from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from saleor.account.models import User


def get_email_base_context():
    site = Site.objects.get_current()
    return {"domain": site.domain, "site_name": site.name}


def send_activate_account_email(pk):
    user = User.objects.get(pk=pk)
    email = user.email
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    current_site = get_email_base_context()
    mail_subject = 'Activate your customer account.'
    message = render_to_string('acc_active_email.html', {
        'domain': current_site.get("domain"),
        'uid': uid,
        'token': token,
    })
    email = EmailMessage(
        mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[
            email]
    )
    email.send()
