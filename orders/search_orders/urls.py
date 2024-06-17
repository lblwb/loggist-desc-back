from django.urls import path

from .views import PendingOrdersView

# Api -> SEARCH Orders [Заявки]
urlpatterns = [
    # # Получение заявок с открытым предложением
    path('pendings/', PendingOrdersView.as_view(), name='pending-orders'),
]
