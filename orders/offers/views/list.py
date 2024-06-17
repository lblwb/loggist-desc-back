# Представление - Полная информация об офферах к заявке
from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import OffersOrderSerializer
from ...models import Order, OffersOrder
from ...serializers import OrderSerializer


class OrderDetailOffersView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'idx'

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(idx=kwargs.get('idx'))
            serializer = self.get_serializer(order)
            offers = order.offers.all()
            # print(order)
            # Получаем все офферы для данного заказа
            serializer_offers = OffersOrderSerializer(offers, many=True)
            # print(serializer_offers.data)

            offers = order.offers.all()
            for offer in offers:
                print(offer.offer_amount)

            return Response({
                # "order": serializer.data,
                "offers": serializer_offers.data
            })

        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
