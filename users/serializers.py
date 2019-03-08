from rest_framework import serializers
from django.contrib.auth import get_user_model 
from users.models import Users
from rest_framework_jwt.settings import api_settings
import django.contrib.auth.password_validation as validators
from django.core import exceptions

UserModel = get_user_model()

class QuestionaireUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionaireUsers
        # fields = ('firstname', 'lastname','is_admin')
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):


    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ( "id", "username", "email","password","token" )