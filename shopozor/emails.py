from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, get_connection
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from saleor.account.models import User
from shopozor.models import EmailSmtpConfiguration
from shopozor.tokens import activation_token_generator


class EmailSender:

    def __init__(self):
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
            config = EmailSmtpConfiguration.objects.get(pk=1)
            self.__CONNECTION = EmailBackend(host=config.host, port=config.port, username=config.host_user,
                                             password=config.host_password, use_tls=config.use_tls, use_ssl=config.use_ssl)
        else:
            self.__CONNECTION = None

    def get_email_base_context(self):
        site = Site.objects.get_current()
        return {"domain": site.domain, "site_name": site.name}

    def __get_email_base_info(self, user):
        email = user.email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = self.get_email_base_context()
        return {'email': email, 'uid': uid, 'current_site': current_site}

    def send_activate_account_email(self, pk):
        user = User.objects.get(pk=pk)
        base_info = self.__get_email_base_info(user)
        token = activation_token_generator.make_token(user)
        mail_subject = 'Activate your customer account.'
        message = render_to_string('acc_active_email.html', {
            'domain': base_info['current_site'].get("domain"),
            'uid': base_info['uid'],
            'token': token,
        })
        email = EmailMessage(
            mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[
                base_info['email']], connection=self.__CONNECTION
        )
        email.send()

    def send_hacker_abuse_email_notification(self, email):
        current_site = self.get_email_base_context()
        mail_subject = 'Someone tried to create a user account with your email.'
        time_event = datetime.now()
        message = render_to_string('hacker_abuse_email.html', {
            'domain': current_site.get("domain"),
            'day': time_event.day,
            'month': time_event.month,
            'year': time_event.year,
            'hour': time_event.hour,
            'minute': time_event.minute
        })
        email = EmailMessage(
            mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[
                email], connection=self.__CONNECTION
        )
        email.send()

    def send_password_reset(self, user):
        email = user.email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = self.get_email_base_context()
        mail_subject = 'Password Reset Request.'
        message = render_to_string('password_reset_email.html', {
            'domain': current_site.get("domain"),
            'uid': uid,
            'token': token,
        })
        email = EmailMessage(
            mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[
                email], connection=self.__CONNECTION
        )
        email.send()
