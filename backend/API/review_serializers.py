from rest_framework import serializers
from .models import Review


# This serializer is used to serialize the reviews
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "stars",
            "body",
            "name"

        ]

    # Before successfully creating an instance of the model sending the information for product_id and the user
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product_id = self.context['product_id']
        return Review.objects.create(reviewer=user, product_id=product_id, **validated_data)
