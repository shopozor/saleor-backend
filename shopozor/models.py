from django.db import models
from saleor.account.models import User
from saleor.product.models import Product as SaleorProduct
from saleor.product.models import ProductVariant
from saleor.core.permissions import MODELS_PERMISSIONS

MODELS_PERMISSIONS.append('account.manage_producers')
MODELS_PERMISSIONS.append('account.manage_managers')
MODELS_PERMISSIONS.append('account.manage_rex')


class EmailSmtpConfiguration(models.Model):
    host = models.CharField(max_length=1024)
    port = models.PositiveSmallIntegerField(default=1025)
    host_user = models.CharField(max_length=256)
    host_password = models.CharField(max_length=256)
    use_ssl = models.BooleanField(default=False)
    use_tls = models.BooleanField(default=False)


class HackerAbuseEvents(models.Model):
    message = models.CharField(max_length=256, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Shop(models.Model):
    name = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=46.775501)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=7.037878)
    product_variants = models.ManyToManyField(
        ProductVariant, blank=True)


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(blank=True)


class ProductStaff(models.Model):
    product = models.OneToOneField(
        SaleorProduct, on_delete=models.CASCADE, primary_key=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)


class Product(models.Model):
    product = models.OneToOneField(
        SaleorProduct, on_delete=models.CASCADE, primary_key=True
    )
    conservation_mode = models.CharField(max_length=256, blank=True)
    conservation_until = models.DateField()
    vat_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0)


class MarginDefinitions(models.Model):
    role = models.CharField(max_length=32, blank=True)
    margin = models.DecimalField(max_digits=6, decimal_places=2, default=0)
