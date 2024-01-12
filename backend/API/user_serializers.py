from rest_framework import serializers


# This serializer is used to serialize the  seller/reviewer's data for display
class PublicUserSerializer(serializers.Serializer):
    '''
          This is a simple serializer which will serialize some fields of the user model in order to display them
          with the data. It is not saving anything to the db.
           '''
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
