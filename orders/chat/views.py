# views.py
import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from ..models import OrderChat, OrderChatMsg, Order
from ..serializers import UserSerializer


class ChatMessagesView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, idx=order_id)
        print(order.chats)

        serializer = UserSerializer(request.user)

        #
        chat = order.chats.first()  # Assuming there's only one chat per order for simplicity

        if not chat:
            return JsonResponse({"error": "Chat does not exist for this order.", "success": False}, status=404)

        messages = chat.messages.all()
        messages_data = [{'id': msg.id,
                          'sender': msg.sender.username,
                          'other': msg.sender.username == serializer.data.get('username'),
                          'text': msg.message,
                          'sent_at': msg.sent_at
                          } for msg in messages]

        return JsonResponse({"messages": messages_data, "success": True})


class NewChatMessageView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, idx=order_id)
        user = request.user

        # Check if the user is client or courier in the order
        if user == order.client or user == order.courier:
            message_text = request.POST.get('message', '')

            if message_text.strip():
                chat = order.chats.first()  # Assuming there's only one chat per order for simplicity
                if not chat:
                    chat = OrderChat.objects.create(order=order, client=order.client, courier=order.courier)

                OrderChatMsg.objects.create(chat=chat, sender=user, message=message_text, sent_at=timezone.now())

                return JsonResponse({'success': 'Message added successfully.'})
            else:
                return JsonResponse({'error': 'Message text cannot be empty.'}, status=400)
        else:
            return JsonResponse({'error': 'You are not authorized to send messages for this order.'}, status=403)
