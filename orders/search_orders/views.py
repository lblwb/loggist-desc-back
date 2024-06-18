from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from ..serializers import OrderSerializer
from ..models import Order

'''
Представление - Все ожидающие подтерждения заявки
'''


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

        # Сумма
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset.order_by('-created_at'), many=True)
        return Response({
            "orders": serializer.data,
            "success": True
        })

    def get_serializer_class(self):
        return OrderSerializer
