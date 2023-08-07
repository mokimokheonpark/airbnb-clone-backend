from django.urls import path
from .views import Users, UserProfile, MyProfile, ChangePassword, LogIn, LogOut

urlpatterns = [
    path("", Users.as_view()),
    path("@<str:username>", UserProfile.as_view()),
    path("my-profile", MyProfile.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
]
