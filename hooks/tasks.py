import random
import time
from datetime import timedelta

from django.utils import timezone

from core.celery import app
from hooks.models import Webhook, WebhookData

from django.contrib.auth import get_user_model

User = get_user_model()


@app.task
def create_hook_task(payload: dict) -> str:
    hook = Webhook.objects.create(user=User(payload.get('user_id')))
    WebhookData.objects.create(webhook=hook, data=None)
    return f'Webhook id: {hook.id} created'


@app.task
def write_webhook_data_task(payload: dict) -> str:
    webhook_data = Webhook.objects.get(id=payload.get('id'))
    webhook_data.data = payload.get('data')
    webhook_data.save()
    return f'WebhookData id: {webhook_data.id} updated'


@app.task
def hook_lifetime_task():
    hook_lifetime = timedelta(hours=4)
    last_4_hour_hooks = Webhook.objects.filter(created__gte=timezone.now() - hook_lifetime)
    for hook in last_4_hour_hooks:
        if timezone.now() - hook.created > hook_lifetime:
            hook.delete()
    return 'hook_lifetime_task finished'
