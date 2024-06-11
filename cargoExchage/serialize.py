from django.contrib.auth.models import User
from rest_framework import serializers


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_login', 'username', 'first_name', 'last_name', 'is_active']
