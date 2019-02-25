from django.db import models
from saleor.account.models import User
from saleor.core.permissions import MODELS_PERMISSIONS

MODELS_PERMISSIONS.append('account.manage_producers')
MODELS_PERMISSIONS.append('account.manage_managers')
MODELS_PERMISSIONS.append('account.manage_rex')


class HackerAbuse(models.Model):
    message = models.CharField(max_length=256, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hacker_abuse_event = models.ForeignKey(HackerAbuse, on_delete=models.CASCADE)
