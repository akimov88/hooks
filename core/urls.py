from django.contrib import admin
from django.urls import path, include

from core.views import KeycloakLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hooks/', include('hooks.urls')),
    path('keycloak_auth/', KeycloakLoginView.as_view(), name='keycloak_login'),
]
