# Представление - Полная инфорация о заявке
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response

from ..models import Order
from ..serializers import OrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'idx'

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(idx=kwargs.get('idx'))
        print(order.description)

        serializer = OrderSerializer(order)
        # serializer_offers = OrderOffersSerializer()

        #
        chat = order.chats.first()  # Assuming there's only one chat per order for simplicity

        if chat is not None and chat.messages is not None:
            # messages =
            messages_data = [{'id': msg.id,
                              'sender': msg.sender.username,
                              'other': msg.sender.username == serializer.data.get('username'),
                              'text': msg.message,
                              'sent_at': msg.sent_at
                              } for msg in chat.messages.all()]
        else:
            messages_data = []

        try:
            return JsonResponse({
                "order": serializer.data,
                # "order_offers": serializer_offers.data,
                "chat": {
                    # "messages": []
                    "messages": messages_data
                },
                "success": True
            })

        except Order.DoesNotExist:
            return JsonResponse({
                "offer": [],
                "success": False
            })
