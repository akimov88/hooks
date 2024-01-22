from hooks.views import WebhookViewSet
from django.urls import path


urlpatterns = [
    path('webhook/', WebhookViewSet.as_view({'post': 'create'})),
    path('webhook/list/', WebhookViewSet.as_view({'get': 'list'})),
    path('webhook/<int:pk>/', WebhookViewSet.as_view({'get': 'retrieve'})),
    path('webhook/<int:pk>/write/', WebhookViewSet.as_view({'post': 'update'})),
    path('webhook/<int:pk>/delete/', WebhookViewSet.as_view({'post': 'delete'})),
]
