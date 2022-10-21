from rest_framework import mixins, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Comment, Genre, Title, Review
from .permissions import AuthorOrReadOnly
from .serializers import (
    CategorySerializer, 
    CommentSerializer,
    GenreSerializer,
    TitleSerializer,
    TitlePostPatchSerializer,
    ReviewSerializer
)


class CreateListDel(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Кастомный класс для создания и удаления категорий и жанров."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateListDel):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)


class GenreViewSet(CreateListDel):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostPatchSerializer
        return TitleSerializer
        

class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.select_related()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
