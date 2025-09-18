from django.urls import path
from .views import TrackerHomeView

urlpatterns = [
    path("", TrackerHomeView.as_view(), name="home"),
]
