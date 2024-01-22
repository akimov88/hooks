from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Webhook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.PositiveIntegerField()
    data = models.JSONField(blank=True, null=True)

    @property
    def user(self):
        if self.__user is None:
            self.__user = User.objects.get(id=self.user_id)
        return self.__user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__user = None
