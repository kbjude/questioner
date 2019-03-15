from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer


class Index(APIView):
    """
    get:
    Welcome to Questioner route
    operation_description:welcome
    """

    @classmethod
    @swagger_auto_schema(
        operation_description="Welcome to Questioner",
        operation_id="welcome To Questioner",
        security=None,
    )
    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})


class SignUp(APIView):
    """
    post:
    Register a user.
    """

    serializer_class = UserSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Create a user account.",
        operation_id="Sign up a user",
        request_body=UserSerializer,
        responses={201: UserSerializer(many=False), 400: "BAD REQUEST"},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "username": user.username,
                            "email": user.email,
                            "is_admin": user.is_superuser,
                        }
                    ],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"status": 400, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class Login(APIView):
    """
    post:
    login a user.
    """

    serializer_class = LoginSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Login a User",
        operation_id="Login a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(many=False), 401: "Invalid Login"},
    )
    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data={"Username":serializer.data['username'],
                  "Email":serializer.data['email']},
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

                        "user": {"Username":serializer.data['username'],
                                 "Email":serializer.data['email']}

                    }
                ],
            },
            status=status.HTTP_200_OK,
        )
