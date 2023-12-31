from django.db import models
from common.models import CommonModel


# Room Model Definition
class Room(CommonModel):
    def __str__(self) -> str:
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self):
        rating_count = self.reviews.count()
        if rating_count == 0:
            return 0
        rating_sum = 0
        for review in self.reviews.all().values("rating"):
            rating_sum += review["rating"]
        rating_average = rating_sum / rating_count
        return round(rating_average, 1)

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

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

    room_kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )

    rooms = models.PositiveBigIntegerField()

    toilets = models.PositiveBigIntegerField()

    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )

    pet_friendly = models.BooleanField(
        default=True,
    )

    description = models.TextField()

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )


# Amenity Model Definition
class Amenity(CommonModel):
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

    name = models.CharField(
        max_length=50,
    )

    description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
