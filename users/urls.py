from django.urls import path
from .views import (
    Users,
    UserProfile,
    MyProfile,
    ChangePassword,
    LogIn,
    LogOut,
    JWTLogIn,
    GitHubLogIn,
    SignUp,
    CustomAuthToken,
)

urlpatterns = [
    path("", Users.as_view()),
    path("@<str:username>", UserProfile.as_view()),
    path("my-profile", MyProfile.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", LogIn.as_view()),  # log in with Cookies
    path("log-out", LogOut.as_view()),
    path("auth-token-log-in", CustomAuthToken.as_view()),  # log in with Auth Tokens
    path("jwt-log-in", JWTLogIn.as_view()),  # log in with JSON Web Tokens
    path("github-log-in", GitHubLogIn.as_view()),  # log in with GitHub Account
    path("sign-up", SignUp.as_view()),
]
