from rest_framework.serializers import ModelSerializer, HiddenField, JSONField

from hooks.models import Webhook, WebhookData


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


class QueryParamsWebhookDefault:
    requires_context = True

    def __call__(self, serializer_field):
        pk = serializer_field.context['request'].parser_context.get('kwargs').get('pk')
        return Webhook.objects.get(id=pk)


class WebhookSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Webhook
        fields = ('id', 'created', 'data', 'user_id', 'user')


class WebhookDataSerializer(ModelSerializer):
    webhook = HiddenField(default=QueryParamsWebhookDefault())

    class Meta:
        model = WebhookData
        fields = '__all__'
