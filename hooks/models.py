from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Webhook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def user_id(self):
        return self.user.id

    @property
    def data(self):
        return WebhookData.objects.get(webhook=self).data

    def __str__(self):
        return f'Webhook {self.id}'


class WebhookData(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'WebhookData {self.id}]'
