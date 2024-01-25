from django.core.exceptions import ObjectDoesNotExist
from celery.result import AsyncResult
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hooks.models import Webhook, WebhookData
from hooks.serializers import WebhookSerializer, WebhookDataSerializer
from hooks.tasks import create_hook_task, write_webhook_data_task


class WebhookViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer

    def get_queryset(self):
        if self.request.user.id == 1:
            return Webhook.objects.all()
        return Webhook.objects.filter(user_id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        try:
            obj = Webhook.objects.get(id=kwargs.get('pk'))
            serializer = self.get_serializer_class()
            return Response(serializer(obj).data)
        except ObjectDoesNotExist as error:
            raise ValidationError(f'object_does_not_exists: {error}')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = create_hook_task.delay(payload={'user_id': request.user.id})
        return Response({'task_id': task.id}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        pass


class WebhookDataViewSet(UpdateModelMixin, GenericViewSet):
    queryset = WebhookData.objects.all()
    serializer_class = WebhookDataSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = write_webhook_data_task.delay(payload={'webhook_id': kwargs.get('pk'),
                                                      'data': request.data.get('data')})
        return Response({'task_id': task.id}, status=status.HTTP_201_CREATED)


class TaskResultViewSet(RetrieveModelMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        task_result = AsyncResult(id=kwargs.get('task_id'))
        return Response({
            'id': task_result.id,
            'state': task_result.state,
            'status': task_result.status,
            'result': task_result.result if not TypeError else task_result.result.__str__(),
        })
