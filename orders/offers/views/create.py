from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Order
from ..serializers import OfferCreateSerializer

'''
Создание нового предложия для заявки
'''


class OfferCreateAPIView(APIView):
    def post(self, request, order_uuid):
        try:
            order = Order.objects.get(uuid=order_uuid)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
