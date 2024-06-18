# views.py
import json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import OrderChat, OrderChatMsg, Order
from ..serializers import UserSerializer


class ChatMessagesView(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, idx=order_id)
        # print(order.chats)

        serializer = UserSerializer(request.user)

        #
        chat = order.chats.first()  # Assuming there's only one chat per order for simplicity

        if not chat:
            return JsonResponse({"error": "Chat does not exist for this order.", "success": False}, status=404)

        #
        messages = chat.messages.all()
        messages_data = [{'id': msg.id,
                          'sender': msg.sender.username,
                          'other': msg.sender.username == serializer.data.get('username'),
                          'text': msg.message,
                          'sent_at': msg.sent_at
                          } for msg in messages]

        return JsonResponse({"messages": messages_data, "success": True})


class NewChatMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, idx=order_id)
        user = request.user

        # Assuming the request body contains JSON data
        try:
            data = json.loads(request.body)
            message_text = data.get('message', '')

            if message_text.strip():
                if user == order.client or user == order.courier:
                    chat = order.chats.first()  # Assuming there's only one chat per order for simplicity

                    if not chat:
                        chat = OrderChat.objects.create(order=order, client=order.client, courier=order.courier)

                    # Create new message
                    message = OrderChatMsg.objects.create(chat=chat, sender=user, message=message_text, sent_at=timezone.now())

                    # Retrieve all messages in the chat
                    messages = chat.messages.all()

                    # Prepare messages data for response
                    messages_data = [{'id': msg.id,
                                      'sender': msg.sender.username,
                                      'other': msg.sender.username != user.username,  # Check if sender is not the current user
                                      'text': msg.message,
                                      'sent_at': msg.sent_at
                                      } for msg in messages]

                    return JsonResponse({"messages": messages_data, "success": True}, status=200)
                else:
                    return JsonResponse({'error': 'You are not authorized to send messages for this order.', 'success': False}, status=403)
            else:
                return JsonResponse({'error': 'Message text cannot be empty.', 'success': False}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format', 'success': False}, status=400)
