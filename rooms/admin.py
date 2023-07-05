from django.contrib import admin
from .models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "room_kind",
        "total_amenities",
        "owner",
        "created_at",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "room_kind",
        "rooms",
        "toilets",
        "amenities",
        "pet_friendly",
        "created_at",
        "updated_at",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
