import logging
import uuid

from django.db.models import Q
from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
#
from .models import Order
from .serializers import OrderSerializer, OrderOffersSerializer, OfferCreateSerializer

logger = logging.getLogger(__name__)





# Представление для подтверждение - заявки
class AcceptOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        #
        if order.status == 'pending':
            order.status = 'accepted'
            order.courier = request.user
            order.save()
            return Response({
                'status': 'Order accepted',
                'success': True
            })
        #
        return Response({'status': 'Order cannot be accepted', 'success': False}, status=400)


# Представление для отмены - заявок
class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        #
        if order.status == 'pending':
            order.status = 'cancel'
            order.courier = request.user
            order.save()
            return Response({
                'status': 'Order Canceled',
                'success': True
            })
        #
        return Response({'status': 'Order cannot be canceled', 'success': False}, status=400)

