from django.urls import path, include

from .orders.detail import OrderDetailView
from .orders.list import OrderListCreateView
from .user.my_orders import MyOrdersView

# from sub.orders.chat.views import ChatMessagesView, NewChatMessageView
# from sub.orders.detail import OrderDetailView
# from sub.orders.list import OrderListCreateView

# from sub.orders.search_orders import PendingOrdersView
# from sub.orders.user.my_orders import MyOrdersView

# Api -> Orders [Заявки]
urlpatterns = [

    # Создание новой заявки
    path('request/new', OrderListCreateView.as_view(), name='order-list-create'),
    #


    path('search/', include('orders.search_orders.urls')),
    #
    # # Получение полной информации о заказе
    path('show/<str:idx>/', OrderDetailView.as_view(), name='order-detail'),


    # Подтверждение оффера
    # path('orders/<str:idx>/offer/<str:idx>/accept', AcceptOrderView.as_view(), name='order-offer-accept-order'),
    # Отклонение оффера
    # path('orders/<str:idx>/offer/<str:idx>/cancel', AcceptOrderView.as_view(), name='cancel-order'),

    # Отменить заявку (заказ)
    # path('orders/<str:idx>/cancel_pending', OfferCreateAPIView.as_view(), name="order-canceled"),
    #

    # Оферы

    path('', include('orders.offers.urls')),

    # ЧАТЫ

    path('', include('orders.chat.urls')),

    # Orders -> Current user
    path('by_user', MyOrdersView.as_view(), name='my-orders'),
]
