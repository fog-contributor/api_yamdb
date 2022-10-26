from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, SignUpView, LoginUserView,
                    CategoryViewSet, GenreViewSet, CommentViewSet,
                    TitleViewSet, ReviewViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
auth_patterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', LoginUserView.as_view()),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
