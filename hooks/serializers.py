from rest_framework.serializers import ModelSerializer, HiddenField

from hooks.models import Webhook


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


class WebhookDefaultSerializer(ModelSerializer):
    class Meta:
        model = Webhook
        fields = '__all__'


class WebhookCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Webhook
        fields = '__all__'
        read_only_fields = ('user_id',)
