import random
import time
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from core.celery import app
from hooks.models import Webhook


@app.task
def create_hook_task(payload: dict) -> str:
    time.sleep(random.randint(0, 2))
    hook = Webhook.objects.create(user_id=payload.get('user_id'), data=payload.get('data'))
    return f'webhook id: {hook.id} created'


@app.task
def update_hook_data_task(payload: dict) -> str:
    try:
        time.sleep(random.randint(0, 2))
        hook = Webhook.objects.get(id=payload.get('id'))
        hook.data = payload.get('data')
        hook.save()
        return f'webhook id: {hook.id} updated'
    except ObjectDoesNotExist as error:
        return f'Webhook {payload.get("id")} does not exists:\n\n{error}'


@app.task
def delete_hook_task(payload: dict) -> str:
    try:
        time.sleep(random.randint(0, 2))
        hook = Webhook.objects.get(id=payload.get('id'))
        hook.data = payload.get('data')
        hook.delete()
        return f'webhook id: {payload.get("id")} deleted'
    except ObjectDoesNotExist as error:
        return f'Webhook {payload.get("id")} does not exists:\n\n{error}'


@app.task
def hook_lifetime_task():
    hook_lifetime = timedelta(hours=4)
    last_hour_hooks = Webhook.objects.filter(created__gte=timezone.now() - hook_lifetime)
    for hook in last_hour_hooks:
        if timezone.now() - hook.created > hook_lifetime:
            hook.delete()
    return 'hook_lifetime_task finished'
