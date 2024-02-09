from django.urls import path
from .views import Photos, PhotoDetail, PhotoUpload

urlpatterns = [
    path("photos", Photos.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
    path("upload-photo", PhotoUpload.as_view(), name="photo-upload"),
]
