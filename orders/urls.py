from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import OrderListCreateView, OrderDetailView, MyOrdersView, AcceptOrderView, PendingOrdersView, \
    OfferCreateAPIView, OrderDetailOffersView

# Api -> Orders [Заявки]
urlpatterns = [
    # Создание новой заявки
    path('orders/new', OrderListCreateView.as_view(), name='order-list-create'),

    # Получение заявок с открытым предложением
    path('orders/search/pendings', PendingOrdersView.as_view(), name='pending-orders'),

    # Получение полной информации о заказе
    path('orders/show/<str:idx>/', OrderDetailView.as_view(), name='order-detail'),

    # Получить только офферы по заказу
    path('orders/<str:idx>/offers', OrderDetailOffersView.as_view(), name="order-detail-offers"),

    # Создание нового предложения
    path('orders/<str:idx>/offers/new', OfferCreateAPIView.as_view(), name="order-offers-create"),

    # path('/orders/offers/list', OfferCreateAPIView.as_view(), name="order-offers-create"),
    # Подтверждение оффера
    # path('orders/<str:idx>/offer/<str:idx>/accept', AcceptOrderView.as_view(), name='order-offer-accept-order'),
    # Отклонение оффера
    # path('orders/<str:idx>/offer/<str:idx>/cancel', AcceptOrderView.as_view(), name='cancel-order'),

    # Отменить заявку (заказ)
    path('orders/<str:idx>/cancel_pending', OfferCreateAPIView.as_view(), name="order-canceled"),

    # Orders -> Current user
    path('orders/by_user', MyOrdersView.as_view(), name='my-orders'),
]
