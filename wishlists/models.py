from django.db import models
from common.models import CommonModel


# Wishlist Model Definition
class Wishlist(CommonModel):
    def __str__(self) -> str:
        return self.name

    name = models.CharField(
        max_length=200,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    rooms = models.ManyToManyField(
        "rooms.Room",
        blank=True,
        related_name="wishlists",
    )

    experiences = models.ManyToManyField(
        "experiences.Experience",
        blank=True,
        related_name="wishlists",
    )
