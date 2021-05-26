from django.db import models
from django.conf import settings
from datetime import datetime as dt

from ..product.models import ProductVariant

class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_email = models.EmailField(max_length=100, null=True, blank=True)
    # lines = models.ForeignKey(CheckoutLine, related_name='lines', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} - {dt.now.strftime('%m/%d/%Y, %H:%M:%S')}"

class CheckoutLine(models.Model):
    checkout = models.ForeignKey(Checkout, related_name='checkout', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='name', on_delete=models.CASCADE)
    variant_price = models.ForeignKey(ProductVariant, related_name='price', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.checkout} > Variant: {self.variant} Quantity: {self.quantity}"
