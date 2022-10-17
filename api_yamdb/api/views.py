from rest_framework import viewsets
from reviews.models import Comment, Rating, Review


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related()


class RatingViewset(viewsets.ModelViewSet):
    queryset = Rating.objects.select_related()


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.select_related()
