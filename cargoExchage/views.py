from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serialize import UserDataSerializer


class UserViewGet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        #
        serializer = UserDataSerializer(user)

        return Response({
            "user": serializer.data
        })
