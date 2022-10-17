from rest_framework import viewsets
from reviews.models import Comment, Review

from .permissions import AuthorOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.select_related()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)
