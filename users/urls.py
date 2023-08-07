from django.urls import path
from .views import Users, UserProfile

urlpatterns = [
    path("", Users.as_view()),
    path("profile", UserProfile.as_view()),
]
