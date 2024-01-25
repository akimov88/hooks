from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from core.utils import get_client

User = get_user_model()


class KeycloakLoginView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None
        self.user = None

    def get(self, request, *args, **kwargs):
        self.client = get_client()
        redirect_uri = request.build_absolute_uri(reverse('keycloak_login'))
        code = request.GET.get('code')
        if code:
            token = self.client.token(
                grant_type='authorization_code',
                code=code,
                redirect_uri=redirect_uri
            )
            user_info = self.client.userinfo(token.get('access_token'))
            self._get_or_create_user(user_info=user_info)
            login(request, self.user)
            return redirect(reverse('admin:index'))
        login_url = self.client.auth_url(redirect_uri=redirect_uri, scope='openid profile roles')
        return redirect(login_url)

    def _get_or_create_user(self, user_info):
        self.user, created = User.objects.get_or_create(username=user_info.get('preferred_username'))
        if created or any((not self.user.first_name, not self.user.last_name, not self.user.email)):
            self.user.email = user_info.get('email'),
            self.user.first_name = user_info.get('first_name'),
            self.user.last_name = user_info.get('last_name'),
            self.user.save()
