from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db.models import Q
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def validate_username(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(username=value).exists():
            raise serializers.ValidationError("User already exists")
        return value

    def validate_email(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(email=value).exists():
            raise serializers.ValidationError("User already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )

        return user

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    token = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "token", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data.get("password", None)

        if not username:
            raise serializers.ValidationError(
                "Username or email is required to login")

        user = User.objects.filter(
            Q(email=username) | Q(username=username)).distinct()
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("Invalid Username/Email")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError(
                    "Incorrect credentials please try again")

        data["token"] = Token.objects.get_or_create(user=user_obj)[0].key
        data["email"] = user_obj.email

        return data
