from rest_framework.serializers import ModelSerializer
from .models import Review
from users.serializers import TinyUserSerializer


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "user",
            "review",
            "rating",
        )

    user = TinyUserSerializer(read_only=True)
