from django.core.exceptions import ObjectDoesNotExist
from django_celery_results.models import TaskResult
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hooks.models import Webhook
from hooks.serializers import WebhookCreateSerializer, WebhookDefaultSerializer
from hooks.tasks import create_hook_task, update_hook_data_task, delete_hook_task


class WebhookViewSet(RetrieveModelMixin, CreateModelMixin, ListModelMixin,
                     UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Webhook.objects.all()

    def get_queryset(self):
        if self.request.user.id == 1:
            return Webhook.objects.all()
        return Webhook.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list', 'update', 'destroy'):
            return WebhookDefaultSerializer
        return WebhookCreateSerializer

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
        task = create_hook_task.delay({
            'user_id': request.user.id,
            'data': serializer.data,
        })
        return Response({'task_id': task.id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = update_hook_data_task.delay({
            'id': kwargs.get('pk'),
            'data': serializer.data,
        })
        return Response({'task_id': task.id}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = delete_hook_task({
            'id': kwargs.get('pk'),
            'data': serializer.data,
        })
        return Response({'task_id': task.id}, status=status.HTTP_200_OK)


class TaskResultViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = TaskResult.objects.all()

    def retrieve(self, request, *args, **kwargs):
        task_result = self.queryset.get(task_id=kwargs.get('task_id'))
        return Response({'result': task_result.result})
