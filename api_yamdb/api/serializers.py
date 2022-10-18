from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User, Role


class UserSerializer(serializers.ModelSerializer):

    role = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
