from django.contrib import admin

from .models import Checkout, CheckoutLine

admin.site.register(Checkout)
admin.site.register(CheckoutLine)