from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
import logging

from .serializers import UserRegisterSerializer

'''
I want to have sperate accounts for buyers and sellers
I want to log buyers in seperately and log sellers in seperately
I want to add the group of is_buyer to buyer and the group of is_seller to seller in order to seperate their views 
I want a seller to be automatically logged out if he leaves the seller interface
I dont want the seller to be able to access the buyer-specific views using his seller account
I dont want to make it absolutely necessary for a buyer to log in, in order to make a transaction. He should be able to do so 
  
'''
# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserRegistrationView(CreateAPIView):
    '''
    This view creates account for the user and gives him authority of seller or buyer by assigning
    relevant group
    '''
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            logger.info("Received registration request.")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Create the user
                user = get_user_model().objects.create_user(username=serializer.validated_data['username'],
                                                            password=serializer.validated_data['password']
                                                            , email=serializer.validated_data['email'])
                if serializer.validated_data['is_buyer']:
                    buyer_group = Group.objects.get(name="buyer")
                    user.groups.add(buyer_group)
                elif serializer.validated_data['is_seller']:
                    seller_group = Group.objects.get(name="seller")
                    user.groups.add(seller_group)

                user.save()
                return Response("User Account successfully created", status=status.HTTP_201_CREATED)

        except ValidationError as validation_error:
            # Handle serializer validation errors
            logger.error(f"Validation error: {validation_error}")
            return Response({"error": str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(f"The following error occurred {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
