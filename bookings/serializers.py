from rest_framework.serializers import ModelSerializer
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
