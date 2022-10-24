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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.average_rating

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        model = Title


class TitlePostPatchSerializer(serializers.ModelSerializer):
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
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError("Only one review is allowed")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    review = serializers.SlugRelatedField(slug_field="text", read_only=True)

    class Meta:
        fields = ("id", "author", "review", "text", "pub_date")
        model = Comment
