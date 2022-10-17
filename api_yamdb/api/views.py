from rest_framework import viewsets
from reviews.models import Comment, Review


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related()


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.select_related()
