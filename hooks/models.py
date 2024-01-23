from django.contrib.auth import get_user_model
from django.db import models

from hooks.utils import send_data

User = get_user_model()


class Webhook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.PositiveIntegerField()
    data = models.JSONField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        send_data({f'hook_id: {self.id}': self.data})

    @property
    def user(self):
        if self.__user is None:
            self.__user = User.objects.get(id=self.user_id)
        return self.__user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__user = None
