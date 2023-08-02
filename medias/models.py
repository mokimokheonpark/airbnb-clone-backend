from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    def __str__(self) -> str:
        return "Photo File"

    file = models.URLField()

    description = models.CharField(
        max_length=200,
    )

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )


class Video(CommonModel):
    def __str__(self) -> str:
        return "Video File"

    file = models.URLField()

    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )
