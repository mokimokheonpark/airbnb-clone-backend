from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from common.models import CommonModel


class S3MediaStorage(S3Boto3Storage):
    location = "photos"
    file_overwrite = False


class Photo(CommonModel):
    def __str__(self) -> str:
        return f"{self.room}"

    file = models.ImageField(storage=S3MediaStorage())

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
