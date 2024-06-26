from rest_framework import serializers
from .models import Order
from django.contrib.auth.models import User

# from .offers.serializers import OrderOffersSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class OrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    courier = UserSerializer(read_only=True)
    # offers = OrderOffersSerializer(read_only=True)

    class Meta:
        model = Order
        # fields = '__all__'
        fields = [
            # 'id',
            'idx', 'cargo_type', 'cargo_inf_to', 'cargo_inf_from',
            'cargo_inf_size', 'cargo_inf_wht', 'cargo_deliv_start_at',
            'cargo_deliv_end_at', 'status', 'description',
            # 'comment',
            'client', 'courier', 'created_at', 'updated_at'
        ]
        read_only_fields = ['idx', 'client', 'courier', 'offers', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['client'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        courier_data = validated_data.pop('courier', None)
        if courier_data:
            instance.courier = User.objects.get(
                username=courier_data['username'])  # Используем 'username' для получения пользователя
        return super().update(instance, validated_data)
