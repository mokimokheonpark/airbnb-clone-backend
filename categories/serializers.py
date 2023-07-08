from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.Serializer):
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            "name",
            instance.name,
        )
        instance.category_kind = validated_data.get(
            "category_kind",
            instance.category_kind,
        )
        instance.save()
        return instance

    pk = serializers.IntegerField(
        read_only=True,
    )

    name = serializers.CharField(
        required=True,
        max_length=50,
    )

    category_kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )

    created_at = serializers.DateTimeField(
        read_only=True,
    )
