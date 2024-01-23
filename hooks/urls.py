from django.urls import path

from hooks.views import WebhookViewSet
from hooks.views import TaskResultAPIView

urlpatterns = [
    path('webhook/', WebhookViewSet.as_view({'post': 'create'})),
    path('webhook/list/', WebhookViewSet.as_view({'get': 'list'})),
    path('webhook/<int:pk>/', WebhookViewSet.as_view({'get': 'retrieve'})),
    path('webhook/<int:pk>/write/', WebhookViewSet.as_view({'post': 'update'})),
    path('webhook/<int:pk>/delete/', WebhookViewSet.as_view({'post': 'delete'})),
    path('task/<str:task_id>/', TaskResultAPIView.as_view({'get': 'retrieve'})),
]
