from rest_framework.serializers import ModelSerializer, HiddenField, JSONField

from hooks.models import Webhook


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


class WebhookSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Webhook
        fields = ('id', 'data', 'user_id', 'user', 'created')
        read_only_fields = ('user',)
