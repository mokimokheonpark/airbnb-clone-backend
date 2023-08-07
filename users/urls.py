from django.urls import path
from .views import Users, UserProfile, MyProfile, ChangePassword

urlpatterns = [
    path("", Users.as_view()),
    path("@<str:username>", UserProfile.as_view()),
    path("my-profile", MyProfile.as_view()),
    path("change-password", ChangePassword.as_view()),
]
