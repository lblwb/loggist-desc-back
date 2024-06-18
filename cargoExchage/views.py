from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serialize import UserSerializer


class UserViewGet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        #
        user_serializer = UserSerializer(user)

        return Response({
            "user": user_serializer.data,
        })
