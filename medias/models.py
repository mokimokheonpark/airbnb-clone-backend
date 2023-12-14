from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    def __str__(self) -> str:
        return f"{self.room}"

    file = models.URLField()

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
