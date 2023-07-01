from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = (
        "user",
        "guests",
        "booking_kind",
        "room",
        "room_check_in",
        "room_check_out",
        "experience",
        "experience_time",
    )

    list_filter = ("booking_kind",)
