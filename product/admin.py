from django.contrib import admin

# Register your models here.
from .models import Product, ProductVariant

admin.site.register(Product)
admin.site.register(ProductVariant)
