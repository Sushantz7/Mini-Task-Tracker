from django.urls import path
from .views import TrackerHomeView, LoginPageView, RegisterPageView, TaskListView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", TrackerHomeView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterPageView.as_view(), name="register"),
    path("tasktracker/", TaskListView.as_view(), name="tasktracker"),
]
