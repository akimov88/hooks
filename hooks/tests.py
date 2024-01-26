import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate

from hooks.models import Webhook, WebhookData
from hooks.views import WebhookViewSet, WebhookDataViewSet, TaskResultViewSet

User = get_user_model()
db_tests = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'tests',
}


class AbstractTestCase(TestCase):
    databases = {'default': db_tests}
    factory = APIRequestFactory()

    def setUp(self):
        self.user = User.objects.create(username='admin')
        self.hook = Webhook.objects.create(user_id=self.user.id)
        self.data = WebhookData.objects.create(webhook=self.hook, data=json.dumps({'1': '1'}))


class WebhookTestCase(AbstractTestCase):
    def test_retrieve(self):
        request = self.factory.get(path='/webhook/<int:pk>', format='json')
        force_authenticate(request=request, user=self.user)
        response = WebhookViewSet.as_view(actions={'get': 'retrieve'})(request, pk=self.hook.id)
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        request = self.factory.get(path='/webhook/list', format='json')
        force_authenticate(request=request, user=self.user)
        response = WebhookViewSet.as_view(actions={'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        request = self.factory.post(path='/webhook/', format='json')
        force_authenticate(request=request, user=self.user)
        response = WebhookViewSet.as_view(actions={'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        request = self.factory.post(path=f'/webhook/<int:pk>/write', format='json')
        force_authenticate(request=request, user=self.user)
        response = WebhookDataViewSet.as_view(actions={'post': 'update'})(request, pk=self.hook.id)
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        request = self.factory.delete(path=f'/webhook/<int:pk>/delete', format='json')
        force_authenticate(request=request, user=self.user)
        response = WebhookViewSet.as_view(actions={'delete': 'destroy'})(request, pk=self.hook.id)
        self.assertEqual(response.status_code, 204)

    def test_task_result(self):
        pass
