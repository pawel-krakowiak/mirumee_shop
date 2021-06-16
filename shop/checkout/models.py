from django.db import models
from django.conf import settings
from ..product.models import ProductVariant


class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    user_email = models.EmailField()


class CheckoutLine(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    checkout = models.ForeignKey(Checkout, related_name='lines', on_delete=models.CASCADE)
