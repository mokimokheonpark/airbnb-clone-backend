from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializers import RoomListSerializer


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            "name",
            "rooms",
        )

    rooms = RoomListSerializer(
        read_only=True,
        many=True,
    )
