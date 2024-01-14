from rest_framework import generics, status
from rest_framework.response import Response

from .models import Cart
from .serializers import BuyerProductSerializer


class BuyerListCartAddItemView(generics.ListCreateAPIView):
    '''
    This  view is responsible for both adding a cart_item and displaying users cart
    '''
    serializer_class = BuyerProductSerializer

    # Returning only those items associated with the end user
    def get_queryset(self):
        return Cart.objects.filter(buyer=self.request.user)

    # The create method  here is necessary as my serializer is not associated to one specific model
    def create(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            Cart.objects.create(product_id=product_id,
                                buyer=serializer.validated_data['buyer'],
                                quantity=serializer.validated_data['quantity'])
            return Response(f"Item was successfully added to cart {product_id} {serializer.data}",
                            status=status.HTTP_201_CREATED)

        return Response("Error with adding item to cart", status=status.HTTP_400_BAD_REQUEST)


class BuyerUpdateCartItemView(generics.RetrieveUpdateAPIView):
    serializer_class = BuyerProductSerializer

    def get_queryset(self):
        return Cart.objects.filter(buyer=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, id=self.kwargs.get('pk'))
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Manually update the instance with validated data
        instance.quantity = serializer.validated_data.get('quantity', instance.quantity)
        instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class BuyerDeleteCartItemView(generics.DestroyAPIView):
    serializer_class = BuyerProductSerializer

    def get_queryset(self):
        return Cart.objects.filter(buyer=self.request.user)


class CheckoutView:
    pass
