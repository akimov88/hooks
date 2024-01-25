import hashlib
import json
import random
import time
from datetime import timedelta

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.celery import app
from hooks.models import Webhook, WebhookData

User = get_user_model()


@app.task(bind=True)
def create_hook_task(payload: dict) -> str:
    hook = Webhook.objects.create(user=User(payload.get('user_id')))
    WebhookData.objects.create(webhook=hook, data=None)
    return f'Webhook {hook.id} created'


@app.task(bind=True)
def write_webhook_data_task(payload: dict) -> str:
    try:
        webhook_data = WebhookData.objects.get(id=payload.get('id'))
        webhook_data.data = payload.get('data')
        webhook_data.save()
        return f'WebhookData {webhook_data.id} updated'
    except WebhookData.DoesNotExist as error:
        return f'WebhookData {payload.get("id")} does not exists'


@shared_task(bind=True)
def send_data(self, data: dict) -> dict:
    try:
        time.sleep(random.random())
        result = random.randint(0, 50)
        hash_data = hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
        if result <= 10:
            raise ValueError('send_data_error')
        return {'number': result, 'md5': hash_data}
    except ValueError:
        try:
            self.retry(countdown=5, max_retries=5)
        except MaxRetriesExceededError as error:
            return {'error': f'send_data_error:\n\n{error}'}


@app.task
def hook_lifetime_task():
    hook_lifetime = timedelta(hours=4)
    last_4_hour_hooks = Webhook.objects.filter(created__gte=timezone.now() - hook_lifetime)
    for hook in last_4_hour_hooks:
        if timezone.now() - hook.created > hook_lifetime:
            hook.delete()
    return 'hook_lifetime_task finished'
