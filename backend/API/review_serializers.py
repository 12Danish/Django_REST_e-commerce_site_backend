from rest_framework import serializers
from .models import Review
from .user_serializers import PublicUserSerializer

# This serializer is used to serialize the reviews
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        reviewer = PublicUserSerializer(source="reviewer", read_only=True)
        fields = [
            "reviewer",
            "stars",
            "body"

        ]
