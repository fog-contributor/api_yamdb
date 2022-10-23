from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import User, Category, Comment, Genre, Title, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        model = User

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('role',)
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitlePostPatchSerializer(serializers.ModelSerializer):
    """
    Дополнительный сериализатор для post и patch запросов модели Title.
    """
    category = serializers.SlugRelatedField(
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs['title_id']
        )
        review_qs = title.review.filter(author=self.context['request'].user)
        if review_qs.exists():
            raise ValidationError('Можно оставить только один отзыв.')
        return data
