from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status


class Index(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})


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
                              'is_admin': user.is_admin
                              }]
                })
        else:
            return Response({
                'status': 400,
                'errors': serializer.errors                            
            })


class Login(ObtainAuthToken):
    """ 
    login a user. 
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status': 200,
            'token': token.key,
            'data': [{'user_id': user.pk,
                      'email': user.email
                      }]
        })
