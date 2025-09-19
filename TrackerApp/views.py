from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegistrationForm
from .models import CustomUser
# Create your views here.


class TrackerHomeView(TemplateView):
    template_name = "LandingPage.html"


class LoginPageView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True  # To redirect the authenticated user to the LOGIN_REDIRECT_URL defined in the settings.


class RegisterPageView(CreateView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    model = CustomUser
    success_url = reverse_lazy("login")
