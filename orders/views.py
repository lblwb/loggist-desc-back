import logging
import uuid

from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
#
from .models import Order
from .serializers import OrderSerializer, OrderOffersSerializer, OfferCreateSerializer

logger = logging.getLogger(__name__)


# Представление -Добавление новой заявки
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


# Представление - Полная инфорация о заявке
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'idx'

    # lookup_field = 'idx'

    # def get_object(self, idx):
    #     try:
    #         return Order.objects.get(idx=idx)
    #     except Order.DoesNotExist:
    #         raise Http404

    def get(self, request, *args, **kwargs):
        # snippet = self.get_object()
        # serializer = OrderSerializer(snippet)

        # kwargs.get('idx')
        order = Order.objects.get(idx=kwargs.get('idx'))
        print(order.description)

        serializer = OrderSerializer(order)
        serializer_offers = OrderOffersSerializer()

        # offer = Offer.objects.get(id=offer_id)
        # serializer = OrderOffersSerializer(offer)

        try:
            return Response({
                "order": serializer.data,
                "order_offers": serializer_offers.data,
                "chat": {
                    "chat_idx": ""
                },
                "success": True
            })

        except Order.DoesNotExist:
            return Response({
                "offer": [],
                "success": False
            })


# Представление - Полная инфорация о заявке
class OrderDetailOffersView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'idx'

    # lookup_field = 'idx'

    # def get_object(self, idx):
    #     try:
    #         return Order.objects.get(idx=idx)
    #     except Order.DoesNotExist:
    #         raise Http404

    def get(self, request, *args, **kwargs):
        # snippet = self.get_object()
        # serializer = OrderSerializer(snippet)

        # kwargs.get('idx')
        order = Order.objects.get(idx=kwargs.get('idx'))
        # print(order.description)
        serializer_offers = OrderOffersSerializer()

        # offer = Offer.objects.get(id=offer_id)
        # serializer = OrderOffersSerializer(offer)

        try:
            return Response({
                "order_offers": serializer_offers.data,
                "success": True
            })

        except Order.DoesNotExist:
            return Response({
                "offer": [],
                "success": False
            })


# Представление - Все заявки
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


# Представление - Все ожидающие подтерждения заявки
class PendingOrdersView(generics.ListAPIView):
    # Фильтр по полям
    def get_queryset(self):
        queryset = Order.objects.filter(status='pending_accept', courier__isnull=True)
        #
        destination = self.request.query_params.get('from')
        #
        date = self.request.query_params.get('date')

        #
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')

        if destination:
            queryset = queryset.filter(
                Q(cargo_inf_to__icontains=destination) | Q(cargo_inf_from__icontains=destination))

        if date:
            parsed_date = timezone.datetime.strptime(date, '%d-%m-%Y')  # Пример формата: "01-06-2024"
            queryset = queryset.filter(cargo_deliv_start_at__date=parsed_date)
            # queryset = queryset.filter(cargo_deliv_start_at__in=date)

        # Сумма
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "orders": serializer.data,
            "success": True
        })

    def get_serializer_class(self):
        return OrderSerializer
    # serializer_class = OrderSerializer


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
