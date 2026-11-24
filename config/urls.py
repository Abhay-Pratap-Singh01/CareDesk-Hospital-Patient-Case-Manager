from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from .demo_auth import demo_login


production_login_view = auth_views.LoginView.as_view(
    template_name="registration/login.html"
)


def login_view(request):
    if settings.DEMO_MODE:
        return demo_login(request)
    return production_login_view(request)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("patients.urls")),
]
