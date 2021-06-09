from django.contrib import admin

# Register your models here.
from .models import User, UserManager

admin.site.register(User)