from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status

class SignUp(APIView):
    """
    Register a user.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({
                    'status': status.HTTP_201_CREATED,
                    'data': [{'user_id': user.pk,
                              'username': user.username,
                              'email': user.email,
                              'is_admin': user.is_superuser
                              }]
                })
        else:
            return Response({
                'status': 400,
                'errors': serializer.errors
            })