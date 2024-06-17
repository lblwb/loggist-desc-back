# Представление - Все заявки
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import OrderSerializer
from ..models import Order


class MyOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        client_orders = Order.objects.filter(client=request.user)
        courier_orders = Order.objects.filter(courier=request.user)
        #
        orders = client_orders | courier_orders
        #
        serializer = OrderSerializer(orders, many=True)
        return Response({
            "orders": serializer.data,
            "success": True
        })
