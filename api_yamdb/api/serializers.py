from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        model = User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User


class LoginUserSerializer(serializers.Serializer):

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
