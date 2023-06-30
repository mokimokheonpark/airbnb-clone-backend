from django.db import models
from common.models import CommonModel


# Category Model Definition
# Category of Room or Experience
class Category(CommonModel):
    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"

    class CategoryKindChoices(models.TextChoices):
        ROOMS = ("rooms", "Rooms")
        EXPERIENCES = ("experiences", "Experiences")

    name = models.CharField(
        max_length=50,
    )

    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )
