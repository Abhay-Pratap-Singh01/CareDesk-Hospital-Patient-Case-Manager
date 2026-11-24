from django import forms
from django.conf import settings
from django.shortcuts import redirect, render


DEMO_SESSION_KEY = "caredesk_demo_username"


class DemoLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)


class DemoUser:
    is_authenticated = True
    is_anonymous = False
    is_active = True
    is_staff = False
    is_superuser = False

    def __init__(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def get_full_name(self):
        return self.username

    def __str__(self):
        return self.username


def demo_login(request):
    form = DemoLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"].strip()
        password = form.cleaned_data["password"]
        if username and password.strip():
            request.session[DEMO_SESSION_KEY] = username
            return redirect(settings.LOGIN_REDIRECT_URL)
        form.add_error(None, "Enter both a username and password.")
    return render(request, "registration/login.html", {"form": form})


class DemoAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEMO_MODE:
            username = request.session.get(DEMO_SESSION_KEY)
            if isinstance(username, str) and username:
                request.user = DemoUser(username)
        return self.get_response(request)
