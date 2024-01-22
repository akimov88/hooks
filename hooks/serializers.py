from hooks.models import Webhook
from rest_framework.serializers import ModelSerializer, HiddenField


class CurrentUserIdDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.id


class WebhookDefaultSerializer(ModelSerializer):
    user_id = HiddenField(default=CurrentUserIdDefault())

    class Meta:
        model = Webhook
        fields = '__all__'


class WebhookCreateSerializer(ModelSerializer):
    user_id = HiddenField(default=CurrentUserIdDefault())

    class Meta:
        model = Webhook
        fields = '__all__'
        read_only_fields = ('user_id',)
