from rest_framework import serializers


# This serializer is used to seria;ize the  seller/reviewer's data for display
class PublicUserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
