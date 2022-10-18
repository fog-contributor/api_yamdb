from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]