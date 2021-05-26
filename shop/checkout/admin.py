from django.contrib import admin

# Register your models here.
from .models import Checkout, CheckoutLines

admin.site.register(Checkout)
admin.site.register(CheckoutLines)