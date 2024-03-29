from django.urls import path

from hooks.views import WebhookViewSet, WebhookDataViewSet
from hooks.views import TaskResultViewSet

urlpatterns = [
    path('webhook/', WebhookViewSet.as_view({'post': 'create'})),
    path('webhook/list/', WebhookViewSet.as_view({'get': 'list'})),
    path('webhook/<int:pk>/', WebhookViewSet.as_view({'get': 'retrieve'})),
    path('webhook/<int:pk>/delete', WebhookViewSet.as_view({'delete': 'destroy'})),
    path('webhook/<int:pk>/write', WebhookDataViewSet.as_view({'post': 'update'})),
    path('task/<str:task_id>/', TaskResultViewSet.as_view({'get': 'retrieve'})),
]
