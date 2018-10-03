from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

# User serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # These are most likely unnecessary, but for testing
        fields = ("id", "username", "is_staff")


class UserSerializerWithToken(serializers.ModelSerializer):
    """
    This serializer is used for signups. The server responds with user data and
    the token to be stored in the browser.
    """

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        """
        Creates the token.
        :param obj:
        :return:
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        """
        Default method overridden to set the password.
        :param validated_data:
        :return:
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')
