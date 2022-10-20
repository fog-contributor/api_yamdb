from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError
from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score' 'pub_date',)

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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date',)
