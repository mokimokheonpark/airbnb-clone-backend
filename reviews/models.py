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
    )

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    review = models.TextField()

    rating = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(5)],
    )
