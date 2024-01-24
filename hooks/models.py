from django.contrib.auth import get_user_model
from django.db import models

from hooks.utils import send_data

User = get_user_model()


class Webhook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
