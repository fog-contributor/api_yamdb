from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre, Title
# from api.permission import AuthorOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     pagination_class = LimitOffsetPagination
#     permission_classes = (AuthorOrReadOnly,)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

