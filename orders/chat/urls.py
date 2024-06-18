from django.urls import path

from .views import ChatMessagesView, NewChatMessageView

# Api -> Orders [Заявки]
urlpatterns = [
    # ЧАТ
    path('<str:order_id>/chat/msg/get', ChatMessagesView.as_view(), name='chat_messages'),
    path('<str:order_id>/chat/new_message', NewChatMessageView.as_view(), name='new_chat_message'),
]
