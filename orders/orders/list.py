# Представление -Добавление новой заявки
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from ..models import Order
from ..serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Perform any validation before saving using validated_data
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)

            return Response({
                "order": serializer.data,
                "success": True
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                "order": None,
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer: OrderSerializer):
        serializer.save(client=self.request.user)
