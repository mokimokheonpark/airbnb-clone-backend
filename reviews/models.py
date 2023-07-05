from django.db import models
from django.core.validators import MaxValueValidator
from common.models import CommonModel


# Review Model Definition
# Review from a User to a Room or Experience
class Review(CommonModel):
    def __str__(self) -> str:
        return f"{self.user}'s review"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    review = models.TextField()

    rating = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(5)],
    )
