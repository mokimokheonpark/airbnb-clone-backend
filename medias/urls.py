from django.urls import path
from .views import Photos, PhotoDetail

urlpatterns = [
    path("photos", Photos.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
]
