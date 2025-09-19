from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import LoginForm
# Create your views here.


class TrackerHomeView(TemplateView):
    template_name = "LandingPage.html"


class LoginPageView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True  # To redirect the authenticated user to the LOGIN_REDIRECT_URL defined in the settings.
