import random
import time

from hooks.models import Webhook
from core.celery import app


@app.task
def create_hook_task(payload: dict):
    time.sleep(random.randint(0, 1))
    hook = Webhook.objects.create(user_id=payload.get('user_id'), data=payload.get('data'))
    return f'webhook id: {hook.id} created'


@app.task
def update_hook_data_task(payload: dict):
    time.sleep(random.randint(0, 1))
    hook = Webhook.objects.get(id=payload.get('id'))
    hook.data = payload.get('data')
    hook.save()
    return f'webhook id: {hook.id} updated'


@app.task
def delete_hook_task(payload: dict):
    time.sleep(random.randint(0, 1))
    hook = Webhook.objects.get(id=payload.get('id'))
    hook.data = payload.get('data')
    hook.delete()
    return f'webhook id: {payload.get("id")} updated'
