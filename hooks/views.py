from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from hooks.models import Webhook
from hooks.serializers import WebhookCreateSerializer, WebhookDefaultSerializer


class WebhookViewSet(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Webhook.objects.all()

    def get_queryset(self):
        if self.request.user.id == 1:
            return Webhook.objects.all()
        return Webhook.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update', 'destroy'):
            return WebhookDefaultSerializer
        return WebhookCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            obj = Webhook.objects.get(id=kwargs.get('pk'))
            serializer = self.get_serializer_class()
            return Response(serializer(obj).data)
        except ObjectDoesNotExist as error:
            raise ValidationError(f'object_does_not_exists: {error}')

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
