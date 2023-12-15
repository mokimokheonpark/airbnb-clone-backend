from rest_framework.serializers import ModelSerializer
from .models import Photo


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "id",
            "file",
            "room",
        )


class PhotoDetailSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"
