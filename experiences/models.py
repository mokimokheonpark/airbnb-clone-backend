from django.db import models
from common.models import CommonModel


# Experience Model Definition
class Experience(CommonModel):
    def __str__(self) -> str:
        return self.name

    name = models.CharField(
        max_length=100,
        default="",
    )

    country = models.CharField(
        max_length=50,
        default="Canada",
    )

    city = models.CharField(
        max_length=50,
        default="Toronto",
    )

    address = models.CharField(
        max_length=100,
    )

    price = models.PositiveBigIntegerField()

    start = models.TimeField()
    end = models.TimeField()

    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    description = models.TextField()

    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )


# Perk Definition
# Something included on an Experience
class Perk(CommonModel):
    def __str__(self) -> str:
        return self.name

    name = models.CharField(
        max_length=100,
        default="",
    )

    detail = models.CharField(
        max_length=200,
        default="",
        blank=True,
    )

    description = models.TextField(
        default="",
        blank=True,
    )
