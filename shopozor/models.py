from django.db import models
from saleor.account.models import User
from saleor.product.models import Product as SaleorProduct
from saleor.product.models import ProductVariant
from saleor.core.permissions import MODELS_PERMISSIONS

MODELS_PERMISSIONS.append('account.manage_producers')
MODELS_PERMISSIONS.append('account.manage_managers')
MODELS_PERMISSIONS.append('account.manage_rex')


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