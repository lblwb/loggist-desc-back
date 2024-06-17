from rest_framework import serializers

from ..models import OffersOrder
from ..serializers import UserSerializer, OrderSerializer


class OffersOrderSerializer(serializers.ModelSerializer):
    courier = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OffersOrder
        fields = '__all__'


# Создание нового предложения
class OfferCreateSerializer(serializers.ModelSerializer):
    # client = UserSerializer(read_only=True)
    courier = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OffersOrder
        fields = '__all__'
