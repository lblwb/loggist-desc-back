from django.contrib.auth.models import User, Group
from rest_framework import serializers


# class UserDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['last_login', 'username', 'first_name', 'last_name', 'is_active']
#

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=False)

    class Meta:
        model = User
        fields = ['last_login', 'username', 'first_name', 'last_name', 'is_active', 'groups']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['groups'] = GroupSerializer(instance.groups.all(), many=True).data
        return data
