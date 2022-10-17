from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewset, RatingViewset, ReviewViewset

router_v1 = DefaultRouter()

router_v1.register(r'comments', CommentViewset, basename='comments')
router_v1.register(r'ratings', RatingViewset, basename='ratings')
router_v1.register(r'reviews', ReviewViewset, basename='reviews')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
