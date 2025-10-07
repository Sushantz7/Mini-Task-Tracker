from django.contrib.auth.views import LogoutView
from django.urls import path

from utils.helper_functions import audit_detail
from .views import (
    TrackerHomeView,
    LoginPageView,
    RegisterPageView,
    TaskListView,
    TaskAjaxView,
    CategoryAjaxCreateView,
)

urlpatterns = [
    path("", TrackerHomeView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterPageView.as_view(), name="register"),
    path("tasktracker/", TaskListView.as_view(), name="tasktracker"),
    path("tasktracker/ajax/", TaskAjaxView.as_view(), name="task_ajax"),
    path("audit/<int:pk>/", audit_detail, name="audit_detail"),
    path("add-category/", CategoryAjaxCreateView.as_view(), name="add_category_ajax"),
]
