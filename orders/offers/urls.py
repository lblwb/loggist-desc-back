from django.urls import path, include

from .views.create import OfferCreateAPIView
from .views.list import OrderDetailOffersView

# from .views.list import OrderDetailOffersView

urlpatterns = [
    # Создание нового предложения
    path('<str:idx>/offers/new', OfferCreateAPIView.as_view(), name="order-offers-create"),
    # Получить только офферы по заказу
    path('<str:idx>/offers', OrderDetailOffersView.as_view(), name="order-detail-offers"),

    # path('/orders/offers/list', OfferCreateAPIView.as_view(), name="order-offers-create"),
]
