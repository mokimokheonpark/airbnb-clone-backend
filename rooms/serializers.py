from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
