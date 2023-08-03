from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializers import RoomListSerializer


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )

    rooms = RoomListSerializer(
        read_only=True,
        many=True,
    )
