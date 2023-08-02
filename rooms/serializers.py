from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
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
            "rating",
            "is_owner",
            "photos",
        )

    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


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
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )
    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
