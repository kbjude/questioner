from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class Index(APIView):
    @classmethod
    def get(self,request):
        return Response({"The Dojos": "Welcome to Questioner."})


class SignUp(APIView):
    """
    Register a user.
    """
    @classmethod
    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "user_id": user.pk,
                            "username": user.username,
                            "email": user.email,
                            "is_admin": user.is_superuser,
                        }
                    ],
                },
                status = status.HTTP_201_CREATED

            )
        return Response(
            data = {"status": 400, "errors": serializer.errors},
            status = status.HTTP_400_BAD_REQUEST
            )


class Login(ObtainAuthToken):
    """
    login a user.
    """
    @classmethod
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = Token.objects.get_or_create(user=user)[0]
        return Response(
            data={
                "status": 200,
                "token": token.key,
                "data": [{"user_id": user.pk, "email": user.email}],
            },
            status = status.HTTP_200_OK

        )
