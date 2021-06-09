from django.db import models


class Checkout(models.Model):
    user_email = models.EmailField()
    #lines


class CheckoutLine(models.Model):
    checkout = models.ForeignKey(
        Checkout, related_name="lines", on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        "product.ProductVariant", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
