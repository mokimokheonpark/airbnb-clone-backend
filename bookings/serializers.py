from django.utils import timezone
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Booking


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "guests",
            "room_check_in",
            "room_check_out",
            "experience_time",
        )


class RoomBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "guests",
            "room_check_in",
            "room_check_out",
        )

    def validate_room_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if value < now:
            raise ValidationError(
                "Error: The date of room_check_in must be greater than or equal to today."
            )
        return value

    def validate_room_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        tomorrow = now + timezone.timedelta(days=1)
        if value < tomorrow:
            raise ValidationError(
                "Error: The date of room_check_out must be greater than today."
            )
        return value

    def validate(self, data):
        room = self.context.get("room")
        if data["room_check_out"] <= data["room_check_in"]:
            raise ValidationError(
                "Error: The date of room_check_out must be greater then the date of room_check_in"
            )
        if Booking.objects.filter(
            room=room,
            room_check_in__lt=data["room_check_out"],
            room_check_out__gt=data["room_check_in"],
        ).exists():
            raise ValidationError(
                "Error: The room has been already booked on some (or all) of the dates"
            )
        return data
