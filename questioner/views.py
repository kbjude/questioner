from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated


class Index(APIView):
    @classmethod
    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})


class SignUp(APIView):
    """
    Register a user.
    """

    serializer_class = UserSerializer

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
                status=status.HTTP_201_CREATED

            )
        return Response(
            data={"status": 400, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class Login(APIView):
    """
    login a user.
    """

    serializer_class = LoginSerializer

    @classmethod
    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK

        )

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# accounts/profile/
class profile(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):

        user = request.user
        serializer = UserSerializer(user, many=False)
        serializer.is_valid

        return Response(
            data={

                "status": status.HTTP_200_OK,
                "data": [
                    {

                        "user": serializer.data,

                    }
                ],
            },
            status=status.HTTP_200_OK
        )