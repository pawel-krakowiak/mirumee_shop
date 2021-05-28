from django.db import models
from django.conf import settings
from datetime import datetime as dt

from ..product.models import ProductVariant

class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    user_email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.user_email:
            if self.user != None:
                return f"Checkout: {self.user_email} ID: {self.id} - User: ({self.user})"
            return f"Checkout: {self.user_email} ID: {self.id}"
        else:
            return f"Checkout: (Uknown Owner) ID: {self.id}"

class CheckoutLine(models.Model):
    checkout = models.ForeignKey(Checkout, related_name='lines', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='+', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"ID: {self.id} Variant: {self.variant} Quantity: {self.quantity}"