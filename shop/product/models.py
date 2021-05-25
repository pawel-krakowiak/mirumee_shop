from django.db import models


class Product(models.Model):
    name = models.CharField(null=False, blank=False, max_length=50)
    price = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=12)
    description = models.CharField(null=False, blank=False, max_length=255)
    quantity = models.IntegerField(default=0)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    sku = models.CharField(max_length=255, blank=False, null=False, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)