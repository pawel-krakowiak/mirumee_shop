from django.contrib import admin

# Register your models here.
from .models import Checkout, CheckoutLine

admin.site.register(Checkout)
admin.site.register(CheckoutLine)