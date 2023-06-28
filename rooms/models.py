from django.db import models
from common.models import CommonModel


class Room(CommonModel):
    # Room Model Definition

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

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
    )

    pet_friendly = models.BooleanField(
        default=True,
    )

    description = models.TextField()

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )


class Amenity(CommonModel):
    # Amenity Definition

    name = models.CharField(
        max_length=50,
    )

    description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
