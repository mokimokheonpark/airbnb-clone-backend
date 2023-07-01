from django.db import models
from common.models import CommonModel


# Booking Model Definition
class Booking(CommonModel):
    def __str__(self) -> str:
        return f"{self.user}'s {self.booking_kind} booking"

    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    guests = models.PositiveIntegerField()

    booking_kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    room_check_in = models.DateField(
        null=True,
        blank=True,
    )

    room_check_out = models.DateField(
        null=True,
        blank=True,
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
