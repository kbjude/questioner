from django.contrib.auth.models import User
from django.contrib.auth.password_validation import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings
from .models import Meeting
import import_string


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, value):
        '''
        Validate whether the username meets all validator requirements.

        If the username is valid, return the username.
        If the password is invalid, raise ValidationError.
        '''

        ModelClass = self.Meta.model
        if ModelClass.objects.filter(email=value).exists():
            raise serializers.ValidationError('User already exists')
        return value

    def validate_username(self, value):
        '''
        Validate whether the username meets all validator requirements.
        If the username is valid, return the username.
        If the password is invalid, raise ValidationError.
        '''

        ModelClass = self.Meta.model
        if ModelClass.objects.filter(username=value).exists():
            raise serializers.ValidationError('User already exists')
        return value

    def validate_password(self, password, user=None, password_validators=None):
        '''
        Validate whether the password meets all validator requirements.
        If the password is valid, return ``None``.
        If the password is invalid, raise ValidationError.
        '''

        errors = []
        if password_validators is None:
            password_validators = self.get_default_password_validators()
        for validator in password_validators:
            try:
                validator.validate(password, user)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors)

    def get_default_password_validators(self):
        return self.get_password_validators(
                settings.AUTH_PASSWORD_VALIDATORS
               )

    def get_password_validators(self, validator_config):
        validators = []
        for validator in validator_config:
            try:
                klass = import_string(validator['NAME'])
            except ImportError:
                msg = "The module in NAME could not be imported: %s."
                raise ImproperlyConfigured(msg % validator['NAME'])
            validators.append(klass(**validator.get('OPTIONS', {})))

        return validators

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
            )

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class MeetingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Meeting
        fields = ('title', 'date', 'start', 'end', 'created_at', 'user')
