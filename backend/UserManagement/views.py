from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
import logging
from .serializers import UserRegisterSerializer, UserLoginSerializer
import base64
from django.contrib.auth.hashers import check_password

from rest_framework_simplejwt.tokens import RefreshToken

'''
I want to have sperate accounts for buyers and sellers -- Done
I want to log buyers in seperately and log sellers in seperately -- done
I want to add the group of is_buyer to buyer and the group of is_seller to seller in order to seperate their views -- done 
I want a seller to be automatically logged out if he leaves the seller interface
I dont want the seller to be able to access the seller-specific views using his seller account
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

            logger.info(f"Received registration request. The data is {request.data}")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():

                logger.info(f"Serialization was successfull")
                # Create the user
                user = get_user_model().objects.create_user(username=serializer.validated_data['username'],
                                                            password=serializer.validated_data['password']
                                                            , email=serializer.validated_data['email'])
                logger.info(f"User was created successufully {user.username}")
                try:
                    if serializer.validated_data['is_buyer']:
                        logger.info(f"Statement entered for buyer")
                        logger.info(f"The groups  are {Group.objects.all()}")
                        buyer_group = Group.objects.get(name="buyer")
                        logger.info(f"The buyer group was found {buyer_group} ")
                        user.groups.add(buyer_group)
                        logger.info(f"Buyer group was addedd {user.groups.filter(name='is_buyer')}")
                    elif serializer.validated_data['is_seller']:
                        seller_group = Group.objects.get(name="seller")
                        user.groups.add(seller_group)
                        logger.info(f"Seller group was addedd {user.groups.filter(name='is_buyer')}")
                except Exception as e:
                    return Response(f"An error occurred while assigning group {e}")

                user.save()
                logger.info(f"User was saved to the database")
                return Response({"message": "User Account successfully created"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Credentials were not correctly provided", "data": serializer.data},
                                status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as validation_error:
            # Handle serializer validation errors
            return Response({"error": str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(generics.GenericAPIView):
    '''
    This view logs the user in according to his group i.e seller or buyer.
    It returns a jwt token after successful authentication
    '''
    serializer_class = UserLoginSerializer

    def post(self, request):

        # calling the function to get the decoded credentials
        credentials_str = self.get_credentials_from_header(request)
        try:
            username, password = credentials_str.split(':', 1)
            logger.info(f"{username} : {password}")
        except ValueError:
            return Response("Invalid credentials format", status=status.HTTP_401_UNAUTHORIZED)

        data = {
            'username': username,
            'password': password,
            'is_buyer': request.data.get('is_buyer'),
            'is_seller': request.data.get('is_seller'),
        }
        # getting the data serialized
        serialized_data = self.get_serializer(data=data)
        authorized = False
        # If the data is valid then  matching the credentials for the specific group i.e buyer or seller
        if serialized_data.is_valid():
            logger.info(serialized_data.validated_data)
            try:
                logger.info(f"{serialized_data.validated_data['username']} ")
                user = get_user_model().objects.get(username=serialized_data.validated_data['username'])
            except:
                return Response("No user with this username", status=status.HTTP_404_NOT_FOUND)

            if serialized_data.validated_data['is_buyer']:
                if user.groups.filter(name="buyer").exists():
                    authorized = check_password(serialized_data.validated_data['password'], user.password)
                    logger.info(f"hello {authorized}")
                    logger.info(f"{serialized_data.validated_data['password']}, {user.password}")
                else:
                    return Response("There is no buyer registered with these credentials",
                                    status=status.HTTP_404_NOT_FOUND)

            elif serialized_data.validated_data['is_seller']:
                if user.groups.filter(name="seller").exists():
                    authorized = check_password(serialized_data.validated_data["password"], user.password)
                else:
                    return Response("There is no seller registered with these credentials",
                                    status=status.HTTP_404_NOT_FOUND)

            if not authorized:
                return Response("Incorrect password", status=status.HTTP_401_UNAUTHORIZED)

            refresh_token = RefreshToken.for_user(user)
            refresh_token['username'] = user.username
            refresh_token['customer_type'] = "seller" if user.groups.filter(name="seller").exists() else "buyer"

            return Response({
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            })
        else:
            return Response("Invalid Data", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_credentials_from_header(request):
        '''
        This function extracts the authentication header from the request then
        decodes it and sends it back
        '''
        authorization_header = request.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Basic '):
            return Response("Authorization header is missing or in the wrong format",
                            status=status.HTTP_401_UNAUTHORIZED)

        # Extract and decode base64-encoded credentials
        credentials_b64 = authorization_header[len('Basic '):]
        logger.info(f"{credentials_b64}")
        return base64.b64decode(credentials_b64).decode('utf-8')
