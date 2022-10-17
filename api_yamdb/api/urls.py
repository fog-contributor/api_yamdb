from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewset, ReviewViewset

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewset, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewset,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
