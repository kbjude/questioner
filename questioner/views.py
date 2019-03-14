from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
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
                            "user_id": user.pk,
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


class Login(ObtainAuthToken):
    """
    post:
    login a user.
    """

    @classmethod
    @swagger_auto_schema(
        operation_description="Login a User",
        operation_id="Login a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(many=False), 401: "Invalid Login"},
    )
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
            status=status.HTTP_200_OK,
        )
