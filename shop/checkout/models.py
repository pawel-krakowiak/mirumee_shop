from django.db import models
from django.conf import settings
from datetime import datetime as dt

class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_email = model.EmailField(max_lenght=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {dt.now().strftime("%Y/%m/%d %H:%M:%S")}"