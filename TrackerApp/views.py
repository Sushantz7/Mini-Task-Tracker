from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegistrationForm
from .models import CustomUser,Task
from django.contrib.auth.mixins import LoginRequiredMixin
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


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "TaskTrackerPage.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")
